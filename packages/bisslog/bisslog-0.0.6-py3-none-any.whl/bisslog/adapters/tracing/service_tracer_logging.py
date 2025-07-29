"""Module providing logging-based implementation of the ServiceTracer interface."""
import logging
from typing import Optional, Any

from ...ports.tracing.service_tracer import ServiceTracer


class ServiceTracerLogging(ServiceTracer):
    """Implementation of ServiceTracer that logs messages using Python's logging module."""

    def __init__(self):
        self._logger = logging.getLogger("service-logger")

    def info(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
             extra: dict = None, **kwargs):
        """Logs an informational message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        args: tuple
            Arguments to pass to the logger.
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.
        kwargs
            Keyword arguments"""
        extra = extra or {}
        extra['checkpoint_id'] = checkpoint_id or ''
        extra['transaction_id'] = 'service-logging'
        self._logger.info(payload, *args, **kwargs, extra=extra)

    def debug(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
              extra: dict = None, **kwargs):
        """Logs a debug message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        args: tuple
            Arguments to pass to the logger
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.
        kwargs
            Keyword arguments"""
        extra = extra or {}
        extra['checkpoint_id'] = checkpoint_id or ''
        extra['transaction_id'] = 'service-logging'
        self._logger.debug(payload, *args, **kwargs)

    def warning(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
                extra: dict = None, **kwargs):
        """Logs a warning message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        args: tuple
            Arguments to pass to the logger
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.
        kwargs
            Keyword arguments"""
        extra = extra or {}
        extra['checkpoint_id'] = checkpoint_id or ''
        extra['transaction_id'] = 'service-logging'
        self._logger.warning(payload, *args, **kwargs, extra=extra)

    def error(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
              extra: dict = None, **kwargs):
        """Logs an error message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        args: tuple
            Arguments to pass to the logger
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.
        kwargs
            Keyword arguments"""
        extra = extra or {}
        extra['checkpoint_id'] = checkpoint_id or ''
        extra['transaction_id'] = 'service-logging'
        self._logger.error(payload, *args, **kwargs, extra=extra)

    def critical(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
                 extra: dict = None, **kwargs):
        """Logs a critical error message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        args: tuple
            Arguments to pass to the logger
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.
        kwargs
            Keyword arguments"""
        extra = extra or {}
        extra['checkpoint_id'] = checkpoint_id or ''
        extra['transaction_id'] = 'service-logging'
        self._logger.critical(payload, *args, **kwargs, extra=extra)

    def func_error(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
                   extra: dict = None, **kwargs):
        """Logs a function-related error message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        args: tuple
            Arguments to pass to the logger
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.
        kwargs
            Keyword arguments"""
        extra = extra or {}
        extra['checkpoint_id'] = checkpoint_id or ''
        extra['transaction_id'] = 'service-logging'
        self._logger.error(payload, *args, **kwargs, extra=extra)

    def tech_error(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
                   error: Exception = None, extra: dict = None, **kwargs):
        """Logs a technical error message, optionally including an exception.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        args: tuple
            Arguments to pass to the logger
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        error : Exception, optional
            The exception to include in the log, by default None.
        extra : dict, optional
            Additional logging context, by default None.
        kwargs
            Keyword arguments"""
        new_payload: str = str(payload)
        if error is not None:
            new_payload = new_payload + " " + str(error)
        extra = extra or {}
        extra['checkpoint_id'] = checkpoint_id or ''
        extra['transaction_id'] = 'service-logging'
        self._logger.critical(new_payload, *args, **kwargs, extra=extra)

    def report_start_external(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
                              extra: dict = None, **kwargs):
        """Logs the start of an external process or interaction.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        args: tuple
            Arguments to pass to the logger
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.
        kwargs
            Keyword arguments"""
        extra = extra or {}
        extra['checkpoint_id'] = checkpoint_id or ''
        extra['transaction_id'] = 'service-logging'
        self._logger.info(payload, *args, **kwargs, extra=extra)

    def report_end_external(self, payload: Any, *args, checkpoint_id: Optional[str] = None,
                            extra: dict = None, **kwargs):
        """Logs the end of an external process or interaction.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        args: tuple
            Arguments to pass to the logger
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.
        kwargs
            Keyword arguments"""
        extra = extra or {}
        extra['checkpoint_id'] = checkpoint_id or ''
        extra['transaction_id'] = 'service-logging'
        self._logger.info(payload, *args, **kwargs, extra=extra)
