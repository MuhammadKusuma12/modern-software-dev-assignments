from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemRead

router = APIRouter(prefix="/action-items", tags=["action_items"])


@router.get("/", response_model=dict)
def list_items(
    completed: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
) -> dict:
    query = select(ActionItem)
    count_query = select(func.count(ActionItem.id))

    if completed is not None:
        query = query.where(ActionItem.completed == completed)
        count_query = count_query.where(ActionItem.completed == completed)

    total = db.execute(count_query).scalar() or 0
    query = query.offset((page - 1) * page_size).limit(page_size)
    rows = db.execute(query).scalars().all()
    return {
        "items": [ActionItemRead.model_validate(row).model_dump() for row in rows],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.post("/bulk-complete", response_model=dict)
def bulk_complete(item_ids: list[int], db: Session = Depends(get_db)) -> dict:
    items = db.execute(select(ActionItem).where(ActionItem.id.in_(item_ids))).scalars().all()
    found_ids = {item.id for item in items}
    missing = [i for i in item_ids if i not in found_ids]
    if missing:
        raise HTTPException(
            status_code=404,
            detail=f"Action items not found: {missing}",
        )
    for item in items:
        item.completed = True
    db.flush()
    return {"ok": True, "completed": len(items)}