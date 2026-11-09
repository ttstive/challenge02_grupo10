from challenge02_grupo10.indexing.page_index import PageIndex


def test_page_index_builds_documents_for_speech_neurocognition():
    index = PageIndex.from_topic_set(
        "speech neurocognition",
        [
            {
                "title": "Speech production",
                "content": "Speech production integrates phonological planning and motor execution.",
                "page_number": 1,
            },
            {
                "title": "Language semantics",
                "content": "Semantic processing supports lexical retrieval and meaning construction.",
                "page_number": 2,
            },
        ],
    )

    assert len(index.pages) == 2
    assert index.pages[0].title == "Speech production"
    assert "phonological" in index.to_documents()[0].page_content
