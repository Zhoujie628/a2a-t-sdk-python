"""Configuration management for a2a_t."""

from __future__ import annotations

from importlib import import_module

__all__ = [
    "A2ATConfig",
    "ConfigError",
    "ConfigFileNotFoundError",
    "PromptComplianceConfig",
    "PromptRuntimeConfig",
]


def __getattr__(name: str):
    if name in {"ConfigError", "ConfigFileNotFoundError"}:
        value = getattr(import_module("a2a_t.config.errors"), name)
    elif name == "A2ATConfig":
        value = getattr(import_module("a2a_t.config.models"), name)
    elif name in {"PromptRuntimeConfig", "PromptComplianceConfig"}:
        value = getattr(import_module("a2a_t.config.models"), name)
    else:
        raise AttributeError(f"module 'a2a_t.config' has no attribute {name!r}")

    globals()[name] = value
    return value
