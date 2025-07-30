from typing import TypedDict


class ResponseStatus(TypedDict, total=False):
    success: bool
    code: str
    message: str
    data: dict
