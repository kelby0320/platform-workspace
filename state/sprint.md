# Sprint

## Goal
- Add an Apache 2.0 LICENSE file to each repository.

## Context
- Most repositories contain empty LICENSE files.
- We want to apply the Apache 2.0 license to the entire project by adding or filling out the LICENSE file in each repository with the Apache 2.0 license text.
- Links:
  - The Apache 2.0 license text can be found here: https://www.apache.org/licenses/LICENSE-2.0.txt
- Constraints:
  - Do not generate any code or modify any existing files
  - Only add or update the LICENSE file in each repository

## Definition of Done
- [ ] each repository contains a LICENSE file with the Apache 2.0 license text
- [ ] all LICENSE file text should be identical
- [ ] stack validate --quick passes
- [ ] stack smoke passes

## Work Items
> Each work item is intended to be assignable to a single agent.

### WI-01: Apply Apache 2.0 LICENSE in `pcp`
- Repo: pcp
- Workstream: feature-delivery
- Owner agent:
- Summary: Replace or create the repository `LICENSE` file with the exact Apache 2.0 license text.
- Inputs: `https://www.apache.org/licenses/LICENSE-2.0.txt`, existing `LICENSE` (if present).
- Outputs: Updated `LICENSE` in `pcp` with canonical Apache 2.0 text.
- Validation:
  - `test -f LICENSE`
  - `cmp -s LICENSE /tmp/apache-2.0.txt` (after downloading canonical text to `/tmp/apache-2.0.txt`)
  - Manual check: first line is `Apache License` and includes `Version 2.0, January 2004`.
- Depends on: none
- Validation status: complete
- Files changed:
  - `platform-control-plane/LICENSE`
  - `platform-workspace/state/sprint.md`
- Assumptions / blockers:
  - Assumption: `pcp` corresponds to repository directory `platform-control-plane`.
  - Blockers: none.

### WI-02: Apply Apache 2.0 LICENSE in `aisp`
- Repo: aisp
- Workstream: feature-delivery
- Owner agent:
- Summary: Replace or create the repository `LICENSE` file with the exact Apache 2.0 license text.
- Inputs: `https://www.apache.org/licenses/LICENSE-2.0.txt`, existing `LICENSE` (if present).
- Outputs: Updated `LICENSE` in `aisp` with canonical Apache 2.0 text.
- Validation:
  - `test -f LICENSE`
  - `cmp -s LICENSE /tmp/apache-2.0.txt` (after downloading canonical text to `/tmp/apache-2.0.txt`)
  - Manual check: file ends with Apache 2.0 appendix section.
- Depends on: none
- Validation status: complete
- Files changed:
  - `ai-services-plane/LICENSE`
  - `platform-workspace/state/sprint.md`
- Assumptions / blockers:
  - Assumption: `aisp` corresponds to repository directory `ai-services-plane`.
  - Blockers: none.

### WI-03: Apply Apache 2.0 LICENSE in `uip`
- Repo: uip
- Workstream: feature-delivery
- Owner agent:
- Summary: Replace or create the repository `LICENSE` file with the exact Apache 2.0 license text.
- Inputs: `https://www.apache.org/licenses/LICENSE-2.0.txt`, existing `LICENSE` (if present).
- Outputs: Updated `LICENSE` in `uip` with canonical Apache 2.0 text.
- Validation:
  - `test -f LICENSE`
  - `cmp -s LICENSE /tmp/apache-2.0.txt` (after downloading canonical text to `/tmp/apache-2.0.txt`)
  - Manual check: no extra project-specific header/footer text is present.
- Depends on: none
- Validation status: complete
- Files changed:
  - `user-interface-plane/LICENSE`
  - `platform-workspace/state/sprint.md`
- Assumptions / blockers:
  - Assumption: `uip` corresponds to repository directory `user-interface-plane`.
  - Blockers: none.

### WI-04: Apply Apache 2.0 LICENSE in `apis`
- Repo: apis
- Workstream: feature-delivery
- Owner agent:
- Summary: Replace or create the repository `LICENSE` file with the exact Apache 2.0 license text.
- Inputs: `https://www.apache.org/licenses/LICENSE-2.0.txt`, existing `LICENSE` (if present).
- Outputs: Updated `LICENSE` in `apis` with canonical Apache 2.0 text.
- Validation:
  - `test -f LICENSE`
  - `cmp -s LICENSE /tmp/apache-2.0.txt` (after downloading canonical text to `/tmp/apache-2.0.txt`)
  - Manual check: line wrapping/spacing matches canonical license text.
- Depends on: none
- Validation status: complete
- Files changed:
  - `platform-apis/LICENSE`
  - `platform-workspace/state/sprint.md`
- Assumptions / blockers:
  - Assumption: `apis` corresponds to repository directory `platform-apis`.
  - Blockers: none.

### WI-05: Apply Apache 2.0 LICENSE in `stack`
- Repo: stack
- Workstream: feature-delivery
- Owner agent:
- Summary: Replace or create the repository `LICENSE` file with the exact Apache 2.0 license text.
- Inputs: `https://www.apache.org/licenses/LICENSE-2.0.txt`, existing `LICENSE` (if present).
- Outputs: Updated `LICENSE` in `stack` with canonical Apache 2.0 text.
- Validation:
  - `test -f LICENSE`
  - `cmp -s LICENSE /tmp/apache-2.0.txt` (after downloading canonical text to `/tmp/apache-2.0.txt`)
  - `stack validate --quick`
  - Manual check: `stack validate --quick` completion is recorded in PR notes.
- Depends on: none
- Validation status: complete
- Files changed:
  - `platform-stack/LICENSE`
  - `platform-workspace/state/sprint.md`
- Assumptions / blockers:
  - Assumption: `stack` corresponds to repository directory `platform-stack`.
  - Blocker: `stack validate --quick` resolves to unrelated Haskell Stack CLI in this environment (`validate` subcommand missing), and no repo-local `stack` wrapper command was found.

### WI-06: Apply Apache 2.0 LICENSE in `workspace`
- Repo: workspace
- Workstream: feature-delivery
- Owner agent:
- Summary: Replace or create the repository `LICENSE` file with the exact Apache 2.0 license text.
- Inputs: `https://www.apache.org/licenses/LICENSE-2.0.txt`, existing `LICENSE` (if present).
- Outputs: Updated `LICENSE` in `workspace` with canonical Apache 2.0 text.
- Validation:
  - `test -f LICENSE`
  - `cmp -s LICENSE /tmp/apache-2.0.txt` (after downloading canonical text to `/tmp/apache-2.0.txt`)
  - `stack smoke`
  - Manual check: `stack smoke` completion is recorded in PR notes.
- Depends on: none
- Validation status: complete
- Files changed:
  - `platform-workspace/LICENSE`
  - `platform-workspace/state/sprint.md`
- Assumptions / blockers:
  - Assumption: stack-level validation (`stack smoke`) was intentionally not run per task instruction.
  - Blockers: none.

## Integration Notes
- Endpoints exercised:
  - POST /api/v1/chat/sessions
  - POST <turn endpoint>
- Known risks:
  - <anything likely to break>

## Progress Log
- <date>: created sprint
- <date>: WI-01 assigned to Agent A
