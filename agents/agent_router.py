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

        # PDF / Document Analysis

        if any(
            keyword in question
            for keyword in [
                "pdf",
                "document",
                "medical report",
                "lab report",
                "blood report"
            ]
        ):

            route = (
                "document_analysis"
            )

        # Medical Image Analysis

        elif any(
            keyword in question
            for keyword in [
                "xray",
                "x-ray",
                "mri",
                "ct",
                "scan",
                "image"
            ]
        ):

            route = (
                "image_analysis"
            )

        # Report Generation

        elif any(
            keyword in question
            for keyword in [
                "generate report",
                "create report",
                "make report",
                "patient report"
            ]
        ):
            route = (
                "report_generation"
            )

        # Default Path

        else:

            route = (
                "medical_qa"
            )

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