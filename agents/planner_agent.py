# Placeholder for planner_agent.py
from agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="PlannerAgent"
        )

    def run(
        self,
        state
    ):

        question = state.question

        plan = {
            "task": "medical_qa",
            "question": question,
            "next_agent": "retrieval"
        }

        state.metadata["plan"] = plan

        state.current_agent = self.name

        state.add_history(
            self.name
        )

        return state