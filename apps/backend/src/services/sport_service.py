"""Sport service — catalog CRUD, activity CRUD, stats aggregation, PR detection."""

import json
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.db import RaceEvent, Sport, SportActivity
from src.models.schemas import (
    PersonalRecordResponse,
    SportActivityCreate,
    SportActivityResponse,
    SportActivityUpdate,
    SportCreate,
    SportResponse,
    SportStatsResponse,
)


# ---------------------------------------------------------------------------
# Sport catalog
# ---------------------------------------------------------------------------


def list_sports(db: Session, custom_only: bool = False) -> list[SportResponse]:
    """List all sports, optionally filtering to custom only."""
    query = db.query(Sport)
    if custom_only:
        query = query.filter(Sport.is_custom == True)
    sports = query.order_by(Sport.name).all()
    return [SportResponse.model_validate(s) for s in sports]


def create_sport(db: Session, user_id: int, data: SportCreate) -> SportResponse:
    """Create a custom sport for a user."""
    sport = Sport(
        name=data.name,
        icon=data.icon,
        is_custom=True,
        user_id=user_id,
    )
    db.add(sport)
    db.commit()
    db.refresh(sport)
    return SportResponse.model_validate(sport)


# ---------------------------------------------------------------------------
# SportActivity CRUD
# ---------------------------------------------------------------------------


def log_activity(
    db: Session, user_id: int, data: SportActivityCreate
) -> SportActivityResponse:
    """Log a new sport activity."""
    activity = SportActivity(
        user_id=user_id,
        sport_id=data.sport_id,
        date=data.date,
        duration_seconds=data.duration_seconds,
        distance_km=data.distance_km,
        calories=data.calories,
        heart_rate_avg=data.heart_rate_avg,
        extra_data=json.dumps(data.extra_data) if data.extra_data else None,
        notes=data.notes,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return _to_activity_response(activity)


def list_activities(
    db: Session,
    user_id: int,
    from_date: str | None = None,
    to_date: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[SportActivityResponse]:
    """List activities for a user with optional date range filter."""
    query = db.query(SportActivity).filter(SportActivity.user_id == user_id)
    if from_date:
        from_dt = datetime.fromisoformat(from_date)
        if from_dt.tzinfo is None:
            from_dt = from_dt.replace(tzinfo=timezone.utc)
        query = query.filter(SportActivity.date >= from_dt)
    if to_date:
        to_dt = datetime.fromisoformat(to_date)
        if to_dt.tzinfo is None:
            to_dt = to_dt.replace(tzinfo=timezone.utc)
        query = query.filter(SportActivity.date <= to_dt)
    activities = (
        query.order_by(SportActivity.date.desc()).offset(offset).limit(limit).all()
    )
    return [_to_activity_response(a) for a in activities]


def get_activity(
    db: Session, activity_id: int, user_id: int
) -> SportActivityResponse | None:
    """Get a single activity by ID, enforcing user ownership."""
    activity = (
        db.query(SportActivity)
        .filter(SportActivity.id == activity_id, SportActivity.user_id == user_id)
        .first()
    )
    if not activity:
        return None
    return _to_activity_response(activity)


def update_activity(
    db: Session, activity_id: int, user_id: int, data: SportActivityUpdate
) -> SportActivityResponse | None:
    """Update an activity. Returns None if not found."""
    activity = (
        db.query(SportActivity)
        .filter(SportActivity.id == activity_id, SportActivity.user_id == user_id)
        .first()
    )
    if not activity:
        return None
    update_data = data.model_dump(exclude_unset=True)
    if "extra_data" in update_data and update_data["extra_data"] is not None:
        update_data["extra_data"] = json.dumps(update_data["extra_data"])
    for key, value in update_data.items():
        setattr(activity, key, value)
    db.commit()
    db.refresh(activity)
    return _to_activity_response(activity)


def delete_activity(db: Session, activity_id: int, user_id: int) -> bool:
    """Delete an activity. Returns True if deleted, False if not found."""
    activity = (
        db.query(SportActivity)
        .filter(SportActivity.id == activity_id, SportActivity.user_id == user_id)
        .first()
    )
    if not activity:
        return False
    db.delete(activity)
    db.commit()
    return True


# ---------------------------------------------------------------------------
# Stats & PRs
# ---------------------------------------------------------------------------


def get_sport_stats(db: Session, user_id: int, sport_id: int) -> SportStatsResponse:
    """Aggregate activity statistics for a specific sport."""
    stats = (
        db.query(
            func.count(SportActivity.id).label("total_activities"),
            func.sum(SportActivity.duration_seconds).label("total_time_seconds"),
            func.sum(SportActivity.distance_km).label("total_distance_km"),
            func.avg(SportActivity.duration_seconds).label(
                "average_duration_seconds"
            ),
        )
        .filter(
            SportActivity.user_id == user_id,
            SportActivity.sport_id == sport_id,
        )
        .first()
    )
    sport = db.query(Sport).filter(Sport.id == sport_id).first()
    return SportStatsResponse(
        sport_id=sport_id,
        sport_name=sport.name if sport else f"Sport #{sport_id}",
        total_activities=stats.total_activities or 0,
        total_time_seconds=stats.total_time_seconds or 0,
        total_distance_km=stats.total_distance_km,
        average_duration_seconds=(
            int(stats.average_duration_seconds)
            if stats.average_duration_seconds
            else None
        ),
    )


def get_personal_records(
    db: Session, user_id: int, sport_id: int
) -> PersonalRecordResponse:
    """Calculate personal records for a specific sport."""
    activities = (
        db.query(SportActivity)
        .filter(
            SportActivity.user_id == user_id,
            SportActivity.sport_id == sport_id,
        )
        .all()
    )

    best_time = None
    best_time_date = None
    best_distance = None
    best_distance_date = None
    best_pace = None

    for a in activities:
        # Best time (shortest duration)
        if best_time is None or a.duration_seconds < best_time:
            best_time = a.duration_seconds
            best_time_date = a.date

        # Best distance (longest)
        if a.distance_km is not None:
            if best_distance is None or a.distance_km > best_distance:
                best_distance = a.distance_km
                best_distance_date = a.date

        # Best pace (lowest seconds per km)
        if a.distance_km and a.distance_km > 0:
            pace = int(a.duration_seconds / a.distance_km)
            if best_pace is None or pace < best_pace:
                best_pace = pace

    return PersonalRecordResponse(
        sport_id=sport_id,
        best_time_seconds=best_time,
        best_distance_km=best_distance,
        best_pace_seconds_per_km=best_pace,
        best_time_date=best_time_date,
        best_distance_date=best_distance_date,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_activity_response(activity: SportActivity) -> SportActivityResponse:
    """Convert ORM activity to Pydantic response."""
    extra_data = None
    if activity.extra_data:
        try:
            extra_data = json.loads(activity.extra_data)
        except (json.JSONDecodeError, TypeError):
            extra_data = None
    return SportActivityResponse(
        id=activity.id,
        user_id=activity.user_id,
        sport_id=activity.sport_id,
        date=activity.date,
        duration_seconds=activity.duration_seconds,
        distance_km=activity.distance_km,
        calories=activity.calories,
        heart_rate_avg=activity.heart_rate_avg,
        extra_data=extra_data,
        notes=activity.notes,
        created_at=activity.created_at,
    )
