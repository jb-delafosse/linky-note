import typer
from linky_note.entrypoints.commands import command_mapping
from linky_note.infrastructure.db_connection import setup_db
from linky_note.infrastructure.markdown import setup_markdown
from linky_note.interfaces import (
    modifier,
    parser,
    reference_extractor,
    references_db,
    renderer,
)
from typer.core import TyperCommand
from typer.models import CommandInfo


def setup_app(config) -> typer.Typer:
    references_db.REFERENCE_DB_FACTORY = setup_db()
    (
        parser.PARSER,
        reference_extractor.EXTRACTOR_FACTORY,
        modifier.MODIFIER,
        renderer.RENDERER,
    ) = setup_markdown(config)

    app = typer.Typer(
        name="linky-note",
        help='linky-note adds a "Linked References" at the bottom of you markdown files',
        add_completion=False,
    )

    for command_name, command in command_mapping.items():
        app.registered_commands.append(
            CommandInfo(
                name=command_name,
                cls=TyperCommand,
                callback=command,
            )
        )
    return app
