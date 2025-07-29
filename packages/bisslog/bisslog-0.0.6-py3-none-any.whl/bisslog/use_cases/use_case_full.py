"""Module defining the FullUseCase class."""

from abc import ABCMeta
from typing import Optional, Any

from ..ports.upload_file import IUploadFile
from ..ports.publisher import IPublisher

from ..adapt_handler.file_uploader_handler import bisslog_upload_file
from ..adapt_handler.publisher_handler import bisslog_pubsub
from .use_case_basic import BasicUseCase


class FullUseCase(BasicUseCase, metaclass=ABCMeta):
    """Extends `BasicUseCase` with additional functionalities.

    This class integrates message publishing and file uploading capabilities,
    leveraging predefined adapters."""

    @property
    def __publisher(self) -> IPublisher:
        """Property to access the publisher handler."""
        return bisslog_pubsub.main

    @property
    def __upload_file_adapter(self) -> IUploadFile:
        """Returns the global transaction manager instance."""
        return bisslog_upload_file.main

    def publish(self, queue_name: str, body: Any, *args,
                partition: Optional[str] = None, **kwargs) -> None:
        """Publishes a message to the specified queue.

        Parameters
        ----------
        queue_name : str
            The name of the queue where the message should be published.
        body : Any
            The message payload to be published.
        *args
            Arguments to the publisher.
        partition : Optional[str]
            Optional partition identifier for the message.
        **kwargs
            Keyword arguments"""
        self.__publisher(queue_name, body, *args, partition=partition, **kwargs)

    def upload_file_stream(self, remote_path: str, stream: bytes, *args,
                           transaction_id: Optional[str] = None, **kwargs) -> bool:
        """Uploads a file from a byte stream to a remote location.

        Parameters
        ----------
        remote_path : str
            The destination path where the file should be uploaded.
        stream : bytes
            The file content in bytes.
        *args
            Arguments to file uploader.
        transaction_id : Optional[str], default=None
            Optional transaction identifier.
        **kwargs
            Keyword arguments

        Returns
        -------
        bool
            True if the upload is successful, False otherwise."""
        return self.__upload_file_adapter.upload_file_stream(
            remote_path, stream, *args, transaction_id=transaction_id, **kwargs)

    def upload_file_from_local(self, local_path: str, remote_path: str, *args,
                               transaction_id: Optional[str] = None, **kwargs) -> bool:
        """Uploads a file from a local path to a remote location.

        Parameters
        ----------
        local_path : str
            The local file path to be uploaded.
        remote_path : str
            The destination path where the file should be stored.
        *args
            Arguments to file uploader.
        transaction_id : Optional[str], default=None
            Optional transaction identifier.
        **kwargs
            Keyword arguments

        Returns
        -------
        bool
            True if the upload is successful, False otherwise."""
        return self.__upload_file_adapter.upload_file_from_local(
            local_path, remote_path, *args, transaction_id=transaction_id, **kwargs)
