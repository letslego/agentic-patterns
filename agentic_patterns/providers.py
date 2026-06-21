"""Optional real LLM provider adapters."""

from __future__ import annotations

import os

from agentic_patterns.common import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self, model: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install openai: pip install openai") from exc

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Set OPENAI_API_KEY to use OpenAI provider")
        self._client = OpenAI(api_key=api_key)
        self._model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = self._client.chat.completions.create(model=self._model, messages=messages)
        return response.choices[0].message.content or ""
