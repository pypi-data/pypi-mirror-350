from abc import ABC, abstractmethod
from agentutil.utils.agentAssistant import AgentAssistant
from agentutil.utils.sjAssistant import SJAssistant
from django.forms import Form


# 🎭 Abstract Base Class for Agents
class Agent(ABC):
    def __init__(self, assistant: AgentAssistant=None, form: Form=None):
        self.form = form
        if assistant:
            self.assistant = assistant
        else:
            self.assistant = SJAssistant()
    @abstractmethod
    async def run(self, data):
        pass
