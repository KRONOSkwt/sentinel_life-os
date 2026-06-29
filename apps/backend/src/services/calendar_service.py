"""Calendar service — heatmap data aggregation.

Groups completed sessions by DATE(started_at) and detects PR days.
Returns a 365-day array of {date, intensity, workout_count}.
"""

from datetime import date, datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.db import WorkoutSession, WorkoutSet
from src.models.schemas import HeatmapDay, HeatmapResponse


def get_heatmap(
    db: Session,
    user_id: int,
    year: Optional[int] = None,
) -> HeatmapResponse:
    """Get heatmap data for a given year (default: current year).

    Intensity levels:
      0 = no workout
      1 = workout completed, no PRs
      2 = workout with 1-2 PRs
      3 = workout with 3+ PRs
    """
    if year is None:
        year = datetime.now(timezone.utc).year

    # Query sessions grouped by date
    session_rows = (
        db.query(
            func.date(WorkoutSession.started_at).label("day"),
            func.count(WorkoutSession.id).label("session_count"),
        )
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at.isnot(None),
            func.strftime("%Y", WorkoutSession.started_at) == str(year),
        )
        .group_by(func.date(WorkoutSession.started_at))
        .all()
    )

    # Query PR counts per day
    pr_rows = (
        db.query(
            func.date(WorkoutSession.started_at).label("day"),
            func.count(WorkoutSet.id).label("pr_count"),
        )
        .join(WorkoutSet, WorkoutSet.session_id == WorkoutSession.id)
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at.isnot(None),
            WorkoutSet.is_pr.is_(True),
            func.strftime("%Y", WorkoutSession.started_at) == str(year),
        )
        .group_by(func.date(WorkoutSession.started_at))
        .all()
    )

    # Build lookup maps
    session_map = {str(row.day): row.session_count for row in session_rows}
    pr_map = {str(row.day): row.pr_count for row in pr_rows}

    # Generate all 365 (or 366) days of the year
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    days = []

    current = start_date
    while current <= end_date:
        day_str = current.isoformat()
        session_count = session_map.get(day_str, 0)
        pr_count = pr_map.get(day_str, 0)

        if session_count == 0:
            intensity = 0
        elif pr_count >= 3:
            intensity = 3
        elif pr_count >= 1:
            intensity = 2
        else:
            intensity = 1

        days.append(
            HeatmapDay(
                date=day_str,
                intensity=intensity,
                workout_count=session_count,
            )
        )
        current += timedelta(days=1)

    return HeatmapResponse(year=year, days=days)


def get_month_summary(
    db: Session,
    user_id: int,
    year: int,
    month: int,
) -> dict:
    """Get a summary for a specific month."""
    month_str = f"{year}-{month:02d}"

    result = (
        db.query(
            func.count(WorkoutSession.id).label("total_sessions"),
            func.sum(WorkoutSession.duration_seconds).label("total_duration"),
        )
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at.isnot(None),
            func.strftime("%Y-%m", WorkoutSession.started_at) == month_str,
        )
        .first()
    )

    pr_count = (
        db.query(func.count(WorkoutSet.id))
        .join(WorkoutSession, WorkoutSet.session_id == WorkoutSession.id)
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSet.is_pr.is_(True),
            func.strftime("%Y-%m", WorkoutSession.started_at) == month_str,
        )
        .scalar()
    )

    return {
        "year": year,
        "month": month,
        "total_sessions": result.total_sessions or 0,
        "total_duration_seconds": result.total_duration or 0,
        "pr_count": pr_count or 0,
    }
