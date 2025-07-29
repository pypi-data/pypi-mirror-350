import pytest

from bisslog.adapt_handler.adapt_handler import AdaptHandler
from bisslog.adapters.blank_adapter import BlankAdapter
from bisslog.domain_context import domain_context


@pytest.fixture
def mock_service_tracer():
    """Mock implementation of the traceability service."""

    class MockServiceTracer:
        def __init__(self):
            self.warnings = []

        def warning(self, message, checkpoint_id=None):
            self.warnings.append((message, checkpoint_id))

    return MockServiceTracer()


@pytest.fixture
def mock_domain_context(mock_service_tracer):
    """Mock for the domain context."""
    domain_context.service_tracer = mock_service_tracer
    return domain_context


@pytest.fixture
def adapt_handler(mock_domain_context):
    """Returns an AdaptHandler instance with mocked dependencies."""
    return AdaptHandler(component="test_component")


def test_initialization(adapt_handler):
    """Verifies that initialization is correct."""
    assert adapt_handler.component == "test_component"
    assert adapt_handler._divisions == {}


def test_register_main_adapter(adapt_handler):
    """Verifies that registering the main adapter is valid."""
    mock_adapter = object()
    adapt_handler.register_main_adapter(mock_adapter)
    assert adapt_handler._divisions["main"] == mock_adapter


def test_register_adapters(adapt_handler):
    """Verifies that adapters are registered correctly."""
    adapter1 = object()
    adapter2 = object()

    adapt_handler.register_adapters(finance=adapter1, sales=adapter2)

    assert adapt_handler._divisions["finance"] == adapter1
    assert adapt_handler._divisions["sales"] == adapter2


def test_register_duplicate_adapter(adapt_handler, mock_service_tracer):
    """Verifies that duplicate division names are detected and a warning is issued."""
    adapter1 = object()
    adapter2 = object()

    adapt_handler.register_adapters(finance=adapter1)
    adapt_handler.register_adapters(finance=adapter2)

    assert adapt_handler._divisions["finance"] == adapter1
    assert len(mock_service_tracer.warnings) == 1
    assert "The division named 'finance' already exists" in mock_service_tracer.warnings[0][0]
    assert mock_service_tracer.warnings[0][1] == "repeated-division"


def test_generate_blank_adapter(adapt_handler):
    """Verifies that a BlankAdapter is generated correctly when the division does not exist."""
    blank_adapter = adapt_handler.generate_blank_adapter("new_division")
    assert isinstance(blank_adapter, BlankAdapter)
    assert blank_adapter.division_name == "new_division"
    assert blank_adapter.original_comp == "test_component"


def test_get_existing_division(adapt_handler):
    """Verifies that retrieving an existing division returns the correct adapter."""
    adapter = object()
    adapt_handler.register_adapters(finance=adapter)

    result = adapt_handler.get_division("finance")
    assert result == adapter


def test_get_non_existing_division(adapt_handler):
    """Verifies that an AttributeError is raised when trying to access a non-existing division."""
    with pytest.raises(AttributeError, match="Division named 'marketing' does not exist."):
        adapt_handler.get_division("marketing")


def test_getattribute_existing_division(adapt_handler):
    """Verifies that __getattribute__ returns a registered adapter when accessed as an attribute."""
    adapter = object()
    adapt_handler.register_adapters(it=adapter)

    assert adapt_handler.it == adapter


def test_getattribute_creates_blank_adapter(adapt_handler):
    """Verifies that __getattribute__ creates and stores a BlankAdapter when the division does not exist."""
    blank_adapter = adapt_handler.unknown_division
    assert isinstance(blank_adapter, BlankAdapter)
    assert blank_adapter.division_name == "unknown_division"
    assert blank_adapter.original_comp == "test_component"
    assert adapt_handler._divisions["unknown_division"] == blank_adapter
