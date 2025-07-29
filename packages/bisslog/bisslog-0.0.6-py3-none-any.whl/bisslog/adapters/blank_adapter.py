"""Module providing a blank adapter implementation."""
from .base_adapter import BaseAdapter


class BlankAdapter(BaseAdapter):
    """Adapter that handles undefined components in a division by logging method calls."""

    def __init__(self, name_division_not_found: str, original_comp: str):
        self.division_name = name_division_not_found
        self.original_comp = original_comp

    def _log_blank_call(self, method_name: str, *args, **kwargs):
        """Centralized logging for undefined adapter method calls."""
        separator = "#" * 80
        self.log.info(
            "\n" + separator + "\n" +
            f"Blank adapter for {self.original_comp} on division: {self.division_name} \n"
            f"execution of method '{method_name}' with args {args}, kwargs {kwargs}\n" +
            separator,
            checkpoint_id="bisslog-blank-division"
        )

    def __getattribute__(self, item):
        """Overrides attribute access to provide a blank implementation for undefined methods.

        Parameters
        ----------
        item : str
            The name of the attribute being accessed.

        Returns
        -------
        Callable
            A function that logs the method call with its arguments when invoked."""
        try:
            return super().__getattribute__(item)
        except AttributeError:
            pass

        def blank_use_of_adapter(*args, **kwargs):
            self._log_blank_call(item, *args, **kwargs)

        return blank_use_of_adapter

    def __call__(self, *args, **kwargs):
        self._log_blank_call("__call__", *args, **kwargs)
