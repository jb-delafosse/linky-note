from pathlib import Path
from unittest import mock

from linky_note.dto.dto import LinkyNoteConfig, ParseConfig
from linky_note.entrypoints.append_linked_references import app
from tests.e2e.common import check_files_did_not_change, runner


@mock.patch(
    "linky_note.usecases.config.Config.read",
    return_value=(
        LinkyNoteConfig(parse_config=ParseConfig(parse_wikilinks=False)),
    ),
)
def test_link_subfolders(_, working_dir):
    # Given
    input_directory = str(working_dir / Path("link_subfolders") / Path("data"))
    output_directory = "/tmp/test-link-subfolders"

    # When
    result = runner.invoke(
        app, ["apply", input_directory, "--output-dir", output_directory]
    )

    # Then
    assert result.exit_code == 0
    check_files_did_not_change(Path(input_directory), Path(output_directory))
