# Workstream: Feature Delivery

This is the standard lane for delivering product features.

Features may span multiple repositories but MUST respect existing contracts
unless explicitly routed through the Interface Changes workstream.

---

## What Belongs in This Workstream

Use this lane for:

- New user-facing functionality
- Backend behavior changes that fit existing contracts
- Coordinated PCP / AISP / UIP changes
- Internal feature flags or configuration changes
- Incremental extensions that do not alter API meaning

This is the default lane unless a stricter one applies.

---

## What Does NOT Belong Here

- Contract or schema changes
- Streaming event changes
- Observability-only work
- Refactors without user-visible impact

---

## Planning Requirements

Every feature MUST be decomposed into work orders that:

- Target a single repository where possible
- Declare dependencies on other work orders
- List validation commands explicitly
- Reference the repo-local AGENTS.md

Large features should prefer more small work orders over fewer large ones.

---

## Execution Model

- Work orders MAY be executed in parallel
- Each work order operates on its own branch
- Cross-repo dependencies must be explicit
- No work order may assume another is merged unless stated

---

## Validation Requirements

A feature is not complete unless:

- All work orders are marked DONE
- Repo-level validation passes in each affected repo
- End-to-end `integration_smoke` passes (if multi-repo)

---

## Failure Handling

If integration fails:

- Identify the smallest responsible work order
- Route fixes back to that work order
- Do NOT open a new “mega agent” to fix everything at once

---

## Definition of Done

A feature is DONE when:

- Intended behavior is observable and correct
- No contracts were implicitly changed
- Validation and smoke checks pass
- The feature can be explained without caveats
