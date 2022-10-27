# type: ignore[attr-defined]

import os
from pathlib import Path

import typer
from click import Choice
from linky_note import __version__
from linky_note.dto.dto import LinkyNoteConfig, ModifyConfig, ParseConfig
from linky_note.infrastructure.cli_app import setup_app
from linky_note.usecases.config import Config
from linky_note.usecases.modify import modify
from linky_note.usecases.parse import parse
from linky_note.usecases.read_references import read_references
from linky_note.usecases.write import write
from rich.console import Console

config = Config.read(Path(os.getcwd()) / ".linky-note.yml")

app = setup_app(config)
console = Console()


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]linky-note[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


if __name__ == "__main__":
    app()
