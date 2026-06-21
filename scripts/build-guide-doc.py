#!/usr/bin/env python3
"""Concatenate chapter markdown into a single guide document."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docs"
PARTS = [
    ROOT / "index.md",
    ROOT / "introduction.md",
    *sorted((ROOT / "part-1-foundational").glob("*.md")),
    *sorted((ROOT / "part-2-advanced").glob("*.md")),
    *sorted((ROOT / "part-3-production").glob("*.md")),
    *sorted((ROOT / "part-4-multi-agent").glob("*.md")),
    ROOT / "appendix" / "frameworks.md",
    ROOT / "appendix" / "framework-adapters.md",
]

out = ROOT.parent / "AGENTIC-PATTERNS-GUIDE.md"
chunks = []
for path in PARTS:
    chunks.append(f"<!-- source: {path.relative_to(ROOT.parent)} -->\n")
    chunks.append(path.read_text())
    chunks.append("\n\n---\n\n")
out.write_text("".join(chunks))
print(f"Wrote {out}")
