"""Chat completion via OpenRouter (preferred) or NVIDIA Nemotron with mock fallback."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Iterator

DEFAULT_OPENROUTER_MODEL = "nvidia/llama-3.1-nemotron-70b-instruct"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

DEFAULT_NEMOTRON_MODEL = "nvidia/llama-3.1-nemotron-70b-instruct"
DEFAULT_NIM_BASE_URL = "https://integrate.api.nvidia.com/v1"


class ChatLLM(ABC):
    @abstractmethod
    def chat(self, messages: list[dict[str, str]], *, stream: bool = False) -> str | Iterator[str]:
        raise NotImplementedError

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def provider(self) -> str:
        raise NotImplementedError


class OpenRouterClient(ChatLLM):
    """OpenRouter chat completions via OpenAI-compatible API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install openai: pip install openai") from exc

        key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("Set OPENROUTER_API_KEY to use OpenRouter")
        self._client = OpenAI(
            api_key=key,
            base_url=base_url or os.getenv("OPENROUTER_BASE_URL", DEFAULT_OPENROUTER_BASE_URL),
        )
        self._model = model or os.getenv("OPENROUTER_MODEL", DEFAULT_OPENROUTER_MODEL)

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider(self) -> str:
        return "openrouter"

    def chat(self, messages: list[dict[str, str]], *, stream: bool = False) -> str | Iterator[str]:
        if stream:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                stream=True,
                temperature=0.3,
            )

            def _iter() -> Iterator[str]:
                for chunk in response:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta

            return _iter()

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0].message.content or ""


class NemotronClient(ChatLLM):
    """NVIDIA Nemotron via NIM OpenAI-compatible API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
    ) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install openai: pip install openai") from exc

        key = api_key or os.environ.get("NVIDIA_API_KEY")
        if not key:
            raise RuntimeError("Set NVIDIA_API_KEY to use Nemotron")
        self._client = OpenAI(api_key=key, base_url=base_url or os.getenv("NVIDIA_BASE_URL", DEFAULT_NIM_BASE_URL))
        self._model = model or os.getenv("NEMOTRON_MODEL", DEFAULT_NEMOTRON_MODEL)

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider(self) -> str:
        return "nemotron"

    def chat(self, messages: list[dict[str, str]], *, stream: bool = False) -> str | Iterator[str]:
        if stream:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                stream=True,
                temperature=0.3,
            )

            def _iter() -> Iterator[str]:
                for chunk in response:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta

            return _iter()

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0].message.content or ""


class MockChatLLM(ChatLLM):
    """Template responses using retrieved context when no API key is set."""

    @property
    def model_name(self) -> str:
        return "mock"

    @property
    def provider(self) -> str:
        return "mock"

    def chat(self, messages: list[dict[str, str]], *, stream: bool = False) -> str | Iterator[str]:
        user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        context = next((m["content"] for m in messages if m["role"] == "system" and "Retrieved context" in m["content"]), "")

        answer = (
            "**Mock mode** — set `OPENROUTER_API_KEY` (or `NVIDIA_API_KEY`) for live LLM responses.\n\n"
            f"**Your question:** {user_msg}\n\n"
            "Here is relevant material from the agentic-patterns repository:\n\n"
        )
        if context:
            snippet = context[:2000] + ("…" if len(context) > 2000 else "")
            answer += snippet
        else:
            answer += "_No retrieved context. Run `python -m chat.ingest` to build the vector store._"

        answer += (
            "\n\n**Tip:** Each pattern has a runnable example at `code/NN_name/main.py` "
            "and a guide chapter under `docs/`."
        )

        if stream:

            def _iter() -> Iterator[str]:
                yield answer

            return _iter()
        return answer


def get_chat_llm() -> ChatLLM:
    if os.environ.get("OPENROUTER_API_KEY"):
        return OpenRouterClient()
    if os.environ.get("NVIDIA_API_KEY"):
        return NemotronClient()
    return MockChatLLM()
