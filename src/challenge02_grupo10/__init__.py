"""Challenge 02 package exposing the RAG and page-index building blocks."""

from .indexing.page_index import PageIndex
from .langgraph.workflow import RAGState, build_rag_graph
from .rag.retrieval_chain import NeurocognitiveSpeechRAG, build_rag_chain

__all__ = [
    "PageIndex",
    "RAGState",
    "NeurocognitiveSpeechRAG",
    "build_rag_chain",
    "build_rag_graph",
]


def main() -> None:
    print("Challenge02 neurocognitive speech RAG scaffold ready.")
