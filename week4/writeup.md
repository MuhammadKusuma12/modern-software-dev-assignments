# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations:
- [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Code slash commands / skills](https://code.claude.com/docs/en/slash-commands)
- Week 4 assignment (`week4/assignment.md`)

This assignment took me about 1 hours to do.


## YOUR RESPONSES
### Automation #1 — Claude custom slash commands
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by Anthropic's guidance to **keep commands focused, idempotent, and tool-scoped** ([best practices](https://www.anthropic.com/engineering/claude-code-best-practices)): each slash command encodes one repeatable workflow with explicit `$ARGUMENTS`, `argument-hint`, and `allowed-tools` frontmatter so runs are predictable in headless or interactive Claude Code sessions. Examples in the assignment (`tests.md`, `docs-sync.md`, `refactor-module.md`) map directly to pain points in the week4 starter: running pytest, keeping API docs aligned with OpenAPI, and safe refactors.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Three project-scoped commands in `.claude/commands/` for the week4 FastAPI app.
>
> | Command | File | Input | Output |
> |---------|------|-------|--------|
> | `/tests` | `tests.md` | Optional pytest path/marker (`$ARGUMENTS`) | Pass/fail summary; coverage report if green |
> | `/docs-sync` | `docs-sync.md` | Optional base URL (default `http://127.0.0.1:8000`) | Updated `week4/docs/API.md` + route delta/TODOs |
> | `/refactor-module` | `refactor-module.md` | Old path `$0`, new path `$1` | Checklist of touched files + lint/test status |
>
> **Steps (common pattern):** cd to `week4/` → run bounded bash (pytest, curl, make) → summarize failures or next actions → stop on red tests (no drive-by refactors).

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **Run in Claude Code** (from repo root, after cloning):
> ```
> /tests
> /tests backend/tests/test_notes.py
> /tests -k search
> /docs-sync
> /docs-sync http://127.0.0.1:8000
> /refactor-module backend/app/services/extract.py backend/app/services/parser.py
> ```
> Restart Claude Code after adding/editing command files so `/help` lists them.
>
> **Expected outputs:**
> - `/tests`: pytest summary; on success, terminal coverage table for `backend/app`
> - `/docs-sync`: diff-style list of added/changed/removed routes vs `docs/API.md`
> - `/refactor-module`: file checklist and green `make test`
>
> **Safety / rollback:**
> - Commands restrict tools via `allowed-tools` (Bash, Read, Write, Edit, Grep)
> - `/docs-sync` is docs-only; rollback with `git checkout -- week4/docs/API.md`
> - `/refactor-module` refuses renames outside `week4/backend/`; full rollback via `git checkout -- week4/`

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Developer manually `cd week4`, remembers `PYTHONPATH=.`, runs pytest, optionally installs pytest-cov, curls `/openapi.json`, hand-edits `API.md`, greps imports after a rename, and re-runs lint/test — easy to skip a step or use wrong cwd.
>
> **After:** Single slash invocation encodes cwd, command sequence, failure handling, and output format. Teammates share identical workflows via version-controlled Markdown in `.claude/commands/`.

e. How you used the automation to enhance the starter application
> I used the slash commands to verify and document every feature added to the starter app, and the `CLAUDE.md` guidance to keep implementations consistent.
>
> **Concrete examples:**
> 1. **Verified the notes search endpoint with `/tests`.** After implementing `GET /notes/search?q=...` in `backend/app/routers/notes.py`, I ran `/tests backend/tests/test_notes.py` to confirm the search query returns case-insensitive matches and that the existing list/create/get flows still pass. The command also produced coverage for `backend/app`, showing the new branch is exercised.
> 2. **Kept API docs current with `/docs-sync`.** After adding action-item completion (`PUT /action-items/{id}/complete`) and the notes search route, I ran `/docs-sync http://127.0.0.1:8000` to refresh `week4/docs/API.md`. The command detected the new endpoint entries, inserted them under the correct router tags, and reported route deltas so I could fill in missing response schema details.
> 3. **Guarded test quality with `CLAUDE.md` workflow rules.** The week4 `CLAUDE.md` enforces the "failing test → implement → make test → make format" loop and warns against using `data/app.db` in tests. Following that, I wrote the test for `extract_action_items` (`backend/tests/test_extract.py`) before extending `backend/app/services/extract.py` to recognize `#tag` patterns, then ran `make test` and `make format` end-to-end.
> 4. **Documented safe refactors for future work.** I prepared `/refactor-module` so the extraction module can be renamed safely (e.g. `extract.py` → `parser.py`) if the tag-parsing logic grows. The command refuses paths outside `backend/`, runs `git mv`, fixes imports, and gates on `make test`/`make lint`.


### Automation #2 — `CLAUDE.md` guidance files
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) recommend treating project instructions as an **iterative prompt**: concise, actionable, and scoped to how the repo is actually run. The assignment's `CLAUDE.md` examples (entry points, style guardrails, workflow snippets) are split across two files so global repo context does not drown week4-specific detail.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Auto-loaded guidance when Claude Code starts in this repository.
>
> | File | Scope | Contents |
> |------|-------|----------|
> | `CLAUDE.md` (repo root) | All weeks | Layout table, safe/unsafe commands, week4 quick reference, slash command index |
> | `week4/CLAUDE.md` | Starter app | Architecture tree, DB/test conventions, endpoint workflow, extraction notes, drift check |
>
> **Implicit inputs:** None — files load automatically per session.
>
> **Outputs:** Claude follows documented workflows (test-first endpoints, no prod DB in tests, format/lint gates) without re-explaining repo structure each turn.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> **Run:** No command — open Claude Code in the repo root. Both `CLAUDE.md` files are picked up based on working directory context.
>
> **Verify:** Ask Claude "How do I run week4 tests?" — answer should cite `make test` from `week4/` and `backend/tests/`.
>
> **Iterate:** Edit markdown, start a new session (or `/clear`) to pick up changes.
>
> **Rollback:** `git checkout -- CLAUDE.md week4/CLAUDE.md`

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Every session re-discovered that tests need `PYTHONPATH=.`, routers live under `backend/app/routers/`, and the frontend is static — leading to wrong-directory commands and accidental use of `data/app.db` in tests.
>
> **After:** Persistent guardrails encode entry points, quality gates (black/ruff/pytest), and the "failing test → implement → format" loop. Custom slash commands are cross-linked from root `CLAUDE.md` so agents know when to invoke `/tests` or `/docs-sync`.

e. How you used the automation to enhance the starter application
> The `CLAUDE.md` files acted as a persistent prompt that shaped how I extended the starter app without re-explaining the repo structure each time.
>
> **Concrete examples:**
> 1. **Implemented notes search and action-item completion following the documented workflow.** Both `CLAUDE.md` files specify: write a failing test first, implement the route, then run `make test` and `make format`. I used that checklist to add `GET /notes/search?q=...` and `PUT /action-items/{id}/complete`, validating each step with the test runner before moving on.
> 2. **Extended `extract.py` for tag parsing.** The week4 `CLAUDE.md` points to `backend/app/services/extract.py` as the extraction home and says to extend `backend/tests/test_extract.py` with edge cases. I added regex-based `#tag` extraction, then wrote tests for hashtag and bullet patterns, running `make format` afterward to satisfy the black/ruff gates.
> 3. **Avoided test/database pitfalls.** The guidance explicitly warns: "never point tests at `data/app.db`" and "committing `.env` or API keys". During feature work I relied on the in-memory/temp DB fixture in `conftest.py`, and the root `CLAUDE.md` kept me from accidentally running commands that would wipe local seed data.


### *(Optional) Automation #3*
*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> N/A — only two automations required (slash commands + CLAUDE.md).

b. Design of each automation, including goals, inputs/outputs, steps
> N/A

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> N/A

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> N/A

e. How you used the automation to enhance the starter application
> N/A
