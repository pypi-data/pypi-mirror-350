from abc import ABC, abstractmethod
from .reasoner_base import ActionDescription


class SkillBase(ABC):       
    @staticmethod
    @abstractmethod
    def getDescription() -> dict[str, ActionDescription]:
        '''provide a clear description of skill posibilities, reasoner will be matching user utterance based on this description'''
        pass
 