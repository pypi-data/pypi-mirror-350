"""Module providing logging-based implementation of the TransactionalTracer interface."""

import logging
from typing import Optional, Any

from ...ports.tracing.transactional_tracer import TransactionalTracer


class TransactionalTracerLogging(TransactionalTracer):
    """Implementation of TransactionalTracer that logs messages using Python's logging module."""

    def __init__(self):
        self._logger = logging.getLogger("transactional-tracer")

    def info(self, payload: Any, *args, transaction_id: Optional[str] = None,
             checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs an informational message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None."""
        new_extra = self._re_args_with_main(transaction_id, checkpoint_id)
        if extra:
            new_extra.update(extra)
        self._logger.info(payload, *args, **kwargs, extra=new_extra)

    def debug(self, payload: Any, *args, transaction_id: Optional[str] = None,
              checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs a debug message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.        """
        new_extra = self._re_args_with_main(transaction_id, checkpoint_id)
        if extra:
            new_extra.update(extra)
        self._logger.debug(payload, *args, **kwargs, extra=new_extra)

    def warning(self, payload: Any, *args, transaction_id: Optional[str] = None,
                checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs a warning message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.        """
        new_extra = self._re_args_with_main(transaction_id, checkpoint_id)
        if extra:
            new_extra.update(extra)
        self._logger.warning(payload, *args, **kwargs, extra=new_extra)

    def error(self, payload: Any, *args, transaction_id: Optional[str] = None,
              checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs an error message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None."""
        new_extra = self._re_args_with_main(transaction_id, checkpoint_id)
        if extra:
            new_extra.update(extra)
        self._logger.error(payload, *args, **kwargs, extra=new_extra)

    def critical(self, payload: Any, *args, transaction_id: Optional[str] = None,
                 checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs a critical error message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.        """
        new_extra = self._re_args_with_main(transaction_id, checkpoint_id)
        if extra:
            new_extra.update(extra)
        self._logger.critical(payload, *args, **kwargs, extra=new_extra)

    def func_error(self, payload: Any, *args, transaction_id: Optional[str] = None,
                   checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs a function-related error message.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.        """
        new_extra = self._re_args_with_main(transaction_id, checkpoint_id)
        if extra:
            new_extra.update(extra)
        self._logger.error(payload, *args, **kwargs, extra=new_extra)

    def tech_error(self, payload: Any, *args, transaction_id: Optional[str] = None,
                   checkpoint_id: Optional[str] = None, error: Exception = None, extra: dict = None,
                   **kwargs):
        """Logs a technical error message, optionally including an exception.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None.
        error: Exception
            Captured error to be logged."""
        new_extra = self._re_args_with_main(transaction_id, checkpoint_id)
        if extra:
            new_extra.update(extra)
        error_payload = ""
        if isinstance(error, Exception):
            error_payload = ": " + str(error)

        self._logger.critical(str(payload) + error_payload , *args, **kwargs, extra=new_extra)

    def report_start_external(self, payload: Any, *args, transaction_id: Optional[str] = None,
                              checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs the start of an external operation.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None."""
        new_extra = self._re_args_with_main(transaction_id, checkpoint_id)
        if extra:
            new_extra.update(extra)
        self._logger.info(payload, *args, **kwargs, extra=new_extra)

    def report_end_external(self, payload: Any, *args, transaction_id: Optional[str] = None,
                            checkpoint_id: Optional[str] = None, extra: dict = None, **kwargs):
        """Logs the end of an external operation.

        Parameters
        ----------
        payload : Any
            The message or object to log.
        transaction_id : Optional[str], optional
            An identifier for the transaction, by default None.
        checkpoint_id : Optional[str], optional
            An identifier for the logging checkpoint, by default None.
        extra : dict, optional
            Additional logging context, by default None."""
        new_extra = self._re_args_with_main(transaction_id, checkpoint_id)
        if extra:
            new_extra.update(extra)
        self._logger.info(payload, *args, **kwargs, extra=new_extra)
