from explainability.explanation_report import (
    ExplanationReport
)


class ExplainabilityService:

    def __init__(
        self,
        model=None
    ):

        self.report_engine = (
            ExplanationReport(
                model
            )
        )

    def analyze(
        self,
        image_tensor,
        prediction,
        confidence
    ):

        report = (
            self.report_engine.generate(
                image_tensor=image_tensor,
                prediction=prediction,
                confidence=confidence
            )
        )

        return report