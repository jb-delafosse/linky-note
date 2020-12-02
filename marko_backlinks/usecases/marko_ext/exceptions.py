from typing import Optional


class MarkoBacklinksException(Exception):
    """Base class for all business errors in marko-backlinks.
    Args:
        code: An unique identifier for this kind of error.
    """

    def __init__(self, code: str, message: Optional[str] = None) -> None:
        self.code = code
        super().__init__(message)


class TitleNotFoundException(Exception):
    def __init__(self):
        super().__init__("title_not_found", f"Title Not Found.")


class TwoTitlesFoundException(Exception):
    def __init__(self):
        super().__init__("two_titles_found", f"Two Titles Found.")
