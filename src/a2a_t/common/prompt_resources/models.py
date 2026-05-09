from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ScenarioDefinition:
    """Describe one scenario candidate available to scenario recognition."""

    scenario_code: str
    scenario_name: str
    description: str
    example: str


@dataclass(slots=True)
class PromptMessages:
    """Bundle the system and user prompts used for one analysis action."""

    system_prompt: str
    user_prompt: str


@dataclass(slots=True)
class SlotRange:
    """Describe the optional numeric range constraint of a slot."""

    min: float | int | None
    max: float | int | None


@dataclass(slots=True)
class SlotDefinition:
    """Describe one slot expected by a scenario template."""

    name: str
    required: bool
    description: str
    example: str
    value_constraint: str
    type: str | None
    allowed_values: list[object] | None
    range: SlotRange | None
    pattern: str | None


@dataclass(slots=True)
class SlotSchema:
    """Describe all slots defined for one scenario resource."""

    scenario_code: str
    slots: list[SlotDefinition]
