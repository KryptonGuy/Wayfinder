from collections.abc import AsyncIterator

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from app.agents import get_agent
from app.schemas import ChatMessage


def _to_langchain_messages(messages: list[ChatMessage]) -> list[BaseMessage]:
    converted: list[BaseMessage] = []
    for message in messages:
        if message.role == "user":
            converted.append(HumanMessage(content=message.content))
        else:
            converted.append(AIMessage(content=message.content))
    return converted


def _content_text(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(
        part if isinstance(part, str) else part.get("text", "")
        for part in content
        if isinstance(part, str) or part.get("type") == "text"
    )


async def run_chat(messages: list[ChatMessage], agent: str = "chat") -> str:
    result = await get_agent(agent).ainvoke({"messages": _to_langchain_messages(messages)})
    return _content_text(result["messages"][-1].content)


async def stream_chat(messages: list[ChatMessage], agent: str = "chat") -> AsyncIterator[str]:
    async for message_chunk, _metadata in get_agent(agent).astream(
        {"messages": _to_langchain_messages(messages)},
        stream_mode="messages",
    ):
        content = _content_text(message_chunk.content)
        if content:
            yield content
