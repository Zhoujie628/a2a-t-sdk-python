# a2a-t-sample — Sample Use Cases

Sample use cases built on **a2a-t-sdk**, organized as sibling use-case directories.

## Directory Structure

```
a2a-t-sample/
├── env.example              # shared environment config template
├── requirements.txt         # shared dependencies
├── ruff.toml                # shared lint config
├── README.md / README-zh.md # this document
└── subscribe_incident/      # use case: fault (incident) subscription
    ├── src/                 #   client / server / registry / common modules
    ├── test/                #   unit tests
    └── resources/           #   use-case mock LLM response data (zh-CN / en-US)
```

Shared configuration (`env.example`, `requirements.txt`, `ruff.toml`) lives at the container level so every use case can reuse it. Each use case carries its own `src/`, `test/`, and `resources/`.

## Available Use Cases

| Directory | Description |
|-----------|-------------|
| [subscribe_incident/](subscribe_incident/) | Fault (incident) subscription — streaming Incident artifact push with registry center |

New use cases are added as sibling directories of `subscribe_incident/`.

## Quick Start (shared)

```bash
cd a2a-t-sample
cp env.example .env
uv pip install -r requirements.txt
```

> If `A2AT_LLM_API_KEY` is left empty in `.env`, the samples automatically use mock LLM responses from `resources/mock_responses/`. No real API key is needed to run the full flow.

## Use Case: subscribe_incident

A minimal end-to-end use case demonstrating the **subscribe_incident (fault subscription)** scenario: client generates prompt -> server validates -> streaming Incident artifact push.

### Start services (three terminals)

```bash
# Terminal 1: start registry
uv run python -m agentcard_example.registry_main

# Terminal 2: start server
uv run python -m server_example.server_main

# Terminal 3: start client
uv run python -m client_example.client_main
```

The client will continuously receive artifacts. Press `Ctrl+C` to stop.

### Limit received count (optional)

```bash
A2AT_SAMPLE_MAX_ARTIFACTS=5 uv run python -m client_example.client_main
```

### Flow

| Stage | Who calls SDK | What SDK does | LLM calls |
|-------|--------------|---------------|-----------|
| Startup | client + server | A2ATClient / A2ATServer init | 0 |
| Prompt generation | client | scenario recognition + slot extraction + template render | 2 |
| Prompt validation | server | scenario recognition -> slot extraction -> semantic validation | 3 |
| Streaming push | client | normalize_event for stream events | 0 |

### Key Points

- **SDK as middleware**: client/server never call LLM directly; they go through A2ATClient/A2ATServer
- **LLM only for prompt phase**: no LLM calls during artifact push
- **No negotiation**: client submits complete input; server validates and pushes directly
- **Three-layer decoupling**: client (discover + consume) -> server (register + push) -> registry (registry center)

## Run Tests

```bash
# Run all use case tests
uv run pytest subscribe_incident/test/ -v
```