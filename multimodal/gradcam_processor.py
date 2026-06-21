import cv2
import numpy as np
import torch

from PIL import Image
from torchvision import transforms

from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

from models.chest_xray_model import (
    ChestXRayModel
)


class GradCAMProcessor:

    def __init__(
        self,
        model_path
    ):

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model = (
            ChestXRayModel()
        )

        self.model.load_state_dict(
            torch.load(
                model_path,
                map_location=self.device
            )
        )

        self.model.to(
            self.device
        )

        self.model.eval()

        self.transform = transforms.Compose([

            transforms.Resize(
                (224, 224)
            ),

            transforms.ToTensor(),

            transforms.Normalize(

                mean=[
                    0.485,
                    0.456,
                    0.406
                ],

                std=[
                    0.229,
                    0.224,
                    0.225
                ]
            )
        ])

    def generate_heatmap(
        self,
        image_path,
        output_path=
        "outputs/gradcam_result.jpg"
    ):

        # Load image
        image = Image.open(
            image_path
        ).convert(
            "RGB"
        )

        # Resize image to model input size
        image = image.resize(
            (224, 224)
        )

        # Convert for GradCAM visualization
        rgb_image = (
            np.array(image)
            .astype(np.float32)
            / 255.0
        )

        # Prepare tensor
        input_tensor = (
            self.transform(image)
            .unsqueeze(0)
            .to(self.device)
        )

        # Last DenseNet block
        target_layers = [
            self.model.model.features.denseblock4
        ]

        # Generate Grad-CAM
        with GradCAM(
            model=self.model,
            target_layers=target_layers
        ) as cam:

            grayscale_cam = cam(
                input_tensor=input_tensor
            )

            grayscale_cam = (
                grayscale_cam[0]
            )

        # Overlay heatmap
        visualization = (
            show_cam_on_image(
                rgb_image,
                grayscale_cam,
                use_rgb=True
            )
        )

        # Save result
        cv2.imwrite(
            output_path,
            cv2.cvtColor(
                visualization,
                cv2.COLOR_RGB2BGR
            )
        )

        return output_path