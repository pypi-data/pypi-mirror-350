from abc import ABC, abstractmethod

class Communicator(ABC):    
    @abstractmethod
    def say(self, text: str):
        pass
    
    @abstractmethod
    def sayAndPrint(self, text: str):
        pass
    
    @abstractmethod
    def print(self, text: str):
        pass
    
    @abstractmethod
    def getUserResponse(self, question: str) -> str:
        pass
