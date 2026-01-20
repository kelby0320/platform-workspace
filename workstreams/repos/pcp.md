# Repo Playbook: platform-control-plane (PCP)

This document describes how to work in the Platform Control Plane (PCP)
repository as part of the multi-repo workflow.

PCP owns the public API boundary and coordinates request flow between
the UI and internal services. Correctness and stability are critical.

---

## Responsibilities

PCP is responsible for:

- Public HTTP APIs consumed by UIP
- SSE streaming of chat turn responses
- Request lifecycle management
- Request identity generation and propagation
- Chat history persistence
- Artifact persistence (user-uploaded and AI-generated; future)
- Translating internal gRPC streams into public SSE streams

PCP is the integration boundary between UIP and AISP.

---

## Hard Constraints

- MUST NOT call LLMs directly
- MUST NOT implement AI orchestration logic
- MUST NOT reinterpret or reorder streaming events
- MUST NOT expose internal AISP APIs directly
- MUST NOT bypass platform-apis contracts

All public and internal interfaces must be defined in platform-apis.

---

## Interfaces Owned by PCP

PCP owns:

- Public HTTP APIs (OpenAPI)
- Public SSE streaming APIs (AsyncAPI)
- Internal gRPC client calls to AISP (Protobuf-defined)

PCP does not own:
- AI orchestration behavior
- AI model selection
- AI-specific databases

---

## When PCP Must Change

PCP changes are required when:

- Public API behavior changes
- Streaming behavior changes (without contract changes)
- Request lifecycle or persistence logic changes
- New orchestration calls to AISP are added
- Observability concerns require request propagation changes

If a change requires contract updates, route it through the
Interface Changes workstream first.

---

## Dependency Discipline

PCP enforces a layered crate architecture:

- `domain`
- `infra`
- `platform-api`

Agents MUST follow the rules in `platform-control-plane/AGENTS.md`.

Common violations to avoid:
- Business logic in `platform-api`
- Infrastructure logic leaking into `domain`
- Direct dependency inversion violations

---

## Streaming Semantics (Critical)

PCP acts as a streaming adapter.

Rules:
- gRPC stream events from AISP must be forwarded to UIP as SSE events
- Event meaning, ordering, and cardinality MUST be preserved
- PCP may wrap events but MUST NOT change semantics
- Errors must propagate as defined in AsyncAPI

If an event model change is required, stop and route through Interface Changes.

---

## Tooling and Validation

PCP is a Rust codebase.

Agents MUST use Cargo tooling:

```sh
cargo fmt
cargo clippy --all-targets --all-features -- -D warnings
cargo test
```

Dependency management rules:
- MUST use cargo add to add dependencies
- MUST NOT manually edit Cargo.toml for dependencies

Validation failures block completion.

---

## Generation Responsibilities

PCP is responsible for:
- Generating gRPC client/server code from Protobuf definitions
- Regenerating code when platform-apis Protobuf files change

Generated code:
- MUST NOT be hand-edited
- MUST be committed as generated

If generation output changes unexpectedly, the issue belongs in platform-apis.

---

## Validation Requirements (Definition of Done)

A PCP change is DONE only when:
- Repo-local validation passes
- Layering and dependency rules are preserved
- Streaming behavior matches contracts
- Integration smoke passes (for cross-repo changes)

Passing unit tests alone is not sufficient.

---

## Failure Handling

If integration fails:
- Identify whether the failure is contract, PCP, or downstream
- Do NOT patch behavior to “make it work”
- Fix the root cause or escalate appropriately

---

## Mandatory Stop Conditions

Agents MUST STOP and report if::
- a change violates crate dependency rules
- streaming semantics are unclear
- a public API change is required but not planned
- behavior drifts from platform-apis definitions