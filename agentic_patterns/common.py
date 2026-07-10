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

        # Pattern 01 — prompt chaining (topic → outline → expand → json)
        if "key points for explaining" in text:
            return "1. Decompose tasks\n2. Pass outputs forward\n3. Validate each stage"
        if "expand each point" in text:
            return (
                "Decompose complex work into single-purpose steps.\n"
                "Each stage consumes prior output as context.\n"
                "Validate intermediate results before continuing."
            )
        if "convert to json" in text and "points array" in text:
            return json.dumps(
                {
                    "topic": "prompt chaining",
                    "points": ["decompose", "chain context", "validate stages"],
                },
                indent=2,
            )

        # Pattern 01 legacy — recipe pipeline (adapter demos)
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

        # Pattern 02 — routing (pattern questions + legacy helpdesk)
        if "choose one route label" in text or "route label:" in text:
            msg_part = text
            if "message:" in text:
                msg_part = text.split("message:", 1)[1].split("choose", 1)[0].lower()
            if "code" in msg_part or "show me" in msg_part:
                return "code_example"
            if " vs " in msg_part or "compare" in msg_part or "when to use" in msg_part:
                return "pattern_comparison"
            if "password" in msg_part or "locked out" in msg_part:
                return "password_reset"
            if "install" in msg_part or "software" in msg_part or "figma" in msg_part:
                return "software_install"
            return "concept_explanation"

        # Pattern 04 — reflection (explanation loop + legacy press release)
        if "draft a one-paragraph explanation" in text:
            return "Reflection lets an agent critique and revise its own draft output."
        if "critique this explanation" in text:
            return "Add a concrete example and mention iteration limits."
        if "revise using feedback" in text:
            return (
                "Reflection runs draft → critique → revise loops so agents self-correct "
                "before returning a final answer."
            )
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

        # Pattern 07 — multi-agent crew (researcher/writer/reviewer + legacy incident)
        if "you are researcher" in text:
            return "Parallelization uses asyncio.gather to run independent LLM calls concurrently."
        if "you are writer" in text:
            return "Draft: Pattern 03 fans out per-item prompts, then merges summaries."
        if "you are reviewer" in text:
            return "Looks accurate; mention concurrency limits and error handling."
        if "role: sre" in text:
            return "Detected elevated 5xx on checkout API."
        if "role: comms" in text:
            return "Draft status page update for checkout degradation."
        if "role: fix" in text:
            return "Rollback deploy v842 and scale pods +2."

        # Pattern 03 — parallelization
        if "summarize this text" in text:
            return "One-line summary of an agentic design pattern concept."
        if "merge these summaries" in text:
            return (
                "Chaining, routing, and RAG are foundational patterns: "
                "sequential stages, specialized dispatch, and retrieval-grounded generation."
            )
        if "summarize" in text and "survey" in text:
            return "Theme: onboarding friction (n=12 mentions)."
        if "merge themes" in text:
            return "Users report onboarding friction and unclear billing emails."

        if "retrieved documents" in text or "context:\n" in text:
            return (
                "Based on the retrieved documents: RAG embeds the query and chunks, "
                "ranks them by cosine similarity, and grounds the LLM answer in the top-k hits."
            )

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
    if provider == "openrouter":
        from agentic_patterns.providers import OpenRouterClient

        return OpenRouterClient()
    if provider in ("nemotron", "nvidia"):
        from agentic_patterns.providers import NemotronClient

        return NemotronClient()
    return MockLLMClient()


def extract_json(text: str) -> dict[str, Any]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in: {text!r}")
    return json.loads(match.group())
