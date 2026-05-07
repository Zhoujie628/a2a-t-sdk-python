from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .errors import PromptResourceNotFoundError


class PromptResourceProvider(Protocol):
    """Describe the file access operations required by a resource source."""

    def read_text(self, *, locator: Path) -> str: ...

    def exists(self, *, locator: Path) -> bool: ...


class LocalPromptResourceProvider:
    """Read A2A-T resource files directly from the local filesystem."""

    def read_text(self, *, locator: Path) -> str:
        """Read a UTF-8 resource file or raise a not-found error."""
        if not locator.exists() or not locator.is_file():
            raise PromptResourceNotFoundError("Prompt resource file does not exist.", path=str(locator))
        return locator.read_text(encoding="utf-8")

    def exists(self, *, locator: Path) -> bool:
        """Return whether the given resource locator points to a file."""
        return locator.exists() and locator.is_file()
