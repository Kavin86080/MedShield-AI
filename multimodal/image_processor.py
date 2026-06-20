# Placeholder for image_processor.py
from PIL import Image

import torch

from torchvision import transforms


class ImageProcessor:

    def __init__(self):

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

    def load_image(
        self,
        image_path
    ):

        image = Image.open(
            image_path
        ).convert(
            "RGB"
        )

        return image

    def preprocess(
        self,
        image_path
    ):

        image = self.load_image(
            image_path
        )

        tensor = self.transform(
            image
        )

        tensor = tensor.unsqueeze(
            0
        )

        return tensor