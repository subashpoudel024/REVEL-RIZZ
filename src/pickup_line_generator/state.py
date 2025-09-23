from typing import Optional , TypedDict , Annotated
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    conversation_chat: str
    tones: list
    attributes:list
    pickup_lines:dict