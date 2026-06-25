# Security Findings Report

## Project Information

- Repository: `modern-software-dev-assignments/week6`
- Scanner: Semgrep
- Scan Date: 2026-06-25
- Total Findings: 7

---

# Finding 1: Code Injection

## Summary

- Severity: Critical
- Confidence: High
- Category: Security
- Rule: `python.fastapi.code.tainted-code-stdlib-fastapi.tainted-code-stdlib-fastapi`

## Location

File:

`backend/app/routers/notes.py`

Line:

`104`

## Description

The application might dynamically evaluate untrusted input, which can lead to a code injection vulnerability.

An attacker can execute arbitrary code, potentially gaining complete control of the system.

### Recommended Fix

- Avoid using `eval()`, `exec()`, or dynamic code execution on user input.
- Validate and sanitize all user-controlled data.
- Replace dynamic execution with safer alternatives whenever possible.

---

# Finding 2: SQL Injection

## Summary

- Severity: Critical
- Confidence: High
- Category: Security
- Rule: `python.fastapi.db.generic-sql-fastapi.generic-sql-fastapi`

## Location

File:

`backend/app/routers/action_items.py`

Line:

`33`

## Description

Untrusted input might be used to build a database query, leading to SQL injection.

An attacker could:

- Read sensitive data
- Modify database contents
- Delete records
- Execute unauthorized SQL commands

### Recommended Fix

- Use parameterized queries.
- Avoid string concatenation when building SQL.
- Use ORM query builders.

---

# Finding 3: SQL Injection

## Summary

- Severity: Critical
- Confidence: High
- Category: Security
- Rule: `python.fastapi.db.generic-sql-fastapi.generic-sql-fastapi`

## Location

File:

`backend/app/routers/notes.py`

Line:

`33`

## Description

User-controlled input is used in database query construction and may result in SQL injection.

### Recommended Fix

- Replace dynamic SQL with parameterized statements.
- Use SQLAlchemy ORM methods.

---

# Finding 4: SQL Injection

## Summary

- Severity: Critical
- Confidence: High
- Category: Security
- Rule: `python.fastapi.db.generic-sql-fastapi.generic-sql-fastapi`

## Location

File:

`backend/app/routers/notes.py`

Line:

`80`

## Description

Database query construction may contain untrusted input.

### Recommended Fix

- Use parameterized SQL.
- Avoid f-strings and string concatenation in queries.
- Validate user input before query execution.

---

# Finding 5: SQLAlchemy Query Injection

## Summary

- Severity: Critical
- Confidence: High
- Category: Security
- Rule: `python.fastapi.db.sqlalchemy-fastapi.sqlalchemy-fastapi`

## Location

File:

`backend/app/routers/notes.py`

Line:

`72`

## Description

Untrusted input might be used to build a database query, resulting in SQL injection.

### Recommended Fix

Use SQLAlchemy ORM methods such as:

```python
session.query(Model).filter(Model.id == user_input)
```

Instead of:

```python
text(f"SELECT * FROM notes WHERE id = {user_input}")
```

---

# Finding 6: Path Traversal

## Summary

- Severity: High
- Confidence: High
- Category: Security
- Rule: `python.fastapi.file.tainted-path-traversal-stdlib-fastapi.tainted-path-traversal-stdlib-fastapi`

## Location

File:

`backend/app/routers/notes.py`

Line:

`128`

## Description

The application builds a file path from potentially untrusted data.

An attacker may:

- Access arbitrary files
- Read sensitive configuration
- Overwrite files
- Escape intended directories

### Recommended Fix

- Validate filenames.
- Restrict access to approved directories.
- Use `pathlib.Path.resolve()`.
- Reject paths containing `../`.

Example:

```python
from pathlib import Path

BASE_DIR = Path("/safe/storage")

file_path = (BASE_DIR / filename).resolve()

if not str(file_path).startswith(str(BASE_DIR)):
    raise ValueError("Invalid path")
```

---

# Finding 7: Command Injection

## Summary

- Severity: High
- Confidence: High
- Category: Security
- Rule: `python.fastapi.os.tainted-os-command-stdlib-fastapi-secure-default.tainted-os-command-stdlib-fastapi-secure-default`

## Location

File:

`backend/app/routers/notes.py`

Line:

`112`

## Description

Untrusted input may be passed into OS commands.

An attacker could execute arbitrary system commands and gain full system access.

### Recommended Fix

Avoid:

```python
os.system(user_input)
```

Avoid:

```python
subprocess.run(command, shell=True)
```

Prefer:

```python
subprocess.run(
    ["ls", safe_argument],
    check=True
)
```

Additional protections:

- Use allowlists.
- Validate input.
- Avoid shell execution.
- Never pass raw user input into commands.

---

# Request For AI Review

Please:

1. Analyze each finding.
2. Explain why the code is vulnerable.
3. Show the vulnerable code pattern likely causing the issue.
4. Generate secure replacement code.
5. Explain the security principles involved.
6. Prioritize fixes from highest risk to lowest risk.
7. Identify whether any findings may be false positives.
8. Refactor the affected FastAPI routes using security best practices.
9. Provide a complete patched version of the affected files.