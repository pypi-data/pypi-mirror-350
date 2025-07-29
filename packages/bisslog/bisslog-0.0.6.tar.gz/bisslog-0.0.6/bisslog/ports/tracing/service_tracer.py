"""Module defining the ServiceTracer interface."""

from abc import ABC, abstractmethod
from typing import Optional, Any

from .tracer import Tracer


class ServiceTracer(Tracer, ABC):
    """Abstract base class for service tracing.

    This class extends `Tracer` and defines a contract for implementing
    service-level tracing mechanisms.

    Notes
    -----
    - This class is intended to be subclassed by specific service tracing implementations.
    - It does not define any concrete methods but serves as a structural base."""

    @abstractmethod
    def info(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
             extra: dict = None, **kwargs):
        """Logs an informational message.

        Parameters
        ----------
        payload : Any
            The data or message to be logged.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional logging context, by default None."""
        raise NotImplementedError("TracingManager must implement method info")  # pragma: no cover

    @abstractmethod
    def debug(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
              extra: dict = None, **kwargs):
        """Logs a debug message.

        Parameters
        ----------
        payload : Any
            The data or message to be logged.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging."""
        raise NotImplementedError("TracingManager must implement method debug")  # pragma: no cover

    @abstractmethod
    def warning(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
                extra: dict = None, **kwargs):
        """Logs a warning message.

        Parameters
        ----------
        payload : Any
            The data or message to be logged.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging."""
        raise NotImplementedError(
            "TracingManager must implement method warning")  # pragma: no cover

    @abstractmethod
    def error(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
              extra: dict = None, **kwargs):
        """Logs an error message.

        Parameters
        ----------
        payload : Any
            The data or message to be logged.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging."""
        raise NotImplementedError("TracingManager must implement method error")  # pragma: no cover

    @abstractmethod
    def critical(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
                 extra: dict = None, **kwargs):
        """Logs a critical error message.

        Parameters
        ----------
        payload : Any
            The data or message to be logged.
        checkpoint_id : str, optional
            An identifier for the tracing checkpoint.
        extra : dict, optional
            Additional context information for debugging."""
        raise NotImplementedError(
            "TracingManager must implement method critical")  # pragma: no cover
