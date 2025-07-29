from abc import ABC

import pytest

from bisslog.ports.notifier import INotifier


class DummyNotifier(INotifier):
    def __call__(self, notification_obj: object) -> None:
        self.last_notification = notification_obj


@pytest.fixture
def notifier():
    return DummyNotifier()


def test_interface_notifier_call_stores_notification(notifier):
    payload = {"message": "Test"}
    notifier(payload)

    assert notifier.last_notification == payload


def test_interface_notifier_is_subclass_of_abc():
    assert issubclass(INotifier, ABC)


def test_dummy_notifier_is_instance_of_interface_notifier(notifier):
    assert isinstance(notifier, INotifier)
