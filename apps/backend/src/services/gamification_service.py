"""Gamification service — points, streaks, achievements, levels.

Points awarded:
  - Workout logged (set created): 10 pts
  - Session completed: 20 pts
  - Personal record: 25 pts
  - Achievement unlocked: 50 pts

Streak: consecutive days with at least one completed session (UTC boundaries).
Level: floor(total_points / 500) + 1

All operations are designed to run atomically on session complete.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.db import UserAchievement, UserStats, WorkoutSession, WorkoutSet
from src.models.schemas import AchievementResponse, GamificationStatsResponse

# ---------------------------------------------------------------------------
# Points constants
# ---------------------------------------------------------------------------

POINTS_PER_LOG = 10
POINTS_PER_COMPLETE = 20
POINTS_PER_PR = 25
POINTS_PER_ACHIEVEMENT = 50
LEVEL_DIVISOR = 500

# ---------------------------------------------------------------------------
# Achievement definitions
# ---------------------------------------------------------------------------

ACHIEVEMENTS = {
    "first_workout": {"name": "First Workout", "check": lambda stats, sessions: sessions >= 1},
    "workout_5": {"name": "5 Workouts", "check": lambda stats, sessions: sessions >= 5},
    "workout_10": {"name": "10 Workouts", "check": lambda stats, sessions: sessions >= 10},
    "workout_25": {"name": "25 Workouts", "check": lambda stats, sessions: sessions >= 25},
    "workout_50": {"name": "50 Workouts", "check": lambda stats, sessions: sessions >= 50},
    "workout_100": {"name": "100 Workouts", "check": lambda stats, sessions: sessions >= 100},
    "streak_3": {"name": "3-Day Streak", "check": lambda stats, _: stats.current_streak >= 3},
    "streak_7": {"name": "Week Warrior", "check": lambda stats, _: stats.current_streak >= 7},
    "streak_30": {"name": "Monthly Master", "check": lambda stats, _: stats.current_streak >= 30},
    "level_5": {"name": "Level 5", "check": lambda stats, _: stats.level >= 5},
}


# ---------------------------------------------------------------------------
# Core operations
# ---------------------------------------------------------------------------


def get_or_create_stats(db: Session, user_id: int) -> UserStats:
    """Get or create user gamification stats."""
    stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    if not stats:
        stats = UserStats(user_id=user_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    return stats


def on_session_complete(db: Session, user_id: int) -> GamificationStatsResponse:
    """Process gamification after a session completes.

    Awards points and checks achievements atomically.
    Call this AFTER the session is marked completed.
    """
    stats = get_or_create_stats(db, user_id)
    now = datetime.now(timezone.utc)
    today = now.date()

    # Count total completed sessions
    total_sessions = (
        db.query(func.count(WorkoutSession.id))
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at.isnot(None),
        )
        .scalar()
    )

    # Count PRs in the just-completed session (use latest session)
    latest_session = (
        db.query(WorkoutSession)
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.completed_at.isnot(None),
        )
        .order_by(WorkoutSession.completed_at.desc())
        .first()
    )

    pr_count = 0
    if latest_session:
        pr_count = (
            db.query(func.count(WorkoutSet.id))
            .filter(WorkoutSet.session_id == latest_session.id, WorkoutSet.is_pr.is_(True))
            .scalar()
        )

    # Award points
    points_earned = POINTS_PER_COMPLETE + (pr_count * POINTS_PER_PR)
    stats.total_points += points_earned
    stats.level = (stats.total_points // LEVEL_DIVISOR) + 1

    # Update streak
    _update_streak(db, stats, user_id, today)

    # Check achievements
    newly_unlocked = _check_achievements(db, user_id, stats, total_sessions)
    stats.total_points += len(newly_unlocked) * POINTS_PER_ACHIEVEMENT
    stats.level = (stats.total_points // LEVEL_DIVISOR) + 1

    db.commit()
    db.refresh(stats)

    return GamificationStatsResponse(
        total_points=stats.total_points,
        current_streak=stats.current_streak,
        longest_streak=stats.longest_streak,
        level=stats.level,
        last_workout_date=stats.last_workout_date,
    )


def get_stats(db: Session, user_id: int) -> GamificationStatsResponse:
    """Get current gamification stats for a user."""
    stats = get_or_create_stats(db, user_id)
    return GamificationStatsResponse(
        total_points=stats.total_points,
        current_streak=stats.current_streak,
        longest_streak=stats.longest_streak,
        level=stats.level,
        last_workout_date=stats.last_workout_date,
    )


def get_achievements(db: Session, user_id: int) -> list[AchievementResponse]:
    """Get all unlocked achievements for a user."""
    rows = (
        db.query(UserAchievement)
        .filter(UserAchievement.user_id == user_id)
        .order_by(UserAchievement.unlocked_at.desc())
        .all()
    )
    return [
        AchievementResponse(
            id=a.id,
            achievement_key=a.achievement_key,
            unlocked_at=a.unlocked_at,
        )
        for a in rows
    ]


# ---------------------------------------------------------------------------
# Streak logic
# ---------------------------------------------------------------------------


def _update_streak(
    db: Session, stats: UserStats, user_id: int, today
) -> None:
    """Update streak based on consecutive workout days (UTC)."""
    if stats.last_workout_date is None:
        # First workout ever
        stats.current_streak = 1
        stats.last_workout_date = datetime.now(timezone.utc)
        if stats.longest_streak < 1:
            stats.longest_streak = 1
        return

    last_date = stats.last_workout_date.date()
    days_since_last = (today - last_date).days

    if days_since_last == 0:
        # Already worked out today — streak unchanged
        return
    elif days_since_last == 1:
        # Consecutive day — extend streak
        stats.current_streak += 1
    else:
        # Streak broken
        stats.current_streak = 1

    stats.last_workout_date = datetime.now(timezone.utc)

    if stats.current_streak > stats.longest_streak:
        stats.longest_streak = stats.current_streak


# ---------------------------------------------------------------------------
# Achievement logic
# ---------------------------------------------------------------------------


def _check_achievements(
    db: Session, user_id: int, stats: UserStats, total_sessions: int
) -> list[str]:
    """Check all achievement conditions. Returns list of newly unlocked keys."""
    # Get already unlocked
    existing = {
        a.achievement_key
        for a in db.query(UserAchievement.achievement_key)
        .filter(UserAchievement.user_id == user_id)
        .all()
    }

    newly_unlocked = []
    for key, defn in ACHIEVEMENTS.items():
        if key in existing:
            continue
        if defn["check"](stats, total_sessions):
            achievement = UserAchievement(
                user_id=user_id,
                achievement_key=key,
                unlocked_at=datetime.now(timezone.utc),
            )
            db.add(achievement)
            newly_unlocked.append(key)

    return newly_unlocked
