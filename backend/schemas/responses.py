from pydantic import BaseModel


class APIResponse(
    BaseModel
):

    status: str

    result: dict