from __future__ import annotations


class PromptLoaderError(Exception):
    """Base class for prompt loading errors that carry source context."""

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = context


class PromptSourceError(PromptLoaderError):
    """Raised when a prompt cannot be read from its configured source."""

    pass


class PromptConfigError(PromptLoaderError):
    """Raised when prompt loading configuration is invalid."""

    pass


class PromptFetchError(PromptLoaderError):
    """Raised when prompt content cannot be fetched from the source."""

    pass


class PromptParseError(PromptLoaderError):
    """Raised when prompt content cannot be parsed."""

    pass


class PromptMetadataError(PromptLoaderError):
    """Raised when prompt metadata is missing or malformed."""

    pass


class PromptCacheError(PromptLoaderError):
    """Raised when prompt cache access fails."""

    pass


class PromptConflictError(PromptLoaderError):
    """Raised when conflicting prompt content cannot be reconciled."""

    pass


class PromptVersionComparisonError(PromptLoaderError):
    """Raised when prompt versions cannot be compared safely."""

    pass


class PromptCatalogRegistryError(PromptLoaderError):
    """Raised when prompt catalog or registry resolution fails."""

    pass


class TaskPromptFormatError(ValueError):
    """Describe a task prompt front-matter formatting error."""

    def __init__(self, message: str, *, field: str | None = None) -> None:
        super().__init__(message)
        self.field = field
