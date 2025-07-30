import pathlib
import click
from click.testing import CliRunner
from clonf import clonf_click
from pydantic import AliasChoices, BaseModel, Field
import typing as t
from clonf import CliArgument, CliOption
import uuid
import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import pytest

runner = CliRunner()


def test_simple_click_app() -> None:
    class SimpleConfig(BaseModel):
        name: t.Annotated[str, CliArgument()] = "World"
        greeting_word: t.Annotated[str, CliOption()] = "Hello"

    @click.command()
    @clonf_click
    def hello(config: SimpleConfig) -> None:
        click.echo(f"{config.greeting_word} {config.name}!")

    result = runner.invoke(hello, ["Guido"], catch_exceptions=False)
    assert result.exit_code == 0

    assert result.output == "Hello Guido!\n"

    result = runner.invoke(hello, catch_exceptions=False)
    assert result.exit_code == 0

    assert result.output == "Hello World!\n"


def test_click_int_range() -> None:
    class SimpleConfig(BaseModel):
        value: t.Annotated[int, Field(gt=1, lt=10), CliArgument()] = 5

    @click.command()
    @clonf_click
    def what_is_value(config: SimpleConfig) -> None:
        click.echo(f"The value is {config.value}")

    assert len(what_is_value.params) == 1
    assert isinstance(what_is_value.params[0].type, click.IntRange)


def test_click_float_range() -> None:
    class SimpleConfig(BaseModel):
        value: t.Annotated[float, Field(gt=1, lt=10), CliArgument()] = 5

    @click.command()
    @clonf_click
    def what_is_value(config: SimpleConfig) -> None:
        click.echo(f"The value is {config.value}")

    assert len(what_is_value.params) == 1
    assert isinstance(what_is_value.params[0].type, click.FloatRange)


def test_click_literal() -> None:
    class SimpleConfig(BaseModel):
        answer: t.Annotated[t.Literal["yes", "no"], CliArgument()] = "yes"

    @click.command()
    @clonf_click
    def what_is_answer(config: SimpleConfig) -> None:
        click.echo(f"The answer is {config.answer}")

    assert len(what_is_answer.params) == 1
    assert isinstance(what_is_answer.params[0].type, click.Choice)


def test_click_unsupported_type() -> None:
    class SimpleConfig(BaseModel):
        value: t.Annotated[t.Set[str], CliOption()]  # noqa: UP006

    with pytest.raises(TypeError):

        @click.command()
        @clonf_click
        def what_is_value(config: SimpleConfig) -> None:
            click.echo(f"The answer is {config.value}")

        runner.invoke(what_is_value)


def test_click_path() -> None:
    class SimpleConfig(BaseModel):
        value: t.Annotated[pathlib.Path, CliArgument()] = pathlib.Path()

    @click.command()
    @clonf_click
    def what_is_value(config: SimpleConfig) -> None:
        click.echo(f"The value is {config.value}")

    assert len(what_is_value.params) == 1
    assert isinstance(what_is_value.params[0].type, click.Path)


def test_click_path_exists() -> None:
    class SimpleConfig(BaseModel):
        value: t.Annotated[pathlib.Path, CliArgument(), click.Path(exists=True)] = (
            pathlib.Path()
        )

    @click.command()
    @clonf_click
    def what_is_value(config: SimpleConfig) -> None:
        click.echo(f"The value is {config.value}")

    assert len(what_is_value.params) == 1
    assert (
        isinstance(what_is_value.params[0].type, click.Path)
        and what_is_value.params[0].type.exists is True
    )


def test_click_uuid() -> None:
    class SimpleConfig(BaseModel):
        value: t.Annotated[uuid.UUID, CliArgument()] = uuid.uuid4()

    @click.command()
    @clonf_click
    def what_is_value(config: SimpleConfig) -> None:
        click.echo(f"The value is {config.value}")

    assert len(what_is_value.params) == 1
    assert what_is_value.params[0].type is click.UUID


def test_click_datetime() -> None:
    class SimpleConfig(BaseModel):
        value: t.Annotated[datetime.date, CliArgument()] = datetime.date(2025, 5, 4)

    @click.command()
    @clonf_click
    def what_is_value(config: SimpleConfig) -> None:
        click.echo(f"The value is {config.value}")

    assert len(what_is_value.params) == 1
    assert isinstance(what_is_value.params[0].type, click.DateTime)


def test_click_bool() -> None:
    class SimpleConfig(BaseModel):
        value: t.Annotated[bool, CliArgument()] = False

    @click.command()
    @clonf_click
    def what_is_value(config: SimpleConfig) -> None:
        click.echo(f"The value is {config.value}")

    assert len(what_is_value.params) == 1
    assert what_is_value.params[0].type is click.BOOL


def test_click_settings_sources_priority(tmp_path: pathlib.Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("TEST_VALUE=31")

    class Config(BaseSettings):
        value: t.Annotated[int, CliArgument()] = 42

        model_config = SettingsConfigDict(
            env_prefix="TEST_",
            case_sensitive=False,
            env_file=str(env_file),
        )

    @click.command
    @clonf_click
    def cli(config: Config) -> None:
        click.echo(f"The value is {config.value}")

    result = runner.invoke(cli, catch_exceptions=False)

    assert result.exit_code == 0

    assert result.output == "The value is 31\n"

    os.environ["TEST_VALUE"] = "31"
    result = runner.invoke(cli, catch_exceptions=False)

    assert result.exit_code == 0

    assert result.output == "The value is 31\n"


def test_click_multiple_models() -> None:
    class Config(BaseModel):
        value: t.Annotated[int, CliArgument()] = 42

    class Config2(BaseModel):
        value2: t.Annotated[int, CliArgument()] = 1337

    @click.command
    @clonf_click
    def cli(config: Config, config2: Config2) -> None:
        click.echo(f"{config.value} {config2.value2}")

    result = runner.invoke(cli, catch_exceptions=False)
    assert result.exit_code == 0
    assert result.output == "42 1337\n"


def test_click_alias() -> None:
    class Config(BaseModel):
        answer_value: t.Annotated[
            int,
            CliOption(),
            Field(
                alias="answer-value",
                # defining validation aliases is required
                validation_alias=AliasChoices("answer-value", "answer_value"),
            ),
        ] = 42

    @click.command
    @clonf_click
    def cli(config: Config) -> None:
        assert config.answer_value == 43
        click.echo(f"{config.answer_value}")

    result = runner.invoke(cli, ["--answer-value", "43"], catch_exceptions=False)
    assert result.exit_code == 0


def test_click_flag_value() -> None:
    class Config(BaseModel):
        flag: t.Annotated[bool, CliOption(is_flag=True)] = False

    @click.command()
    @clonf_click
    def cli(config: Config) -> None:
        click.echo(config.flag)

    result = runner.invoke(cli, catch_exceptions=False)
    assert result.exit_code == 0
    assert result.output == "False\n"

    result = runner.invoke(cli, ["--flag"], catch_exceptions=False)
    assert result.exit_code == 0
    assert result.output == "True\n"


def test_click_dict() -> None:
    class Config(BaseModel):
        mapping: t.Annotated[dict[str, int], CliOption(), Field(default_factory=dict)]
        str_mapping: t.Annotated[
            dict[str, str], CliOption(), Field(default_factory=dict)
        ]

    @click.command()
    @clonf_click
    def cli(config: Config) -> None:
        click.echo(config.mapping)

    result = runner.invoke(cli, ["--mapping", '{"value": 42}'], catch_exceptions=False)
    assert result.exit_code == 0, result.output
    assert result.output == "{'value': 42}\n", result.output

    result = runner.invoke(
        cli, ["--str_mapping", '{"value": 42}'], catch_exceptions=False
    )

    assert result.exit_code == 2, result.output
    assert (
        "Pydantic validation error: msg='Input should be a valid string' path=('value',) input=42"
        in result.output
    ), result.output
