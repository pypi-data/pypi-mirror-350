from ..communicator import Communicator

class TestCommunicator(Communicator):
    def say(self, text: str):
        print('voice: ' + text)
    
    def sayAndPrint(self, text: str):
        print(text)
        print('voice: ' + text)
    
    def print(self, text: str):
        print(text)
    
    def getUserResponse(self, question: str) -> str:
        return input(question)