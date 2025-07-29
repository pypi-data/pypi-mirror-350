"""Implementation of the mapping group class"""
from .mapper import Mapper

ERROR = {"target-dup": "The target destination will be overwritten",
         "output-differs": "The types of outputs are different",
         "input-differs": "The types of inputs are different",
         "no-container": "There is nothing in the container"}


class MappingGroup:
    """Container class of mappers that can be run in conjunction with each
    other"""

    def __init__(self, container, resources=None):
        if not container:
            raise ValueError(ERROR["no-container"])

        self._container = container
        self._resources = resources or {}
        self._validate_mappers(container)
        self._check_duplicate_targets(container)

    @staticmethod
    def _validate_mappers(container):
        """Checks the mappers in container"""
        buffer_input = None
        buffer_output = None

        for mapper in container:
            if not isinstance(mapper, Mapper):
                raise ValueError(f'{mapper} is not a mapper')

            if buffer_output and buffer_output != mapper.output_type:
                raise ValueError(ERROR['output-differs'] +
                                 f" {buffer_output} != {mapper.output_type}")
            if buffer_input and buffer_input != mapper.input_type:
                raise ValueError(ERROR['input-differs'] +
                                 f" {buffer_input} != {mapper.input_type}")

            buffer_input = buffer_input or mapper.input_type
            buffer_output = buffer_output or mapper.output_type

    @staticmethod
    def _check_duplicate_targets(container):
        """Checks if the duplicate keys on mappers values"""
        target_keys = set()

        for mapper in container:
            for value in mapper.base.values():
                if value in target_keys:
                    raise ValueError(ERROR["target-dup"])
                target_keys.add(value)


    def map(self, data):
        """Map data with multiple mappers"""
        res = self._container[0].map(data)
        for mapper in self._container[1:]:
            res.update(mapper.map(data))
        return res
