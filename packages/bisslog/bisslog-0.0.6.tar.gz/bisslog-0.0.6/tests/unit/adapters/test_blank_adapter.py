import pytest

from bisslog.adapters.blank_adapter import BlankAdapter
from tests.unit.utils.fake_tracer import FakeTracer


@pytest.fixture
def fake_tracer():
    return FakeTracer()


@pytest.fixture
def blank_adapter(fake_tracer):
    """Creates an instance of BlankAdapter."""

    class BlankAdapterModified(BlankAdapter):
        tracer = fake_tracer

        @BlankAdapter.log.getter
        def log(self):
            return self.tracer

    return BlankAdapterModified(name_division_not_found="unknown_division",
                                original_comp="test_component")


def test_initialization(blank_adapter):
    """Ensures BlankAdapter is initialized with correct attributes."""
    assert blank_adapter.division_name == "unknown_division"
    assert blank_adapter.original_comp == "test_component"


def test_get_existing_attribute(blank_adapter):
    """Checks if an existing attribute is accessed correctly."""
    assert blank_adapter.division_name == "unknown_division"
    assert blank_adapter.original_comp == "test_component"


def test_get_non_existing_method(blank_adapter, fake_tracer):
    """Ensures calling a non-existing method does not raise an error and logs properly."""
    fake_method = blank_adapter.non_existent_method
    assert callable(fake_method)
    fake_method(42, key="value")
    assert len(fake_tracer._calls["info"]) == 1
    assert fake_tracer._calls["info"][0][0][0].replace("#", "").strip() == (
        "Blank adapter for test_component on division: unknown_division \n"
        "execution of method 'non_existent_method' with args (42,), kwargs {'key': 'value'}"
    )
