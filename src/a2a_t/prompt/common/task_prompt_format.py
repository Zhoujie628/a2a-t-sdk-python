from __future__ import annotations

from dataclasses import dataclass

from .models import PromptReference

_FRONT_MATTER_OPEN = "---\n"
_FRONT_MATTER_CLOSE = "\n---\n"


class TaskPromptFormatError(ValueError):
    """Describe a task prompt front-matter formatting error."""

    def __init__(self, message: str, *, field: str | None = None) -> None:
        super().__init__(message)
        self.field = field


@dataclass(slots=True)
class TaskPromptMetadata:
    """Represent the front-matter metadata embedded in task prompts."""

    scenario_code: str
    language: str
    description: str

    def to_prompt_reference(self) -> PromptReference:
        """Convert prompt metadata into the shared prompt reference model."""
        return PromptReference(
            scenario_code=self.scenario_code,
            language=self.language,
        )


def format_task_prompt(*, body: str, metadata: TaskPromptMetadata) -> str:
    """Embed task prompt metadata as front matter above the rendered body."""
    return (
        _FRONT_MATTER_OPEN
        + f"scenario_code: {metadata.scenario_code}\n"
        + f"language: {metadata.language}\n"
        + f"description: {metadata.description}\n"
        + "---\n\n"
        + f"{body}"
    )


def parse_task_prompt_metadata(prompt_text: str) -> TaskPromptMetadata:
    """Parse and validate task prompt front matter into structured metadata."""
    if not prompt_text.startswith(_FRONT_MATTER_OPEN):
        raise TaskPromptFormatError("Task prompt must start with front matter.")

    closing_index = prompt_text.find(_FRONT_MATTER_CLOSE, len(_FRONT_MATTER_OPEN))
    if closing_index == -1:
        raise TaskPromptFormatError("Task prompt front matter is not closed.")

    header = prompt_text[len(_FRONT_MATTER_OPEN) : closing_index]
    metadata: dict[str, str] = {}

    for line in header.splitlines():
        # Preserve a minimal parser here so format violations surface with field-specific errors.
        if not line.strip():
            continue
        if ":" not in line:
            raise TaskPromptFormatError(f"Invalid front matter line: {line}")

        key, value = line.split(":", 1)
        normalized_key = key.strip()
        normalized_value = value.strip()
        if not normalized_key:
            raise TaskPromptFormatError(f"Invalid front matter line: {line}")
        metadata[normalized_key] = normalized_value

    scenario_code = _require_metadata_field(metadata, "scenario_code")
    language = _require_metadata_field(metadata, "language")
    description = _require_metadata_field(metadata, "description")

    return TaskPromptMetadata(
        scenario_code=scenario_code,
        language=language,
        description=description,
    )


def _require_metadata_field(metadata: dict[str, str], field: str) -> str:
    """Return a required metadata field or raise a field-specific format error."""
    value = metadata.get(field)
    if value is None or not value.strip():
        raise TaskPromptFormatError(
            f"Task prompt is missing required field: {field}.",
            field=field,
        )
    return value
