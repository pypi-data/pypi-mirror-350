import pytest

from bisslog.ports.publisher import IPublisher


class TestPublisher(IPublisher):
    def __call__(self, queue_name: str, body: object, *args, partition: str = None, **kwargs):
        pass


def test_interface_publisher_cannot_be_instantiated():
    with pytest.raises(TypeError):
        IPublisher()


def test_concrete_publisher_can_be_instantiated():
    publisher = TestPublisher()
    assert isinstance(publisher, IPublisher)


def test_call_method_is_callable():
    publisher = TestPublisher()
    mock_queue = "test_queue"
    mock_body = {"message": "Hello"}

    try:
        publisher(mock_queue, mock_body)
    except NotImplementedError:
        pytest.fail("__call__ method should be implemented in subclass")
