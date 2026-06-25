---
description: Warp Drive Automation — Multi-agent workflow for concurrent task execution
---

# Week 5 Multi-Agent Workflow

Coordinate multiple Warp agents to work on independent tasks concurrently.

## Setup

```bash
# Create worktrees for each agent (run from repo root)
git worktree add ../week5-agent-backend agent-backend
git worktree add ../week5-agent-frontend agent-frontend
git worktree add ../week5-agent-tests agent-tests
```

## Agent Roles

### Agent 1: Backend API
- **Tab:** 1
- **Worktree:** `../week5-agent-backend`
- **Tasks:** Implement API endpoints (routers, schemas, services)
- **Command:**
  ```bash
  cd ../week5-agent-backend/week5
  # Implement backend changes...
  PYTHONPATH=. python -m pytest -q backend/tests --maxfail=1 -x
  ```

### Agent 2: Frontend UI
- **Tab:** 2
- **Worktree:** `../week5-agent-frontend`
- **Tasks:** Update frontend HTML/JS/CSS
- **Command:**
  ```bash
  cd ../week5-agent-frontend/week5
  # Implement frontend changes...
  ```

### Agent 3: Tests
- **Tab:** 3
- **Worktree:** `../week5-agent-tests`
- **Tasks:** Write and run tests
- **Command:**
  ```bash
  cd ../week5-agent-tests/week5
  PYTHONPATH=. python -m pytest -q backend/tests --cov=backend/app --cov-report=term-missing
  ```

## Coordination Strategy

1. **API Contract First:** Finalize the OpenAPI schema before distributing tasks
2. **Isolated Worktrees:** Each agent works in its own directory — no file conflicts
3. **Merge & Verify:** After all agents complete, merge branches and run full suite:
   ```bash
   cd /home/mukuma/RPL/modern-software-dev-assignments
   git merge agent-backend
   git merge agent-frontend
   git merge agent-tests
   cd week5 && PYTHONPATH=. python -m pytest -q backend/tests --cov=backend/app --cov-report=term-missing
   ```

## Saved Prompt (copy into Warp Drive)

```
Title: Week 5 Multi-Agent Setup
Prompt:
Set up a multi-agent workflow for week5:
1. Create git worktrees: git worktree add ../week5-agent-backend agent-backend && git worktree add ../week5-agent-frontend agent-frontend && git worktree add ../week5-agent-tests agent-tests
2. Open 3 Warp tabs, one for each worktree
3. Assign: Tab 1 = backend API, Tab 2 = frontend UI, Tab 3 = tests
4. After all complete, merge branches and run full test suite with coverage