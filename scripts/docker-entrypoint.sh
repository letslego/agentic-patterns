#!/bin/sh
set -e

# Seed the persistent volume from the image-baked index, or ingest if missing.
python - <<'PY'
import shutil
from pathlib import Path

from chat.rag import get_store

store = get_store()
if store.count() > 0:
    print(f"RAG store ready: {store.count()} chunks at {store.db_path}")
    raise SystemExit(0)

baked = Path("/app/data/chat")
if baked.joinpath("rag.sqlite").is_file():
    print(f"Seeding empty volume from baked index at {baked}")
    store.db_path.parent.mkdir(parents=True, exist_ok=True)
    for item in baked.iterdir():
        dest = store.db_path.parent / item.name
        if item.is_file():
            shutil.copy2(item, dest)
        elif item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
    store.close()
    store = get_store()
    if store.count() > 0:
        print(f"Seeded {store.count()} chunks into {store.db_path}")
        raise SystemExit(0)

print("No baked index found; running ingest…")
from chat.ingest import ingest

count = ingest()
print(f"Ingested {count} chunks into {store.db_path}")
PY

# Start serving immediately; embedder + Redis sync happen in background via FastAPI startup.
exec uvicorn chat.main:app --host 0.0.0.0 --port "${PORT:-8080}"
