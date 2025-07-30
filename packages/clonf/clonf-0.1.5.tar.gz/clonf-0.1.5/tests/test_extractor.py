from pydantic import BaseModel, Field
import typing as t

from clonf.annotations import ClonfAnnotation
from clonf.extractor import extract_cli_info


def test_extract_clonf_annotation() -> None:
    class SimpleModel(BaseModel):
        debug: t.Annotated[bool, Field(), ClonfAnnotation()]

    cli_info = extract_cli_info(SimpleModel)
    assert len(cli_info) == 1
    for ann in cli_info:
        assert isinstance(ann, ClonfAnnotation)
