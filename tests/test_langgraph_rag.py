from challenge02_grupo10.indexing.page_index import PageIndex
from challenge02_grupo10.langgraph.workflow import build_rag_graph


def test_langgraph_rag_graph_builds_context_from_page_index():
    index = PageIndex.from_topic_set(
        "speech neurocognition",
        [
            {
                "title": "Speech production",
                "content": "Speech production integrates phonological planning and motor execution.",
                "page_number": 1,
            },
            {
                "title": "Semantic retrieval",
                "content": "Semantic retrieval supports lexical access and comprehension during conversation.",
                "page_number": 2,
            },
        ],
    )

    app = build_rag_graph(index)
    result = app.invoke({"question": "What supports speech production?"})

    assert "speech production" in result["context"].lower()
    assert "question" in result["answer"].lower() or "speech" in result["answer"].lower()
