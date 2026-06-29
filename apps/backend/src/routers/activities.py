"""Activities CRUD routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.deps import get_current_user
from src.models.db import Activity, Module, User
from src.models.schemas import ActivityCreate, ActivityResponse

router = APIRouter(prefix="/activities", tags=["activities"])


# ---------------------------------------------------------------------------
# List activities (for a module owned by current user)
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[ActivityResponse])
def list_activities(
    module_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return activities. Optionally filter by module_id (must own the module)."""
    query = (
        db.query(Activity)
        .join(Module, Activity.module_id == Module.id)
        .filter(Module.owner_id == current_user.id)
    )
    if module_id is not None:
        query = query.filter(Activity.module_id == module_id)
    return query.all()


# ---------------------------------------------------------------------------
# Get activity by ID
# ---------------------------------------------------------------------------

@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return a single activity by ID (must own the parent module)."""
    activity = (
        db.query(Activity)
        .join(Module, Activity.module_id == Module.id)
        .filter(Activity.id == activity_id, Module.owner_id == current_user.id)
        .first()
    )
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )
    return activity


# ---------------------------------------------------------------------------
# Create activity
# ---------------------------------------------------------------------------

@router.post("/", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(
    body: ActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log a new activity. The target module must be owned by the current user."""
    module = (
        db.query(Module)
        .filter(Module.id == body.module_id, Module.owner_id == current_user.id)
        .first()
    )
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found or not owned by you",
        )

    activity = Activity(
        module_id=body.module_id,
        type=body.type,
        value=body.value,
        metadata=body.metadata,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


# ---------------------------------------------------------------------------
# Delete activity
# ---------------------------------------------------------------------------

@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an activity (must own the parent module)."""
    activity = (
        db.query(Activity)
        .join(Module, Activity.module_id == Module.id)
        .filter(Activity.id == activity_id, Module.owner_id == current_user.id)
        .first()
    )
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )
    db.delete(activity)
    db.commit()
