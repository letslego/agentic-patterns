#!/usr/bin/env python3
"""Record a demo video of the agentic-patterns chat app."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://agentic-patterns-chat.fly.dev/"
OUT_DIR = Path(__file__).resolve().parents[1] / "docs"
OUTPUT_MP4 = OUT_DIR / "demo-chat-app.mp4"

QUESTIONS = [
    "What is prompt chaining?",
    "Show me code for pattern 03 parallelization",
    "How does reflection work in agentic systems?",
    "What's the difference between routing and planning?",
]


def wait_for_response(page, timeout_ms: int = 180_000) -> None:
    page.wait_for_function(
        """() => {
            const btn = document.getElementById('send-btn');
            if (btn && btn.disabled) return false;
            const msgs = document.querySelectorAll('.message.assistant:not(.welcome) .content');
            if (!msgs.length) return false;
            const text = msgs[msgs.length - 1].innerText.trim();
            return text.length > 20 && text !== '…';
        }""",
        timeout=timeout_ms,
    )


def collect_responses(page) -> list[dict[str, str]]:
    return page.evaluate(
        """() => {
            const msgs = [...document.querySelectorAll('.message.assistant:not(.welcome) .content')];
            return msgs.map(el => ({ text: el.innerText.slice(0, 500) }));
        }"""
    )


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, str]] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1400, "height": 900},
            record_video_dir=str(OUT_DIR),
            record_video_size={"width": 1400, "height": 900},
        )
        page = context.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_function(
            "() => !document.getElementById('status-line').textContent.includes('Loading')",
            timeout=120_000,
        )
        time.sleep(2)

        for question in QUESTIONS:
            page.fill("#input", question)
            page.click("#send-btn")
            wait_for_response(page)
            time.sleep(3)

        responses = collect_responses(page)
        for i, question in enumerate(QUESTIONS):
            snippet = responses[i]["text"] if i < len(responses) else ""
            results.append({"question": question, "response_preview": snippet})

        video_path = Path(page.video.path()) if page.video else None
        context.close()
        browser.close()

    if not video_path or not video_path.exists():
        print("ERROR: no video recorded", file=sys.stderr)
        return 1

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(OUTPUT_MP4),
        ],
        check=True,
        capture_output=True,
    )
    video_path.unlink(missing_ok=True)

    meta = {
        "url": URL,
        "output": str(OUTPUT_MP4),
        "questions": results,
    }
    meta_path = OUT_DIR / "demo-chat-app-meta.json"
    meta_path.write_text(json.dumps(meta, indent=2))

    print(json.dumps(meta, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
