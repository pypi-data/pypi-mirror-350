"""Module defining the abstract IUploadFile class for file upload operations."""

from abc import ABC, abstractmethod

from typing import Optional


class IUploadFile(ABC):
    """Abstract base class for file upload operations.

    This interface defines methods for uploading files either from a local
    path or as a byte stream."""

    @abstractmethod
    def upload_file_from_local(self, local_path: str, remote_path: str, *args,
                               transaction_id: Optional[str] = None, **kwargs) -> bool:
        """Uploads a file from the local filesystem to a remote location.

        Parameters
        ----------
        local_path : str
            The local file path to be uploaded.
        remote_path : str
            The destination path where the file should be stored remotely.
        transaction_id : Optional[str], optional
            Unique identifier for tracing the upload operation, by default None.

        Returns
        -------
        bool
            True if the upload is successful, False otherwise."""
        raise NotImplementedError("upload_file_from_local must be implemented")  # pragma: no cover

    @abstractmethod
    def upload_file_stream(self, remote_path: str, stream: bytes, *args,
                           transaction_id: Optional[str] = None, **kwargs) -> bool:
        """Uploads a file from a byte stream to a remote location.

        Parameters
        ----------
        remote_path : str
            The destination path where the file should be stored remotely.
        stream : bytes
            The byte stream representing the file content.
        transaction_id : Optional[str], optional
            Unique identifier for tracing the upload operation, by default None.

        Returns
        -------
        bool
            True if the upload is successful, False otherwise."""
        raise NotImplementedError("upload_file_stream must be implemented")  # pragma: no cover
