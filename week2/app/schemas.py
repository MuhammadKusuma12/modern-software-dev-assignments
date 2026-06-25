"""Pydantic schemas defining API request/response contracts."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


# --- Extraction schemas ---


class ExtractRequest(BaseModel):
    text: str = Field(..., description="Free-form notes to extract action items from")
    save_note: bool = Field(default=False, description="Persist the input text as a note")


class ActionItemOut(BaseModel):
    id: int
    text: str


class ExtractResponse(BaseModel):
    note_id: Optional[int] = None
    items: list[ActionItemOut]


# --- Action item schemas ---


class ActionItemDetail(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str


class MarkDoneRequest(BaseModel):
    done: bool = True


class MarkDoneResponse(BaseModel):
    id: int
    done: bool


# --- Note schemas ---


class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1)


class NoteOut(BaseModel):
    id: int
    content: str
    created_at: str


class NoteListResponse(BaseModel):
    notes: list[NoteOut]


# --- LLM extraction schema (used by Ollama structured output) ---


class ActionItemsLLMResult(BaseModel):
    """Structured output schema for Ollama action-item extraction."""

    items: list[str]
