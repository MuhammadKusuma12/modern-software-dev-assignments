# Week 4 — Developer command center

FastAPI backend, SQLite via SQLAlchemy, static HTML/JS frontend. No Node toolchain.

## Run & test
```bash
cd week4
conda activate cs146s   # if using course env
make run                # http://127.0.0.1:8000 — UI at /, OpenAPI at /docs
make test               # PYTHONPATH=. pytest -q backend/tests
make format && make lint
```

## Architecture
```
backend/app/
  main.py           # FastAPI app, mounts /static, includes routers
  db.py             # engine, session, get_db, apply_seed_if_needed()
  models.py         # Note, ActionItem ORM models
  schemas.py        # Pydantic request/response models
  routers/
    notes.py        # GET/POST /notes, GET /notes/search/, GET /notes/{id}
    action_items.py # CRUD-ish /action-items, PUT .../complete
  services/
    extract.py      # Parse note text into action items / tags
frontend/
  index.html, app.js, styles.css
data/
  seed.sql          # idempotent seed; DB file created at runtime
docs/
  TASKS.md          # suggested agent-driven improvements
  API.md            # hand-maintained API reference (keep in sync with OpenAPI)
```

## Database
- SQLite file: `data/app.db` (created on startup)
- `apply_seed_if_needed()` runs `data/seed.sql` once
- Tests use in-memory/temp DB via `conftest.py` — never point tests at `data/app.db`

## Style & quality gates
- **Formatter:** black
- **Linter:** ruff (`pre-commit-config.yaml` in this folder)
- Type hints on public functions; FastAPI `response_model` on routes
- HTTP errors: 404 for missing resources, 400 for validation (see `schemas.py`)

## When adding an endpoint
1. Add/update test in `backend/tests/test_<router>.py`
2. Add Pydantic schema if needed in `schemas.py`
3. Implement route in `backend/app/routers/`
4. Wire frontend in `frontend/app.js` if user-facing
5. Run `make test` and `make format`
6. Update `docs/API.md` or run `/docs-sync`

## When changing extraction logic
- Edit `backend/app/services/extract.py`
- Extend `backend/tests/test_extract.py` with edge cases (#tags, bullet lines, etc.)

## Commands to avoid here
- `rm -rf data/` — loses local DB
- Running uvicorn from repo root without `cd week4` (imports break)
- Committing `.env` or API keys

## OpenAPI drift
After router changes, compare `/openapi.json` with `docs/API.md`. Task list item 7 in `docs/TASKS.md` describes the manual process; prefer `/docs-sync` for repeatability.
