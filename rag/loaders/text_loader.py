# Placeholder for text_loader.py
from pathlib import Path


class TextLoader:

    def __init__(self):
        pass

    def load(self, file_path):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"{file_path} not found"
            )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        return content