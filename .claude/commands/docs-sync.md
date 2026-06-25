---
description: Sync week4/docs/API.md with live OpenAPI schema and list route drift
argument-hint: [optional base URL, default http://127.0.0.1:8000]
allowed-tools: Bash, Read, Write, Edit, Grep
---

Keep Week 4 API documentation in sync with the running FastAPI app.

## Context
- App entry: `week4/backend/app/main.py`
- Target doc: `week4/docs/API.md` (create if missing)
- OpenAPI URL: `{base}/openapi.json` where base is `$ARGUMENTS` or `http://127.0.0.1:8000`
- Reference tasks: `week4/docs/TASKS.md` (task 7 — docs drift check)

## Steps
1. Confirm the server is reachable:
   ```bash
   curl -sf "${BASE:-http://127.0.0.1:8000}/openapi.json" -o /tmp/week4-openapi.json
   ```
   If curl fails, start the app from `week4/` with `make run` in the background, wait a few seconds, and retry once.
2. Read `/tmp/week4-openapi.json` and the current `week4/docs/API.md`.
3. For each path/method in OpenAPI, ensure `API.md` documents:
   - HTTP method and path
   - Summary/purpose
   - Request body or query params (with types)
   - Response shape and status codes
   - Example curl if non-obvious
4. Update `week4/docs/API.md` idempotently (preserve human-readable sections; fix inaccuracies only).
5. Produce a **delta report**:
   - Routes added/removed/changed since last doc version
   - Fields or status codes that still drift
   - TODOs for undocumented endpoints
6. Do **not** change router code unless the user asked for an API change — this command is docs-only.

## Safety
- Never commit secrets or `.env` contents.
- Back up `API.md` mentally by showing a diff summary before writing.
- Rollback: `git checkout -- week4/docs/API.md` restores the previous doc.
