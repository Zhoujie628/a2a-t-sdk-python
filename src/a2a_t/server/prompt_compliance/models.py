from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PromptComplianceResult:
    """Unified compliance execution result."""

    success: bool
    failure: dict[str, str] | None = None


@dataclass(frozen=True)
class SemanticValidationError:
    slot_name: str
    code: str
    message: str


@dataclass(frozen=True)
class SemanticValidationResult:
    passed: bool
    errors: list[SemanticValidationError]
