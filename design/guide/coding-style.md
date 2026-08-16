# Coding Style

Enforced by `ruff` and `mypy` (strict). Do not fight the linter.

## General Principles

- Follow Python best practices and idiomatic patterns.
- Follow software principles such as DRY and YAGNI.
- Keep diffs as minimal as possible.
- Do not add comments unless a non-obvious invariant requires explanation.

## Imports & Module Structure

- `from __future__ import annotations` at the top of every module.
- Import ordering is enforced by ruff rule `I` (isort-compatible). Group stdlib, then third-party, then `a2a_t.*`.
- Lazy imports: top-level `a2a_t/__init__.py` uses `__getattr__` to import submodules on demand. Keep heavy imports out of `__init__.py` unless they are cheap.

## Type Hints

- Type hints are **required** on all public functions; `mypy --strict` is the baseline.

## Dataclasses

Follow dataclass conventions from `design-principles.md`.

## Formatting

- Line length is 120.
- Tests relax `E402` (module-level import not at top) and `E501` (line length) because they manipulate `sys.path` before importing `a2a_t`.

## Naming

Ruff rule `N` enforces PEP 8 naming:

- Classes: `PascalCase`
- Functions and variables: `snake_case`
- Constants: `UPPER_SNAKE`

## Error Handling

- No bare except; catch specific exceptions and re-raise as SDK error types.
- Never raise bare `Exception` in SDK code. Wrap provider errors into `LLMRuntimeError`.
- Raise the most specific subclass available (see `config/errors.py`, `llm/errors.py`).