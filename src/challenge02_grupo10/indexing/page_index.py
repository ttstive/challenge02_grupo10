from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence

try:
    from langchain_core.documents import Document
except ImportError:  # pragma: no cover - fallback for lightweight usage
    @dataclass
    class Document:
        page_content: str
        metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class IndexedPage:
    title: str
    content: str
    page_number: int
    topic: str
    metadata: dict[str, Any] = field(default_factory=dict)


class PageIndex:
    """Lightweight typed page index for a domain-specific retrieval chain."""

    def __init__(self, topic: str, pages: Sequence[IndexedPage]):
        self.topic = topic
        self.pages = list(pages)

    @classmethod
    def from_topic_set(
        cls,
        topic: str,
        page_payloads: Sequence[dict[str, Any] | str],
    ) -> "PageIndex":
        indexed_pages: list[IndexedPage] = []

        for index, payload in enumerate(page_payloads, start=1):
            if isinstance(payload, str):
                content = payload
                title = f"{topic} page {index}"
                page_number = index
                metadata = {"source": "manual"}
            elif isinstance(payload, dict):
                content = str(payload.get("content", ""))
                title = str(payload.get("title", f"{topic} page {index}"))
                page_number = int(payload.get("page_number", index))
                metadata = dict(payload.get("metadata", {}))
                metadata.setdefault("source", payload.get("source", "manual"))
            else:
                raise TypeError("Each page entry must be a string or mapping.")

            indexed_pages.append(
                IndexedPage(
                    title=title,
                    content=content,
                    page_number=page_number,
                    topic=topic,
                    metadata={**metadata, "topic": topic},
                )
            )

        return cls(topic=topic, pages=indexed_pages)

    def add_page(self, page: IndexedPage) -> None:
        self.pages.append(page)

    def search(self, query: str, k: int = 3) -> list[IndexedPage]:
        if not query:
            return self.pages[:k]

        normalized_query = query.lower().split()
        scored_pages: list[tuple[int, IndexedPage]] = []

        for page in self.pages:
            text = f"{page.title} {page.content}".lower()
            score = sum(1 for term in normalized_query if term in text)
            if score > 0:
                scored_pages.append((score, page))

        scored_pages.sort(key=lambda item: item[0], reverse=True)
        return [page for _, page in scored_pages[:k]]

    def to_documents(self) -> list[Document]:
        documents: list[Document] = []
        for page in self.pages:
            metadata = {
                "title": page.title,
                "topic": page.topic,
                "page_number": page.page_number,
                **page.metadata,
            }
            documents.append(Document(page_content=page.content, metadata=metadata))
        return documents

    def __len__(self) -> int:
        return len(self.pages)

    def __iter__(self):
        return iter(self.pages)
