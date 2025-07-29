import pytest

from bisslog.adapt_handler.external_system_handler import ExtSysHandler
from bisslog.adapters.blank_adapter import BlankAdapter


@pytest.fixture
def ext_sys_handler():
    """Instance of ExtSysHandler for testing."""
    return ExtSysHandler("ext-system-test")


def test_ext_sys_handler_inherits_adapt_handler(ext_sys_handler):
    """Verifies that ExtSysHandler correctly inherits from AdaptHandler."""
    from bisslog.adapt_handler.adapt_handler import AdaptHandler
    assert isinstance(ext_sys_handler, AdaptHandler)


def test_ext_sys_handler_initialization(ext_sys_handler):
    """Verifies that ExtSysHandler is initialized correctly."""
    assert ext_sys_handler.component == "ext-system-test"
    assert isinstance(ext_sys_handler._divisions, dict)
    assert ext_sys_handler._divisions == {}


def test_ext_sys_handler_register_and_get_adapter(ext_sys_handler):
    """Verifies that an adapter can be registered and retrieved in ExtSysHandler."""
    mock_adapter = object()
    ext_sys_handler.register_adapters(external=mock_adapter)

    assert ext_sys_handler.get_division("external") == mock_adapter
    assert ext_sys_handler.external == mock_adapter


def test_ext_sys_handler_blank_adapter_generation(ext_sys_handler):
    """Verifies that a BlankAdapter is generated if the division does not exist."""
    adapter = ext_sys_handler.some_unknown_division

    assert isinstance(adapter, BlankAdapter)
    assert adapter.division_name == "some_unknown_division"
    assert adapter.original_comp == "ext-system-test"


def test_global_ext_sys_instance():
    """Verifies that the global instance bisslog_ext_sys is initialized correctly."""
    from bisslog.adapt_handler.external_system_handler import bisslog_ext_sys
    assert isinstance(bisslog_ext_sys, ExtSysHandler)
    assert bisslog_ext_sys.component == "main-ext-system-handler"
