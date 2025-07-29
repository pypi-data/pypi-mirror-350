import pytest

from bisslog.adapters.tracing.transactional_tracer_logging import TransactionalTracerLogging


@pytest.fixture
def tracer():
    """Returns an instance of TransactionalTracerLogging."""
    return TransactionalTracerLogging()


@pytest.mark.parametrize("method, level", [
    ("debug", "DEBUG"),
    ("info", "INFO"),
    ("warning", "WARNING"),
    ("error", "ERROR"),
    ("critical", "CRITICAL"),
    ("func_error", "ERROR"),
    ("tech_error", "CRITICAL"),
    ("report_start_external", "INFO"),
    ("report_end_external", "INFO"),
])
@pytest.mark.parametrize("payload", [
    ("plain string",),
    ("plain string with params %s", "Hello"),
    (42,),
    ({"key": "value"},),
    (["a", "b", "c"],),
    (Exception("something went wrong"),),
    (object(),),
])
def test_logging_payloads(tracer, caplog, method, level, payload):
    """Tests all log levels with various payload types."""
    log_func = getattr(tracer, method)

    with caplog.at_level(level):
        if method == "tech_error":
            log_func(*payload, error=ValueError("test exception"), transaction_id="tx123",
                     checkpoint_id="cp456", extra={"extra_key1": "something"})
        else:
            log_func(*payload, transaction_id="tx123", checkpoint_id="cp456",
                     extra={"extra_key1": "something"})

    # Confirm that something was logged
    assert len(caplog.records) > 0
    last_record = caplog.records[-1]
    assert last_record.levelname == level
    assert "tx123" in last_record.__dict__.get("extra", {}) or last_record.__dict__.get(
        "transaction_id") == "tx123"
    assert "cp456" in last_record.__dict__.get("extra", {}) or last_record.__dict__.get(
        "checkpoint_id") == "cp456"
    assert str(payload[0]).split()[0] in last_record.message


def test_raises_tech_error_with_string_exception(tracer, caplog):
    """Ensures tech_error logs exception details."""
    with caplog.at_level("CRITICAL"):
        tracer.tech_error("Error occurred", error=RuntimeError("fail!"), transaction_id="tx-id")

    assert any("fail!" in record.message for record in caplog.records)
    assert any("Error occurred" in record.message for record in caplog.records)
