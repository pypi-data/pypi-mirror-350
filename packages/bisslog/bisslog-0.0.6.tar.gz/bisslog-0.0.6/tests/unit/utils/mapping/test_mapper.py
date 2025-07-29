import pytest

from bisslog.utils.mapping.mapper import Mapper, ERRORS


def test_mapper_initialization_with_dict():
    base = {"source": "target"}
    mapper = Mapper("test_mapper", base)
    assert mapper.base == base
    assert mapper.name == "test_mapper"
    assert mapper.input_type == "dict"
    assert mapper.output_type == "dict"


def test_mapper_initialization_with_list():
    base = [{"from": "source", "to": "target"}]
    mapper = Mapper("test_mapper", base)
    assert mapper.base == base


def test_mapper_invalid_base_type():
    with pytest.raises(TypeError, match=ERRORS["base-type-error"]):
        Mapper("test_mapper", "invalid_base")


def test_mapper_invalid_base_key():
    base = {123: "target"}
    with pytest.raises(TypeError, match=ERRORS["base-kv-type-error"]):
        Mapper("test_mapper", base)


def test_mapper_invalid_base_value():
    base = {"source": 123}  # Invalid value type
    with pytest.raises(TypeError, match=ERRORS["base-kv-type-error"]):
        Mapper("test_mapper", base)


def test_mapper_resource_replacement():
    base = {"$.source": "$.target"}
    resources = {"source": "real_source", "target": "real_target"}
    mapper = Mapper("test_mapper", base, resources=resources)
    assert mapper.base == {"real_source": "real_target"}


def test_mapper_map_dict():
    base = {"user.name": "customer.full_name"}
    mapper = Mapper("test_mapper", base)
    data = {"user": {"name": "John Doe"}}
    result = mapper.map(data)
    assert result == {"customer": {"full_name": "John Doe"}}


def test_mapper_map_list():
    base = [{"from": "user.age", "to": "customer.age"}]
    mapper = Mapper("test_mapper", base)
    data = {"user": {"age": 30}}
    result = mapper.map(data)
    assert result == {"customer": {"age": 30}}


def test_mapper_no_values():
    base = {"": "target"}
    with pytest.raises(ValueError, match=ERRORS["no-values"]):
        Mapper("test_mapper", base)


def test_mapper_no_route():
    base = {"source": ""}
    with pytest.raises(ValueError, match=ERRORS["no-values"]):
        Mapper("test_mapper", base)


def test_mapper_path_naming_incorrect():
    base = {"$.source": "$.unknown"}
    resources = {"source": "real_source"}
    with pytest.raises(ValueError, match=ERRORS["path-naming-incorrect"]):
        Mapper("test_mapper", base, resources=resources)


def test_mapper_get_initial_object_dict():
    base = {"source": "target"}
    mapper = Mapper("test_mapper", base, output_type="dict")
    assert mapper.get_initial_object() == {}


def test_mapper_get_initial_object_list():
    base = [{"from": "source", "to": "target"}]
    mapper = Mapper("test_mapper", base, output_type="list")
    assert mapper.get_initial_object() == []


def test_mapper_call_alias_for_map():
    base = {"a.b": "x.y", "c": "x.z"}
    mapper = Mapper("test_mapper", base)
    data = {"a": {"b": "value"}, "c": 3556}
    result = mapper(data)
    assert result == {"x": {"y": "value", "z": 3556}}


def test_mapper_set_buffer_creates_nested_structure():
    mapper = Mapper("test_mapper", {"a": "b"})
    initial = {}
    mapper._Mapper__set_buffer("x.y.z", initial, 123)
    assert initial == {"x": {"y": {"z": 123}}}


def test_mapper_execute_mapper_as_dict_handles_missing_path():
    base = {"user.name": "person.fullname"}
    mapper = Mapper("test_mapper", base)
    data = {"user": {}}
    result = mapper.map(data)
    assert result == {"person": {"fullname": None}}


def test_mapper_execute_mapper_as_list_with_arrange_value():
    class CustomMapper(Mapper):
        def arrange_value(self, value, **kwargs):
            return value * 2 if isinstance(value, int) else value

    base = [{"from": "user.age", "to": "person.age"}]
    mapper = CustomMapper("test_mapper", base)
    data = {"user": {"age": 21}}
    result = mapper.map(data)
    assert result == {"person": {"age": 42}}


def test_mapper_execute_mapper_as_list_handles_missing_nested_path():
    base = [{"from": "user.age", "to": "person.age"}]
    mapper = Mapper("test_mapper", base)
    data = {"user": {}}
    result = mapper.map(data)
    assert result == {"person": {"age": None}}
