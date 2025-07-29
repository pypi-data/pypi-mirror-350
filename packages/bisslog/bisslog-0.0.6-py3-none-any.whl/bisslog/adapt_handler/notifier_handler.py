"""This module defines the PublisherHandler, an adapter handler
responsible for managing message publishing operations."""

from .adapt_handler import AdaptHandler


class NotifierHandler(AdaptHandler):
    """Handler for managing message publishing operations.

    This class serves as an adapter handler for message publishing, allowing
    the integration of different messaging systems.

    It extends `AdaptHandler` to provide a structured way to handle
    message publishing dynamically."""


bisslog_notifier = NotifierHandler("publisher-default")
