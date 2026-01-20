# Repo Playbook: user-interface-plane (UIP)

This document describes how to work in the User Interface Plane (UIP)
repository as part of the multi-repo workflow.

UIP contains all client-facing applications and shared frontend packages.
It presents data and interactions but does not define system behavior.

---

## Responsibilities

UIP is responsible for:

- Client applications:
  - apps/web-app (React + Vite)
  - apps/portal (Next.js)
- Shared UI components (packages/ui)
- Consuming PCP public HTTP APIs
- Consuming PCP SSE streams
- Rendering streamed events to users

UIP treats PCP as its only backend dependency.

---

## Hard Constraints

- MUST NOT contain business logic
- MUST NOT implement backend workflows
- MUST NOT call internal services directly
- MUST NOT reinterpret or reorder streaming events
- MUST NOT bypass platform-apis contracts

All client-visible behavior must be driven by data received from PCP.

---

## Generated API Client (Critical)

The `packages/api-client` package is GENERATED.

Rules:
- MUST NOT hand-edit generated files
- MUST regenerate the client when platform-apis OpenAPI changes
- MUST commit generated output as-is
- MUST NOT add application logic to generated code

If generated output appears incorrect, the fix belongs in platform-apis,
not in UIP.

---

## Package and App Boundaries

Structure:

```
apps/
├── web-app/
├── portal/
packages/
├── ui/
└── api-client/
```

Rules:
- apps MAY depend on packages/ui and packages/api-client
- packages/ui MUST NOT depend on application code
- packages/api-client MUST NOT depend on UI code
- Shared components belong in packages/ui, not in apps

Violating boundaries is a correctness failure.

---

## Streaming Semantics (Critical)

- SSE event types and payloads are defined in platform-apis (AsyncAPI)
- UIP is a passive consumer of streamed events
- Event meaning and ordering MUST be preserved
- Error events MUST be surfaced without reinterpretation

UIP MUST NOT:
- infer hidden semantics from event timing
- merge, reorder, or synthesize events
- embed backend assumptions in UI logic

---

## Tooling and Validation

UIP uses pnpm and a pnpm workspace.

Agents MUST use pnpm commands.

Typical validation commands:
```sh
pnpm install
pnpm -r lint
pnpm -r test
pnpm -r build
```

Workspace-aware commands SHOULD be preferred.

---

## Dependency Management (Critical Rule)

- MUST NOT manually edit package.json to add dependencies
- MUST add dependencies using pnpm commands

Required usage:

```sh
pnpm add <package> --filter <workspace>
pnpm add -D <package> --filter <workspace>
```

Manual dependency edits are a tooling violation.

---

## When UIP Must Change

UIP changes are required when:
- UI behavior or layout changes
- New client-visible features are added
- Streaming presentation changes (without contract changes)
- API client regeneration is required due to contract updates

If a change requires modifying contracts, route it through the
Interface Changes workstream first.

---

## Validation Requirements (Definition of Done)

A UIP change is DONE only when:
- Repo-level validation passes (lint, test, build)
- Generated client code (if any) is up to date
- Streaming behavior renders correctly
- Integration smoke passes (for cross-repo changes)

Passing a local dev server check alone is not sufficient.

---

## Failure Handling

If integration fails:
- Determine whether the failure is client logic, generated code, or upstream
- Do NOT patch generated clients to make things work
- Route contract issues back to platform-apis
- Keep UI changes minimal and explicit

---

## Mandatory Stop Conditions

Agents MUST STOP and report if:
- generated client code appears incorrect
- a dependency change affects multiple workspaces unexpectedly
- streaming semantics are unclear
- UI logic begins to encode backend behavior