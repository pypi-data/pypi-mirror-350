"""Module defining the abstract INotifier class for sending notifications."""

from abc import ABC, abstractmethod
from typing import Any


class INotifier(ABC):
    """Abstract base class for a notification sender.

    This interface defines the method required for sending notifications."""

    @abstractmethod
    def __call__(self, notification_obj: Any) -> None:
        """Sends a notification.

        Parameters
        ----------
        notification_obj : Any
            The notification payload to be sent."""
        raise NotImplementedError("Callable must be implemented")  # pragma: no cover
