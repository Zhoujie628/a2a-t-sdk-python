# Design Principles

Design principles that must be followed when creating spec and impl documents. These principles are derived from the project's existing code patterns, not imposed from outside.

## Architecture Design (for spec documents)

Spec documents define capability boundaries, module interactions, and contracts. The following principles constrain how specs are designed.

### Module Boundary

A capability owns its data, its logic, and its error types. When a feature crosses module boundaries, define a clear contract: what data flows in, what data flows out, and which errors can propagate.

- Prefer **narrow contracts** — expose only what downstream modules need.
- A module should not reach into another module's internal data structures.
- Cross-module dependencies should flow from high-level (orchestrator) to low-level (utility), not sideways.

### Dependency Direction

Dependencies must flow from high-level (orchestrator/facade) to low-level (utility/common). No circular dependencies. See `architecture.md` for the concrete layering.

When adding a new capability, follow this layering: define the contract in a shared package, implement the logic in an orchestrator, expose it through the client or server facade.

### Capability Decomposition

A capability is a self-contained feature with a clear input/output boundary. When designing a spec:

- One spec = one capability. Do not merge unrelated features into one spec.
- If a feature has server-side and client-side responsibilities, they may share a spec but must clearly separate the two roles.
- Do not prematurely split a capability into sub-features. Start with one spec and split when the spec becomes too large to reason about.

### Error Hierarchy

Every module that can fail must define its own error hierarchy:

- One base error class per module (e.g., `LLMError`, `ConfigError`).
- Specific subclasses for distinct failure modes (e.g., `LLMConfigError`, `LLMRuntimeError`).
- Error types should carry enough context for callers to handle them programmatically (e.g., `ConfigFileNotFoundError` carries the file path).

### Degradation Strategy

When a dependency is optional or may fail, define a degradation strategy in the spec:

- Fall back to a safe default (e.g., `NegotiationStateStoreFactory` falls back to in-memory store).
- Log a warning — do not silently swallow errors.
- Do not degrade across security boundaries.

## Code Design (for impl documents)

Impl documents translate architecture decisions into class-level design. The following principles constrain how code is organized.

### SOLID Principles (Python-adapted)

| Principle | In this project |
|-----------|----------------|
| **Single Responsibility (SRP)** | Each class does one thing. An orchestrator coordinates, a builder wires, a renderer renders. Do not merge them. |
| **Open/Closed (OCP)** | Extend through new classes, not by modifying existing ones. Add a new negotiation type by subclassing `BaseNegotiationType`, not by adding branches to it. |
| **Liskov Substitution (LSP)** | Subtypes must honor the contract of their base type. Override hook methods, not core logic methods. |
| **Interface Segregation (ISP)** | Keep Protocols narrow. `LLMClient` exposes only `structured()`, not every capability an LLM might have. |
| **Dependency Inversion (DIP)** | Depend on Protocols, not concrete classes. `LLMClientFactory` depends on `LLMClient` Protocol, not `OpenAIClient`. |

### Python-Specific Principles

**Composition over inheritance.** Prefer passing dependencies through constructors over inheriting behavior. `BaseNegotiationType` uses composition: it receives a `NegotiationPromptRenderer` via the constructor rather than inheriting rendering logic.

**Protocol over ABC.** Use `typing.Protocol` for extension interfaces. Structural subtyping means implementers don't need to inherit — they just need the right method signatures. Use `@runtime_checkable` when `isinstance()` checks are needed.

**Dataclasses for data, classes for behavior.** Use `@dataclass(slots=True)` for configuration objects, `@dataclass(frozen=True)` for immutable value objects. Use regular classes for objects with behavior.

**Keyword-only parameters.** Use `*,` before non-self parameters on all public APIs. This makes call sites explicit and prevents positional argument confusion.

**Explicit dependency wiring.** No global state, no service locators, no magic auto-wiring. Every dependency is passed through the constructor. Builders are the single place where wiring happens.

### Project Patterns

These patterns are proven in the existing codebase. New code should follow them.

**Builder + Orchestrator.** High-level facades (`A2ATClient`, `A2ATServer`) are thin. Each capability has a `*OrchestratorBuilder` that constructs a `*Orchestrator`. The builder is the wiring point; the orchestrator is the logic point. Do not put logic in builders or wiring in orchestrators.

**Factory + Registry.** For pluggable backends, use a class-level registry dict mapping name → class. The factory creates instances from the registry. See `LLMClientFactory` for the canonical pattern.

**Strategy pattern for variant behavior.** When a behavior has multiple variants, define a base class with hook methods and subclass for each variant. The base class provides defaults; subclasses override only what they need. See `BaseNegotiationType` → `InformationNegotiationType`, `FeasibilityNegotiationType`, `TargetNegotiationType`.

**Typed errors, typed results.** Orchestrator methods return either a success result or a failure result (not raise exceptions for expected failures). Use dedicated result types for the success path, error types for the failure path. See `PromptGenerationResult` / `PromptGenerationFailure`.

### When to Abstract

| Situation | Action |
|-----------|--------|
| Single implementation, no cross-module boundary | Concrete class. No abstraction needed. |
| Single implementation, cross-module boundary | Define a Protocol so the caller doesn't depend on the implementation module. |
| Multiple implementations expected | Protocol + Factory + Registry. |
| Behavior variant within same module | Strategy pattern (base class + subclasses). |

Do not abstract for hypothetical future needs. Abstract when a second implementation is actually needed, or when a cross-module boundary demands it.

### Anti-Patterns

**Middle Man.** A class that does nothing but delegate every method call to another class without adding logic. If a class is just a pass-through, remove it and let callers depend on the real implementation directly.

**Premature Abstraction.** A Protocol or abstract class created for a single implementation "just in case." Wait until a second implementation exists before introducing the abstraction.