# Chapter 14: Knowledge Retrieval (RAG)

## Pattern overview

Retrieve relevant documents, inject them into context, then generate grounded answers.

![RAG diagram](../images/rag.svg)

## Reference implementation

**Source:** [`code/14_rag/main.py`](https://github.com/letslego/agentic-patterns/blob/main/code/14_rag/main.py)

Keyword retriever over an in-memory corpus plus grounded generation.

### Run locally

```bash
python code/14_rag/main.py
```

## Key takeaways

- Chunk and embed thoughtfully.
- Cite sources in answers.
- Monitor retrieval precision.
