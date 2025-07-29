from typing import Optional
from unittest.mock import MagicMock

from bisslog.ports.upload_file import IUploadFile


class UploadFileMock(IUploadFile):
    def upload_file_from_local(self, local_path: str, remote_path: str, *args,
                               transaction_id: Optional[str] = None, **kwargs) -> bool:
        return True

    def upload_file_stream(self, remote_path: str, stream: bytes, *args,
                           transaction_id: Optional[str] = None, **kwargs) -> bool:
        return True


def test_upload_file_from_local():
    uploader = UploadFileMock()
    uploader_mock = MagicMock(wraps=uploader)

    assert uploader_mock.upload_file_from_local("local.txt", "remote.txt") is True
    uploader_mock.upload_file_from_local.assert_called_once_with("local.txt", "remote.txt")


def test_upload_file_stream():
    uploader = UploadFileMock()
    uploader_mock = MagicMock(wraps=uploader)

    assert uploader_mock.upload_file_stream("remote.txt", b"data") is True
    uploader_mock.upload_file_stream.assert_called_once_with("remote.txt", b"data")
