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

            # ---------------------------------
            # User Query
            # ---------------------------------

            "question":
                state.question,

            # ---------------------------------
            # Final Answer
            # ---------------------------------

            "answer":
                state.answer,

            # ---------------------------------
            # Retrieved Contexts
            # ---------------------------------

            "contexts":
                state.contexts,

            # ---------------------------------
            # Selected Route
            # ---------------------------------

            "route":
                state.metadata.get(
                    "route"
                ),

            # ---------------------------------
            # Image Analysis Results
            # ---------------------------------

            "prediction":
                state.metadata.get(
                    "prediction"
                ),

            "heatmap_path":
                state.metadata.get(
                    "heatmap_path"
                ),

            # ---------------------------------
            # Future Extensions
            # ---------------------------------

            "document_source":
                state.metadata.get(
                    "document_source"
                ),

            "confidence":
                state.metadata.get(
                    "confidence"
                ),

            # ---------------------------------
            # Agent Execution History
            # ---------------------------------

            "execution_history":
                state.execution_history

        }

        state.report = report

        state.current_agent = (
            self.name
        )

        state.add_history(
            self.name
        )

        return state