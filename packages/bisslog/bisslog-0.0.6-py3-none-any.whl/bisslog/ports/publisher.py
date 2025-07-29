"""Module defining the abstract IPublisher class for message publishing."""

from abc import ABC, abstractmethod
from typing import Any


class IPublisher(ABC):
    """Abstract base class for a message publisher.

    This interface defines the method required for publishing messages
    to a queue or topic."""

    @abstractmethod
    def __call__(self, queue_name: str, body: Any, *args, partition: str = None,  **kwargs):
        """Publishes a message to the specified queue or topic.

        Parameters
        ----------
        queue_name : str
            The name of the queue or topic where the message will be published.
        body : Any
            The message payload to be sent.
        partition : str, optional
            The partition key, if applicable (default is None)."""
        raise NotImplementedError("Method publish must be implemented")  # pragma: no cover
