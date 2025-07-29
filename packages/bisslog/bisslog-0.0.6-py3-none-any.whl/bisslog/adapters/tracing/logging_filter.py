"""Bisslog Filter for Logging."""

import logging


class BisslogFilterLogging(logging.Filter):
    """A custom logging filter to enforce transaction-related attributes.

    This filter ensures that log records always contain the attributes
    `transaction_id` and `checkpoint_id`. If these attributes are missing,
    it assigns default values.

    Methods
    -------
    filter(record)
        Ensures `transaction_id` and `checkpoint_id` exist in the log record."""

    def filter(self, record):
        """Add default `transaction_id` and `checkpoint_id` to log records if missing.

        Parameters
        ----------
        record : logging.LogRecord
            The log record being processed.

        Returns
        -------
        bool
            Always returns True to allow log processing to continue."""
        if not hasattr(record, "transaction_id"):
            record.transaction_id = "service-logging"
        if not hasattr(record, "checkpoint_id"):
            record.checkpoint_id = "unknown-checkpoint"
        return True
