"""Module defining the abstract Tracer class for logging and tracing."""

from abc import ABC


class Tracer(ABC):
    """Abstract base class for logging and tracing events.

    This class defines methods for logging information, debugging, warnings,
    errors, and critical issues, ensuring a consistent tracing mechanism."""
