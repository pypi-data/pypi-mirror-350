from jvcore import Reasoner, Communicator
from jvcore.testing import TestCommunicator
from .openai_reasoner import OpenAiReasoner

def getReasoner(communicator: Communicator) -> Reasoner:
    return OpenAiReasoner(communicator)

def test():
    comm = TestCommunicator()
    reasoner = getReasoner(comm)
    # todo ML 0 get from file skills
    skills = {name: skill.getDescription() for name, skill in self.__services.getSkills().items()} # todo ML get form file maybe
    comm.print(skills)
    while True:
        request = comm.getUserResponse('>')
        response = reasoner.selectSkill(skills, request)
        comm.print(response)