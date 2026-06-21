"""Common types and LLM clients used across pattern examples."""

from __future__ import annotations

import json
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    role: str
    content: str


class LLMClient(ABC):
    @abstractmethod
    def complete(self, prompt: str, *, system: str | None = None) -> str:
        raise NotImplementedError


class MockLLMClient(LLMClient):
    """Deterministic stand-in for demos and tests without API keys."""

    def complete(self, prompt: str, *, system: str | None = None) -> str:
        text = prompt.lower()
        if "extract" in text and "specification" in text:
            return "CPU: 3.5 GHz octa-core, Memory: 16GB RAM, Storage: 1TB NVMe SSD"
        if "json" in text or "transform" in text:
            return json.dumps(
                {"cpu": "3.5 GHz octa-core", "memory": "16GB", "storage": "1TB NVMe SSD"},
                indent=2,
            )
        if "route" in text or "classify" in text:
            if "refund" in text:
                return "billing"
            if "bug" in text or "error" in text:
                return "engineering"
            return "general"
        if "critique" in text or "review" in text:
            return "Improve clarity and add concrete acceptance criteria."
        if "revise" in text or "rewrite" in text:
            return "Revised draft with clearer structure and acceptance criteria."
        if "plan" in text or "steps" in text:
            return "1. Gather requirements\n2. Design API\n3. Implement\n4. Test\n5. Deploy"
        if "summarize" in text:
            return "Summary: " + prompt[:120]
        if "search" in text or "retrieve" in text:
            return "Retrieved doc: Agents use tools, memory, and planning to achieve goals."
        if "calculator" in text or "pick a tool" in text:
            return '{"tool": "calculator", "args": {"expression": "12 * (4 + 3)"}}'
        if "score" in text or "evaluate" in text or "rate answer" in text:
            return "0.82"
        if "reason" in text or "think" in text:
            return "Thought: break problem into sub-goals.\nAction: call_search\nObservation: found 3 docs"
        return f"[mock response] {prompt[:160]}"


def get_llm() -> LLMClient:
    provider = os.getenv("AGENTIC_LLM_PROVIDER", "mock").lower()
    if provider == "openai":
        from agentic_patterns.providers import OpenAIClient

        return OpenAIClient()
    return MockLLMClient()


def extract_json(text: str) -> dict[str, Any]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in: {text!r}")
    return json.loads(match.group())
