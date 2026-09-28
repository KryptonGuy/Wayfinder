from functools import lru_cache

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph

from app.config import get_settings
from app.graph.state import ChatState
from app.schemas import ChatMessage


def _to_langchain_messages(messages: list[ChatMessage]) -> list[BaseMessage]:
    converted: list[BaseMessage] = []
    for message in messages:
        if message.role == "user":
            converted.append(HumanMessage(content=message.content))
        else:
            converted.append(AIMessage(content=message.content))
    return converted


@lru_cache
def _get_chat_graph():
    settings = get_settings()
    if not settings.google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured")

    llm = ChatGoogleGenerativeAI(
        google_api_key=settings.google_api_key,
        model=settings.google_model,
    )

    async def call_model(state: ChatState) -> ChatState:
        response = await llm.ainvoke(state["messages"])
        return {"messages": [response]}

    graph = StateGraph(ChatState)
    graph.add_node("llm", call_model)
    graph.add_edge(START, "llm")
    graph.add_edge("llm", END)
    return graph.compile()

graph = _get_chat_graph()


async def run_chat(messages: list[ChatMessage]) -> str:
    result = await _get_chat_graph().ainvoke({"messages": _to_langchain_messages(messages)})
    last_message = result["messages"][-1]
    return str(last_message.content)


async def stream_chat(messages: list[ChatMessage]):
    async for message_chunk, _metadata in _get_chat_graph().astream(
        {"messages": _to_langchain_messages(messages)},
        stream_mode="messages",
    ):
        content = message_chunk.content
        if isinstance(content, str) and content:
            yield content