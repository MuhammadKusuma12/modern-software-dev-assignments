"""Note creation and retrieval endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import NoteCreate, NoteListResponse, NoteOut

router = APIRouter(prefix="/notes", tags=["notes"])


def _note_to_schema(note: db.NoteRecord) -> NoteOut:
    return NoteOut(id=note.id, content=note.content, created_at=note.created_at)


@router.get("", response_model=NoteListResponse)
def list_all_notes() -> NoteListResponse:
    """Return all saved notes, newest first (Exercise 4)."""
    notes = db.list_notes()
    return NoteListResponse(notes=[_note_to_schema(n) for n in notes])


@router.post("", response_model=NoteOut)
def create_note(payload: NoteCreate) -> NoteOut:
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    assert note is not None
    return _note_to_schema(note)


@router.get("/{note_id}", response_model=NoteOut)
def get_single_note(note_id: int) -> NoteOut:
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return _note_to_schema(row)
