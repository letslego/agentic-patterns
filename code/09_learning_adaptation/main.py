"""Pattern 09: Learning and Adaptation — update behavior from feedback."""

from __future__ import annotations

from dataclasses import dataclass, field

from agentic_patterns.common import get_llm


@dataclass
class AdaptiveAgent:
    system_prompt: str = "You are a concise helpful assistant."
    feedback_log: list[str] = field(default_factory=list)

    def respond(self, user_input: str) -> str:
        llm = get_llm()
        return llm.complete(user_input, system=self.system_prompt)

    def learn_from_feedback(self, feedback: str) -> None:
        self.feedback_log.append(feedback)
        llm = get_llm()
        self.system_prompt = llm.complete(
            "Update the system prompt using this feedback. Return prompt text only.\n"
            f"Current prompt:\n{self.system_prompt}\n\nFeedback:\n{feedback}"
        )


if __name__ == "__main__":
    agent = AdaptiveAgent()
    print(agent.respond("Explain prompt chaining in one sentence."))
    agent.learn_from_feedback("Prefer bullet points and include a code pointer.")
    print("\nUpdated system prompt:\n", agent.system_prompt)
