from __future__ import annotations

from datetime import datetime
from typing import Protocol

from a2a_t.prompt.common.models import CacheStatus, CachedPromptRecord


class PromptStore(Protocol):
    """Describe the persistence contract for cached prompt content."""

    def write(self, *, record: CachedPromptRecord, content: str) -> None: ...

    def read(self, *, source_type: str, name: str, language: str) -> tuple[CachedPromptRecord, str]: ...

    def resolve(
        self,
        *,
        source_type: str,
        name: str,
        language: str,
        now: datetime,
        allow_stale_fallback: bool,
    ) -> tuple[CachedPromptRecord | None, str | None, CacheStatus]: ...


class ExpirationPolicy(Protocol):
    """Describe the policy used to decide whether cached content is stale."""

    def is_expired(self, *, record: CachedPromptRecord, now: datetime) -> bool: ...


class ConflictResolutionPolicy(Protocol):
    """Describe the policy used to decide whether cached content should be replaced."""

    def should_overwrite(self, *, existing_record: CachedPromptRecord, new_record: CachedPromptRecord) -> bool: ...
