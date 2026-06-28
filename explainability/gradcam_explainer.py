from pytorch_grad_cam import (
    GradCAM,
    ScoreCAM,
    EigenCAM,
    LayerCAM
)


class CAMExplainer:

    def __init__(
        self,
        model,
        target_layer
    ):
        self.model = model
        self.target_layer = target_layer

    def generate_gradcam(
        self,
        image_tensor
    ):

        cam = GradCAM(
            model=self.model,
            target_layers=[
                self.target_layer
            ]
        )

        heatmap = cam(
            input_tensor=image_tensor
        )[0]

        return heatmap

    def generate_scorecam(
        self,
        image_tensor
    ):

        cam = ScoreCAM(
            model=self.model,
            target_layers=[
                self.target_layer
            ]
        )

        heatmap = cam(
            input_tensor=image_tensor
        )[0]

        return heatmap

    def generate_eigencam(
        self,
        image_tensor
    ):

        cam = EigenCAM(
            model=self.model,
            target_layers=[
                self.target_layer
            ]
        )

        heatmap = cam(
            input_tensor=image_tensor
        )[0]

        return heatmap

    def generate_layercam(
        self,
        image_tensor
    ):

        cam = LayerCAM(
            model=self.model,
            target_layers=[
                self.target_layer
            ]
        )

        heatmap = cam(
            input_tensor=image_tensor
        )[0]

        return heatmap