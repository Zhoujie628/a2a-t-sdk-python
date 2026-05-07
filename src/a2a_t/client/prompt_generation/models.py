from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(slots=True)
class NormalizedInput:
    """Carry the normalized text and the input shape detected upstream."""

    input_kind: str
    normalized_input: str


@dataclass(slots=True)
class PromptGenerationFailure:
    """Describe why prompt generation stopped before producing a valid result."""

    code: str
    message: str
    stage: str | None

    def to_dict(self) -> dict[str, object]:
        """Serialize failure details into the public response shape."""
        return asdict(self)


@dataclass(slots=True)
class PromptGenerationResult:
    """Represent the final outcome of prompt generation."""

    success: bool
    prompt_text: str | None
    failure: PromptGenerationFailure | None

    def to_dict(self) -> dict[str, object]:
        """Serialize the generation result into the public response shape."""
        return {
            "success": self.success,
            "prompt_text": self.prompt_text,
            "failure": self.failure.to_dict() if self.failure is not None else None,
        }
