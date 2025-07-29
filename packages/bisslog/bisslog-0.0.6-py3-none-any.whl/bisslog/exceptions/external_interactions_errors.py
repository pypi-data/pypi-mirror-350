"""This module adapts the PEP-249 standard, which refers to database apis,
to a more general application that has to do with the interaction with external
components or dependencies such as messaging systems (RabbitMQ, Kafka, sqs, ...),
file uploads, notifiers such as e-mail or sms sending."""

# ref: https://peps.python.org/pep-0249/#exceptions

class ExternalInteractionError(Exception):
    """Base exception for all service-related errors."""

class WarningExtException(ExternalInteractionError):
    """Exception raised for important warnings like data truncations while inserting, etc.

    ref: https://peps.python.org/pep-0249/#warning"""


class ErrorExtException(ExternalInteractionError):
    """Exception that is the base class of all other error exceptions.
    You can use this to catch all errors with one single except statement.
    Warnings are not considered errors and thus should not use this class as base.

    ref: https://peps.python.org/pep-0249/#error"""

class InterfaceExtException(ErrorExtException):
    """Exception raised for errors that are related to the database interface
    rather than the database itself.

    ref: https://peps.python.org/pep-0249/#interfaceerror"""

class ExternalDependencyErrorExtException(ErrorExtException):
    """Exception raised for errors that are related to the external dependency.

    ref: https://peps.python.org/pep-0249/#databaseerror"""



class DataErrorExtException(ExternalDependencyErrorExtException):
    """Exception raised for errors that are due to problems with the processed
    data like division by zero, numeric value out of range, etc.

    ref: https://peps.python.org/pep-0249/#dataerror"""


class OperationalErrorExtException(ExternalDependencyErrorExtException):
    """Exception raised for errors that are related to the database’s operation
    and not necessarily under the control of the programmer, e.g. an unexpected
    disconnect occurs, the data source name is not found, a transaction could not
    be processed, a memory allocation error occurred during processing, etc.

    ref: https://peps.python.org/pep-0249/#operationalerror"""

class IntegrityErrorExtException(ExternalDependencyErrorExtException):
    """Exception raised when the relational integrity of the database is affected,
     e.g. a foreign key check fails.

     ref: https://peps.python.org/pep-0249/#integrityerror"""

class InternalErrorExtException(ExternalDependencyErrorExtException):
    """Exception raised when the database encounters an internal error, e.g. the
    cursor is not valid anymore, the transaction is out of sync, etc.

    ref: https://peps.python.org/pep-0249/#internalerror"""

class ProgrammingErrorExtException(ExternalDependencyErrorExtException):
    """Exception raised for programming errors, e.g. table not found or already
    exists, syntax error in the SQL statement, wrong number of parameters
    specified,etc.

    ref: https://peps.python.org/pep-0249/#programmingerror"""

class NotSupportedErrorExtException(ExternalDependencyErrorExtException):
    """Exception raised in case a method or database API was used which is not
    supported by the database, e.g. requesting a .rollback() on a connection
    that does not support transaction or has transactions turned off.

    ref: https://peps.python.org/pep-0249/#notsupportederror"""

class ConnectionExtException(OperationalErrorExtException):
    """Raised when a connection to a service fails."""

class TimeoutExtException(OperationalErrorExtException):
    """Raised when a service request times out."""

class AuthenticationExtException(OperationalErrorExtException):
    """Raised when authentication to a service fails."""

class AuthorizationExtException(OperationalErrorExtException):
    """Raised when a user lacks the necessary permissions."""

class ConfigurationExtException(InterfaceExtException):
    """Raised when a service is misconfigured."""

class InvalidDataExtException(ExternalDependencyErrorExtException):
    """Raised when data is malformed or unexpected."""

class ProcessingExtException(InternalErrorExtException):
    """Raised when a process (DB transaction, message, file upload) fails."""

class DeliveryExtException(OperationalErrorExtException):
    """Raised when a message or file cannot be delivered."""
