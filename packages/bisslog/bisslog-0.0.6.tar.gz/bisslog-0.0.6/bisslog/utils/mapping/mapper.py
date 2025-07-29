"""Implementation of the general mapper class"""
from typing import Union, List, Dict

from .arranger import IArranger

ERRORS = {
    "base-type-error": "Base must be a dictionary or list",
    "base-kv-type-error": "Base must be a dict with key-value string",
    "no-values": "There is no key or value",
    "no-route": "There is no route or path",
    "no-base": "There is no base",
    "path-naming-incorrect": "Resources to be added in the path naming are missing"
}


class Mapper(IArranger):
    """Redirects information to specific fields and combines those fields"""

    default_separator = '.'
    list_identifier = '[]'
    _default_path_naming = '$'

    def __init__(self, name: str, base: Union[Dict[str, str], List[Dict[str, str]]],
                 input_type: str = "dict", output_type: str = "dict", *, resources: dict = None,
                 **kwargs):
        super().__init__()
        self._format_base(base)

        self._name = name
        self._input_type = input_type
        self._output_type = output_type
        self._resources = resources or {}
        self._separator = kwargs.get('separator') or self.default_separator
        self._path_naming = kwargs.get('path_naming') or self._default_path_naming
        self.__format = "dict" if isinstance(base, dict) else "list"

        self._base = self._replace_paths(base)

    def _replace_paths(self, base):
        """Replaces the paths in the base using the resources without repeating computations."""
        if isinstance(base, dict):
            return {new_k: new_v for k, v in base.items()
                    for new_k, new_v in self.__check_resources_and_replace(k, v)}

        return [{"from": new_k, "to": new_v} for obj in base
                for new_k, new_v in self.__check_resources_and_replace(obj["from"], obj["to"])]

    def _format_base(self, base):
        """Checks and formats the initial base."""
        if isinstance(base, dict):
            for key, value in base.items():
                self.__check_source_target(key, value)
        elif isinstance(base, list):
            for obj in base:
                self.__check_source_target(obj.get("from"), obj.get("to"))
        else:
            raise TypeError(ERRORS["base-type-error"])

    @staticmethod
    def __check_source_target(source, target):
        """Performs various validations on data paths

        Parameters
        ----------
        source: str
        target: str
        """
        if not isinstance(source, str):
            raise TypeError(f'{ERRORS["base-kv-type-error"]} in key {source}')
        if not source or not target:
            raise ValueError(ERRORS["no-values"])
        if not isinstance(target, str):
            raise TypeError(ERRORS["base-kv-type-error"] + " in value of key " + str(source))

    def __check_resources_and_replace(self, path_source, path_target):
        """Validates and applies resource substitution in the given paths.

        Parameters
        ----------
        path_source: str
        path_target: str

        Returns
        -------
        new_path_source: str
        new_path_target: str
        """
        new_path_source, new_path_target = path_source, path_target
        for key in self._resources:
            new_path_source = new_path_source.replace(
                self._path_naming + "." + key, self._resources[key])
            new_path_target = new_path_target.replace(
                self._path_naming + "." + key, self._resources[key])
        if self._path_naming in new_path_source or self._path_naming in new_path_target:
            raise ValueError(ERRORS["path-naming-incorrect"])
        yield new_path_source, new_path_target

    @property
    def base(self) -> dict:
        """Returns the base mapping configuration."""
        return self._base

    @property
    def name(self) -> str:
        """Returns the name of the mapper."""
        return self._name

    @property
    def input_type(self) -> str:
        """Returns the expected input type."""
        return self._input_type

    @property
    def output_type(self) -> str:
        """Returns the expected output type."""
        return self._output_type

    def get_initial_object(self):
        """Returns the initial output object as a buffer."""
        res = None
        if self._output_type == "dict":
            res = {}
        elif self._output_type == "list":
            res = []
        return res

    def __execute__(self, data=None):
        """Processes the input data and maps it according to the configuration.

        Parameters
        ----------
        data: dict, list
            Input data from which information will be mapped

        Returns
        -------
        res: dict, list
            Mapped data output
        """
        if self.__format == "dict":
            res = self.__execute_mapper_as_dict(data)
        else:
            res = self.__execute_mapper_as_list(data)
        return res

    def __set_buffer(self, target: str, initial: Union[list, dict], buffer):
        route = target.split(self._separator)
        buffer_target = initial
        while len(route) >= 1:
            path = route.pop(0)
            if not route:
                buffer_target[path] = buffer
            elif path in buffer_target:
                buffer_target = buffer_target[path]
            elif path not in buffer_target:
                buffer_target[path] = {}
                buffer_target = buffer_target[path]

    def __execute_mapper_as_dict(self, data):
        """Performs mapping of data based on a dictionary-formatted base."""
        res = self.get_initial_object()
        for source, target in self._base.items():
            route = source.split(self._separator)
            buffer = data.get(route[0], {})
            for path_i in route[1:]:
                if path_i in buffer:
                    buffer = buffer[path_i]
                else:
                    buffer = None
                    break
            self.__set_buffer(target, res, buffer)
        return res

    def __execute_mapper_as_list(self, data):
        """Performs mapping of data based on a list-formatted base."""
        res = self.get_initial_object()
        self._base : list
        for obj in self._base:
            source, target = obj["from"], obj["to"]
            route = source.split(self._separator)
            buffer = data.get(route[0], {})
            for path_i in route[1:]:
                if path_i in buffer:
                    buffer = buffer[path_i]
                else:
                    buffer = None
                    break
            buffer = self.arrange_value(buffer, **obj)
            self.__set_buffer(target, res, buffer)
        return res

    def map(self, data):
        """Redirects input data to the configured output fields."""
        res = self.__execute__(data)
        return res

    __call__ = map
