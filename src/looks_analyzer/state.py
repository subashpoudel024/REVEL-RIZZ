from typing import Optional , TypedDict , Annotated
from langgraph.graph.message import add_messages


class State(TypedDict):
    image: bytes
    messages: Annotated[list, add_messages]
    suggestions: str
