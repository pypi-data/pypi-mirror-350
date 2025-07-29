from abc import ABC

class Waker(ABC):
    def wakeword_detected(self) -> str:
        '''detected wakeword'''
        pass