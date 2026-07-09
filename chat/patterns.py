"""Metadata for all 21 agentic design patterns."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Pattern:
    number: int
    slug: str
    name: str
    code_path: str
    doc_path: str


PATTERNS: list[Pattern] = [
    Pattern(1, "prompt_chaining", "Prompt Chaining", "code/01_prompt_chaining/main.py", "docs/part-1-foundational/01-prompt-chaining.md"),
    Pattern(2, "routing", "Routing", "code/02_routing/main.py", "docs/part-1-foundational/02-routing.md"),
    Pattern(3, "parallelization", "Parallelization", "code/03_parallelization/main.py", "docs/part-1-foundational/03-parallelization.md"),
    Pattern(4, "reflection", "Reflection", "code/04_reflection/main.py", "docs/part-1-foundational/04-reflection.md"),
    Pattern(5, "tool_use", "Tool Use", "code/05_tool_use/main.py", "docs/part-1-foundational/05-tool-use.md"),
    Pattern(6, "planning", "Planning", "code/06_planning/main.py", "docs/part-1-foundational/06-planning.md"),
    Pattern(7, "multi_agent", "Multi-Agent", "code/07_multi_agent/main.py", "docs/part-1-foundational/07-multi-agent.md"),
    Pattern(8, "memory_management", "Memory Management", "code/08_memory_management/main.py", "docs/part-2-advanced/08-memory-management.md"),
    Pattern(9, "learning_adaptation", "Learning & Adaptation", "code/09_learning_adaptation/main.py", "docs/part-2-advanced/09-learning-adaptation.md"),
    Pattern(10, "mcp", "MCP", "code/10_mcp/main.py", "docs/part-2-advanced/10-mcp.md"),
    Pattern(11, "goal_monitoring", "Goal Setting & Monitoring", "code/11_goal_monitoring/main.py", "docs/part-2-advanced/11-goal-monitoring.md"),
    Pattern(12, "exception_handling", "Exception Handling", "code/12_exception_handling/main.py", "docs/part-3-production/12-exception-handling.md"),
    Pattern(13, "human_in_the_loop", "Human-in-the-Loop", "code/13_human_in_the_loop/main.py", "docs/part-3-production/13-human-in-the-loop.md"),
    Pattern(14, "rag", "RAG", "code/14_rag/main.py", "docs/part-3-production/14-rag.md"),
    Pattern(15, "inter_agent_communication", "Inter-Agent Communication", "code/15_inter_agent_communication/main.py", "docs/part-4-multi-agent/15-inter-agent-communication.md"),
    Pattern(16, "resource_optimization", "Resource-Aware Optimization", "code/16_resource_optimization/main.py", "docs/part-4-multi-agent/16-resource-optimization.md"),
    Pattern(17, "reasoning", "Reasoning Techniques", "code/17_reasoning/main.py", "docs/part-4-multi-agent/17-reasoning.md"),
    Pattern(18, "guardrails", "Guardrails & Safety", "code/18_guardrails/main.py", "docs/part-4-multi-agent/18-guardrails.md"),
    Pattern(19, "evaluation", "Evaluation & Monitoring", "code/19_evaluation/main.py", "docs/part-4-multi-agent/19-evaluation.md"),
    Pattern(20, "prioritization", "Prioritization", "code/20_prioritization/main.py", "docs/part-4-multi-agent/20-prioritization.md"),
    Pattern(21, "exploration", "Exploration & Discovery", "code/21_exploration/main.py", "docs/part-4-multi-agent/21-exploration.md"),
]


def pattern_for_path(path: str) -> Pattern | None:
    normalized = path.replace("\\", "/")
    for pattern in PATTERNS:
        if pattern.code_path in normalized or pattern.doc_path in normalized:
            return pattern
        folder = f"code/{pattern.number:02d}_{pattern.slug}"
        if folder in normalized:
            return pattern
    return None


def patterns_payload() -> list[dict]:
    return [
        {
            "number": p.number,
            "slug": p.slug,
            "name": p.name,
            "code_path": p.code_path,
            "doc_path": p.doc_path,
        }
        for p in PATTERNS
    ]
