import pytest

from bisslog import BasicUseCase


def test_use_method_called():
    class MyUseCase(BasicUseCase):
        def use(self, x):
            return f"used {x}"

    use_case = MyUseCase()
    assert use_case("test") == "used test"


def test_run_method_called_if_no_use():
    class MyUseCase(BasicUseCase):
        def run(self, x):
            return f"ran {x}"

    use_case = MyUseCase()
    assert use_case("foo") == "ran foo"


def test_decorated_method_takes_priority():
    from bisslog import use_case

    class MyUseCase(BasicUseCase):
        def use(self, x):
            return f"used {x}"

        @use_case
        def run(self, x):
            return f"decorated {x}"

    use_case_instance = MyUseCase()
    assert use_case_instance("y") == "used y"


def test_fails_if_no_entrypoint():
    class MyUseCase(BasicUseCase):
        pass

    with pytest.raises(AttributeError):
        MyUseCase()


def test_keyname_default():
    class MyUseCase(BasicUseCase):
        def use(self, x):
            return x

    uc = MyUseCase()
    assert uc.keyname == "MyUseCase"


def test_keyname_custom():
    class MyUseCase(BasicUseCase):
        def use(self, x):
            return x

    uc = MyUseCase("custom_key")
    assert uc.keyname == "custom_key"
