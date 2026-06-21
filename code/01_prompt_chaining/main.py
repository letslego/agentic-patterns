"""Pattern 01: Prompt Chaining — sequential LLM pipeline."""

from __future__ import annotations

from agentic_patterns.common import get_llm


def extract_specs(text: str) -> str:
    llm = get_llm()
    return llm.complete(
        f"Extract the technical specifications from the following text:\n\n{text}",
        system="You extract hardware specs only.",
    )


def to_json(specs: str) -> str:
    llm = get_llm()
    return llm.complete(
        "Transform the following specifications into JSON with keys cpu, memory, storage:\n\n"
        + specs
    )


def run_pipeline(text: str) -> str:
    specs = extract_specs(text)
    return to_json(specs)


if __name__ == "__main__":
    sample = (
        "The new laptop features a 3.5 GHz octa-core processor, 16GB RAM, "
        "and a 1TB NVMe SSD."
    )
    print(run_pipeline(sample))
