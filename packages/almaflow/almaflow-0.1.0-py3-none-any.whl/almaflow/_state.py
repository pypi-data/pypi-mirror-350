import typing

import almanet

__all__ = [
    "observable_state",
]


@almanet.shared.dataclass
class observable_state:
    _uri_: typing.ClassVar[str]

    def __init_subclass__(klass) -> None:
        klass._uri_ = f"{klass.__module__}.{klass.__name__}"
        super().__init_subclass__()
