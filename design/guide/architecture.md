# Architecture & Key Patterns

## Repository Layout

```
src/a2a_t/            # SDK package (import name: a2a_t)
  __init__.py         # lazy module loader via __getattr__
  client/             # A2ATClient + prompt_generation/ + negotiation/
  server/             # A2ATServer + prompt_compliance/ + negotiation/
  common/             # prompt resource loading, prompt runtime, resource_roots.py
  config/             # A2ATConfig, DotEnvConfigSource, config errors
  llm/                # LLMClient Protocol, factory, config loader, providers/
  negotiation/        # types/ (strategies), runtime/, store/, handling/, rendering/, common/
  prompt/             # analysis/, task_rendering/, validation/, common/
package_data/         # packaged data files shipped with the wheel
  env.example         # template .env -> copy to package_data/.env
  prompt_resources/   # prompts/, scenarios/, slots/, templates/
tests/                # pytest suite; support.py holds shared helpers
.github/workflows/    # ci.yml (test + advisory lint), publish.yml (PyPI on v* tags)
```

### Package Data Note

`package_data/` is shipped with the wheel via `tool.uv.build-backend.data`. The prompt resources under `package_data/prompt_resources/` are resolved at runtime by `a2a_t/common/resource_roots.py::resolve_prompt_resource_root`, which handles **both** source checkouts (path relative to the module file) and installed wheels (`sysconfig.get_path("data")`). Resolution works in both source-checkout and installed-wheel layouts.

## Orchestrator + Builder

High-level `A2ATClient` / `A2ATServer` are thin facades. Each capability is a `*OrchestratorBuilder` that constructs a `*Orchestrator`, which does the real work. The facade delegates every public call.

- `client/prompt_generation/prompt_generation_orchestrator_builder.py`
- `client/negotiation/negotiation_orchestrator_builder.py`
- `server/prompt_compliance/prompt_compliance_orchestrator_builder.py`
- `server/negotiation/negotiation_orchestrator_builder.py`
- `negotiation/runtime/base_negotiation_orchestrator.py`

## Factory + Registry

`a2a_t/llm/factory.py::LLMClientFactory` keeps a class-level `_clients` dict mapping provider name -> client class. New providers are registered via `LLMClientFactory.register()` and created via `LLMClientFactory.create()`. The negotiation state store follows the same pattern (`negotiation/store/factory.py`).

## Protocol-based Interfaces

`a2a_t/llm/provider.py::LLMClient` is a `@runtime_checkable Protocol` with a single `structured(...)` method. Provider clients (e.g. `providers/openai.py::OpenAIClient`) implement it structurally; inheritance is not required.

## Configuration from .env

All runtime config is read from a single `.env` file via `a2a_t/config/source.py::DotEnvConfigSource.load()`. Two loaders build typed dataclasses:

- `a2a_t/config/models.py::A2ATConfig.load(env_path)` -> `PromptRuntimeConfig` + `PromptComplianceConfig`.
- `a2a_t/llm/config_loader.py::LLMConfigLoader.load(env_path)` -> `LLMClientConfig`.

Both validate and raise typed errors (`ConfigError`, `LLMConfigError`) on bad input. `A2ATClient` / `A2ATServer` default to `package_data/.env`; callers can pass `env_path=` to override.

## Error Hierarchy

- `config/errors.py`: `ConfigError` -> `ConfigFileNotFoundError`
- `llm/errors.py`: `LLMError` -> `LLMConfigError`, `LLMRuntimeError`

## Negotiation Types

`negotiation/types/base.py::BaseNegotiationType` defines the default behavior (`render_start_prompt`, `process_received_message`, `render_continue_prompt`). Concrete strategies live alongside it: `information.py`, `feasibility.py`, `target.py`. They are registered in `negotiation/types/__init__.py`.