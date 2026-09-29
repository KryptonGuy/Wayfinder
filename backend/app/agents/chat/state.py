from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

#TODO: Modify for context
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]