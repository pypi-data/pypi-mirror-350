"""Module defining the base class for use cases."""
from abc import ABC

from typing import Optional

class UseCaseBase(ABC):
    """In UML, a complete task of a system that provides a measurable result of
    value for an actor 2. sequence of tasks that a system can perform,
    interacting with users of the system and providing a measurable result of
    value for the user [ISO/IEC 26513:2009 Systems and software
    engineering - Requirements for testers and reviewers of user documentation,
    3.43]3. description of the behavioral requirements of a system and its
    interaction with a user [ISO/IEC/IEEE 26515: 2011 Systems and software
    engineering: Developing user documentation in an agile environment, 4.15]

    Reference: https://www.iso.org/obp/ui/#iso:std:iso-iec-ieee:24765:ed-2:v1:en"""

    __is_use_case__ = True

    def __init__(self, keyname: Optional[str] = None):
        self.keyname = keyname if keyname else self.__class__.__name__
