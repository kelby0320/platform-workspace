# Repo Playbook: ai-services-plane (AISP)

This document describes how to work in the AI Services Plane (AISP)
repository as part of the multi-repo workflow.

AISP owns AI execution and orchestration.
It is the only component allowed to call an LLM.

---

## Responsibilities

AISP is responsible for:

- AI orchestration logic (LangGraph)
- Executing a single chat turn
- Calling LLM providers
- Producing streaming events for chat turns
- Serving internal, read-only informational HTTP APIs:
  - model_profile
  - graph_profile
- Managing AI-specific persistence (e.g. future RAG databases)

AISP is an internal service and has no public client-facing APIs.

---

## Hard Constraints

- MUST be the only component that calls an LLM
- MUST NOT expose public APIs directly to clients
- MUST NOT own chat history persistence
- MUST NOT reinterpret UI concerns or presentation logic
- MUST NOT bypass platform-apis contracts

All gRPC and HTTP interfaces must be defined in platform-apis.

---

## Interfaces Owned by AISP

AISP owns:

- Internal gRPC streaming service for chat turns (Protobuf-defined)
- Internal HTTP informational APIs (OpenAPI-defined)
- AI orchestration graph semantics

AISP does not own:
- Public HTTP APIs
- SSE semantics (PCP responsibility)
- Client-side models or UI state

---

## When AISP Must Change

AISP changes are required when:

- AI orchestration logic changes
- LLM invocation behavior changes
- Streaming event production changes (within existing contracts)
- New informational metadata must be exposed
- AI-specific persistence is added or modified

If a change requires contract updates, route it through the
Interface Changes workstream first.

---

## Streaming Semantics (Critical)

AISP is the SOURCE of truth for chat turn events.

Rules:
- gRPC stream events MUST conform exactly to Protobuf definitions
- Event meaning and ordering MUST be correct at emission time
- Events MUST be emitted incrementally (no buffering to completion)
- Errors MUST be emitted using defined error event types

AISP MUST NOT:
- assume how PCP or UIP will present events
- emit undocumented event types
- change event semantics without contract changes

---

## Tooling and Validation

AISP uses uv for all tooling.

Agents MUST use uv commands exclusively:

```sh
uv run ruff format
uv run ruff check
uv run mypy .
uv run pytest
```

Dependency management rules:
- MUST use uv add to add dependencies
- MUST NOT manually edit pyproject.toml for dependencies

Manual dependency edits are a tooling violation.

---

## Generation Responsibilities

AISP is responsible for:
- Generating gRPC server/client stubs from Protobuf definitions
- Regenerating stubs when platform-apis Protobuf files change

Generated code:
- MUST NOT be hand-edited
- MUST be committed as generated

If generation output is incorrect, the issue belongs in platform-apis.

---

## Validation Requirements (Definition of Done)

An AISP change is DONE only when:
- Repo-local validation passes (format, lint, type check, tests)
- Streaming behavior matches Protobuf definitions
- No additional LLM calls are introduced outside orchestration
- Integration smoke passes (for cross-repo changes)

Passing unit tests alone is not sufficient.

---

## Failure Handling

If integration fails:
- Determine whether the failure is contract-level or implementation-level
- Do NOT patch behavior to satisfy callers incorrectly
- Fix the root cause or escalate via the Interface Changes workstream

---

## Mandatory Stop Conditions

Agents MUST STOP and report if:
- a change would require calling an LLM outside AISP
- streaming semantics are unclear or inconsistent
- a contract change is required but not planned
- orchestration logic leaks into transport or API layers