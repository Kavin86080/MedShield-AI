from rag.pipelines.medical_rag_pipeline import (
    MedicalRAGPipeline
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

from agents.image_agent import (
    ImageAgent
)


class AgentOrchestrator:

    def __init__(self): 
        print( "\nAgentOrchestrator Initialized" )

        # -------------------------
        # Router
        # -------------------------

        self.router = AgentRouter()

        # -------------------------
        # Medical Knowledge Base
        # -------------------------

        print(
            "\nLOADING MEDICAL KNOWLEDGE BASE..."
        )

        self.rag_pipeline = (
            MedicalRAGPipeline()
        )

        self.rag_pipeline.index_medical_knowledge(
            "datasets/medical_knowledge"
        )

        print(
            "\nMEDICAL KNOWLEDGE BASE READY"
        )

        # -------------------------
        # Medical QA Agents
        # -------------------------

        self.planner = (
            PlannerAgent()
        )

        self.retrieval = (
            RetrievalAgent(
                self.rag_pipeline
            )
        )

        self.reasoning = (
            ReasoningAgent()
        )

        self.report = (
            ReportAgent()
        )

        # -------------------------
        # Document Agent
        # -------------------------

        try:

           self.document_agent = (
               DocumentAgent()
           )

           print(
               "\nDOCUMENT AGENT READY"
           )

        except Exception as e:

            print(
                f"\nDOCUMENT AGENT FAILED: {e}"
            )

            self.document_agent = None

        # -------------------------
        # Image Agent
        # -------------------------

        self.image_agent = (
            ImageAgent()
        )

    def run(
        self,
        state
    ):

        # =========================
        # Route Question
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

            if self.document_agent is None:

                state.answer = (
                    "Document Analysis Agent is unavailable."
                )

                state = (
                    self.report.run(
                        state
                    )
                )

                return (
                    state.report
                )

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

            state = (
                self.image_agent.run(
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
        # REPORT GENERATION
        # =========================

        elif route == (
            "report_generation"
        ):

            state.answer = (
                "Report Generation Agent will be implemented in Phase 10."
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

        state = (
            self.planner.run(
                state
            )
        )

        state = (
            self.retrieval.run(
                state
            )
        )

        state = (
            self.reasoning.run(
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