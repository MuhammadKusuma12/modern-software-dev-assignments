from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NotePatch, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])

# Allowlist of safe sort fields to prevent attribute injection
SAFE_SORT_FIELDS = {"created_at", "updated_at", "title", "id"}


@router.get("/", response_model=list[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[NoteRead]:
    stmt = select(Note)
    if q:
        # Use parameterized binding via SQLAlchemy ORM — safe from SQL injection
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    # Use allowlist instead of hasattr to prevent attribute injection
    if sort_field in SAFE_SORT_FIELDS:
        stmt = stmt.order_by(order_fn(getattr(Note, sort_field)))
    else:
        stmt = stmt.order_by(desc(Note.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, payload: NotePatch, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.get("/search", response_model=list[NoteRead])
def search_notes(q: str, db: Session = Depends(get_db)) -> list[NoteRead]:
    """Safe search endpoint using SQLAlchemy ORM parameterized queries."""
    stmt = (
        select(Note)
        .where((Note.title.contains(q)) | (Note.content.contains(q)))
        .order_by(Note.created_at.desc())
        .limit(50)
    )
    rows = db.execute(stmt).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


# ---------------------------------------------------------------------------
# Debug endpoints — intentionally vulnerable for security scanning exercises.
# These are DISABLED in production and should only be enabled during
# controlled security training sessions.
# ---------------------------------------------------------------------------
# To enable: set ENABLE_DEBUG_ENDPOINTS=true in your environment.
import os  # noqa: E402

_ENABLE_DEBUG = os.getenv("ENABLE_DEBUG_ENDPOINTS", "").lower() in ("true", "1", "yes")


@router.get("/debug/hash-md5")
def debug_hash_md5(q: str) -> dict[str, str]:
    if not _ENABLE_DEBUG:
        raise HTTPException(status_code=404, detail="Not found")
    import hashlib

    return {"algo": "md5", "hex": hashlib.md5(q.encode()).hexdigest()}


@router.get("/debug/eval")
def debug_eval(expr: str) -> dict[str, str]:
    if not _ENABLE_DEBUG:
        raise HTTPException(status_code=404, detail="Not found")
    # SECURITY: eval() is dangerous. This endpoint is gated behind
    # ENABLE_DEBUG_ENDPOINTS and should only be used in isolated training.
    result = str(eval(expr))  # noqa: S307
    return {"result": result}


@router.get("/debug/run")
def debug_run(cmd: str) -> dict[str, str]:
    if not _ENABLE_DEBUG:
        raise HTTPException(status_code=404, detail="Not found")
    import subprocess

    # SECURITY: shell=True is dangerous. Gated behind ENABLE_DEBUG_ENDPOINTS.
    completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)  # noqa: S602,S603
    return {"returncode": str(completed.returncode), "stdout": completed.stdout, "stderr": completed.stderr}


@router.get("/debug/fetch")
def debug_fetch(url: str) -> dict[str, str]:
    if not _ENABLE_DEBUG:
        raise HTTPException(status_code=404, detail="Not found")
    from urllib.request import urlopen

    with urlopen(url) as res:  # noqa: S310
        body = res.read(1024).decode(errors="ignore")
    return {"snippet": body}


@router.get("/debug/read")
def debug_read(path: str) -> dict[str, str]:
    if not _ENABLE_DEBUG:
        raise HTTPException(status_code=404, detail="Not found")
    # SECURITY: Arbitrary file read. Gated behind ENABLE_DEBUG_ENDPOINTS.
    # Restrict to a safe base directory when enabled.
    from pathlib import Path as PathLib

    safe_base = PathLib("data").resolve()
    requested = (safe_base / path).resolve()
    if not str(requested).startswith(str(safe_base)):
        raise HTTPException(status_code=400, detail="Path traversal denied")
    try:
        content = requested.read_text(encoding="utf-8", errors="ignore")[:1024]
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc))
    return {"snippet": content}