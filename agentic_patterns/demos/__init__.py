"""Shared demo workflows used by pattern examples and framework adapters."""

from agentic_patterns.demos.helpdesk import build_helpdesk_router
from agentic_patterns.demos.press_release import (
    draft_release,
    editorial_review,
    revise_release,
)
from agentic_patterns.demos.recipe_pipeline import build_recipe_pipeline

__all__ = [
    "build_recipe_pipeline",
    "build_helpdesk_router",
    "draft_release",
    "editorial_review",
    "revise_release",
]
