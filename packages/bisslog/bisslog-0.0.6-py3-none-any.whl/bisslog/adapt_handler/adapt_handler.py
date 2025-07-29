"""Module providing the AdaptHandler class for managing adapters in a
domain-driven design (DDD) context."""
from ..adapters.blank_adapter import BlankAdapter
from ..domain_context import domain_context
from ..ports.tracing.service_tracer import ServiceTracer


class AdaptHandler:
    """Handler for managing adapters associated with different divisions of a component.

    This class allows registering adapters for various divisions within a component,
    retrieving them, and handling undefined divisions by generating blank adapters.

    Parameters
    ----------
    component : str
        The name of the component to which this adapter handler belongs."""

    def __init__(self, component: str):
        """Initializes the AdaptHandler with a component name and logging service.

        Parameters
        ----------
        component : str
            The name of the component that this handler manages adapters for."""
        self.log_service: ServiceTracer = domain_context.service_tracer
        self._divisions = {}
        self.component = component

    def register_main_adapter(self, adapter):
        """Registers the main adapter for this component.

        Parameters
        ----------
        adapter : Any
            The adapter instance to be set as the main adapter."""
        self._divisions["main"] = adapter

    def register_adapters(self, **named_division_instances) -> None:
        """Registers multiple named adapters for different divisions.

        Parameters
        ----------
        **named_division_instances
            A mapping of division names to their respective adapter instances."""
        for division_name, adapter in named_division_instances.items():
            if division_name in self._divisions:
                self.log_service.warning(
                    f"The division named '{division_name}' already exists"
                    f" in the adapter handler {self.component}. Are you trying to replace it?"
                    " To comply with DDD (Domain-Driven Design) principles, "
                    "each division should have a distinct"
                    " and well-defined language",
                    checkpoint_id="repeated-division",
                )
                continue
            self._divisions[division_name] = adapter

    def generate_blank_adapter(self, division_name: str):
        """Generates a blank adapter for a division that does not have a registered adapter.

        Parameters
        ----------
        division_name : str
            The name of the division for which a blank adapter should be created.

        Returns
        -------
        BlankAdapter
            A new instance of a blank adapter for the specified division."""
        return BlankAdapter(division_name, self.component)

    def get_division(self, division_name: str):
        """Retrieves the adapter associated with a given division.

        Parameters
        ----------
        division_name : str
            The name of the division whose adapter is being retrieved.

        Returns
        -------
        Any
            The adapter instance for the requested division.

        Raises
        ------
        AttributeError
            If the requested division does not exist."""
        if division_name in self._divisions:
            return self._divisions[division_name]
        raise AttributeError(f"Division named '{division_name}' does not exist.")

    def __getattribute__(self, name):
        """Retrieves an attribute or dynamically generates a blank adapter
        if the attribute is a division name.

        Parameters
        ----------
        name : str
            The name of the attribute or division to retrieve.

        Returns
        -------
        Any
            The retrieved attribute or a blank adapter if the name corresponds
            to an unregistered division."""
        try:
            return super().__getattribute__(name)
        except AttributeError:
            pass
        if name in self._divisions:
            return self._divisions[name]
        res = self.generate_blank_adapter(name)
        self._divisions[name] = res
        return res
