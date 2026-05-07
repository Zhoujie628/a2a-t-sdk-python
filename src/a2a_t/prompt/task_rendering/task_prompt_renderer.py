from __future__ import annotations

from collections import UserDict

from a2a_t.prompt.common.task_prompt_format import TaskPromptMetadata, format_task_prompt

from .exceptions import TaskPromptRenderError


class _StrictSlotMap(UserDict[str, str]):
    def __missing__(self, key: str) -> str:
        """Translate missing template keys into the renderer's domain error."""
        raise TaskPromptRenderError(f"Template references unknown slot: {key}")


class TaskPromptRenderer:
    """Render task prompt templates and attach the required front matter."""

    def render(
        self,
        *,
        template_text: str,
        slots: dict[str, str | None],
        scenario_code: str,
        language: str,
        version: str,
        description: str,
    ) -> str:
        """Render a processed task prompt from a template and extracted slots."""
        # Normalize missing optional slot values to empty strings so template rendering stays deterministic.
        normalized_slots = _StrictSlotMap({key: "" if value is None else value for key, value in slots.items()})
        try:
            body = template_text.format_map(normalized_slots)
        except KeyError as error:
            raise TaskPromptRenderError(f"Template references unknown slot: {error.args[0]}") from error

        return format_task_prompt(
            body=body,
            metadata=TaskPromptMetadata(
                scenario_code=scenario_code,
                language=language,
                version=version,
                description=description,
            ),
        )
