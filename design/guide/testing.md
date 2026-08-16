# Testing

## Framework

`pytest` with `asyncio_mode = "auto"` and `testpaths = ["tests"]`.

## Test Style

- `unittest.TestCase` classes with `unittest.mock.patch` for fakes.
- See `tests/client_prompt/test_a2at_client.py` for the canonical facade-delegation test.
- Focus tests on **behavior**, not implementation details.

## Shared Helpers

`tests/support.py` provides:

- `ManagedTempDirTestCase` — auto-cleans temp dirs under `.tmp_tests/`.
- `FakeRemoteProvider`, `build_markdown`, `TEST_ENV_PATH`, `PROJECT_ROOT`.

## Conventions

- Tests add `src/` to `sys.path` so they run without an installed package.
- Prefer fakes/builder doubles over real LLM calls. Unit tests must not hit the network.
- When adding a feature, add a test file under the matching `tests/<area>/` subdir.

## Running Tests

```bash
uv run pytest                          # run all tests
uv run pytest tests/ -v --tb=short     # CI-style test run
```