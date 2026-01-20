# AGENTS.md — Platform Workspace Rules

These rules apply to all AI agents working across the platform repositories.
Violating a rule makes the work invalid, even if it compiles.

## Core Rules

1) Scope to one repo
- A single work order should modify ONE repository whenever possible.
- Cross-repo changes require an explicit plan and merge order.

2) Contracts first (platform-apis)
- If an API/gRPC/event schema change is needed, it must be made in platform-apis.
- Do not “imply” contract changes by editing callers/servers without updating contracts.

3) No speculative behavior
- If requirements are unclear, STOP and ask for clarification (or propose a work order).
- Do not invent endpoints, fields, or event types.

4) No drive-by refactors
- Only change what the work order requires.
- Do not rename, restructure, or “clean up” unrelated code.

5) Executable completion
- A work order is only “done” after running the required validation commands.
- Report validation commands and results in the work order notes / PR description.

6) Event model stability
- Do not add, remove, or reinterpret streaming event types without updating platform-apis.
- Transport (gRPC vs SSE) must not change event meaning.


## Escalation (Stop Conditions)

Agents MUST STOP and report if:
- A contract change is required but not planned.
- Validation fails due to something outside the work order’s scope.
- A change would break repo ownership boundaries (see ARCHITECTURE.md).
- Multiple repos must be edited simultaneously without a merge plan.

## Ownership Boundaries (Hard Constraints)

- UIP: client-only; consumes PCP via HTTP/SSE. No business logic.
- PCP: public API + chat history; calls AISP via gRPC; no LLM calls.
- AISP: orchestration + LLM calls; internal APIs only; owns AI-specific DBs.
- platform-apis: contracts only; no business logic.
- platform-stack: runtime harness only; no product logic.


## Integration Authority

Final correctness is determined by:
- repo-level validation in each changed repo, AND
- end-to-end smoke validation via platform-stack wiring.
