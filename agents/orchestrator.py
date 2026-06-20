from rag.pipelines.rag_pipeline import (
    RAGPipeline
)

from agents.agent_state import (
    AgentState
)

from agents.agent_router import (
    AgentRouter
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

from agents.document_agent import (
    DocumentAgent
)


class AgentOrchestrator:

    def __init__(self):

        # -------------------------
        # Router
        # -------------------------

        self.router = AgentRouter()

        # -------------------------
        # Traditional Medical QA
        # -------------------------

        self.rag_pipeline = RAGPipeline()

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

        self.rag_pipeline.index_documents(
            documents
        )

        # -------------------------
        # Agents
        # -------------------------

        self.planner = PlannerAgent()

        self.retrieval = RetrievalAgent(
            self.rag_pipeline
        )

        self.reasoning = ReasoningAgent()

        self.report = ReportAgent()

        # -------------------------
        # Document Agent
        # -------------------------

        self.document_agent = (
            DocumentAgent()
        )

        self.document_agent.load_document(
            "datasets/reports/medisense_paper.pdf"
        )

    def run(
        self,
        question
    ):

        state = AgentState(
            question=question
        )

        # =========================
        # Step 1: Route Question
        # =========================

        state = self.router.run(
            state
        )

        route = (
            state.metadata.get(
                "route"
            )
        )

        # =========================
        # DOCUMENT ANALYSIS
        # =========================

        if route == (
            "document_analysis"
        ):

            state = (
                self.document_agent.run(
                    state
                )
            )

            state = (
                self.report.run(
                    state
                )
            )

            return (
                state.report
            )

        # =========================
        # IMAGE ANALYSIS
        # =========================

        elif route == (
            "image_analysis"
        ):

            state.answer = (
                "Image Analysis Agent will be implemented in Phase 7."
            )

            state = (
                self.report.run(
                    state
                )
            )

            return (
                state.report
            )

        # =========================
        # REPORT GENERATION
        # =========================

        elif route == (
            "report_generation"
        ):

            state.answer = (
                "Report Generation Agent will be implemented in Phase 8."
            )

            state = (
                self.report.run(
                    state
                )
            )

            return (
                state.report
            )

        # =========================
        # DEFAULT MEDICAL QA
        # =========================

        state = self.planner.run(
            state
        )

        state = self.retrieval.run(
            state
        )

        state = self.reasoning.run(
            state
        )

        state = self.report.run(
            state
        )

        return (
            state.report
        )