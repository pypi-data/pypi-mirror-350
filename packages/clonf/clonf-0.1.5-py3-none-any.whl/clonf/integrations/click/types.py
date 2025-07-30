import typing_extensions as te
import typing as t

_TReturn = t.TypeVar("_TReturn", covariant=True)


_CliFunc: te.TypeAlias = t.Callable[..., _TReturn]


class _WrappedFunc(t.Protocol, t.Generic[_TReturn]):
    def __call__(self, **kwargs: t.Any) -> _TReturn: ...


class TClonfClick(t.Protocol):
    def __call__(self, func: _CliFunc[_TReturn]) -> _WrappedFunc[_TReturn]: ...
