"""Pattern 09: Learning and Adaptation — style profile from feedback."""

from __future__ import annotations

from dataclasses import dataclass, field

from agentic_patterns.common import get_llm


@dataclass
class StyleProfile:
    tone: str = "neutral"
    format_hint: str = "paragraph"
    notes: list[str] = field(default_factory=list)

    def apply_feedback(self, feedback: str) -> None:
        self.notes.append(feedback)
        llm = get_llm()
        updated = llm.complete(
            "Update writing style profile from feedback.\n"
            f"Current tone={self.tone}, format={self.format_hint}\n"
            f"Feedback: {feedback}\n"
            "Return JSON with tone and format_hint."
        )
        if "bullet" in updated.lower():
            self.format_hint = "bullets"
        if "formal" in updated.lower():
            self.tone = "formal"

    def render(self, topic: str) -> str:
        llm = get_llm()
        return llm.complete(
            f"Explain {topic}",
            system=f"Tone={self.tone}; format={self.format_hint}.",
        )


if __name__ == "__main__":
    profile = StyleProfile()
    print(profile.render("vector indexes"))
    profile.apply_feedback("Use bullet points and a formal tone.")
    print("\nUpdated profile:", profile.tone, profile.format_hint)
