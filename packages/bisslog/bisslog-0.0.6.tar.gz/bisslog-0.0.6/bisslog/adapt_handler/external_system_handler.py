"""Module for external system adapter handling."""

from .adapt_handler import AdaptHandler


class ExtSysHandler(AdaptHandler):
    """Database adapter handler.

    This class extends `AdaptHandler` to provide a standardized way
    to interact with external systems."""


bisslog_ext_sys = ExtSysHandler("main-ext-system-handler")
