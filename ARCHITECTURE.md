# Platform Architecture

This document describes the platform’s high-level architecture and repository
responsibilities. It is the shared mental model for humans and planner agents.

---

## Top-Level Request Flow (Chat Turn)

Primary path for a single chat turn:

UIP -> HTTP -> PCP -> gRPC -> AISP -> LLM  
AISP -> gRPC stream -> PCP -> SSE -> UIP

Key properties:
- UIP communicates with PCP via public HTTP APIs and SSE.
- PCP communicates with AISP via an internal gRPC streaming API.
- AISP is the only component permitted to call an LLM.
- PCP acts as a protocol adapter: gRPC stream → SSE stream.
- Event semantics must be preserved end-to-end.

---

## Repository Responsibilities

### user-interface-plane (UIP)

Client applications and shared frontend packages.

Responsibilities:
- Rendering, interaction logic, client-side state
- Consuming PCP HTTP APIs and SSE streams
- Presenting streamed chat turn events to the user

Constraints:
- No business logic
- No direct access to internal services
- No awareness of gRPC or AISP internals

Future (non-binding):
- Tauri desktop app embedding `web-app`
- Separate mobile client

---

### platform-control-plane (PCP)

Public API and request coordination layer.  
Implemented in Rust using Axum.

Responsibilities:
- Owns the public HTTP API surface
- Owns chat history persistence
- Owns user-uploaded and AI-generated artifacts (future)
- Forwards chat turn requests to AISP via internal gRPC API
- Translates AISP gRPC streams into SSE streams for UIP

Constraints:
- Must not call LLMs directly
- Must preserve streaming semantics and ordering
- Must propagate request identity end-to-end
- Treats AISP as an internal dependency via stable contracts

---

### ai-services-plane (AISP)

AI execution and orchestration layer.  
Implemented in Python using FastAPI + gRPC.

Responsibilities:
- Owns the AI orchestration graph (LangGraph)
- Serves the main chat turn **gRPC streaming API** consumed by PCP
- Serves additional HTTP APIs consumed by PCP
- Owns AI-specific databases (e.g., future History RAG DB)
- The only component allowed to call an LLM

Constraints:
- No public client-facing APIs
- No knowledge of UIP
- No persistence of chat history (beyond AI-specific data)
- Streaming events must conform to platform-apis contracts

---

### platform-apis

Contract source of truth for all cross-repo boundaries.

Contains:
- **OpenAPI**
  - PCP public HTTP APIs
- **AsyncAPI**
  - Chat turn SSE API exposed by PCP
- **Protobuf**
  - Internal PCP → AISP gRPC streaming API

Constraints:
- No business logic
- No implementation details
- All client/server code is derived from these definitions
- Contract changes must be explicit and reviewed

---

### platform-stack

Local runtime and integration harness.

Responsibilities:
- docker-compose definitions for the full stack
- Service wiring and environment configuration
- Observability infrastructure (Grafana, Tempo, Loki, Prometheus, Alloy)
- End-to-end smoke validation entrypoints

Migration note:
- PCP and AISP currently contain local docker-compose files.
- Long-term, platform-stack should be the single “run everything” source of truth.

---

## Event Model

Both gRPC and SSE streams operate on a shared conceptual event model.

Current event types:
- `token_delta`
- `metrics`
- `done`
- `error`

Notes:
- gRPC stream events are defined in Protobuf
- SSE events are defined in AsyncAPI
- PCP must not reinterpret or reorder events
- Event envelope semantics must remain consistent across transports

---

## Key Invariants

1) Contracts are authoritative  
All cross-service boundaries are defined in platform-apis.  
No repo may diverge from or implicitly extend contracts.

2) LLM access is restricted  
Only AISP may call an LLM.

3) Streaming semantics are preserved  
Events emitted by AISP must arrive at UIP unchanged in meaning and order.

4) Ownership boundaries are enforced  
- UIP: presentation only  
- PCP: public API, chat history, artifacts  
- AISP: AI orchestration and AI-specific storage  
- platform-apis: contracts only  
- platform-stack: runtime only

5) Integration defines correctness  
A change is correct only if:
- repo-level validation passes, and
- end-to-end smoke validation passes via platform-stack

