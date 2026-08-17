# Git Workflow & CI/CD

## Commands

The project uses `uv` as its package manager and build backend. Python `>=3.12` is required.

```bash
uv sync --dev                    # install deps (dev) locally
uv run pytest                    # run all tests (see `testing.md`)
uv run pytest tests/ -v --tb=short   # CI-style test run (see `testing.md`)
uv run ruff check src tests      # lint
uv run mypy src                  # type-check (strict)
uv build --no-sources            # build distributions
```

## Submission Checklist

Before committing or creating a PR:

```bash
uv run ruff check src tests
uv run mypy src
uv run pytest
```

Use `git commit -s` to sign off every commit.

Do not commit planning artifacts (`findings.md`, `progress.md`, `task_plan.md`, `reference/`) — they are gitignored.

## CI

`.github/workflows/ci.yml`: runs on push to `main`/`master`/`develop` and PRs to `main`/`master`.

- Job `test`: runs `uv run pytest tests/ -v --tb=short`.
- Job `lint`: runs `ruff check src tests` + `mypy src` (advisory, `continue-on-error`).

CI installs with `uv sync --frozen` (uses `uv.lock` exactly). Do not edit `uv.lock` by hand; run `uv sync` to update it after dependency changes. Before adding a dependency, confirm `pyproject.toml` does not already include an equivalent dependency.

## Publishing

`.github/workflows/publish.yml`: triggered by `v*` tags or manual dispatch. Builds with `uv build --no-sources` and publishes to PyPI via OIDC trusted publishing.

## Code Owners

`@project-openan/maintainers-a2a-t-sdk` (see `CODEOWNERS`, `MAINTAINERS.md`).