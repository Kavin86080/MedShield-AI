from agents.base_agent import BaseAgent


class AgentRouter(BaseAgent):

    def __init__(self):

        super().__init__(
            name="AgentRouter"
        )

    def run(
        self,
        state
    ):

        question = (
            state.question
            .lower()
            .strip()
        )

        # ---------------------------------
        # Document Analysis Route
        # ---------------------------------

        if any(
            keyword in question
            for keyword in [
                "paper",
                "document",
                "pdf",
                "research",
                "medisense",
                "article",
                "publication",
                "chapter"
            ]
        ):

            route = (
                "document_analysis"
            )

        # ---------------------------------
        # Medical Image Analysis Route
        # ---------------------------------

        elif any(
            keyword in question
            for keyword in [
                "xray",
                "x-ray",
                "mri",
                "ct",
                "scan",
                "image",
                "radiology",
                "chest xray",
                "chest x-ray"
            ]
        ):

            route = (
                "image_analysis"
            )

        # ---------------------------------
        # Report Generation Route
        # ---------------------------------

        elif any(
            keyword in question
            for keyword in [
                "generate report",
                "create report",
                "make report",
                "patient report",
                "summary report"
            ]
        ):

            route = (
                "report_generation"
            )

        # ---------------------------------
        # Default Medical QA Route
        # ---------------------------------

        else:

            route = (
                "medical_qa"
            )

        # Store route in state

        state.metadata[
            "route"
        ] = route

        state.current_agent = (
            self.name
        )

        state.add_history(
            self.name
        )

        return state