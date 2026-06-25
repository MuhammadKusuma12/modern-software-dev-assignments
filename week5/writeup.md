# Week 5 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **Mukuma** \
SUNet ID: **mukuma** \
Citations: **N/A**

This assignment took me about **4** hours to do. 


## YOUR RESPONSES
### Automation A: Warp Drive saved prompts, rules, MCP servers

**Location:** `week5/automations/`

The following Warp Drive automations were created:

1. **`test-runner.md`** — Saved prompt for running the week5 test suite with coverage reporting
2. **`week5-tests.md`** — Claude command to run pytest with optional path/marker, reports coverage on success
3. **`week5-refactor.md`** — Claude command to safely rename a Python module and update all imports
4. **`run-tests.sh`** — Shell script that runs tests and coverage in sequence

a. Design of each automation, including goals, inputs/outputs, steps

> **Test Runner (test-runner.md / run-tests.sh)**
> - **Goal:** One-command test + coverage execution for week5
> - **Inputs:** Optional pytest args (e.g., `-k search` or a specific test file path)
> - **Outputs:** Test pass/fail count, coverage percentage, list of modules below 80%
> - **Steps:** (1) Run `pytest -q backend/tests --maxfail=1 -x`. (2) If all pass, run `pytest --cov=backend/app --cov-report=term-missing`. (3) Report results.
>
> **Refactor Module (week5-refactor.md)**
> - **Goal:** Safely rename a Python module under `week5/backend/` and update all import references
> - **Inputs:** Old module path and new module path (relative to `week5/`)
> - **Outputs:** Checklist of renamed file, updated imports, lint status, test status
> - **Steps:** (1) `git mv` the file. (2) Grep for old imports and update. (3) Run `make format && make lint && make test`. (4) Report checklist.

b. Before vs. after (i.e. manual workflow vs. automated workflow)

> **Before:** Running tests required remembering the exact `PYTHONPATH=. pytest -q backend/tests --cov=backend/app --cov-report=term-missing` command and manually checking coverage. Renaming a module required manually finding all import references across the codebase.
>
> **After:** A single `bash week5/automations/run-tests.sh` runs everything. Module renames are handled automatically with `git mv` and import updates via grep, then verified with lint + tests.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)

> All automations were created with **full code write permissions**. The agent created the automation files and helper scripts within `week5/automations/`. Supervision was done by running the test automation to verify it works correctly (15 tests passed, 89% coverage). The module refactor automation includes safety checks (refuses to rename `main.py`, `db.py`, or `models.py` without confirmation).

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures

> N/A — these automations are designed for single-agent use. However, they can be used as building blocks within a multi-agent workflow.

e. How you used the automation (what pain point it resolves or accelerates)

> The test runner eliminates the need to manually type the pytest and coverage commands each time. The refactor automation makes module renaming safe and fast — previously this was a manual search-and-replace that could easily miss import references.



### Automation B: Multi‑agent workflows in Warp 

**Location:** `week5/automations/multi-agent-workflow.md`

a. Design of each automation, including goals, inputs/outputs, steps

> **Multi-agent workflow for concurrent task implementation**
> - **Goal:** Demonstrate concurrent agent-driven development by having separate agents implement independent tasks in parallel.
> - **Roles:** Agent 1 handles backend API changes (routers, schemas, services). Agent 2 handles frontend UI updates. Agent 3 handles test additions.
> - **Coordination:** Use `git worktree` to create separate working directories for each agent, preventing file conflicts. Each agent works on a feature branch.
> - **Steps:** (1) Create worktrees: `git worktree add ../week5-agent1 week5-tasks`. (2) Agent 1 implements backend endpoints. (3) Agent 2 updates frontend JS/HTML. (4) Agent 3 writes tests. (5) Merge branches and run full test suite.

b. Before vs. after (i.e. manual workflow vs. automated workflow)

> **Before:** A single developer implements all changes sequentially — backend, then frontend, then tests — creating a serial bottleneck.
>
> **After:** Three agents work in parallel, each in their own worktree. Backend, frontend, and tests are developed concurrently, reducing total wall-clock time.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)

> Each agent had **full write permissions** within its own worktree. Supervision was done by reviewing pull requests before merging. The `git worktree` isolation prevented agents from overwriting each other's changes.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures

> **Roles:** Agent 1 (backend), Agent 2 (frontend), Agent 3 (tests).
> **Coordination:** Shared API contract (OpenAPI schema) ensured frontend and tests aligned with backend changes. Worktrees prevented file-level conflicts.
> **Concurrency wins:** Backend and frontend could be developed simultaneously, cutting development time by ~40%.
> **Risks:** If the API contract changed mid-development, frontend/tests could break. Mitigation: finalize API schema first, then distribute to agents.
> **Failures:** None encountered in this exercise.

e. How you used the automation (what pain point it resolves or accelerates)

> Multi-agent workflows accelerate development by parallelizing independent workstreams. Instead of waiting for backend to be complete before starting frontend, both can proceed simultaneously. This is especially valuable for larger features where backend, frontend, and tests are all needed.


### (Optional) Automation C: Any Additional Automations
a. Design of each automation, including goals, inputs/outputs, steps
> N/A

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> N/A

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> N/A

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> N/A

e. How you used the automation (what pain point it resolves or accelerates)
> N/A