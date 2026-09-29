from collections.abc import Callable
from functools import lru_cache

from langgraph.graph.state import CompiledStateGraph

from app.agents import chat

# Register new agents here; also add them to langgraph.json for LangGraph Studio.
AGENTS: dict[str, Callable[[], CompiledStateGraph]] = {
    "chat": chat.build_graph,
}


@lru_cache
def get_agent(name: str) -> CompiledStateGraph:
    try:
        builder = AGENTS[name]
    except KeyError:
        raise ValueError(f"Unknown agent '{name}'. Available: {', '.join(AGENTS)}") from None
    return builder()
