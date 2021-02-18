# type: ignore[attr-defined]

import os
from pathlib import Path

import typer
from marko.md_renderer import MarkdownRenderer
from marko_backlinks import __version__
from marko_backlinks.adapters.markdown.factories import MarkoExtractorFactory
from marko_backlinks.adapters.markdown.marko_modifier import MarkoModifierImpl
from marko_backlinks.adapters.markdown.marko_parser import MarkoParserImpl
from marko_backlinks.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from marko_backlinks.infrastructure.db_connection import ENGINE
from marko_backlinks.interfaces import (
    modifier,
    parser,
    reference_extractor,
    references_db,
    renderer,
)
from marko_backlinks.usecases.modify import modify
from marko_backlinks.usecases.parse import parse
from marko_backlinks.usecases.read_references import read_references
from marko_backlinks.usecases.write import write
from rich.console import Console

references_db.REFERENCE_DB_FACTORY = SqlReferenceDatabaseFactory(ENGINE)
parser.PARSER = MarkoParserImpl()
modifier.MODIFIER = MarkoModifierImpl(references_db.REFERENCE_DB_FACTORY)
renderer.RENDERER = MarkdownRenderer()
reference_extractor.EXTRACTOR_FACTORY = MarkoExtractorFactory()

app = typer.Typer(
    name="marko-backlinks",
    help='marko-backlinks adds a "Linked References" at the bottom of you markdown files',
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
        os.getcwd(),
        help="the directory that contains all the notes",
        dir_okay=True,
        exists=True,
        file_okay=False,
        writable=True,
        readable=True,
    ),
    output_dir: Path = typer.Option(
        None,
        help="the output directory",
        dir_okay=True,
        writable=True,
        readable=True,
    ),
):

    files = parse(directory)
    files = read_references(files)
    files = modify(files)
    write(files, output_dir if output_dir else directory)


if __name__ == "__main__":
    app()
