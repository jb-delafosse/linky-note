from typing import Dict

import hashlib
import os
from pathlib import Path
from unittest import mock

import pytest
from linky_note.dto.dto import LinkyNoteConfig, ParseConfig
from linky_note.entrypoints.append_linked_references import app
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(scope="function")
def working_dir() -> Path:
    return os.path.dirname(os.path.abspath(__file__))


def check_files_did_not_change(input_dir: Path, output_dir: Path) -> None:
    input_files_md5 = hash_files(input_dir)
    output_files_md5 = hash_files(output_dir)

    for key, checksum in input_files_md5.items():
        assert input_files_md5[key] == output_files_md5[key]

    for key, checksum in output_files_md5.items():
        assert input_files_md5[key] == output_files_md5[key]


def hash_files(input_dir) -> Dict[str, str]:
    input_files = {}
    for dirpath, dir, filenames in os.walk(input_dir):
        for filename in filenames:
            input_file = Path(os.path.join(dirpath, filename))
            rel_dir = os.path.relpath(dirpath, input_dir)
            rel_path = Path(os.path.join(rel_dir, filename))
            with open(input_file, "rb") as f:
                input_files[str(rel_path)] = hashlib.md5(f.read()).hexdigest()
    return input_files


@mock.patch(
    "linky_note.usecases.config.Config.read",
    return_value=(
        LinkyNoteConfig(parse_config=ParseConfig(parse_wikilinks=False)),
    ),
)
def test_link(_, working_dir):
    # Given
    input_directory = str(working_dir / Path("data"))
    output_directory = "/tmp/test-link"

    # When
    result = runner.invoke(
        app, ["apply", input_directory, "--output-dir", output_directory]
    )

    # Then
    assert result.exit_code == 0
    check_files_did_not_change(Path(input_directory), Path(output_directory))
