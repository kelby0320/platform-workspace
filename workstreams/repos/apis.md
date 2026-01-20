# Repo Playbook: platform-apis

This document describes how to work in the `platform-apis` repository as part of
the multi-repo workflow.

`platform-apis` is the CONTRACT SOURCE OF TRUTH.
It contains schema definitions only and no generated code.

---

## Responsibilities

`platform-apis` owns:

- OpenAPI definitions
  - PCP public HTTP APIs
  - AISP internal HTTP APIs
- AsyncAPI definitions
  - PCP SSE chat turn API
- Protobuf definitions
  - PCP -> AISP internal gRPC streaming API

This repository defines WHAT is communicated, not HOW it is implemented.

---

## Hard Constraints

- MUST NOT contain business logic
- MUST NOT contain generated code
- MUST NOT contain implementation details
- MUST NOT generate client or server code
- MUST NOT modify downstream repositories

All code generation is the responsibility of consuming repositories.

---

## Consumer Responsibilities (Important)

Consuming repositories are responsible for:

- Generating client or server code from these schemas
- Regenerating code when contracts change
- Failing builds if generated artifacts are out of date

Examples:
- PCP generates gRPC client code from Protobuf
- UIP generates API client code from OpenAPI (via orval)
- AISP generates gRPC server code from Protobuf

`platform-apis` does not track or enforce generation.

---

## When This Repo Must Change

Use `platform-apis` whenever any of the following change:

- HTTP endpoints, parameters, request/response bodies, or status codes
- SSE event names, payload schemas, or semantics
- gRPC service definitions or streaming message types
- Required headers or auth context expectations
- Cross-repo DTOs or event envelopes

If a change alters how another repo communicates, it belongs here.

---

## Compatibility Rules

- Prefer backward-compatible changes:
  - additive fields with safe defaults
  - new optional parameters
  - new endpoints over breaking existing ones
- Breaking changes require:
  - explicit migration notes
  - coordinated downstream updates

Do not rely on undocumented behavior.

---

## Change Process (Interface Changes Workstream)

Mandatory order of operations:

1) Update contracts in `platform-apis`
2) Update consuming servers (PCP / AISP)
3) Regenerate client/server code in consuming repos
4) Validate integration via platform-stack

This repo is always changed first.

---

## Event Model Notes (Chat Turn)

Conceptual event types (current):
- token_delta
- metrics
- done
- error

Representations:
- gRPC stream: defined in Protobuf
- SSE stream: defined in AsyncAPI

Semantics must match across transports.
PCP must not reinterpret or reorder events.

---

## Tooling and Validation

This repository currently contains schemas only.

There is no required generation step.

Optional validation (if present):
- schema linting
- structural validation
- compatibility checks

If validation tooling is added, it must:
- remain schema-only
- avoid introducing generated artifacts
- avoid coupling to downstream build systems

---

## Deliverables for Contract Changes

Every contract change must include:

- Updated schema files
- Clear notes describing:
  - what changed
  - compatibility impact
  - which downstream repos must regenerate code

Downstream regeneration must not be implicit.

---

## Definition of Done

A contract change is DONE only when:

- Schemas accurately represent intended behavior
- Changes are unambiguous and documented
- Downstream repos can regenerate code without guesswork
- Integration smoke passes after downstream updates

Passing changes in this repo alone is not sufficient.

---

## Mandatory Stop Conditions

Agents MUST STOP and report if:

- a contract cannot express the intended behavior cleanly
- semantics differ between gRPC and SSE definitions
- a breaking change lacks a migration plan
- downstream regeneration requirements are unclear
