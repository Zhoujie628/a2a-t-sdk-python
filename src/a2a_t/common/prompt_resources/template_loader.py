from __future__ import annotations

from a2a_t.prompt.common.models import PromptReference

from .local_resources import BasePromptResourceLoader


class TemplateLoader(BasePromptResourceLoader):
    """Load scenario-specific task prompt templates."""

    def load(self, *, reference: PromptReference) -> str:
        """Return the template text for the referenced scenario resource."""
        return self._read_scenario_text_with_fallback(
            category="templates",
            scenario_code=reference.scenario_code,
            language=reference.language,
            filename="template.md",
        )
