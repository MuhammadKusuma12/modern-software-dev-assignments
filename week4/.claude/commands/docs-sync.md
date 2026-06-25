---
argument-hint: [base-url]
description: Sync week4/docs/API.md from OpenAPI schema
allowed-tools: Bash Read Write Grep
---

Sync API documentation against running OpenAPI schema.

Steps:
1. cd week4
2. Determine base URL: use $ARGUMENTS if provided, else default `http://127.0.0.1:8000`
3. Confirm server is reachable: `curl -fsS "$base_url/health" || curl -fsS "$base_url/"` (either is fine for this app)
4. Fetch OpenAPI: `curl -fsS "$base_url/openapi.json" -o /tmp/week4-openapi.json`
5. Read current `docs/API.md`
6. Update `docs/API.md`:
   - Base URL line stays
   - For each route in OpenAPI paths, ensure an entry exists (method, path, summary, request body, responses)
   - Preserve readability: group by router tags, keep markdown headers
   - If a route was removed, move it to a "Removed" section with a TODO
   - If a new route exists, add it with a TODO placeholder until filled in
7. Report: list of added, changed, and removed routes vs previous file
8. Exit with a checklist of TODOs for manual review (e.g. "Fill in response schema details for new POST endpoint")
