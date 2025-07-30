from .annotations import CliArgument, CliOption
import typing as t
import importlib

if t.TYPE_CHECKING:
    from clonf.integrations.click.types import TClonfClick

    clonf_click: TClonfClick


def __getattr__(name: str) -> t.Any:
    if name == "clonf_click":
        return getattr(importlib.import_module("clonf.integrations.click"), name)

    raise AttributeError(  # pragma: no cover
        f"module {__name__!r} has no attribute {name!r}"
    )


__all__ = ["CliArgument", "CliOption", "clonf_click"]
