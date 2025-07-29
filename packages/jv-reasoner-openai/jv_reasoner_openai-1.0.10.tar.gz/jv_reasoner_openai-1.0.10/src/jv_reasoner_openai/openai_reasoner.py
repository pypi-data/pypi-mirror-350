import json
from jvcore import Reasoner, ActionDescription, ActionParameters, Communicator
from jvopenai import OpenAIConversation
from .instruction import instruction


class OpenAiReasoner(Reasoner):
    def __init__(self, communicator: Communicator):
        self.__conversation = OpenAIConversation()
        self.__initialised = False
        self.__communicator = communicator

    def selectSkill(self, skillsAndQueries: dict[str, ActionDescription], utterance: str) -> ActionParameters | None:
        self.__initialInstruction(skillsAndQueries)
        response = self.__conversation.getResponse(utterance)
        return json.loads(response) if response != 'none' else None
    
    def __initialInstruction(self, skillsAndQueries: dict[str, ActionDescription]) -> str:
        if not self.__initialised:
            instructions = instruction(skillsAndQueries)
            instructionAccepted = self.__conversation.getResponse(instructions) == '1'
            self.__initialised = True
            if not instructionAccepted:
                raise KeyError('Its wrong error and openai doesnt understand me (reasoner)') # todo 0 this does not make sense, it will always understand

