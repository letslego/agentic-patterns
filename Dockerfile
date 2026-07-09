# syntax=docker/dockerfile:1

FROM python:3.11-slim AS builder

WORKDIR /app
COPY pyproject.toml README.md ./
COPY agentic_patterns ./agentic_patterns
COPY chat ./chat
COPY docs ./docs
COPY code ./code

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ".[chat]" && \
    pip install --no-cache-dir sentence-transformers

# Pre-build RAG index at image build time (uses local embeddings if no OPENAI_API_KEY)
RUN python -m chat.ingest

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

ENV PORT=8080
ENV CHAT_DATA_DIR=/data/chat

EXPOSE 8080

CMD ["uvicorn", "chat.main:app", "--host", "0.0.0.0", "--port", "8080"]
