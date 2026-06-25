# Action Item Extractor

A minimal FastAPI + SQLite application that converts free-form notes into enumerated action items. It supports both heuristic (rule-based) extraction and LLM-powered extraction via [Ollama](https://ollama.com/).

## Overview

Paste meeting notes or todo lists into the web UI and click **Extract** to pull out actionable tasks using pattern matching (bullets, checkboxes, keyword prefixes). Click **Extract LLM** to use a local language model for smarter extraction. Saved notes can be viewed with **List Notes**.

Extracted items are persisted in SQLite and can be marked done from the UI.

## Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management
- [Ollama](https://ollama.com/) (required for LLM extraction only)

## Setup

1. Activate your conda environment:

```bash
conda activate cs146s
```

2. Install dependencies from the project root:

```bash
poetry install
```

3. Pull an Ollama model (start small):

```bash
ollama pull llama3.2
```

4. Optional: set environment variables in a `.env` file at the project root:

```bash
OLLAMA_MODEL=llama3.2
```

## Running the Server

From the project root:

```bash
poetry run uvicorn week2.app.main:app --reload
```

Open http://127.0.0.1:8000/ in your browser.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Web UI (HTML frontend) |
| `POST` | `/action-items/extract` | Heuristic extraction from notes |
| `POST` | `/action-items/extract-llm` | LLM-powered extraction via Ollama |
| `GET` | `/action-items` | List all action items (optional `?note_id=`) |
| `POST` | `/action-items/{id}/done` | Mark an action item done/undone |
| `GET` | `/notes` | List all saved notes |
| `POST` | `/notes` | Create a note |
| `GET` | `/notes/{id}` | Get a single note by ID |

### Example: Heuristic extraction

```bash
curl -X POST http://127.0.0.1:8000/action-items/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "- [ ] Set up database\n- Write tests", "save_note": true}'
```

### Example: LLM extraction

```bash
curl -X POST http://127.0.0.1:8000/action-items/extract-llm \
  -H "Content-Type: application/json" \
  -d '{"text": "We need to deploy Friday and also review the PR.", "save_note": false}'
```

## Running Tests

From the project root:

```bash
poetry run pytest week2/tests/ -v
```

LLM unit tests mock the Ollama client so they run without a live model server.

## Project Structure

```
week2/
├── app/
│   ├── main.py          # FastAPI app, lifecycle, error handlers
│   ├── config.py        # Environment-based settings
│   ├── schemas.py       # Pydantic request/response models
│   ├── db.py            # SQLite data access layer
│   ├── routers/
│   │   ├── action_items.py
│   │   └── notes.py
│   └── services/
│       └── extract.py   # Heuristic + LLM extraction logic
├── frontend/
│   └── index.html       # Minimal web UI
├── tests/
│   └── test_extract.py
└── data/
    └── app.db           # SQLite database (created at runtime)
```
