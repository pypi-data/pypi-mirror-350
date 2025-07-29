from abc import ABC

class SpeechToText(ABC):
    def get_utterance(self, max_seconds) -> str:
        '''gets voice input as text'''
        pass
