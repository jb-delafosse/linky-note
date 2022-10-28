import os
from pathlib import Path

import pytest


@pytest.fixture(scope="function")
def working_dir() -> Path:
    return Path(os.path.dirname(os.path.abspath(__file__)))
