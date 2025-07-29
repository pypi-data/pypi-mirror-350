"""Module for input parameter mapping and transformation.

This module provides utilities to build mappers for transforming input data.
It includes support for single `Mapper` instances, grouped mappers via `MappingGroup`,
and interfaces for arranging mapped data using `IArranger`.
"""

from typing import Union

from .mapping_group import MappingGroup
from .arranger import IArranger
from .mapper import Mapper


def build_mapper(mappers=None) -> Union[MappingGroup, Mapper, None]:
    """Builds a mapper instance based on the given configuration.

    Depending on the type of `mappers`, this function returns a `Mapper`,
    a `MappingGroup` (if a list/tuple of mappers is provided), or passes through
    existing instances.

    Parameters
    ----------
    mappers : Union[None, dict, Mapper, MappingGroup, list, tuple], optional
        The mapping configuration to convert into a Mapper or MappingGroup.
        - If `None`, returns `None`.
        - If `dict`, creates a `Mapper` with that mapping.
        - If a `list` or `tuple`, creates a `MappingGroup` with each element
            as a Mapper or existing instance.
        - If already a `Mapper` or `MappingGroup`, returns it directly.
        - Otherwise, raises `TypeError`.

    Returns
    -------
    Union[MappingGroup, Mapper, None]
        The resulting mapper object or `None` if no configuration is provided.

    Raises
    ------
    TypeError
        If the input type is not supported.
    """
    mapper_ = None
    if mappers:
        if isinstance(mappers, (list, tuple)):
            mapper_ = MappingGroup(
                [Mapper("", i) if isinstance(i, dict) else i for i in mappers])
        elif isinstance(mappers, dict):
            mapper_ = Mapper("Http mapper_", mappers)
        elif isinstance(mappers, (MappingGroup, Mapper)):
            mapper_ = mappers
        else:
            raise TypeError("Invalid mapper type")
    return mapper_


__all__ = ["MappingGroup", "Mapper", "IArranger", "build_mapper"]
