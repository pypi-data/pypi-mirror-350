from typing import TypedDict

from langchain_core.messages.base import BaseMessage
from pydantic import BaseModel


class MessageDict(TypedDict):
    message: list[BaseMessage]


class DestinationModelType(BaseModel):
    target: str
