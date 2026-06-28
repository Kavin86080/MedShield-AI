from pydantic import BaseModel


class QuestionRequest(
    BaseModel
):

    question: str


class ImageRequest(
    BaseModel
):

    image_path: str


class DocumentRequest(
    BaseModel
):

    question: str