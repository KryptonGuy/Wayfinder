from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.agents.chat.state import ChatState
from app.llm import get_llm


def build_graph() -> CompiledStateGraph:
    llm = get_llm()

    async def call_model(state: ChatState) -> ChatState:
        response = await llm.ainvoke(state["messages"])
        return {"messages": [response]}

    graph = StateGraph(ChatState)
    graph.add_node("llm", call_model)
    graph.add_edge(START, "llm")
    graph.add_edge("llm", END)
    return graph.compile()