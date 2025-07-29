"""This module defines a thread-safe transaction management system."""
import threading
import uuid
from dataclasses import dataclass
from typing import Optional, Dict, List

from ..utils.singleton import SingletonReplaceAttrsMeta


@dataclass
class Transaction:
    """Represents a transactional context with a unique identifier and a component name.

    Attributes
    ----------
    transaction_id : str
        Unique identifier for the transaction.
    component : str
        The name of the component initiating the transaction."""
    transaction_id: str
    component: str


class TransactionManager(metaclass=SingletonReplaceAttrsMeta):
    """Manages transactions in a thread-safe manner using a singleton pattern.

    This class allows creating, retrieving, and clearing transactions per thread."""

    def __init__(self):
        self._thread_active_transaction_mapping: Dict[int, List[Transaction]] = {}
        self._loc = threading.Lock()

    @staticmethod
    def get_thread_id() -> int:
        """Retrieves the current thread's identifier.

        Returns
        -------
        int
            The unique identifier of the current thread."""
        return threading.get_ident()

    def create_transaction_id(self, component: str) -> str:
        """Creates a new unique transaction identifier and stores it.

        Parameters
        ----------
        component : str
            The name of the component initiating the transaction.

        Returns
        -------
        str
            The generated UUID as a string."""
        transaction_id = str(uuid.uuid4())
        with self._loc:
            thread_id = self.get_thread_id()
            if thread_id not in self._thread_active_transaction_mapping:
                self._thread_active_transaction_mapping[thread_id] = [
                    Transaction(transaction_id, component)
                ]
            else:
                transactions_ids: list = self._thread_active_transaction_mapping[thread_id]
                transactions_ids.append(Transaction(transaction_id, component))
        return transaction_id

    def get_transaction_id(self) -> Optional[str]:
        """Retrieves the latest transaction ID associated with the current thread.

        Returns
        -------
        str
            The most recent transaction ID.

        Raises
        ------
        KeyError
            If no transaction is found for the current thread."""
        with self._loc:
            thread_id = self.get_thread_id()
            if (
                thread_id in self._thread_active_transaction_mapping and
                self._thread_active_transaction_mapping[thread_id]
            ):
                return self._thread_active_transaction_mapping[thread_id][-1].transaction_id
            return None

    def get_component(self) -> Optional[str]:
        """Retrieves the component associated with the latest transaction of the current thread.

        Returns
        -------
        str
            The component name.

        Raises
        ------
        KeyError
            If no transaction is found for the current thread."""
        with self._loc:
            thread_id = self.get_thread_id()
            if (
                thread_id in self._thread_active_transaction_mapping and
                self._thread_active_transaction_mapping[thread_id]
            ):
                return self._thread_active_transaction_mapping[thread_id][-1].component
            return None

    def get_main_transaction_id(self) -> Optional[str]:
        """Retrieves the first transaction ID created for the current thread.

        Returns
        -------
        Optional[str]
            The first transaction ID.

        Raises
        ------
        KeyError
            If no transaction exists for the current thread."""
        with self._loc:
            thread_id = self.get_thread_id()
            if (
                thread_id in self._thread_active_transaction_mapping and
                self._thread_active_transaction_mapping[thread_id]
            ):
                return self._thread_active_transaction_mapping[thread_id][0].transaction_id
            return None

    def close_transaction(self):
        """Closes the most recent transaction for the current thread.

        Raises
        ------
        IndexError
            If no transaction exists to close."""
        self._thread_active_transaction_mapping.get(self.get_thread_id(), []).pop()

    def clear(self):
        """Clears all transactions from the cache."""
        with self._loc:
            self._thread_active_transaction_mapping.clear()


transaction_manager = TransactionManager()
