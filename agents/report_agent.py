# Placeholder for report_agent.py
from agents.base_agent import BaseAgent


class ReportAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="ReportAgent"
        )

    def run(
        self,
        state
    ):

        report = {

            "question":
                state["question"],

            "answer":
                state["answer"],

            "contexts":
                state["contexts"]

        }

        state["report"] = report

        return state