from unittest.mock import MagicMock, patch

import pytest

from bisslog import FullUseCase, use_case as use_case_decorator


class ConcreteUseCase(FullUseCase):
    _publisher = MagicMock()
    _upload_file_adapter = MagicMock()

    @use_case_decorator
    def use(self, *args, **kwargs):
        """Concrete implementation of the use case."""
        pass


@pytest.fixture
def use_case():
    return ConcreteUseCase()


@patch("bisslog.use_cases.use_case_full.bisslog_pubsub.main")
def test_publish_calls_publisher(mock_publisher, use_case):
    """Verifies that publish() delegates correctly to the publisher adapter."""
    queue = "events"
    payload = {"event": "created"}

    use_case.publish(queue, payload, partition="p1", key="value")

    mock_publisher.assert_called_once_with(queue, payload, partition="p1", key="value")


@patch("bisslog.use_cases.use_case_full.bisslog_upload_file.main")
def test_upload_file_stream_calls_uploader(mock_uploader, use_case):
    """Verifies that upload_file_stream() delegates correctly to the uploader adapter."""
    stream = b"file content"
    remote_path = "files/output.txt"
    mock_uploader.upload_file_stream.return_value = True

    result = use_case.upload_file_stream(remote_path, stream, transaction_id="tx123", extra="info")

    mock_uploader.upload_file_stream.assert_called_once_with(
        remote_path, stream, transaction_id="tx123", extra="info"
    )
    assert result is True


@patch("bisslog.use_cases.use_case_full.bisslog_upload_file.main")
def test_upload_file_from_local_calls_uploader(mock_uploader, use_case):
    """Verifies that upload_file_from_local() delegates correctly to the uploader adapter."""
    local_path = "/tmp/file.csv"
    remote_path = "remote/file.csv"
    mock_uploader.upload_file_from_local.return_value = False

    result = use_case.upload_file_from_local(local_path, remote_path, transaction_id="abc")

    mock_uploader.upload_file_from_local.assert_called_once()
    assert result is False
