from abc import ABC, abstractmethod
from jvcore import ActionDescription


class QueryBase(ABC):
    @staticmethod
    @abstractmethod
    def getDescription() -> ActionDescription:
        '''provide a clear description of query usage, reasoner will be matching user utterance based on this description'''
        pass
