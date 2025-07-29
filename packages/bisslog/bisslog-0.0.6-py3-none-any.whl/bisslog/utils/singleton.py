"""Module implementing a singleton metaclass with attribute replacement."""

from threading import Lock


class SingletonReplaceAttrsMeta(type):
    """Metaclass for implementing a singleton pattern with attribute replacement.

    This metaclass ensures that only one instance of a class exists. If an
    instance is created again, its attributes are updated with the values
    from the new instantiation while maintaining the same instance."""

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """Creates or retrieves the singleton instance while updating its attributes.

        If the class instance does not exist, it is created and stored. If it
        already exists, its attributes are updated with the values from the
        new instantiation.

        Parameters
        ----------
        *args
            Positional arguments for instance initialization.
        **kwargs
            Keyword arguments for instance initialization.

        Returns
        -------
        Any
            The singleton instance of the class."""
        with cls._lock:
            new_instance = super().__call__(*args, **kwargs)
            if cls not in cls._instances:
                cls._instances[cls] = new_instance
            else:
                instance = cls._instances[cls]
                new_attrs = cls.get_all_attributes(new_instance)
                for attr in new_attrs:
                    setattr(instance, attr, getattr(new_instance, attr))
        return cls._instances[cls]

    @staticmethod
    def get_all_attributes(new_inst):
        """Retrieves all non-private and non-null attributes from a new instance.

        Parameters
        ----------
        new_inst : Any
            The newly created instance.

        Returns
        -------
        dict
            A dictionary of attribute names and their values."""
        return {key: value for key, value in new_inst.__dict__.items()
                if value is not None and not key.startswith("_")}
