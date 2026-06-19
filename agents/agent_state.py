from dataclasses import (
    dataclass,
    field
)

from typing import (
    List,
    Dict,
    Any
)


@dataclass
class AgentState:

    question: str

    contexts: List[str] = field(
        default_factory=list
    )

    answer: str = ""

    report: Dict[str, Any] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    current_agent: str = ""

    execution_history: List[str] = field(
        default_factory=list
    )

    status: str = "initialized"

    def update_status(
        self,
        status
    ):
        self.status = status

    def add_history(
        self,
        agent_name
    ):
        self.execution_history.append(
            agent_name
        )

    def to_dict(
        self
    ):

        return {
            "question":
                self.question,

            "contexts":
                self.contexts,

            "answer":
                self.answer,

            "report":
                self.report,

            "metadata":
                self.metadata,

            "current_agent":
                self.current_agent,

            "execution_history":
                self.execution_history,

            "status":
                self.status
        } 