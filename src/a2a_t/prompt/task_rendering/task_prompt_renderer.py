from __future__ import annotations

import re

from .exceptions import TaskPromptRenderError


_DOUBLE_BRACED_SLOT_PATTERN = re.compile(r"\{\{([^{}]+)\}\}")
_SECTION_HEADING_PATTERN = re.compile(r"^\s*##+\s+\S")
_SECTION_SLOT_ONLY_LINE_PATTERN = re.compile(
    r"^\s*(\{[^{}\n]+\})\s*(?:（[^）]*）|\([^)]*\))?\s*$"
)


class TaskPromptRenderer:
    """Render task prompt templates into plain prompt bodies."""

    def render(
        self,
        *,
        template_text: str,
        slots: dict[str, str | None],
        scenario_code: str,
        language: str,
        description: str,
    ) -> str:
        """Render a processed task prompt body from a template and extracted slots."""
        normalized_slots = {key: "" if value is None else value for key, value in slots.items()}
        normalized_template_text = _DOUBLE_BRACED_SLOT_PATTERN.sub(r"{\1}", template_text)
        normalized_template_text = _collapse_slot_only_sections(normalized_template_text)
        try:
            return normalized_template_text.format_map(normalized_slots)
        except KeyError as error:
            raise TaskPromptRenderError(f"Template references unknown slot: {error.args[0]}") from error
        except ValueError as error:
            raise TaskPromptRenderError(str(error)) from error


def _collapse_slot_only_sections(template_text: str) -> str:
    """Reduce markdown sections with a standalone slot line to only that rendered slot value."""
    lines = template_text.splitlines(keepends=True)
    if not lines:
        return template_text

    section_start_indexes = [
        index for index, line in enumerate(lines) if _SECTION_HEADING_PATTERN.match(line)
    ]
    if not section_start_indexes:
        return template_text

    transformed_sections: list[str] = []
    for position, start_index in enumerate(section_start_indexes):
        end_index = (
            section_start_indexes[position + 1]
            if position + 1 < len(section_start_indexes)
            else len(lines)
        )
        section_lines = lines[start_index:end_index]
        transformed_sections.append(
            _transform_section_lines(
                section_lines=section_lines,
                has_following_section=position + 1 < len(section_start_indexes),
                original_template_endswith_newline=template_text.endswith(("\n", "\r")),
            )
        )

    prefix = "".join(lines[:section_start_indexes[0]])
    return prefix + "".join(transformed_sections)


def _transform_section_lines(
    *,
    section_lines: list[str],
    has_following_section: bool,
    original_template_endswith_newline: bool,
) -> str:
    """Collapse one markdown section when its first effective body line is a standalone slot."""
    heading_line = section_lines[0]
    body_lines = section_lines[1:]
    first_content_index = next(
        (index for index, line in enumerate(body_lines) if line.strip()),
        None,
    )
    if first_content_index is None:
        return "".join(section_lines)

    match = _SECTION_SLOT_ONLY_LINE_PATTERN.match(body_lines[first_content_index].rstrip("\r\n"))
    if match is None:
        return "".join(section_lines)

    section_text = heading_line
    if not section_text.endswith(("\n", "\r")):
        section_text += "\n"
    section_text += match.group(1)
    if has_following_section:
        section_text += "\n\n"
    elif original_template_endswith_newline:
        section_text += "\n"
    return section_text
