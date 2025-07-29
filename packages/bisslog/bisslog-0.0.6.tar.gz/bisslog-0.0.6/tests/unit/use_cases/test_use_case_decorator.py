from unittest.mock import MagicMock, patch

import pytest

from bisslog import use_case


@pytest.fixture
def mock_context():
    with patch("bisslog.use_cases.use_case_decorator.tracing_opener") as tracer_mock, \
            patch("bisslog.use_cases.use_case_decorator.transaction_manager") as txn_mock:
        yield tracer_mock, txn_mock


def test_decorator_adds_is_use_case_attribute():

    @use_case
    def sample():
        return "ok"

    assert getattr(sample, "__is_use_case__", False) is True
    assert sample() == "ok"


def test_use_case_without_transaction_id(mock_context):
    tracer, txn = mock_context
    txn.create_transaction_id.return_value = "txn-123"

    tracer.start = MagicMock()
    tracer.end = MagicMock()
    txn.close_transaction = MagicMock()

    @use_case
    def sample():
        return "done"

    result = sample()
    assert result == "done"
    tracer.start.assert_called_once()
    tracer.end.assert_called_once()
    txn.close_transaction.assert_called_once()


def test_use_case_with_transaction_id_argument(mock_context):
    tracer, txn = mock_context
    txn.create_transaction_id.return_value = "txn-456"

    @use_case
    def sample(transaction_id=None):
        return f"received: {transaction_id}"

    result = sample()
    assert result == "received: txn-456"
    tracer.start.assert_called_once()
    tracer.end.assert_called_once()
    txn.close_transaction.assert_called_once()


def test_use_case_with_super_transaction_id(mock_context):
    tracer, txn = mock_context
    txn.create_transaction_id.return_value = "txn-789"

    @use_case
    def sample():
        return "value"

    result = sample(transaction_id="super-txn")
    assert result == "value"
    tracer.start.assert_called_once()
    tracer.end.assert_called_once_with(
        transaction_id="txn-789",
        component="sample",
        super_transaction_id="super-txn",
        result="value"
    )


def test_use_case_does_not_trace_if_disabled(mock_context):
    tracer, txn = mock_context

    @use_case(do_trace=False)
    def sample1():
        return "ok"

    @use_case(do_trace=False)
    def sample2():
        return sample1()

    result = sample2()
    assert result == "ok"
    tracer.start.assert_not_called()
    tracer.end.assert_not_called()
    txn.close_transaction.assert_not_called()


def test_use_case_does_not_trace_if_disabled_one(mock_context):
    tracer, txn = mock_context

    @use_case
    def sample1():
        return "ok"

    @use_case(do_trace=False)
    def sample2():
        return sample1()

    result = sample2()
    assert result == "ok"
    tracer.start.assert_called_once()
    tracer.end.assert_called_once()
    txn.close_transaction.assert_called_once()


def test_use_case_raises_exception_and_traces(mock_context):
    tracer, txn = mock_context
    txn.create_transaction_id.return_value = "txn-ex"

    @use_case
    def sample():
        raise ValueError("failed")

    with pytest.raises(ValueError, match="failed"):
        sample()

    tracer.start.assert_called_once()
    tracer.end.assert_called_once()
    txn.close_transaction.assert_called_once()
