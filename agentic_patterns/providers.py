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


class OpenRouterClient(LLMClient):
    """OpenRouter chat completions via OpenAI-compatible API."""

    def __init__(self, model: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install openai: pip install openai") from exc

        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("Set OPENROUTER_API_KEY to use OpenRouter provider")
        base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self._model = model or os.getenv("OPENROUTER_MODEL", "nvidia/llama-3.1-nemotron-70b-instruct")

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = self._client.chat.completions.create(model=self._model, messages=messages, temperature=0.3)
        return response.choices[0].message.content or ""


class NemotronClient(LLMClient):
    """NVIDIA Nemotron via NIM OpenAI-compatible API."""

    def __init__(self, model: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install openai: pip install openai") from exc

        api_key = os.environ.get("NVIDIA_API_KEY")
        if not api_key:
            raise RuntimeError("Set NVIDIA_API_KEY to use Nemotron provider")
        base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        self._client = OpenAI(api_key=api_key, base_url=base_url)
        self._model = model or os.getenv("NEMOTRON_MODEL", "nvidia/llama-3.1-nemotron-70b-instruct")

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        response = self._client.chat.completions.create(model=self._model, messages=messages, temperature=0.3)
        return response.choices[0].message.content or ""
