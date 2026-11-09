from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph

from challenge02_grupo10.indexing.page_index import PageIndex


class RAGState(TypedDict):
    question: str
    context: str
    answer: str


def _retrieve_context(state: RAGState, page_index: PageIndex) -> RAGState:
    question = state.get("question", "")
    matches = page_index.search(question, k=3)

    if not matches:
        state["context"] = "No relevant pages were found for this neurocognitive speech query."
    else:
        state["context"] = "\n\n".join(
            f"## {page.title}\n{page.content}" for page in matches
        )
    return state


def _generate_answer(state: RAGState) -> RAGState:
    question = state.get("question", "")
    context = state.get("context", "")
    state["answer"] = (
        f"Question: {question}\n\n"
        "Relevant context:\n"
        f"{context}"
    )
    return state


def build_rag_graph(page_index: PageIndex):
    """Construct a minimal LangGraph workflow that retrieves relevant pages and responds."""
    workflow = StateGraph(RAGState)
    workflow.add_node(
        "retrieve_context",
        lambda state: _retrieve_context(state, page_index),
    )
    workflow.add_node("generate_answer", _generate_answer)
    workflow.set_entry_point("retrieve_context")
    workflow.add_edge("retrieve_context", "generate_answer")
    workflow.add_edge("generate_answer", END)
    return workflow.compile()
