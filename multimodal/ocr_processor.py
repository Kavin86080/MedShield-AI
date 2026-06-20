from pathlib import Path
from paddleocr import PaddleOCR


class OCRProcessor:

    def __init__(self):

        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False
        )

    def extract_text(
        self,
        image_path
    ):

        image_path = Path(
            image_path
        )

        if not image_path.exists():

            raise FileNotFoundError(
                f"{image_path} not found"
            )

        result = self.ocr.predict(
            str(image_path)
        )

        extracted_text = []

        for page in result:

            texts = page.get(
                "rec_texts",
                []
            )

            extracted_text.extend(
                texts
            )

        return "\n".join(
            extracted_text
        )