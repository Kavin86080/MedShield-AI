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
                state.question,

            "answer":
                state.answer,

            "contexts":
                state.contexts,

            "route":
                state.metadata.get(
                    "route"
                ),

            "execution_history":
                state.execution_history

        }

        state.report = report

        state.current_agent = self.name

        state.add_history(
            self.name
        )

        return state