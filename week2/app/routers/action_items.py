"""Action item extraction and management endpoints."""

from __future__ import annotations

from typing import Callable, Optional

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import (
    ActionItemDetail,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm

router = APIRouter(prefix="/action-items", tags=["action-items"])


def _run_extraction(
    text: str,
    save_note: bool,
    extractor: Callable[[str], list[str]],
) -> ExtractResponse:
    note_id: Optional[int] = None
    if save_note:
        note_id = db.insert_note(text)

    items = extractor(text)
    ids = db.insert_action_items(items, note_id=note_id)
    return ExtractResponse(
        note_id=note_id,
        items=[{"id": item_id, "text": item_text} for item_id, item_text in zip(ids, items)],
    )


@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    return _run_extraction(text, payload.save_note, extract_action_items)


@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    """LLM-powered extraction endpoint using Ollama (Exercise 4)."""
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    try:
        return _run_extraction(text, payload.save_note, extract_action_items_llm)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"LLM extraction failed: {exc}. Ensure Ollama is running.",
        ) from exc


@router.get("", response_model=list[ActionItemDetail])
def list_all(note_id: Optional[int] = None) -> list[ActionItemDetail]:
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemDetail(
            id=r.id,
            note_id=r.note_id,
            text=r.text,
            done=r.done,
            created_at=r.created_at,
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=MarkDoneResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> MarkDoneResponse:
    db.mark_action_item_done(action_item_id, payload.done)
    return MarkDoneResponse(id=action_item_id, done=payload.done)
