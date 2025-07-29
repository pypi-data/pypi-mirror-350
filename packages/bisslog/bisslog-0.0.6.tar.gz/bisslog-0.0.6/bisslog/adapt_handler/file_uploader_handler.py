"""This module defines the UploadFileHandler, an adapter handler
responsible for managing file upload operations."""

from .adapt_handler import AdaptHandler


class UploadFileHandler(AdaptHandler):
    """Handler for managing file upload operations.

    This class serves as an adapter handler for file uploads, allowing
    the integration of different file storage mechanisms.

    It extends `AdaptHandler` to provide a structured way to handle
    file upload operations dynamically."""


bisslog_upload_file = UploadFileHandler("file-uploader")
