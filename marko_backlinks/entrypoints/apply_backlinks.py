import argparse
import glob
import os

from marko import Markdown
from marko.md_renderer import MarkdownRenderer
from marko_backlinks.adapters.references_db.factories import (
    SqlReferenceDatabaseFactory,
)
from marko_backlinks.infrastructure.db_connection import ENGINE
from marko_backlinks.interfaces import references_db
from marko_backlinks.usecases.extension import ReferencesExtension

references_db.REFERENCE_DB_FACTORY = SqlReferenceDatabaseFactory(ENGINE)
converter = Markdown(
    renderer=MarkdownRenderer, extensions=[ReferencesExtension]
)


def main(directory):
    files = {}
    for filename in glob.glob(os.path.join(directory, "*.md")):
        print(filename)
        with open(filename) as file:
            ast = converter.parse(file.read())
            files[filename] = ast
    for filename, ast in files.items():
        with open(filename, "w") as file:
            text = converter.render(ast)
            file.write(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory", type=str, help="the directory that contains all the notes"
    )
    args = parser.parse_args()
    main(directory=args.directory)
