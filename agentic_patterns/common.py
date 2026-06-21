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

        # Pattern 01 — recipe pipeline (not hardware specs)
        if "ingredient" in text and "extract" in text:
            return "2 cups flour, 1 tsp yeast, 1 cup water, 1 tbsp olive oil"
        if "normalize" in text or "canonical units" in text:
            return "flour: 480g, yeast: 5g, water: 240ml, olive_oil: 15ml"
        if "shopping list" in text or "grocery json" in text:
            return json.dumps(
                {
                    "items": [
                        {"name": "bread flour", "quantity": "480g"},
                        {"name": "instant yeast", "quantity": "5g"},
                        {"name": "water", "quantity": "240ml"},
                        {"name": "olive oil", "quantity": "15ml"},
                    ]
                },
                indent=2,
            )

        # Pattern 02 — IT helpdesk routing (not travel booking)
        if "choose one route label" in text or "route label:" in text:
            msg_part = text
            if "message:" in text:
                msg_part = text.split("message:", 1)[1].split("choose", 1)[0].lower()
            if "password" in msg_part or "locked out" in msg_part:
                return "password_reset"
            if "install" in msg_part or "software" in msg_part or "figma" in msg_part:
                return "software_install"
            return "general_support"

        # Pattern 04 — press release reflection
        if "press release" in text and "draft" in text:
            return "Acme Labs announces Orion SDK for edge inference."
        if "editorial review" in text or "editor feedback" in text:
            return "Add customer quote and ship date."
        if "revise release" in text:
            return "Acme Labs announces Orion SDK; beta ships Q3 with pilot quote."

        # Pattern 05 — travel toolkit selection
        if "select tool" in text or "tool manifest" in text:
            if "timezone" in text:
                return '{"tool":"timezone_lookup","args":{"city":"Tokyo"}}'
            if "currency" in text:
                return '{"tool":"currency_convert","args":{"amount":100,"from":"USD","to":"JPY"}}'
            return '{"tool":"timezone_lookup","args":{"city":"Tokyo"}}'

        # Pattern 06 — data migration plan
        if "migration plan" in text or "numbered milestones" in text:
            return "1. Inventory schemas\n2. Build ETL\n3. Shadow write\n4. Cutover\n5. Validate"

        # Pattern 07 — incident response crew
        if "role: sre" in text:
            return "Detected elevated 5xx on checkout API."
        if "role: comms" in text:
            return "Draft status page update for checkout degradation."
        if "role: fix" in text:
            return "Rollback deploy v842 and scale pods +2."

        if "summarize" in text and "survey" in text:
            return "Theme: onboarding friction (n=12 mentions)."

        if "merge themes" in text:
            return "Users report onboarding friction and unclear billing emails."

        if "retrieve" in text and "policy" in text:
            return "[doc-17] Remote work policy allows 2 WFH days/week."

        if "score" in text or "rate answer" in text:
            return "0.78"

        if "hypothesis" in text:
            return "1. Email campaign caused traffic spike\n2. Deploy regression\n3. Seasonality"

        if "confidence" in text:
            return "0.71"

        if "reasoning trace" in text or "thought/action" in text:
            return "Thought: compare routing vs rules.\nFinal Answer: use hybrid router."

        return f"[mock response] {prompt[:140]}"


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
