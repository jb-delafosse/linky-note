# type: ignore[attr-defined]

import glob
import os
from pathlib import Path

import typer
from marko import Markdown
from marko.md_renderer import MarkdownRenderer
from marko_backlinks import __version__
from marko_backlinks.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from marko_backlinks.infrastructure.db_connection import ENGINE
from marko_backlinks.interfaces import references_db
from marko_backlinks.usecases.extension import ReferencesExtension
from rich.console import Console

references_db.REFERENCE_DB_FACTORY = SqlReferenceDatabaseFactory(ENGINE)
converter = Markdown(
    renderer=MarkdownRenderer, extensions=[ReferencesExtension]
)


app = typer.Typer(
    name="marko-backlinks",
    help="Awesome `marko-backlinks` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]marko-backlinks[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


@app.command(name="apply")
def main(
    directory: Path = typer.Argument(
        ...,
        help="the directory that contains all the notes",
        dir_okay=True,
        exists=True,
        file_okay=False,
        writable=True,
        readable=True,
    )
):
    files = {}
    for filename in glob.glob(os.path.join(directory, "*.md")):
        with open(filename) as file:
            ast = converter.parse(file.read())
            files[filename] = ast
    for filename, ast in files.items():
        with open(filename, "w") as file:
            text = converter.render(ast)
            file.write(text)


if __name__ == "__main__":
    app()
