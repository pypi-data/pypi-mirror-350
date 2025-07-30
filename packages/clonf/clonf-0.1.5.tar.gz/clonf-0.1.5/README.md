# clonf

[![PyPI version](https://badge.fury.io/py/clonf.svg)](https://badge.fury.io/py/clonf)
[![GitHub license](https://img.shields.io/github/license/jvllmr/clonf)](https://github.com/jvllmr/clonf/blob/main/LICENSE)
![PyPI - Downloads](https://img.shields.io/pypi/dd/clonf)

Declaratively connect cli and config definition using pydantic.

## Why another?

There are a lot of tools out there which try to bring cli libraries and pydantic together, but they all seem to forget that more sophisticated applications need to be controlled via configuration files as well. `clonf` tries to solve this problem by focusing on compatibility with `pydantic-settings` and its configuration sources. This allows having a single source of truth for cli and configuration definition. `clonf` uses composition rather than inheritance and utilizes logic from `pydantic` and `pydantic-settings` to achieve this with as much simplicity and flexibility as possible. First versions focus on integration with click, but other cli libraries might receive interfaces as well in the future.

### Key differences to other pydantic x cli libraries

- CLI behavior is opt-in.
- As much as possible is done via annotations. Combined with pydantic best practices, this encourages creating a single source of truth inside your codebase.

## Installation

clonf can be installed via pip or your favorite python package manager with different extras:

```shell
pip install clonf[all,click,settings]
```

## Creating a CLI

### click

#### Quickstart

```python
from pydantic import BaseModel
from clonf import clonf_click, CliArgument, CliOption
from typing import Annotated
import click


class Arguments(BaseModel):
    name: Annotated[str, CliArgument()]


class Options(BaseModel):
    greeting: Annotated[str, CliOption()] = "Hello"


@click.command
@clonf_click
def cli(arguments: Arguments, options: Options) -> None:
    click.echo(f"{options.greeting} {arguments.name}")


if __name__ == "__main__":
    cli()
```

#### Using click types

Similar to `pydanclick`, the following types will be converted automatically:
| Python type | Click type |
| :--------------------------------------- | :------------------- |
| `bool` | `click.BOOL` |
| `str` | `click.STRING` |
| `int` | `click.INT` |
| `float` | `click.FLOAT` |
| `Annotated[int, Field(lt=..., ge=...)` | `click.IntRange()` |
| `Annotated[float, Field(lt=..., ge=...)` | `click.FloatRange()` |
| `pathlib.Path` | `click.Path()` |
| `uuid.UUID` | `click.UUID` |
| `datetime.datetime`, `datetime.date` | `click.DateTime()` |
| `Literal` | `click.Choice` |

Additionally, custom click types can be passed via annotations to have finer control over the resulting click type:

```python
from pydantic import BaseModel
from typing import Annotated
from clonf import CliArgument
import pathlib
import click

class Config(BaseModel):
    file_path: Annotated[pathlib.Path, CliArgument(), click.Path(exists=True)]
```

## Contributing

This project uses PDM as a package manager and pre-commit for linting before commits.

Read more about the tools and how to use them:

- [`PDM`](https://pdm-project.org/en/latest)
- [`pre-commit`](https://pre-commit.com/)
