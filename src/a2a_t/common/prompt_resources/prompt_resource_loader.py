from __future__ import annotations

from ._base import BasePromptResourceLoader
from .models import PromptMessages


class PromptResourceLoader(BasePromptResourceLoader):
    """Load shared analysis prompts used by LLM-powered prompt analysis."""

    def load(self, *, analysis_action: str, language: str) -> PromptMessages:
        """Return the system and user prompts for the requested analysis action."""
        prompt_dir = f"prompts/{analysis_action}/{language}"
        return PromptMessages(
            system_prompt=self._read_text(f"{prompt_dir}/system.md"),
            user_prompt=self._read_text(f"{prompt_dir}/user.md"),
        )
