"""This module defines custom exceptions for handling functional errors
in a structured way throughout the application."""

from dataclasses import dataclass


@dataclass
class DomainException(Exception):
    """Base exception for functional errors in the application.

    This class extends Exception and uses dataclass to provide
    a consistent structure for functional exceptions.

    Attributes
    ----------
    keyname : str
        Unique identifier for the functional error.
    message : str
        Descriptive error message.

    Examples
    --------
    >>> raise DomainException("error-key", "Error description")
    """
    keyname: str
    message: str


class NotFound(DomainException):
    """Exception raised when a requested resource is not found.

    This exception should be used in cases where an entity or record
    does not exist in the system.

    Examples
    --------
    >>> raise NotFound("user-not-found", "User does not exist")
    """


class NotAllowed(DomainException):
    """Exception raised when an operation is not allowed.

    This exception should be used in cases where a user or system
    action is restricted due to permissions or business rules.

    Examples
    --------
    >>> raise NotAllowed("action-not-permitted", "You do not have permission to perform action A")
    """
