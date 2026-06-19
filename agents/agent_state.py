# Placeholder for agent_state.py
from dataclasses import dataclass, field


@dataclass
class AgentState:

    question: str

    contexts: list = field(
        default_factory=list
    )

    answer: str = ""

    report: dict = field(
        default_factory=dict
    )

    metadata: dict = field(
        default_factory=dict
    )