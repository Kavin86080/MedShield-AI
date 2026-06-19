from rag.pipelines.rag_pipeline import (
    RAGPipeline
)

from agents.planner_agent import (
    PlannerAgent
)

from agents.retrieval_agent import (
    RetrievalAgent
)

from agents.reasoning_agent import (
    ReasoningAgent
)

from agents.report_agent import (
    ReportAgent
)
from agents.agent_state import (
    AgentState
)


class AgentOrchestrator:

    def __init__(self):

        # Initialize RAG Pipeline
        self.rag_pipeline = RAGPipeline()

        # Sample documents for testing
        documents = [

            """
            Pneumonia is a lung infection that causes
            fever, cough and breathing difficulty.
            """,

            """
            Diabetes is a chronic disease affecting
            blood glucose regulation.
            """,

            """
            Hypertension is persistent high blood pressure.
            """,

            """
            Asthma causes inflammation of airways.
            """
        ]

        # Index documents into FAISS
        self.rag_pipeline.index_documents(
            documents
        )

        # Initialize Agents
        self.planner = PlannerAgent()

        self.retrieval = RetrievalAgent(
            self.rag_pipeline
        )

        self.reasoning = ReasoningAgent()

        self.report = ReportAgent()

    def run(
        self,
        question
    ):

        state = AgentState(
            question=question
        )

        # Step 1: Planning
        state = self.planner.run(
            state
        )

        # Step 2: Retrieval
        state = self.retrieval.run(
            state
        )

        # Step 3: Reasoning
        state = self.reasoning.run(
            state
        )

        # Step 4: Reporting
        state = self.report.run(
            state
        )

        return state.report