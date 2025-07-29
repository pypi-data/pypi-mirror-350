import logging

import pytest

from bisslog.adapters.tracing.transactional_tracer_logging import TransactionalTracerLogging


@pytest.fixture
def transactional_tracer():
    """Creates an instance of TransactionalTracerLogging."""
    return TransactionalTracerLogging()


def test_info_log(transactional_tracer, caplog):
    """Ensures the info method logs correctly."""
    with caplog.at_level(logging.INFO):
        transactional_tracer.info("Info message", transaction_id="tx-1", checkpoint_id="cp-1")

    assert any("Info message" in record.message for record in caplog.records)
    assert any(record.levelname == "INFO" for record in caplog.records)


def test_debug_log(transactional_tracer, caplog):
    """Ensures the debug method logs correctly."""
    with caplog.at_level(logging.DEBUG):
        transactional_tracer.debug("Debug message", transaction_id="tx-2", checkpoint_id="cp-2")

    assert any("Debug message" in record.message for record in caplog.records)
    assert any(record.levelname == "DEBUG" for record in caplog.records)


def test_warning_log(transactional_tracer, caplog):
    """Ensures the warning method logs correctly."""
    with caplog.at_level(logging.WARNING):
        transactional_tracer.warning("Warning message", transaction_id="tx-3", checkpoint_id="cp-3")

    assert any("Warning message" in record.message for record in caplog.records)
    assert any(record.levelname == "WARNING" for record in caplog.records)


def test_error_log(transactional_tracer, caplog):
    """Ensures the error method logs correctly."""
    with caplog.at_level(logging.ERROR):
        transactional_tracer.error("Error message", transaction_id="tx-4", checkpoint_id="cp-4")

    assert any("Error message" in record.message for record in caplog.records)
    assert any(record.levelname == "ERROR" for record in caplog.records)


def test_critical_log(transactional_tracer, caplog):
    """Ensures the critical method logs correctly."""
    with caplog.at_level(logging.CRITICAL):
        transactional_tracer.critical("Critical message", transaction_id="tx-5",
                                      checkpoint_id="cp-5")

    assert any("Critical message" in record.message for record in caplog.records)
    assert any(record.levelname == "CRITICAL" for record in caplog.records)


def test_func_error_log(transactional_tracer, caplog):
    """Ensures func_error logs as an error."""
    with caplog.at_level(logging.ERROR):
        transactional_tracer.func_error("Function error", transaction_id="tx-6",
                                        checkpoint_id="cp-6")

    assert any("Function error" in record.message for record in caplog.records)
    assert any(record.levelname == "ERROR" for record in caplog.records)


def test_tech_error_log(transactional_tracer, caplog):
    """Ensures tech_error logs as a critical error with exception details."""
    with caplog.at_level(logging.CRITICAL):
        try:
            raise ValueError("Test exception")
        except ValueError as e:
            transactional_tracer.tech_error("Tech error occurred", error=e, transaction_id="tx-7",
                                            checkpoint_id="cp-7")

    assert any("Test exception" in record.message for record in caplog.records)
    assert any(record.levelname == "CRITICAL" for record in caplog.records)


def test_report_start_external_log(transactional_tracer, caplog):
    """Ensures report_start_external logs as info."""
    with caplog.at_level(logging.INFO):
        transactional_tracer.report_start_external("Start external process", transaction_id="tx-8",
                                                   checkpoint_id="cp-8")

    assert any("Start external process" in record.message for record in caplog.records)
    assert any(record.levelname == "INFO" for record in caplog.records)


def test_report_end_external_log(transactional_tracer, caplog):
    """Ensures report_end_external logs as info."""
    with caplog.at_level(logging.INFO):
        transactional_tracer.report_end_external("End external process", transaction_id="tx-9",
                                                 checkpoint_id="cp-9")

    assert any("End external process" in record.message for record in caplog.records)
    assert any(record.levelname == "INFO" for record in caplog.records)
