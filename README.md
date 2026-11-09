# Neurocognitive Speech RAG Scaffold

This project creates the first structure for a retrieval-augmented generation (RAG) workflow focused on neurocognitive speech topics.

## Included structure

- `PageIndex`: typed index for domain pages
- `NeurocognitiveSpeechRAG`: retrieval layer for a specific knowledge chain
- `NEUROCOGNITIVE_SPEECH_CONTEXT`: domain content seed for speech and language research topics

## Quick example

```python
from challenge02_grupo10 import build_rag_chain
from challenge02_grupo10.data import NEUROCOGNITIVE_SPEECH_CONTEXT

rag = build_rag_chain("speech neurocognition", NEUROCOGNITIVE_SPEECH_CONTEXT)
print(rag.build_context("What supports speech production?"))
```

This version is intentionally lightweight so you can expand it with embeddings, vector stores, and a LangChain prompt chain later.
