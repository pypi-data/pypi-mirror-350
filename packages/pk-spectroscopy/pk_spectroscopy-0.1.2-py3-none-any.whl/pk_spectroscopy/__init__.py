"""
pK Spectroscopy
========
Advanced analysis of objects with complex acid composition.

Main entry point: ``pK_Spectroscopy`` class.
"""

from __future__ import annotations
from importlib.metadata import version, PackageNotFoundError

from .core import pK_Spectroscopy, TitrationMode

__all__: list[str] = ["pK_Spectroscopy", "TitrationMode"]

try:
    __version__: str = version(__name__)
except PackageNotFoundError:
    from ._version import __version__
