from abc import ABC, abstractmethod
from enum import Enum
from typing import TypedDict

class ActionType(Enum):
    Query = 1
    Command = 2

class ActionParameters(TypedDict):
    type: ActionType
    actionName: str
    parameters: dict[str,any]

class ParameterDescription(TypedDict):
    description: str
    type: str | dict[str, 'ParameterDescription']

class ActionDescription(TypedDict):
    type: ActionType
    description: str
    parameters: dict[str, ParameterDescription]
    
class Reasoner(ABC):
    @abstractmethod
    def selectSkill(self, skillsAndQueries: dict[str, ActionDescription], utterance: str) -> ActionParameters | None:
        '''Selects requested skill/query based on utterance and list of available skills/queries.'''
        pass
