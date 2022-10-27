from typing import Any, Callable, Dict, Generic, Optional

import os
from pathlib import Path

import typer
from click import Choice
from linky_note.dto.dto import LinkyNoteConfig, ModifyConfig, ParseConfig
from linky_note.usecases.config import Config
from linky_note.usecases.modify import modify
from linky_note.usecases.parse import parse
from linky_note.usecases.read_references import read_references
from linky_note.usecases.write import write
from typer.models import CommandFunctionType


def apply(
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
    parsed_files = parse(directory)
    files = read_references(parsed_files)
    files = modify(files)
    write(files, output_dir if output_dir else directory)


def init():
    config_dir = os.getcwd()
    config_filename = f".linky-note.yml"
    config_path: Path = Path(config_dir) / config_filename
    typer.echo(
        f"👋 Welcome in linky-note, we are going to edit your {config_filename}"
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


command_mapping: Dict[str, Optional[Callable[..., Any]]] = {
    "apply": apply,
    "init": init,
}
