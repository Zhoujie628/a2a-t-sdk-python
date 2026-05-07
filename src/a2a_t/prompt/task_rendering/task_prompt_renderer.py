from __future__ import annotations

from .exceptions import TaskPromptRenderError


class TaskPromptRenderer:
    """Render task prompt templates into plain prompt bodies."""

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
        """Render a processed task prompt body from a template and extracted slots."""
        normalized_slots = {key: "" if value is None else value for key, value in slots.items()}
        try:
            return template_text.format_map(normalized_slots)
        except KeyError as error:
            raise TaskPromptRenderError(f"Template references unknown slot: {error.args[0]}") from error
        except ValueError as error:
            raise TaskPromptRenderError(str(error)) from error
