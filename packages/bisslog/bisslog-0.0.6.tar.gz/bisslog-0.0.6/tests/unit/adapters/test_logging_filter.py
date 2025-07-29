import logging

import pytest

from bisslog.adapters.tracing.logging_filter import \
    BisslogFilterLogging  # Replace 'your_module' with the actual module name


@pytest.fixture
def log_record():
    """Creates a log record for testing purposes."""
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Test log message",
        args=(),
        exc_info=None,
    )
    return record


@pytest.fixture
def bisslog_filter():
    """Creates an instance of BisslogFilterLogging for testing."""
    return BisslogFilterLogging()


def test_filter_adds_missing_attributes(bisslog_filter, log_record):
    """Tests that the filter adds missing attributes `transaction_id` and `checkpoint_id`."""
    assert not hasattr(log_record, "transaction_id")
    assert not hasattr(log_record, "checkpoint_id")

    bisslog_filter.filter(log_record)

    assert log_record.transaction_id == "service-logging"
    assert log_record.checkpoint_id == "unknown-checkpoint"


def test_filter_preserves_existing_attributes(bisslog_filter, log_record):
    """Tests that the filter does not overwrite existing `transaction_id` and `checkpoint_id`."""
    log_record.transaction_id = "custom-tx-id"
    log_record.checkpoint_id = "custom-checkpoint"

    bisslog_filter.filter(log_record)

    assert log_record.transaction_id == "custom-tx-id"
    assert log_record.checkpoint_id == "custom-checkpoint"


def test_filter_allows_logging(bisslog_filter, log_record):
    """Tests that the filter always returns True to allow logging to continue."""
    result = bisslog_filter.filter(log_record)
    assert result is True
