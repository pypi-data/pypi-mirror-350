from unittest.mock import MagicMock, patch

import pytest

from tests.unit.ports.tracing.fake_transactional_tracer import FakeTransactionalTracer


@pytest.fixture
def transactional_tracer():
    return FakeTransactionalTracer()


@patch("bisslog.ports.tracing.transactional_tracer.transaction_manager")
def test_re_args_with_main(mock_manager, transactional_tracer):
    """Test that _re_args_with_main returns expected dictionary."""
    mock_manager.get_main_transaction_id = MagicMock()
    mock_manager.get_main_transaction_id.return_value = "1234-5678"

    result = transactional_tracer._re_args_with_main()

    assert result == {"transaction_id": "1234-5678", "checkpoint_id": ""}


@patch("bisslog.ports.tracing.transactional_tracer.transaction_manager")
def test_re_args_with_current(mock_manager, transactional_tracer):
    """Test that _re_args_with_current returns expected dictionary."""
    mock_manager.get_transaction_id = MagicMock()
    mock_manager.get_transaction_id.return_value = "8765-4321"

    result = transactional_tracer._re_args_with_current()

    assert result == {"transaction_id": "8765-4321", "checkpoint_id": ""}


@patch("bisslog.ports.tracing.transactional_tracer.transaction_manager")
def test_re_args_with_main_defaults(mock_manager, transactional_tracer):
    mock_manager.get_main_transaction_id = MagicMock()
    mock_manager.get_main_transaction_id.return_value = "main-tx-id"

    result = transactional_tracer._re_args_with_main()

    assert result == {
        "transaction_id": "main-tx-id",
        "checkpoint_id": ""
    }
    mock_manager.get_main_transaction_id.assert_called_once()


@patch("bisslog.ports.tracing.transactional_tracer.transaction_manager")
def test_re_args_with_main_provided_values(mock_manager, transactional_tracer):
    result = transactional_tracer._re_args_with_main(transaction_id="tx-123",
                                                     checkpoint_id="cp-456")

    assert result == {
        "transaction_id": "tx-123",
        "checkpoint_id": "cp-456"
    }
    mock_manager.get_main_transaction_id.assert_not_called()


@patch("bisslog.ports.tracing.transactional_tracer.transaction_manager")
def test_re_args_with_current_defaults(mock_manager, transactional_tracer):
    mock_manager.get_transaction_id.return_value = "current-tx-id"

    result = transactional_tracer._re_args_with_current()

    assert result == {
        "transaction_id": "current-tx-id",
        "checkpoint_id": ""
    }
    mock_manager.get_transaction_id.assert_called_once()


@patch("bisslog.ports.tracing.transactional_tracer.transaction_manager")
def test_re_args_with_current_provided_values(mock_manager, transactional_tracer):
    result = transactional_tracer._re_args_with_current(transaction_id="tx-999",
                                                        checkpoint_id="cp-abc")

    assert result == {
        "transaction_id": "tx-999",
        "checkpoint_id": "cp-abc"
    }
    mock_manager.get_transaction_id.assert_not_called()
