from __future__ import annotations

from dataclasses import dataclass

from a2a_t.prompt.validation.models import SlotValidationError


@dataclass(slots=True)
class ScenarioRecognitionResult:
    """Represent the normalized result returned by scenario recognition."""

    matched: bool
    scenario_code: str | None
    error_message: str | None


@dataclass(slots=True)
class SlotExtractionResult:
    """Represent the normalized result returned by slot extraction."""

    slots: dict[str, str | None]
    slot_errors: list[SlotValidationError]
