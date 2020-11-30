# type: ignore[attr-defined]
"""Awesome `marko-backlinks` is a Python cli/package created with https://github.com/TezRomacH/python-package-template"""

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
