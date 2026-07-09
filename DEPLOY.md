# Deploying Agentic Patterns Chat on Fly.io

The chat app uses **OpenRouter** (preferred) for chat completions and a SQLite-backed vector store for RAG.

## Architecture

```
Browser → FastAPI (chat/main.py)
            ├─ GET  /api/health, /api/patterns
            ├─ POST /api/chat  (RAG + OpenRouter)
            └─ static UI (chat/static/)
         SQLite vector store (/data/chat on Fly volume)
         Embeddings: OpenAI text-embedding-3-small OR local sentence-transformers
```

## Prerequisites

- [Fly CLI](https://fly.io/docs/hands-on/install-flyctl/) installed and authenticated
- OpenRouter API key ([openrouter.ai](https://openrouter.ai))
- Optional: OpenAI API key for higher-quality embeddings at ingest time

## First-time setup

```bash
# From repo root
fly apps create agentic-patterns-chat   # or pick another name and update fly.toml

# Persistent volume for RAG database (re-ingest on deploy updates the baked index)
fly volumes create chat_data --region iad --size 1

# Required: OpenRouter chat completions
fly secrets set OPENROUTER_API_KEY=sk-or-...

# Optional: better embeddings (otherwise image uses local sentence-transformers)
fly secrets set OPENAI_API_KEY=sk-...

# Optional overrides
fly secrets set OPENROUTER_MODEL=nvidia/llama-3.1-nemotron-70b-instruct
```

## Deploy

```bash
fly deploy
```

Open the app:

```bash
fly open
```

## Environment variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `OPENROUTER_API_KEY` | Yes (prod) | — | Chat completions via OpenRouter |
| `OPENROUTER_MODEL` | No | `nvidia/llama-3.1-nemotron-70b-instruct` | Chat model on OpenRouter |
| `OPENROUTER_BASE_URL` | No | `https://openrouter.ai/api/v1` | OpenRouter OpenAI-compatible endpoint |
| `NVIDIA_API_KEY` | No | — | Fallback: Nemotron via NVIDIA NIM (if no OpenRouter key) |
| `NEMOTRON_MODEL` | No | `nvidia/llama-3.1-nemotron-70b-instruct` | NVIDIA fallback chat model |
| `NVIDIA_BASE_URL` | No | `https://integrate.api.nvidia.com/v1` | NVIDIA NIM endpoint |
| `OPENAI_API_KEY` | No | — | Embeddings (`text-embedding-3-small`) |
| `OPENAI_EMBEDDING_MODEL` | No | `text-embedding-3-small` | Embedding model name |
| `CHAT_DATA_DIR` | No | `data/chat` (local) / `/data/chat` (Fly) | Vector store directory |
| `PORT` | No | `8080` | HTTP port |

Without `OPENROUTER_API_KEY` or `NVIDIA_API_KEY`, the API runs in **mock mode** (returns retrieved chunks + template text).

## Re-ingest on the volume

After SSH or a one-off machine:

```bash
fly ssh console
python -m chat.ingest
```

Or run ingest during Docker build (default) so each deploy ships an up-to-date index.

## Health check

```bash
curl https://agentic-patterns-chat.fly.dev/api/health
```

Expected:

```json
{
  "status": "ok",
  "chunks": 120,
  "llm_provider": "openrouter",
  "llm_model": "nvidia/llama-3.1-nemotron-70b-instruct",
  "mock_mode": false
}
```

## Local Docker smoke test

```bash
docker build -t agentic-patterns-chat .
docker run --rm -p 8080:8080 -e OPENROUTER_API_KEY=$OPENROUTER_API_KEY agentic-patterns-chat
curl http://localhost:8080/api/health
```
