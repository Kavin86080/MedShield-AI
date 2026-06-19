# Placeholder for base_agent.py
from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self, name):

        self.name = name

    @abstractmethod
    def run(
        self,
        state
    ):
        pass

    def info(self):

        return {
            "agent_name": self.name,
            "status": "ready"
        }