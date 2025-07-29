import typing

import almanet

from . import _state

__all__ = [
    "transition_model",
    "make_transition",
    "transition",
    "make_observer",
    "observe",
]


class _transition_procedure[I, O]:
    __name__: str

    async def __call__(
        self,
        payload: I,
        *,
        session: almanet.Almanet,
        transition: "transition_model",
    ) -> O: ...


@almanet.shared.dataclass
class transition_model[I: type[_state.observable_state], O: type[_state.observable_state]]:
    label: str
    source: I
    target: O
    procedure: _transition_procedure[I, O]
    description: str | None = None
    is_observer: bool = False

    def __post_init__(self):
        self.__name__ = self.label
        self.__doc__ = self.description

    async def _remote_execution(
        self,
        payload: I,
        session: almanet.Almanet,
    ) -> O:
        result = await self.procedure(payload, session=session, transition=self)
        session.delay_call(self.target._uri_, result, 0)
        return result

    async def _local_execution(
        self,
        payload: I,
    ) -> O:
        session = almanet.get_active_session()
        return await self._remote_execution(payload, session=session)

    def __call__(
        self,
        payload: I,
    ) -> typing.Awaitable[O]:
        return self._local_execution(payload)


def make_transition(
    source: type[_state.observable_state],
    target: type[_state.observable_state],
    procedure: _transition_procedure,
    label: str | None = None,
    description: str | None = None,
    **extra,
) -> transition_model:
    if not callable(procedure):
        raise ValueError("decorated function must be callable")

    if label is None:
        label = procedure.__name__

    if description is None:
        description = procedure.__doc__

    if not issubclass(source, _state.observable_state):
        raise ValueError(f"{label}: `source` must be subclass of `observable_state`")

    if not issubclass(target, _state.observable_state):
        raise ValueError(f"{label}: `target` must be subclass of `observable_state`")

    return transition_model(
        label=label,
        description=description,
        source=source,
        target=target,
        procedure=procedure,
        **extra,
    )


def transition(
    *args,
    **extra,
):
    def wrap(function):
        return make_transition(*args, procedure=function, **extra)

    return wrap


def make_observer(
    service: almanet.remote_service,
    source: type[_state.observable_state],
    target: type[_state.observable_state],
    **extra,
) -> transition_model:
    instance = make_transition(
        source,
        target,
        **extra,
    )
    service.add_procedure(
        instance._remote_execution,
        uri=source._uri_,
        payload_model=source,
        return_model=target,
        validate=True,
        include_to_api=False,
    )
    return instance


def observe(
    *args,
    **extra,
):
    def wrap(function):
        return make_observer(
            *args,
            procedure=function,
            is_observer=True,
            **extra,
        )

    return wrap
