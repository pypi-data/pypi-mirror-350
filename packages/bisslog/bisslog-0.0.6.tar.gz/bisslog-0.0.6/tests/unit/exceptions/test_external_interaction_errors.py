import pytest

from bisslog.exceptions.external_interactions_errors import (
    ExternalInteractionError,
    WarningExtException,
    ErrorExtException,
    InterfaceExtException,
    ExternalDependencyErrorExtException,
    DataErrorExtException,
    OperationalErrorExtException,
    IntegrityErrorExtException,
    InternalErrorExtException,
    ProgrammingErrorExtException,
    NotSupportedErrorExtException,
    ConnectionExtException,
    TimeoutExtException,
    AuthenticationExtException,
    AuthorizationExtException,
    ConfigurationExtException,
    InvalidDataExtException,
    ProcessingExtException,
    DeliveryExtException,
)


def test_exception_hierarchy():
    """Tests that the exceptions correctly inherit from the base"""
    assert issubclass(WarningExtException, ExternalInteractionError)
    assert issubclass(AuthenticationExtException, OperationalErrorExtException)
    assert issubclass(NotSupportedErrorExtException, ExternalDependencyErrorExtException)
    assert issubclass(TimeoutExtException, OperationalErrorExtException)
    assert issubclass(ErrorExtException, ExternalInteractionError)
    assert issubclass(InterfaceExtException, ErrorExtException)
    assert issubclass(ExternalDependencyErrorExtException, ErrorExtException)
    assert issubclass(DataErrorExtException, ExternalDependencyErrorExtException)
    assert issubclass(OperationalErrorExtException, ExternalDependencyErrorExtException)
    assert issubclass(ConnectionExtException, OperationalErrorExtException)
    assert issubclass(AuthorizationExtException, OperationalErrorExtException)
    assert issubclass(IntegrityErrorExtException, ExternalDependencyErrorExtException)
    assert issubclass(ProgrammingErrorExtException, ExternalDependencyErrorExtException)
    assert issubclass(ConfigurationExtException, InterfaceExtException)
    assert issubclass(InvalidDataExtException, ExternalDependencyErrorExtException)
    assert issubclass(ProcessingExtException, InternalErrorExtException)
    assert issubclass(DeliveryExtException, OperationalErrorExtException)


def test_warning_ext_exception_is_raised_as_external_interaction_error():
    """Verify that WarningExtException is raised as ExternalInteractionError"""
    with pytest.raises(ExternalInteractionError):
        raise WarningExtException("This is a warning")


def test_external_dependency_error_ext_exception_is_raised_as_error_ext_exception():
    """Verify that ExternalDependencyErrorExtException is raised as ErrorExtException"""
    with pytest.raises(ErrorExtException):
        raise ExternalDependencyErrorExtException("Dependency error")


def test_connection_ext_exception_is_raised_as_operational_error_ext_exception():
    """Verify that ConnectionExtException is raised as OperationalErrorExtException"""
    with pytest.raises(OperationalErrorExtException):
        raise ConnectionExtException("Connection failed")


def test_configuration_ext_exception_is_raised_as_interface_ext_exception():
    """Verify that ConfigurationExtException is raised as InterfaceExtException"""
    with pytest.raises(InterfaceExtException):
        raise ConfigurationExtException("Misconfiguration")


def test_exception_message():
    """Tests that the error message is propagated correctly."""
    err_msg = "A test error occurred"
    with pytest.raises(ProcessingExtException, match=err_msg):
        raise ProcessingExtException(err_msg)
