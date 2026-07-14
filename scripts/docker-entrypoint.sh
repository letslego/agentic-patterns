#!/bin/sh
set -e

# Seed or refresh the persistent volume from the image-baked index.
python - <<'PY'
import shutil
import sqlite3
from pathlib import Path

from chat.rag import get_store

BAKED_DIR = Path("/app/data/chat")
BAKED_DB = BAKED_DIR / "rag.sqlite"


def chunk_count(db_path: Path) -> int:
    if not db_path.is_file():
        return 0
    conn = sqlite3.connect(db_path)
    try:
        return int(conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0])
    finally:
        conn.close()


def copy_baked_index(store) -> int:
    print(f"Refreshing volume from baked index at {BAKED_DIR}")
    db_path = store.db_path
    store.close()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    for item in BAKED_DIR.iterdir():
        dest = db_path.parent / item.name
        if item.is_file():
            shutil.copy2(item, dest)
        elif item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
    count = chunk_count(db_path)
    print(f"Volume now has {count} chunks at {db_path}")
    return count


store = get_store()
volume_count = store.count()
baked_count = chunk_count(BAKED_DB)

if BAKED_DB.is_file():
    copy_baked_index(store)
    try:
        from chat import redis_cache

        redis_cache.clear_cache()
        print("Cleared Redis cache so the refreshed SQLite index can resync")
    except Exception as exc:  # noqa: BLE001 - startup best-effort
        print(f"Redis clear skipped: {exc}")
    raise SystemExit(0)

if volume_count > 0:
    print(f"RAG store ready: {volume_count} chunks at {store.db_path}")
    raise SystemExit(0)

print("No baked index found; running ingest…")
from chat.ingest import ingest

count = ingest()
print(f"Ingested {count} chunks into {store.db_path}")
PY

# Start serving immediately; embedder + Redis sync happen in background via FastAPI startup.
exec uvicorn chat.main:app --host 0.0.0.0 --port "${PORT:-8080}"
