"""Deportes module routes — sports, activities, training plans, races, stats, PRs.

All endpoints require authentication via JWT Bearer token.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.deps import get_current_user
from src.models.db import User
from src.models.schemas import (
    RaceEventCreate,
    RaceEventResponse,
    RaceEventUpdate,
    SportActivityCreate,
    SportActivityResponse,
    SportActivityUpdate,
    SportCreate,
    SportResponse,
    SportStatsResponse,
    PersonalRecordResponse,
    TrainingPlanCreate,
    TrainingPlanDetailResponse,
    TrainingPlanResponse,
    TrainingPlanUpdate,
)
from src.services import race_calendar_service, sport_service, training_plan_service

router = APIRouter(prefix="/deportes", tags=["deportes"])


# ---------------------------------------------------------------------------
# Sports catalog
# ---------------------------------------------------------------------------


@router.get("/sports", response_model=list[SportResponse])
def list_sports(
    custom_only: bool = Query(False, description="Filter: only custom sports"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all sports (seeded + custom)."""
    return sport_service.list_sports(db, custom_only=custom_only)


@router.post(
    "/sports",
    response_model=SportResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sport(
    body: SportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a custom sport."""
    return sport_service.create_sport(db, current_user.id, body)


# ---------------------------------------------------------------------------
# Activities
# ---------------------------------------------------------------------------


@router.post(
    "/activities",
    response_model=SportActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
def log_activity(
    body: SportActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log a sport activity."""
    return sport_service.log_activity(db, current_user.id, body)


@router.get("/activities", response_model=list[SportActivityResponse])
def list_activities(
    from_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    to_date: Optional[str] = Query(None, description="End date (ISO format)"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List activities with optional date range filter."""
    return sport_service.list_activities(
        db,
        current_user.id,
        from_date=from_date,
        to_date=to_date,
        limit=limit,
        offset=offset,
    )


@router.get("/activities/{activity_id}", response_model=SportActivityResponse)
def get_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get activity detail."""
    activity = sport_service.get_activity(db, activity_id, current_user.id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )
    return activity


@router.put("/activities/{activity_id}", response_model=SportActivityResponse)
def update_activity(
    activity_id: int,
    body: SportActivityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an activity."""
    activity = sport_service.update_activity(db, activity_id, current_user.id, body)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )
    return activity


@router.delete(
    "/activities/{activity_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an activity."""
    deleted = sport_service.delete_activity(db, activity_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )


# ---------------------------------------------------------------------------
# Stats & PRs
# ---------------------------------------------------------------------------


@router.get("/stats/{sport_id}", response_model=SportStatsResponse)
def get_sport_stats(
    sport_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get aggregated statistics for a sport."""
    return sport_service.get_sport_stats(db, current_user.id, sport_id)


@router.get("/prs/{sport_id}", response_model=PersonalRecordResponse)
def get_personal_records(
    sport_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get personal records for a sport."""
    return sport_service.get_personal_records(db, current_user.id, sport_id)


# ---------------------------------------------------------------------------
# Training Plans
# ---------------------------------------------------------------------------


@router.post(
    "/plans",
    response_model=TrainingPlanDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_plan(
    body: TrainingPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a training plan with auto-generated weeks."""
    return training_plan_service.create_plan(db, current_user.id, body)


@router.get("/plans", response_model=list[TrainingPlanResponse])
def list_plans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all training plans."""
    return training_plan_service.list_plans(db, current_user.id)


@router.get("/plans/{plan_id}", response_model=TrainingPlanDetailResponse)
def get_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a plan with its weeks."""
    plan = training_plan_service.get_plan(db, plan_id, current_user.id)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )
    return plan


@router.put("/plans/{plan_id}", response_model=TrainingPlanDetailResponse)
def update_plan(
    plan_id: int,
    body: TrainingPlanUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a training plan."""
    plan = training_plan_service.update_plan(db, plan_id, current_user.id, body)
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )
    return plan


@router.delete("/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a training plan."""
    deleted = training_plan_service.delete_plan(db, plan_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )


# ---------------------------------------------------------------------------
# Race Events
# ---------------------------------------------------------------------------


@router.post(
    "/races",
    response_model=RaceEventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_race(
    body: RaceEventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a race event."""
    return race_calendar_service.create_race(db, current_user.id, body)


@router.get("/races", response_model=list[RaceEventResponse])
def list_races(
    upcoming_only: bool = Query(False, description="Filter: only upcoming races"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List race events with optional upcoming filter."""
    return race_calendar_service.list_races(
        db, current_user.id, upcoming_only=upcoming_only,
        limit=limit, offset=offset,
    )


@router.put("/races/{race_id}", response_model=RaceEventResponse)
def update_race(
    race_id: int,
    body: RaceEventUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a race event."""
    race = race_calendar_service.update_race(db, race_id, current_user.id, body)
    if not race:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Race not found",
        )
    return race


@router.delete("/races/{race_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_race(
    race_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a race event."""
    deleted = race_calendar_service.delete_race(db, race_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Race not found",
        )
