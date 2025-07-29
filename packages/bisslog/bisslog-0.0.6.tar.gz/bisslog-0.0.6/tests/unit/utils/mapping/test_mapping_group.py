import pytest

from bisslog.utils.mapping import Mapper, MappingGroup


def test_mapping_group_initialization():
    """Tests that MappingGroup initializes correctly with valid mappers."""
    mapper1 = Mapper("mapper1", {"a": "x"})
    mapper2 = Mapper("mapper2", {"b": "y"})
    group = MappingGroup([mapper1, mapper2])
    assert len(group._container) == 2


def test_mapping_group_invalid_mapper():
    """Tests that MappingGroup raises a ValueError when initialized with an invalid mapper."""
    invalid_mapper = object()  # Not a Mapper instance
    with pytest.raises(ValueError, match="is not a mapper"):
        MappingGroup([invalid_mapper])


def test_mapping_group_empty_container():
    """Tests that MappingGroup raises a ValueError when initialized with an empty container."""
    with pytest.raises(ValueError, match="There is nothing in the container"):
        MappingGroup([])


def test_mapping_group_duplicate_target():
    """Tests that MappingGroup raises a ValueError if multiple mappers have the same target key."""
    mapper1 = Mapper("mapper1", {"a": "x"})
    mapper2 = Mapper("mapper2", {"b": "x"})  # Duplicate target "x"
    with pytest.raises(ValueError, match="The target destination will be overwritten"):
        MappingGroup([mapper1, mapper2])


def test_mapping_group_different_output_types():
    """Tests that MappingGroup raises a ValueError when mappers have different output types."""
    mapper1 = Mapper("mapper1", {"a": "x"}, output_type="dict")
    mapper2 = Mapper("mapper2", {"b": "y"}, output_type="list")
    with pytest.raises(ValueError, match="The types of outputs are different"):
        MappingGroup([mapper1, mapper2])


def test_mapping_group_different_input_types():
    """Tests that MappingGroup raises a ValueError when mappers have different input types."""
    mapper1 = Mapper("mapper1", {"a": "x"}, input_type="dict")
    mapper2 = Mapper("mapper2", {"b": "y"}, input_type="list")
    with pytest.raises(ValueError, match="The types of inputs are different"):
        MappingGroup([mapper1, mapper2])


def test_mapping_group_mapping():
    """Tests that MappingGroup correctly maps data using multiple mappers."""
    mapper1 = Mapper("mapper1", {"a": "x"})
    mapper2 = Mapper("mapper2", {"b": "y"})
    group = MappingGroup([mapper1, mapper2])
    data = {"a": 1, "b": 2}
    expected_output = {"x": 1, "y": 2}
    assert group.map(data) == expected_output
