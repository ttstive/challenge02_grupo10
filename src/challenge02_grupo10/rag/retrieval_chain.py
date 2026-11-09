from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from challenge02_grupo10.indexing.page_index import PageIndex


@dataclass
class NeurocognitiveSpeechRAG:
    """Small retrieval layer focused on neurocognitive speech context."""

    topic: str
    page_index: PageIndex

    @classmethod
    def from_topic_set(
        cls,
        topic: str,
        page_payloads: Sequence[dict[str, Any] | str],
    ) -> "NeurocognitiveSpeechRAG":
        return cls(topic=topic, page_index=PageIndex.from_topic_set(topic, page_payloads))

    def retrieve(self, query: str, k: int = 3) -> list:
        return self.page_index.search(query=query, k=k)

    def build_context(self, query: str, k: int = 3) -> str:
        matches = self.retrieve(query=query, k=k)
        if not matches:
            return "No relevant pages were found in the neurocognitive speech index."

        return "\n\n".join(
            f"## {page.title}\n{page.content}"
            for page in matches
        )


def build_rag_chain(topic: str, page_payloads: Sequence[dict[str, Any] | str]) -> NeurocognitiveSpeechRAG:
    """Factory used to assemble the first version of the domain-aware retrieval chain."""
    return NeurocognitiveSpeechRAG.from_topic_set(topic, page_payloads)
