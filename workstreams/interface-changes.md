# Workstream: Interface Changes

This workstream governs **all changes to system interfaces and contracts**.
It is the most restrictive lane.

An interface change affects how repositories communicate, not just how they are implemented.

---

## What Belongs in This Workstream

This lane MUST be used for any change involving:

- OpenAPI definitions (public or internal HTTP APIs)
- AsyncAPI definitions (SSE streaming APIs)
- Protobuf definitions (PCP ↔ AISP gRPC APIs)
- Streaming event types or envelopes
- Semantics or ordering of streamed events
- Required headers, auth context, or request identity
- Client or server code generation expectations

If a change alters what another repo must send, receive, or assume, it belongs here.

---

## What Does NOT Belong Here

- Pure implementation changes that do not affect contracts
- UI-only changes
- Internal refactors
- Observability-only changes

If unsure, default to this workstream and ask.

---

## Mandatory Order of Operations

All interface changes MUST follow this sequence:

1. **platform-apis**
   - Update OpenAPI / AsyncAPI / Protobuf definitions
   - Review for backward compatibility
   - Commit contract changes first

2. **Servers**
   - PCP and/or AISP updated to match new contracts
   - Old behavior removed only if explicitly allowed

3. **Clients**
   - Regenerate API clients (e.g., orval, protobuf stubs)
   - Update UIP usage as needed
   - Generated code must not be hand-edited

4. **Integration**
   - platform-stack updated if wiring/config is affected
   - End-to-end smoke validation executed

Skipping or reordering these steps is a correctness failure.

---

## Required Artifacts

Every interface change MUST produce:

- Updated contract files in platform-apis
- Regenerated client/server artifacts (where applicable)
- Updated validation or smoke paths if needed
- Clear migration notes if behavior changes

---

## Validation Requirements

The change is not complete unless:

- Repo-level validation passes in all affected repos
- End-to-end `integration_smoke` passes
- Streaming semantics are verified (no reordering or reinterpretation)

---

## Failure Handling

If downstream changes fail:
- Do NOT patch around the contract
- Fix the contract or the implementation explicitly
- Never “hotfix” generated code

---

## Definition of Done

An interface change is DONE only when:

- Contracts are authoritative and merged
- Downstream repos conform exactly
- No repo relies on undocumented behavior
- Integration smoke validation passes
