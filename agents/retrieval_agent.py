from agents.base_agent import BaseAgent


class RetrievalAgent(BaseAgent):

    def __init__(
        self,
        rag_pipeline
    ):

        super().__init__(
            name="RetrievalAgent"
        )

        self.rag = rag_pipeline

    def run(
        self,
        state
    ):

        question = state["question"]

        contexts = self.rag.retrieve_context(
            question
        )

        state["contexts"] = contexts

        return state