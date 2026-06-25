# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: Ollama structured outputs documentation (https://ollama.com/blog/structured-outputs)

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Implement extract_action_items_llm() in week2/app/services/extract.py that uses Ollama with structured JSON output (Pydantic schema) to extract action items from free-form notes. Use the format parameter per https://ollama.com/blog/structured-outputs. Model name should come from OLLAMA_MODEL env var with default llama3.2. Return empty list for blank input and dedupe results.
``` 

Generated Code Snippets:
```
week2/app/services/extract.py — lines 95-137 (extract_action_items_llm, _dedupe_preserve_order helper)
week2/app/schemas.py — lines 58-63 (ActionItemsLLMResult Pydantic schema for Ollama format)
week2/app/config.py — lines 1-24 (Settings with OLLAMA_MODEL)
```

### Exercise 2: Add Unit Tests
Prompt: 
```
Write unit tests for extract_action_items_llm() in week2/tests/test_extract.py covering bullet lists, keyword-prefixed lines, empty input, and deduplication. Mock the ollama chat call so tests run without a live Ollama server.
``` 

Generated Code Snippets:
```
week2/tests/test_extract.py — lines 33-88 (LLM tests with @patch on ollama chat)
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
Refactor the week2 backend: add Pydantic schemas for API contracts in schemas.py, typed dataclass records in db.py with contextmanager connections, app lifespan for init_db in main.py, centralized config in config.py, and consistent error handling. Update routers to use schemas instead of raw dicts.
``` 

Generated/Modified Code Snippets:
```
week2/app/schemas.py — entire file (ExtractRequest, ExtractResponse, NoteOut, ActionItemDetail, etc.)
week2/app/config.py — entire file (Settings, get_settings)
week2/app/db.py — entire file (NoteRecord, ActionItemRecord dataclasses, get_connection contextmanager)
week2/app/main.py — lines 1-48 (lifespan, exception handlers)
week2/app/routers/action_items.py — refactored to use schemas and shared _run_extraction helper
week2/app/routers/notes.py — refactored to use schemas and NoteRecord mapping
week2/app/services/extract.py — extracted _dedupe_preserve_order helper
```

### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
Add POST /action-items/extract-llm endpoint using extract_action_items_llm. Add GET /notes endpoint to list all notes. Update frontend with "Extract LLM" and "List Notes" buttons wired to these endpoints.
``` 

Generated Code Snippets:
```
week2/app/routers/action_items.py — lines 44-56 (extract_llm endpoint)
week2/app/routers/notes.py — lines 17-21 (list_all_notes GET /notes)
week2/frontend/index.html — lines 30-33 (Extract LLM, List Notes buttons), lines 44-108 (JS handlers)
```

### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Analyze the week2 codebase and generate week2/README.md with project overview, setup/run instructions, API endpoint documentation, and test suite instructions.
``` 

Generated Code Snippets:
```
week2/README.md — entire file
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope.
