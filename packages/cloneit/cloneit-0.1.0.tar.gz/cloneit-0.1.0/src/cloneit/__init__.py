"""
cloneit - A lightweight Python package inspired by RPGLE LIKE keyword

This package provides a simple way to define reusable field templates
and clone them with optional overrides, similar to the LIKE keyword in RPGLE.
"""

from .core import FieldTemplate, Field
from .exceptions import CloneItError, TemplateNotFoundError

__all__ = ["FieldTemplate", "Field", "CloneItError", "TemplateNotFoundError"]

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
