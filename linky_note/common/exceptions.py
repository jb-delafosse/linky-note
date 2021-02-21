# This module contains all business Exceptions.
#
# This Exception must correspond to a business case and not
# have technicals information.
from typing import Optional


class LinkyNoteError(Exception):
    """Base class for all business errors in linky-note.
    Args:
        code: An unique indentifier for this kind of error.
    """

    def __init__(self, code: str, message: Optional[str] = None) -> None:
        self.code = code
        super().__init__(message)


class InvalidNoteError(LinkyNoteError):
    def __init__(self, message: Optional[str] = None) -> None:
        super().__init__(code="invalid-note", message=message)
