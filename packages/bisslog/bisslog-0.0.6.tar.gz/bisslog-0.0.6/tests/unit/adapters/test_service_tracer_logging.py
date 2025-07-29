import logging

import pytest

from bisslog.adapters.tracing.service_tracer_logging import ServiceTracerLogging


@pytest.fixture
def service_tracer():
    """Creates an instance of ServiceTracerLogging."""
    return ServiceTracerLogging()


@pytest.fixture
def setup_logger():
    """Configures a test logger."""
    logger = logging.getLogger("service-logger")
    logger.setLevel(logging.DEBUG)
    return logger


def test_info_log(service_tracer, caplog):
    """Ensures the info method logs correctly."""
    with caplog.at_level(logging.INFO):
        service_tracer.info("Info message", checkpoint_id="checkpoint-1")

    assert any("Info message" in record.message for record in caplog.records)
    assert any(record.levelname == "INFO" for record in caplog.records)


def test_debug_log(service_tracer, caplog):
    """Ensures the debug method logs correctly."""
    with caplog.at_level(logging.DEBUG):
        service_tracer.debug("Debug message", checkpoint_id="checkpoint-2")

    assert any("Debug message" in record.message for record in caplog.records)
    assert any(record.levelname == "DEBUG" for record in caplog.records)


def test_warning_log(service_tracer, caplog):
    """Ensures the warning method logs correctly."""
    with caplog.at_level(logging.WARNING):
        service_tracer.warning("Warning message", checkpoint_id="checkpoint-3")

    assert any("Warning message" in record.message for record in caplog.records)
    assert any(record.levelname == "WARNING" for record in caplog.records)


def test_error_log(service_tracer, caplog):
    """Ensures the error method logs correctly."""
    with caplog.at_level(logging.ERROR):
        service_tracer.error("Error message", checkpoint_id="checkpoint-4")

    assert any("Error message" in record.message for record in caplog.records)
    assert any(record.levelname == "ERROR" for record in caplog.records)


def test_critical_log(service_tracer, caplog):
    """Ensures the critical method logs correctly."""
    with caplog.at_level(logging.CRITICAL):
        service_tracer.critical("Critical message", checkpoint_id="checkpoint-5")

    assert any("Critical message" in record.message for record in caplog.records)
    assert any(record.levelname == "CRITICAL" for record in caplog.records)


def test_func_error_log(service_tracer, caplog):
    """Ensures func_error logs as an error."""
    with caplog.at_level(logging.ERROR):
        service_tracer.func_error("Function error", checkpoint_id="checkpoint-6")

    assert any("Function error" in record.message for record in caplog.records)
    assert any(record.levelname == "ERROR" for record in caplog.records)


def test_tech_error_log(service_tracer, caplog):
    """Ensures tech_error logs as a critical error with exception details."""
    with caplog.at_level(logging.CRITICAL):
        try:
            raise ValueError("Test exception")
        except ValueError as e:
            service_tracer.tech_error("Tech error occurred", error=e, checkpoint_id="checkpoint-7")

    assert any("Tech error occurred Test exception" in record.message for record in caplog.records)
    assert any(record.levelname == "CRITICAL" for record in caplog.records)


def test_report_start_external_log(service_tracer, caplog):
    """Ensures report_start_external logs as info."""
    with caplog.at_level(logging.INFO):
        service_tracer.report_start_external("Start external process", checkpoint_id="checkpoint-8")

    assert any("Start external process" in record.message for record in caplog.records)
    assert any(record.levelname == "INFO" for record in caplog.records)


def test_report_end_external_log(service_tracer, caplog):
    """Ensures report_end_external logs as info."""
    with caplog.at_level(logging.INFO):
        service_tracer.report_end_external("End external process", checkpoint_id="checkpoint-9")

    assert any("End external process" in record.message for record in caplog.records)
    assert any(record.levelname == "INFO" for record in caplog.records)
