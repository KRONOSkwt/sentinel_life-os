"""Race calendar service — event CRUD + upcoming filter."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.models.db import RaceEvent
from src.models.schemas import (
    RaceEventCreate,
    RaceEventResponse,
    RaceEventUpdate,
)


# ---------------------------------------------------------------------------
# Race Event CRUD
# ---------------------------------------------------------------------------


def create_race(
    db: Session, user_id: int, data: RaceEventCreate
) -> RaceEventResponse:
    """Create a new race event."""
    race = RaceEvent(
        user_id=user_id,
        name=data.name,
        sport_id=data.sport_id,
        event_date=data.event_date,
        distance_km=data.distance_km,
        location=data.location,
        target_time_seconds=data.target_time_seconds,
        notes=data.notes,
    )
    db.add(race)
    db.commit()
    db.refresh(race)
    return RaceEventResponse.model_validate(race)


def list_races(
    db: Session,
    user_id: int,
    upcoming_only: bool = False,
    limit: int = 50,
    offset: int = 0,
) -> list[RaceEventResponse]:
    """List races for a user with optional upcoming filter."""
    query = db.query(RaceEvent).filter(RaceEvent.user_id == user_id)
    if upcoming_only:
        query = query.filter(RaceEvent.event_date >= datetime.now(timezone.utc))
    races = (
        query.order_by(RaceEvent.event_date.desc()).offset(offset).limit(limit).all()
    )
    return [RaceEventResponse.model_validate(r) for r in races]


def get_race(
    db: Session, race_id: int, user_id: int
) -> RaceEventResponse | None:
    """Get a single race by ID, enforcing user ownership."""
    race = (
        db.query(RaceEvent)
        .filter(RaceEvent.id == race_id, RaceEvent.user_id == user_id)
        .first()
    )
    if not race:
        return None
    return RaceEventResponse.model_validate(race)


def update_race(
    db: Session, race_id: int, user_id: int, data: RaceEventUpdate
) -> RaceEventResponse | None:
    """Update a race event. Returns None if not found."""
    race = (
        db.query(RaceEvent)
        .filter(RaceEvent.id == race_id, RaceEvent.user_id == user_id)
        .first()
    )
    if not race:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(race, key, value)
    db.commit()
    db.refresh(race)
    return RaceEventResponse.model_validate(race)


def delete_race(db: Session, race_id: int, user_id: int) -> bool:
    """Delete a race event. Returns True if deleted."""
    race = (
        db.query(RaceEvent)
        .filter(RaceEvent.id == race_id, RaceEvent.user_id == user_id)
        .first()
    )
    if not race:
        return False
    db.delete(race)
    db.commit()
    return True
