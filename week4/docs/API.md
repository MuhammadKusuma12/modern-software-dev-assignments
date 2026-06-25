# Week 4 API Reference

Hand-maintained summary of the FastAPI starter. Regenerate drift report with `/docs-sync` or compare against `GET /openapi.json`.

Base URL (local): `http://127.0.0.1:8000`

## Notes

### `GET /notes/`
List all notes.

**Response:** `200` — array of `NoteRead` (`id`, `title`, `content`)

### `POST /notes/`
Create a note.

**Body:** `NoteCreate` — `{ "title": string, "content": string }`  
**Response:** `201` — `NoteRead`

### `GET /notes/search/`
Search notes by title or content (case-sensitive substring match via SQL `contains`).

**Query:** `q` (optional string) — if omitted, returns all notes  
**Response:** `200` — array of `NoteRead`

### `GET /notes/{note_id}`
Fetch one note.

**Response:** `200` — `NoteRead` | `404` — note not found

## Action items

### `GET /action-items/`
List all action items.

**Response:** `200` — array of `ActionItemRead` (`id`, `description`, `completed`)

### `POST /action-items/`
Create an action item.

**Body:** `ActionItemCreate` — `{ "description": string }`  
**Response:** `201` — `ActionItemRead`

### `PUT /action-items/{item_id}/complete`
Mark an action item completed.

**Response:** `200` — `ActionItemRead` | `404` — item not found

## Static / meta

| Path | Description |
|------|-------------|
| `GET /` | Serves `frontend/index.html` |
| `GET /static/*` | Static assets (`app.js`, `styles.css`) |
| `GET /docs` | Swagger UI |
| `GET /openapi.json` | OpenAPI schema (source of truth for drift checks) |
