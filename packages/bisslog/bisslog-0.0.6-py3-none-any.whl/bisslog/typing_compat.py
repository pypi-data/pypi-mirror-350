"""
Typing compatibility layer for Python 3.7–3.13.

This module provides fallbacks for newer typing constructs like ParamSpec.
"""

from typing import TypeVar

R = TypeVar("R")

try:
    from typing import ParamSpec  # Python 3.10+
    P = ParamSpec("P")
except ImportError:
    try:
        from typing_extensions import ParamSpec  # Python 3.7–3.9
        P = ParamSpec("P")

    except ImportError:
        P = None
        ParamSpec = None  # ParamSpec not available


__all__ = ["P", "R", "ParamSpec"]
