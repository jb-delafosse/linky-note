from pathlib import Path

from linky_note.dto.dto import LinkyNoteConfig, ParseConfig
from linky_note.infrastructure.cli_app import setup_app
from tests.e2e.common import check_files_did_not_change, runner


def test_link_subfolders(working_dir):
    # Given
    input_directory = str(working_dir / Path("link_subfolders") / Path("data"))
    output_directory = "/tmp/test-link-subfolders"
    app = setup_app(
        LinkyNoteConfig(parse_config=ParseConfig(parse_wikilinks=False))
    )

    # When
    result = runner.invoke(
        app, ["apply", input_directory, "--output-dir", output_directory]
    )

    # Then
    assert result.exit_code == 0
    check_files_did_not_change(Path(input_directory), Path(output_directory))
