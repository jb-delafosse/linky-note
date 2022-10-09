from pathlib import Path
from unittest import mock

from linky_note.dto.dto import NotePath
from linky_note.usecases.parse import parse
from marko.block import Document


@mock.patch(
    "os.walk",
    return_value=(
        ("", [], ["Marketing.md", "DigitalMarketing.md", "BusinessUnit.md"]),
    ),
)
def test_parse_nominal(mock_walk, note_parser):
    # Given
    directory = Path()
    note_parser.return_value = object.__new__(Document)

    # When
    parsed_files = parse(directory)

    # Then
    assert NotePath(Path("Marketing.md")) in parsed_files
    assert NotePath(Path("DigitalMarketing.md")) in parsed_files
    assert NotePath(Path("BusinessUnit.md")) in parsed_files
