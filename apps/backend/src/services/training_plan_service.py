"""Training plan service — plan CRUD + auto-week generation."""

from datetime import timedelta

from sqlalchemy.orm import Session

from src.models.db import TrainingPlan, TrainingPlanWeek
from src.models.schemas import (
    TrainingPlanCreate,
    TrainingPlanDetailResponse,
    TrainingPlanResponse,
    TrainingPlanUpdate,
    TrainingPlanWeekResponse,
)


# ---------------------------------------------------------------------------
# Plan CRUD
# ---------------------------------------------------------------------------


def create_plan(
    db: Session, user_id: int, data: TrainingPlanCreate
) -> TrainingPlanDetailResponse:
    """Create a training plan with auto-generated or explicit weeks."""
    plan = TrainingPlan(
        user_id=user_id,
        name=data.name,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
    )
    db.add(plan)
    db.flush()

    weeks_data = data.weeks or _auto_generate_weeks(data.start_date, data.end_date)
    for w in weeks_data:
        week = TrainingPlanWeek(
            plan_id=plan.id,
            week_number=w.week_number,
            target_sessions=w.target_sessions,
            completed_sessions=w.completed_sessions,
            notes=w.notes,
        )
        db.add(week)

    db.commit()
    db.refresh(plan)
    return _to_detail_response(plan)


def list_plans(db: Session, user_id: int) -> list[TrainingPlanResponse]:
    """List all training plans for a user."""
    plans = (
        db.query(TrainingPlan)
        .filter(TrainingPlan.user_id == user_id)
        .order_by(TrainingPlan.created_at.desc())
        .all()
    )
    return [TrainingPlanResponse.model_validate(p) for p in plans]


def get_plan(
    db: Session, plan_id: int, user_id: int
) -> TrainingPlanDetailResponse | None:
    """Get a plan with its weeks."""
    plan = (
        db.query(TrainingPlan)
        .filter(TrainingPlan.id == plan_id, TrainingPlan.user_id == user_id)
        .first()
    )
    if not plan:
        return None
    return _to_detail_response(plan)


def update_plan(
    db: Session, plan_id: int, user_id: int, data: TrainingPlanUpdate
) -> TrainingPlanDetailResponse | None:
    """Update a plan. If weeks are provided, they replace existing ones."""
    plan = (
        db.query(TrainingPlan)
        .filter(TrainingPlan.id == plan_id, TrainingPlan.user_id == user_id)
        .first()
    )
    if not plan:
        return None

    update_data = data.model_dump(exclude_unset=True, exclude={"weeks"})
    for key, value in update_data.items():
        setattr(plan, key, value)

    if data.weeks is not None:
        # Delete existing weeks and replace
        db.query(TrainingPlanWeek).filter(
            TrainingPlanWeek.plan_id == plan.id
        ).delete()
        for w in data.weeks:
            week = TrainingPlanWeek(
                plan_id=plan.id,
                week_number=w.week_number,
                target_sessions=w.target_sessions,
                completed_sessions=w.completed_sessions,
                notes=w.notes,
            )
            db.add(week)

    db.commit()
    db.refresh(plan)
    return _to_detail_response(plan)


def delete_plan(db: Session, plan_id: int, user_id: int) -> bool:
    """Delete a plan and its weeks. Returns True if deleted."""
    plan = (
        db.query(TrainingPlan)
        .filter(TrainingPlan.id == plan_id, TrainingPlan.user_id == user_id)
        .first()
    )
    if not plan:
        return False
    db.delete(plan)
    db.commit()
    return True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _auto_generate_weeks(start_date, end_date) -> list:
    """Generate weekly targets based on date range."""
    from src.models.schemas import TrainingPlanWeekUpdate

    weeks = []
    current = start_date
    week_num = 1
    while current <= end_date:
        weeks.append(
            TrainingPlanWeekUpdate(
                week_number=week_num,
                target_sessions=3,
                completed_sessions=0,
            )
        )
        current += timedelta(days=7)
        week_num += 1
    return weeks


def _to_detail_response(plan: TrainingPlan) -> TrainingPlanDetailResponse:
    """Convert ORM plan to detail response with weeks."""
    weeks = sorted(plan.weeks, key=lambda w: w.week_number)
    return TrainingPlanDetailResponse(
        id=plan.id,
        name=plan.name,
        description=plan.description,
        start_date=plan.start_date,
        end_date=plan.end_date,
        created_at=plan.created_at,
        updated_at=plan.updated_at,
        weeks=[TrainingPlanWeekResponse.model_validate(w) for w in weeks],
    )
