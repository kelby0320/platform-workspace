# Repo Playbook: platform-stack

This document describes how to work in the `platform-stack` repository as part of
the multi-repo workflow.

`platform-stack` is the RUNTIME AND INTEGRATION HARNESS.
It exists to run the system, not to define product behavior.

---

## Responsibilities

`platform-stack` is responsible for:

- docker-compose definitions for running the full platform locally
- Wiring together:
  - UIP
  - PCP
  - AISP
  - Databases
  - Observability infrastructure
- Environment configuration for local development
- Health checks and service readiness
- End-to-end integration and smoke validation entrypoints

`platform-stack` answers the question:
“Does the system run and integrate correctly?”

---

## Hard Constraints

- MUST NOT contain business logic
- MUST NOT contain API definitions or contracts
- MUST NOT implement application behavior
- MUST NOT duplicate configuration owned by other repos
- MUST NOT bypass platform-apis contracts

All services must be treated as black boxes with defined interfaces.

---

## Ownership Boundaries

`platform-stack` OWNS:
- Service composition
- Environment variables required to run services
- Network wiring and ports
- Observability infrastructure and configuration
- Integration smoke test scripts

`platform-stack` DOES NOT OWN:
- API schemas
- Request/response semantics
- Streaming event models
- Persistence schemas
- Service-specific logic

---

## Service Composition Rules

- Each service runs as its own container
- Containers communicate only via defined network interfaces
- Local overrides must not leak into production assumptions
- Default configuration should favor correctness over convenience

If a service requires a new environment variable:
- Document it
- Provide a safe local default
- Do not hard-code secrets

---

## Observability Wiring

platform-stack is the integration point for observability.

Responsibilities include:
- Wiring log collection
- Wiring trace collection
- Wiring metrics collection
- Ensuring request identity can be correlated end-to-end

Observability configuration must not change service behavior.
If observability changes require API or semantic changes, route that work
through the Observability or Interface Changes workstreams.

---

## Integration Smoke Testing (Critical)

`platform-stack` MUST provide a single, well-defined way to verify
end-to-end integration.

At minimum, the smoke test MUST:
- Start the full stack
- Wait for services to become healthy
- Execute a single “happy path” chat turn:
  - UIP -> PCP -> AISP -> PCP -> UIP (or a direct PCP call)
- Verify that:
  - the request completes
  - streaming events flow end-to-end
- Exit with a non-zero code on failure

The smoke test is the primary judge of correctness across repos.

---

## Tooling and Execution

platform-stack tooling should be simple and explicit.

Recommended interface:
- `./scripts/up.sh`
- `./scripts/down.sh`
- `./scripts/health.sh`
- `./scripts/smoke.sh`

Or equivalent `docker compose` commands if scripts are not present.

Agents MUST:
- Use documented commands
- Avoid inventing ad-hoc run instructions
- Keep scripts idempotent where possible

---

## Validation Requirements (Definition of Done)

A platform-stack change is DONE only when:

- The full stack starts cleanly
- All services report healthy
- Integration smoke test passes
- No service behavior is altered unintentionally

Passing docker-compose validation alone is NOT sufficient.

---

## Failure Handling

If integration fails:

- Determine whether the failure is wiring, configuration, or service behavior
- Do NOT patch service behavior in platform-stack
- Route fixes to the owning repo when appropriate
- Keep stack changes minimal and explicit

---

## Mandatory Stop Conditions

Agents MUST STOP and report if:

- a stack change requires modifying service logic
- a contract change is required to make the stack work
- environment configuration becomes ambiguous
- the smoke test cannot represent the intended integration path
