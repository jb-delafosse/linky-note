# type: ignore[attr-defined]

import os
from pathlib import Path

import typer
from click import Choice
from linky_note import __version__
from linky_note.adapters.markdown.factories import MarkoExtractorFactory
from linky_note.adapters.markdown.marko_modifier import MarkoModifierImpl
from linky_note.adapters.markdown.marko_parser import MarkoParserImpl
from linky_note.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from linky_note.dto.dto import LinkyNoteConfig, ModifyConfig, ParseConfig
from linky_note.infrastructure.db_connection import ENGINE
from linky_note.interfaces import (
    modifier,
    parser,
    reference_extractor,
    references_db,
    renderer,
)
from linky_note.usecases.config import Config
from linky_note.usecases.modify import modify
from linky_note.usecases.parse import parse
from linky_note.usecases.read_references import read_references
from linky_note.usecases.write import write
from marko.md_renderer import MarkdownRenderer
from rich.console import Console

config = Config.read(Path(os.getcwd()) / ".linky-note.yml")

references_db.REFERENCE_DB_FACTORY = SqlReferenceDatabaseFactory(ENGINE)
parser.PARSER = MarkoParserImpl(config.parse_config)
modifier.MODIFIER = MarkoModifierImpl(
    references_db.REFERENCE_DB_FACTORY, config.modify_config
)
renderer.RENDERER = MarkdownRenderer()
reference_extractor.EXTRACTOR_FACTORY = MarkoExtractorFactory()

app = typer.Typer(
    name="linky-note",
    help='linky-note adds a "Linked References" at the bottom of you markdown files',
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]linky-note[/] version: [bold blue]{__version__}[/]"
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


@app.command(name="init")
def init():
    config_dir = os.getcwd()
    config_filename = f".{app.info.name}.yml"
    config_path: Path = Path(config_dir) / config_filename
    typer.echo(
        f"👋 Welcome in {app.info.name}, we are going to edit your {config_filename}"
    )
    understand_wikilinks = typer.confirm(
        "Should it understand wiki-links (example `[[Label]]`):", default=True
    )
    reference_by = typer.prompt(
        "Should the title or the filename be considered as the unique key to reference a note ?",
        type=Choice(["title", "filename"], case_sensitive=False),
        show_choices=True,
        default="filename",
    )

    link_system = typer.prompt(
        "What is your link system links or wiki-links ?",
        type=Choice(["wikilink", "link"], case_sensitive=False),
        show_choices=True,
        default="link",
    )

    init_config = LinkyNoteConfig(
        parse_config=ParseConfig(parse_wikilinks=understand_wikilinks),
        modify_config=ModifyConfig(
            reference_by=reference_by, link_system=link_system
        ),
    )
    Config.write(config_path, init_config)
    # TODO : Add config for the next steps
    # Modify
    #     Linked reference section title
    # Rendering
    #     render to : Markdown / HTML


if __name__ == "__main__":
    app()
