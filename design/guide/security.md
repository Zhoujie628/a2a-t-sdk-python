# Security

## Secrets

- Do not put real API keys or secrets in `tests/.env`, `package_data/.env`, or any committed file. Use placeholder values.
- Before running the SDK locally, copy `package_data/env.example` to `package_data/.env` and fill in the `A2AT_LLM_*` values.

## Package Data

Don't bypass `resolve_prompt_resource_root` when locating packaged resources. This ensures the correct resolution path in both source-checkout and installed-wheel layouts.