from bisslog.utils.singleton import SingletonReplaceAttrsMeta


class MySingleton(metaclass=SingletonReplaceAttrsMeta):
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value
        self._internal = "should not be replaced"


def test_singleton_instance_is_unique():
    a = MySingleton(name="A", value=1)
    b = MySingleton(name="B", value=2)

    assert a is b
    assert a.name == "B"
    assert a.value == 2
    assert a._internal == "should not be replaced"


def test_singleton_does_not_replace_with_none():
    a = MySingleton(name="Initial", value=100)

    b = MySingleton(name=None, value=None)

    assert a is b
    assert a.name == "Initial"
    assert a.value == 100


def test_get_all_attributes_filters_properly():
    class Dummy:
        def __init__(self):
            self.name = "test"
            self.value = 123
            self._private = "hidden"
            self.none_attr = None

    dummy = Dummy()
    attrs = SingletonReplaceAttrsMeta.get_all_attributes(dummy)

    assert "name" in attrs
    assert "value" in attrs
    assert "_private" not in attrs
    assert "none_attr" not in attrs
