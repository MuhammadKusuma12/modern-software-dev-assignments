"""SQLite database layer with typed record models."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Optional


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


@dataclass(frozen=True)
class NoteRecord:
    id: int
    content: str
    created_at: str


@dataclass(frozen=True)
class ActionItemRecord:
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str


def ensure_data_directory_exists() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Yield a SQLite connection with row-factory enabled; auto-closes on exit."""
    ensure_data_directory_exists()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def init_db() -> None:
    """Create tables if they do not already exist."""
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (note_id) REFERENCES notes(id)
            );
            """
        )
        connection.commit()


def _row_to_note(row: sqlite3.Row) -> NoteRecord:
    return NoteRecord(id=row["id"], content=row["content"], created_at=row["created_at"])


def _row_to_action_item(row: sqlite3.Row) -> ActionItemRecord:
    return ActionItemRecord(
        id=row["id"],
        note_id=row["note_id"],
        text=row["text"],
        done=bool(row["done"]),
        created_at=row["created_at"],
    )


def insert_note(content: str) -> int:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        connection.commit()
        return int(cursor.lastrowid)


def list_notes() -> list[NoteRecord]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
        return [_row_to_note(row) for row in cursor.fetchall()]


def get_note(note_id: int) -> Optional[NoteRecord]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, content, created_at FROM notes WHERE id = ?",
            (note_id,),
        )
        row = cursor.fetchone()
        return _row_to_note(row) if row else None


def insert_action_items(items: list[str], note_id: Optional[int] = None) -> list[int]:
    with get_connection() as connection:
        cursor = connection.cursor()
        ids: list[int] = []
        for item in items:
            cursor.execute(
                "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                (note_id, item),
            )
            ids.append(int(cursor.lastrowid))
        connection.commit()
        return ids


def list_action_items(note_id: Optional[int] = None) -> list[ActionItemRecord]:
    with get_connection() as connection:
        cursor = connection.cursor()
        if note_id is None:
            cursor.execute(
                "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC"
            )
        else:
            cursor.execute(
                "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
                (note_id,),
            )
        return [_row_to_action_item(row) for row in cursor.fetchall()]


def mark_action_item_done(action_item_id: int, done: bool) -> None:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE action_items SET done = ? WHERE id = ?",
            (1 if done else 0, action_item_id),
        )
        connection.commit()
