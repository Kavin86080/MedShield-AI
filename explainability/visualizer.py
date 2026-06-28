import cv2

import numpy as np

from pytorch_grad_cam.utils.image import (
    show_cam_on_image
)


class ExplainabilityVisualizer:

    def overlay_heatmap(
        self,
        original_image,
        heatmap
    ):

        rgb_image = (
            np.float32(
                original_image
            ) / 255.0
        )

        visualization = (
            show_cam_on_image(
                rgb_image,
                heatmap,
                use_rgb=True
            )
        )

        return visualization

    def save_visualization(
        self,
        image,
        output_path
    ):

        cv2.imwrite(
            output_path,
            cv2.cvtColor(
                image,
                cv2.COLOR_RGB2BGR
            )
        )

        return output_path