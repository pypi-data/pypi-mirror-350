import pytest

from bisslog.utils.mapping import build_mapper, MappingGroup, Mapper


def test_build_mapper_with_list_of_dicts():
    """Test that build_mapper correctly wraps a list of dicts in MappingGroup."""
    mappers = [{"key1": "value1"}, {"key2": "value2"}]
    result = build_mapper(mappers)
    assert isinstance(result, MappingGroup)
    assert len(result._container) == 2
    assert all(isinstance(m, Mapper) for m in result._container)


def test_build_mapper_with_tuple_of_dicts():
    """Test that build_mapper correctly wraps a tuple of dicts in MappingGroup."""
    mappers = ({"key1": "value1"}, {"key2": "value2"})
    result = build_mapper(mappers)
    assert isinstance(result, MappingGroup)
    assert len(result._container) == 2


def test_build_mapper_with_dict():
    """Test that build_mapper correctly creates a Mapper instance when given a dict."""
    mappers = {"key1": "value1"}
    result = build_mapper(mappers)
    assert isinstance(result, Mapper)
    assert result.base == mappers


def test_build_mapper_with_existing_mapper():
    """Test that build_mapper returns the input when given a Mapper instance."""
    mapper = Mapper("test_mapper", {"key1": "value1"})
    result = build_mapper(mapper)
    assert result is mapper


def test_build_mapper_with_existing_mapping_group():
    """Test that build_mapper returns the input when given a MappingGroup instance."""
    mapping_group = MappingGroup([Mapper("", {"key1": "value1"})])
    result = build_mapper(mapping_group)
    assert result is mapping_group


def test_build_mapper_with_invalid_type():
    """Test that build_mapper raises TypeError when given an invalid type."""
    with pytest.raises(TypeError, match="Invalid mapper type"):
        build_mapper(123)
