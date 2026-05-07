from __future__ import annotations

from typing import Protocol

from a2a_t.config.models import GuardrailProviderConfig

from .models import GuardrailResult


class SafetyGuardrail(Protocol):
    """Describe the interface implemented by prompt safety guardrails."""

    def check(self, prompt_text: str, context: dict[str, object] | None = None) -> GuardrailResult:
        """Check whether the processed prompt passes the safety guardrail."""


class NoopSafetyGuardrail:
    """Accept every prompt without applying any policy checks."""

    def check(self, prompt_text: str, context: dict[str, object] | None = None) -> GuardrailResult:
        """Return an allow result without inspecting the prompt."""
        return GuardrailResult(passed=True)


class SafetyGuardrailFactory:
    """Create guardrail implementations from configuration."""

    _reserved_providers: set[str] = {"aws_bedrock", "azure_content_safety"}

    @classmethod
    def create(cls, config: GuardrailProviderConfig) -> SafetyGuardrail:
        """Create the configured guardrail or fail for unsupported providers."""
        provider_name = config.provider or "noop"
        if provider_name == "noop":
            return NoopSafetyGuardrail()
        if provider_name in cls._reserved_providers:
            raise ValueError(f"Guardrail provider '{provider_name}' is reserved for future support and not implemented.")
        raise ValueError("Unknown guardrail provider: " f"{provider_name}. Available: {cls.available_types()}")

    @classmethod
    def available_types(cls) -> list[str]:
        """List the guardrail provider types currently implemented."""
        return ["noop"]
