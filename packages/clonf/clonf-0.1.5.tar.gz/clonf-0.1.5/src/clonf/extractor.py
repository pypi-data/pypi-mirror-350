from .annotations import CliArgument, ClonfAnnotation, CliOption
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined


def _process_cli_argument(arg: CliArgument, field_info: FieldInfo) -> CliArgument:
    if arg.default is Ellipsis:
        new_default = field_info.default or field_info.default_factory
        if new_default is not PydanticUndefined:
            arg.default = new_default
    return arg


def _process_cli_option(option: CliOption, field_info: FieldInfo) -> CliOption:
    if option.default is Ellipsis:
        new_default = field_info.default or field_info.default_factory
        if new_default is not PydanticUndefined:
            option.default = new_default

    return option


def extract_cli_info(model: type[BaseModel]) -> list[ClonfAnnotation]:
    extracted: list[ClonfAnnotation] = []

    for field, field_info in model.model_fields.items():
        for meta in field_info.metadata:
            if not isinstance(meta, ClonfAnnotation):
                continue

            meta._field_info = field_info
            meta._type = field_info.annotation

            if meta.name is Ellipsis:
                meta.name = field_info.alias or field

            if meta.description is None:
                meta.description = field_info.description

            if isinstance(meta, CliArgument):
                meta = _process_cli_argument(meta, field_info)

            if isinstance(meta, CliOption):
                meta = _process_cli_option(meta, field_info)

            extracted.append(meta)

    return extracted
