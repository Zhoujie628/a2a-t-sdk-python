from __future__ import annotations

from pathlib import Path
from typing import Any

from .source import LocalPromptResourceSource, PromptResourceSource


class BasePromptResourceLoader:
    """Share source-aware file loading helpers across prompt resource loaders."""

    def __init__(self, *, source: PromptResourceSource | None = None, root_dir: str | Path | None = None) -> None:
        self._source = source or LocalPromptResourceSource(root_dir=root_dir)

    @property
    def root_dir(self) -> Path:
        """Expose the effective resource root directory when available."""
        root_dir = getattr(self._source, "root_dir", None)
        if root_dir is None:
            return self._default_root_dir()
        return Path(root_dir)

    @property
    def source(self) -> PromptResourceSource:
        """Expose the backing resource source used by the loader."""
        return self._source

    def _default_root_dir(self) -> Path:
        """Return the packaged prompt resource root used by default loaders."""
        return Path(__file__).resolve().parents[4] / "package_data" / "prompt_resources"

    def _read_text(self, relative_path: str) -> str:
        """Read a text resource through the configured source."""
        return self._source.read_text(relative_path=relative_path)

    def _read_json(self, relative_path: str) -> dict[str, Any]:
        """Read and parse a JSON resource through the configured source."""
        return self._source.read_json(relative_path=relative_path)
