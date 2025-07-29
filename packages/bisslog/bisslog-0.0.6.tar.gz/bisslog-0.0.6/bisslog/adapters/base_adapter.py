"""Module defining the base class for adapters."""

from abc import ABC

from ..transactional.transaction_traceable import TransactionTraceable


class BaseAdapter(TransactionTraceable, ABC):
    """Abstract base class for adapters with transaction tracing.

    This class extends `TransactionTraceable`, ensuring that all derived
    adapters support transactional tracing mechanisms.

    Notes
    -----
    - This class is intended to be subclassed by specific adapter implementations.
    - It does not define any concrete methods but serves as a structural base."""
