from explainability.gradcam_explainer import (
    CAMExplainer
)

from explainability.shap_explainer import (
    SHAPExplainer
)


class ExplanationReport:

    def __init__(
        self,
        cam_explainer,
        shap_explainer
    ):

        self.cam = (
            cam_explainer
        )

        self.shap = (
            shap_explainer
        )

    def generate_report(
        self,
        image_tensor,
        prediction,
        confidence
    ):

        gradcam = (
            self.cam.generate_gradcam(
                image_tensor
            )
        )

        scorecam = (
            self.cam.generate_scorecam(
                image_tensor
            )
        )

        eigencam = (
            self.cam.generate_eigencam(
                image_tensor
            )
        )

        layercam = (
            self.cam.generate_layercam(
                image_tensor
            )
        )

        shap_result = (
            self.shap.explain(
                image_tensor
            )
        )

        return {

            "prediction":
                prediction,

            "confidence":
                confidence,

            "gradcam":
                gradcam,

            "scorecam":
                scorecam,

            "eigencam":
                eigencam,

            "layercam":
                layercam,

            "shap":
                shap_result,

            "clinical_explanation":
                f"Model predicts {prediction} with {confidence:.2f}% confidence."
        }