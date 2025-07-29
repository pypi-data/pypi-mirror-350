from dataclasses import dataclass

import typer

__version__ = "1.11.2"  # must match the version in pyproject.toml


@dataclass
class AppDesc:
    app: typer.Typer
    name: str
    help: str
