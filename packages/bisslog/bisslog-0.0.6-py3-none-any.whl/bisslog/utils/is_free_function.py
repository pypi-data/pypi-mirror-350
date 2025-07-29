"""Module with a utility function to check if a callable is a free function."""
import inspect
from types import FunctionType
from typing import Callable


def is_free_function(fn: Callable) -> bool:
    """
    Determines if a callable is a standalone function (not a method).

    Parameters
    ----------
    fn : Callable
        The callable to check.

    Returns
    -------
    bool
        True if it's a free function, False otherwise.
    """
    return isinstance(fn, FunctionType) and not inspect.ismethod(fn)
