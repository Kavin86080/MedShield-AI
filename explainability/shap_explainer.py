# Placeholder for shap_explainer.py
import shap
import numpy as np


class SHAPExplainer:

    def __init__(
        self,
        model
    ):

        self.model = model

    def explain(
        self,
        image_tensor
    ):

        image = (
            image_tensor
            .detach()
            .cpu()
            .numpy()
        )

        explanation = {
            "importance_score":
            float(
                np.random.uniform(
                    0.7,
                    0.95
                )
            ),

            "top_regions": [
                {
                    "region":
                    "Left Lower Lung",

                    "importance":
                    0.24
                },

                {
                    "region":
                    "Right Hilum",

                    "importance":
                    0.19
                },

                {
                    "region":
                    "Pleural Space",

                    "importance":
                    0.12
                }
            ]
        }

        return explanation