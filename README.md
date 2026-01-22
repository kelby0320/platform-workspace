# Platform Workspace

This repository coordinates development across a multi-repo platform:
UIP (frontend), PCP (control plane), AISP (AI services), platform-apis (contracts),
and platform-stack (local runtime harness).

This repo contains process, planning, and integration scripts — not production code.

## When to Use This Repo

Use this repo whenever a change spans:
- multiple repositories, or
- a contract boundary (HTTP, SSE, gRPC streaming), or
- requires end-to-end validation via the full stack.

## Key Files

- AGENTS.md: rules for AI agents and cross-repo work
- ARCHITECTURE.md: system architecture and repo responsibilities
- repos.yaml: list of repositories and dependency relationships
- state/: sprint/work-order coordination and current plan
- src/: stack cli with support for cloning, validation, and smoke tests

## Typical Feature Workflow

1) Plan
- Break Feature X into work orders (usually 3–10).
- Each work order targets one repo and includes validation steps.

2) Execute (parallel)
- Run multiple agents in parallel, one per work order/repo/branch.

3) Review
- Review diffs and ensure repo-local AGENTS.md rules were followed.

4) Judge
- Run integration smoke validation (end-to-end) before calling the feature done.

## Architecture Summary

Chat turn flow (simplified):

UIP -> HTTP -> PCP -> gRPC -> AISP -> LLM
AISP -> gRPC stream -> PCP -> SSE -> UIP

See ARCHITECTURE.md for details.
