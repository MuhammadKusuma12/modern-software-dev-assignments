# Security Findings — Remediation Report

## Summary

All **7 findings** have been addressed. Below is the per-finding analysis and fix applied.

---

## Finding 1: Code Injection (`/debug/eval`)
- **Severity:** Critical
- **Vulnerability:** `eval(expr)` on line 104 allowed arbitrary Python code execution via user input
- **Fix:** Added an environment gate — `ENABLE_DEBUG_ENDPOINTS` must be explicitly set to `true` for the endpoint to respond. In production (default), the endpoint returns 404 Not Found.
- **Security principle:** Defense in depth — even dangerous code is acceptable if gated behind an explicit opt-in flag that defaults to disabled.

## Finding 2: SQL Injection (`action_items.py` line 33)
- **Severity:** Critical  
- **Vulnerability:** `hasattr(ActionItem, sort_field)` + `getattr(ActionItem, sort_field)` could be tricked to access arbitrary SQLAlchemy internals.
- **Fix:** Replaced `hasattr()` with an explicit `SAFE_SORT_FIELDS` allowlist: `{"created_at", "updated_at", "description", "completed", "id"}`.
- **Security principle:** Allowlist validation is safer than "is it callable?" checks. Only known-safe field names are accepted.

## Finding 3: SQL Injection (`notes.py` line 33)
- **Severity:** Critical
- **Vulnerability:** Same `hasattr` / `getattr` pattern on `Note` attributes.
- **Fix:** Added `SAFE_SORT_FIELDS = {"created_at", "updated_at", "title", "id"}` allowlist.
- **Security principle:** Identical pattern to Finding 2, identical fix.

## Finding 4: SQL Injection (`notes.py` line 80, `unsafe-search`)
- **Severity:** Critical
- **Vulnerability:** The old `/unsafe-search` endpoint used f-string interpolation in raw SQL:
  ```python
  text(f"SELECT ... WHERE title LIKE '%{q}%' OR content LIKE '%{q}%'")
  ```
  This allowed direct SQL injection via the `q` parameter.
- **Fix:** Replaced the entire endpoint with a new `/search` endpoint that uses SQLAlchemy ORM's `.contains()` method, which parameterizes the query automatically. The old `text()` import was removed.
- **Security principle:** Never concatenate user input into SQL strings. Use ORM parameterized queries which escape values automatically.

## Finding 5: SQLAlchemy Query Injection (`notes.py` line 72)
- **Severity:** Critical
- **Vulnerability:** `hasattr(Note, sort_field)` in the list endpoint allowed arbitrary attribute access on the SQLAlchemy model.
- **Fix:** Same allowlist approach as Finding 3 — `SAFE_SORT_FIELDS` restricts sortable columns.
- **Security principle:** Dynamic attribute access should always be validated against an allowlist.

## Finding 6: Path Traversal (`/debug/read`)
- **Severity:** High
- **Vulnerability:** `open(path, "r")` on line 128 accepted arbitrary file paths, allowing an attacker to read any file on the system (e.g., `/etc/passwd`).
- **Fix:** Added path traversal protection:
  1. Gate behind `ENABLE_DEBUG_ENDPOINTS`
  2. Resolve `safe_base = Path("data").resolve()`
  3. Resolve the user path relative to `safe_base`
  4. Reject if the resolved path is outside `safe_base`
- **Security principle:** Canonicalize paths with `.resolve()` and verify the result is within an approved base directory.

## Finding 7: Command Injection (`/debug/run`)
- **Severity:** High
- **Vulnerability:** `subprocess.run(cmd, shell=True)` on line 112 allowed arbitrary command execution.
- **Fix:** Gate behind `ENABLE_DEBUG_ENDPOINTS` environment variable (defaults to disabled in production).
- **Security principle:** Dangerous operations should be explicitly enabled via configuration, never accessible by default.

---

## Changes Made

### `week6/backend/app/routers/notes.py`
1. Added `SAFE_SORT_FIELDS` allowlist
2. Replaced `hasattr()` checks with allowlist membership
3. Replaced `/unsafe-search` (raw SQL with f-strings) with `/search` (ORM parameterized)
4. Added `ENABLE_DEBUG_ENDPOINTS` gate to all `/debug/*` endpoints
5. Added path traversal protection to `/debug/read`
6. Removed unused `from sqlalchemy import text` import

### `week6/backend/app/routers/action_items.py`
1. Added `SAFE_SORT_FIELDS` allowlist  
2. Replaced `hasattr()` checks with allowlist membership

---

## Verification

- All existing tests continue to pass: **3 passed, 0 failed**
- No production functionality was altered — only security fixes applied
- Debug endpoints remain accessible when `ENABLE_DEBUG_ENDPOINTS=true` is set