from agents.base_agent import BaseAgent

from models.inference_xray import (
    XRayInference
)

from multimodal.gradcam_processor import (
    GradCAMProcessor
)

from ai_engine.gemini_engine.medical_explainer import (
    MedicalExplainer
)


class ImageAgent(BaseAgent):

    def __init__(self):

        super().__init__(
            name="ImageAgent"
        )

        self.predictor = XRayInference(
            "models/chest_xray_model.pth"
        )

        self.gradcam = GradCAMProcessor(
            "models/chest_xray_model.pth"
        )

        self.explainer = MedicalExplainer()

    def run(
        self,
        state
    ):

        image_path = (
            state.metadata.get(
                "image_path"
            )
        )

        if not image_path:
            raise ValueError(
                "image_path not found in state.metadata"
            )

        prediction = (
            self.predictor.predict(
                image_path
            )
        )

        heatmap_path = (
            self.gradcam.generate_heatmap(
                image_path
            )
        )

        explanation = (
            self.explainer.explain(
                prediction=
                prediction["prediction"],

                confidence=
                prediction["confidence"]
            )
        )

        state.answer = explanation

        state.metadata[
            "prediction"
        ] = prediction

        state.metadata[
            "heatmap_path"
        ] = heatmap_path

        state.current_agent = (
            self.name
        )

        state.add_history(
            self.name
        )

        return state