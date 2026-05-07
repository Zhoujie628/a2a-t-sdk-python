from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol

from .catalog import LocalPromptResourceCatalog, PromptResourceCatalog
from .errors import PromptResourceParseError
from .providers import LocalPromptResourceProvider, PromptResourceProvider


class PromptResourceSource(Protocol):
    """Describe the minimal interface required by prompt resource loaders."""

    source_type: str

    def read_text(self, *, relative_path: str) -> str: ...

    def read_json(self, *, relative_path: str) -> dict[str, Any]: ...

    def exists(self, *, relative_path: str) -> bool: ...


class LocalPromptResourceSource:
    """Load packaged prompt resources from the local filesystem."""

    source_type = "local_file"

    def __init__(
        self,
        *,
        root_dir: str | Path | None = None,
        catalog: PromptResourceCatalog | None = None,
        provider: PromptResourceProvider | None = None,
        cache: object | None = None,
    ) -> None:
        self._catalog = catalog or LocalPromptResourceCatalog(root_dir=root_dir)
        self._provider = provider or LocalPromptResourceProvider()
        self._cache = cache

    @property
    def root_dir(self) -> Path | None:
        """Expose the configured local resource root when the catalog provides one."""
        return getattr(self._catalog, "root_dir", None)

    def read_text(self, *, relative_path: str) -> str:
        """Read a text resource from the resolved local path."""
        locator = self._catalog.resolve(relative_path=relative_path)
        return self._provider.read_text(locator=locator)

    def read_json(self, *, relative_path: str) -> dict[str, Any]:
        """Read a JSON resource and enforce an object-shaped payload."""
        text = self.read_text(relative_path=relative_path)
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as error:
            raise PromptResourceParseError("Prompt resource JSON is invalid.", path=relative_path) from error

        if not isinstance(payload, dict):
            raise PromptResourceParseError(
                "Prompt resource JSON root must be an object.",
                path=relative_path,
                actual_type=type(payload).__name__,
            )
        return payload

    def exists(self, *, relative_path: str) -> bool:
        """Return whether the resolved local resource path exists."""
        locator = self._catalog.resolve(relative_path=relative_path)
        return self._provider.exists(locator=locator)
