from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Note
from ..schemas import NoteCreate, NoteRead, NoteUpdate
from ..services.extract import extract_from_note

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=dict)
def list_notes(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
) -> dict:
    total = db.execute(select(func.count(Note.id))).scalar() or 0
    query = select(Note).offset((page - 1) * page_size).limit(page_size)
    rows = db.execute(query).scalars().all()
    return {
        "items": [NoteRead.model_validate(row).model_dump() for row in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/search/", response_model=dict)
def search_notes(
    q: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    sort: str = "created_desc",
    db: Session = Depends(get_db),
) -> dict:
    query = select(Note)
    count_query = select(func.count(Note.id))

    if q:
        like_pattern = f"%{q}%"
        filter_clause = (Note.title.ilike(like_pattern)) | (Note.content.ilike(like_pattern))
        query = query.where(filter_clause)
        count_query = count_query.where(filter_clause)

    # Sorting
    if sort == "title_asc":
        query = query.order_by(Note.title.asc())
    elif sort == "title_desc":
        query = query.order_by(Note.title.desc())
    elif sort == "created_asc":
        query = query.order_by(Note.id.asc())
    else:  # created_desc (default)
        query = query.order_by(Note.id.desc())

    total = db.execute(count_query).scalar() or 0
    query = query.offset((page - 1) * page_size).limit(page_size)
    rows = db.execute(query).scalars().all()
    return {
        "items": [NoteRead.model_validate(row).model_dump() for row in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.put("/{note_id}", response_model=NoteRead)
def update_note(
    note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)
) -> NoteRead:
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


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> None:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.flush()


@router.post("/{note_id}/extract", response_model=dict)
def extract_note(
    note_id: int,
    apply: bool = False,
    db: Session = Depends(get_db),
) -> dict:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    result = extract_from_note(note.content)

    if apply:
        # Create action items from extracted items
        for item_text in result["action_items"]:
            action_item = ActionItem(description=item_text, completed=False)
            db.add(action_item)
        db.flush()

    return result
