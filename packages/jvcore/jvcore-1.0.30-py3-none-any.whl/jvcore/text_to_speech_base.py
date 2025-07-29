from abc import ABC

class TextToSpeech(ABC):
    def sayAndWait(self, text) -> str:
        pass