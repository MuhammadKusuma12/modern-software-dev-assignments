# Modern Software Dev Assignments — Claude guidance

Course repo with weekly exercises (`week1/` … `week4/`). Prefer **minimal, focused diffs** that match existing style in each week folder.

## Repository layout
| Path | Purpose |
|------|---------|
| `week1/` | Prompting technique scripts (standalone Python) |
| `week2/` | FastAPI notes/action-items app (earlier iteration) |
| `week3/` | GitHub tooling exercise |
| `week4/` | **Current full-stack starter** — FastAPI + SQLite + static frontend |

When the user refers to "the app" or "starter application" without a week, assume **`week4/`**.

## Safe commands (any week)
- Read/search files, run tests, format, lint
- `conda activate cs146s` before Python work when using the course environment
- Git status/diff/log; commit **only when the user asks**

## Avoid unless explicitly requested
- Force push, hard reset, `git commit --amend` on pushed commits
- Deleting `week4/data/app.db` or seed data without backup
- Installing global system packages; prefer conda/pip in the active env
- Broad refactors across multiple weeks in one change

## Week 4 quick reference
All commands below run from **`week4/`**:
```bash
make run      # uvicorn on :8000
make test     # pytest backend/tests
make format   # black + ruff --fix
make lint     # ruff check
make seed     # apply data/seed.sql if needed
```

Entry points:
- App: `week4/backend/app/main.py`
- Routers: `week4/backend/app/routers/`
- Models/schemas: `week4/backend/app/models.py`, `schemas.py`
- Extraction logic: `week4/backend/app/services/extract.py`
- Tests: `week4/backend/tests/`
- Frontend: `week4/frontend/` (served at `/` and `/static`)
- Agent task backlog: `week4/docs/TASKS.md`

## Custom slash commands (project)
Defined in `.claude/commands/`:
- `/tests` — run pytest (+ coverage on green)
- `/docs-sync` — refresh `week4/docs/API.md` from OpenAPI
- `/refactor-module` — rename module, fix imports, verify

See `week4/CLAUDE.md` for workflow guardrails specific to the starter app.

## Workflow defaults
1. **New API endpoint:** failing test → implement → `make test` → `make format`
2. **Bug fix:** reproduce with test → fix → run affected tests
3. **Docs:** after route changes, run `/docs-sync` or update `week4/docs/API.md`

Pre-commit (optional): from `week4/`, `pre-commit install` then hooks run black + ruff on commit.
