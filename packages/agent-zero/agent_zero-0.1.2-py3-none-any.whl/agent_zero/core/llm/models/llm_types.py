from typing_extensions import Literal, TypedDict
from pydantic import BaseModel


class ResponseFormat(TypedDict):
    type: Literal["text", "json_object"]


class IntentSchema(BaseModel):
    intent: str