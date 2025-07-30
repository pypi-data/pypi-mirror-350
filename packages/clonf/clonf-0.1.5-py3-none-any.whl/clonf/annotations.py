from __future__ import annotations
from dataclasses import dataclass, field
import typing as t
from pydantic.fields import FieldInfo


@dataclass
class ClonfAnnotation:
    name: str | ellipsis = field(default=...)
    description: str | None = field(default=None)
    _type: t.Any | None = field(default=None, init=False)
    _field_info: FieldInfo | None = field(default=None, init=False)


@dataclass
class CliArgument(ClonfAnnotation):
    default: t.Any = field(default=...)


@dataclass
class CliOption(ClonfAnnotation):
    default: t.Any = field(default=...)
    prefix: str = field(default="--")
    is_flag: bool = field(default=False)
