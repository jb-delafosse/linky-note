from typing import Dict

import hashlib
import os
from pathlib import Path

from typer.testing import CliRunner

runner = CliRunner()


def check_files_did_not_change(input_dir: Path, output_dir: Path) -> None:
    input_files_md5 = hash_files(input_dir)
    output_files_md5 = hash_files(output_dir)

    for key, checksum in input_files_md5.items():
        try:
            assert input_files_md5[key] == output_files_md5[key]
        except AssertionError as _:
            raise Exception(f"Input is different from output for {key}")

    for key, checksum in output_files_md5.items():
        try:
            assert input_files_md5[key] == output_files_md5[key]
        except AssertionError as _:
            raise Exception(f"Input is different from output for {key}")


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
