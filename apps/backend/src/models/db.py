"""SQLAlchemy ORM models."""

from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from src.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to modules (one user has many modules)
    modules = relationship("Module", back_populates="owner", cascade="all, delete-orphan")


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    owner_id = Column(Integer, nullable=False)  # Foreign key to users

    owner = relationship("User", back_populates="modules")
    activities = relationship("Activity", back_populates="module", cascade="all, delete-orphan")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)
    extra_data = Column("metadata", Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    module = relationship("Module", back_populates="activities")


# ---------------------------------------------------------------------------
# Gimnasio Module
# ---------------------------------------------------------------------------


class Exercise(Base):
    """Exercise catalog — seed data + user-created custom exercises."""

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)  # strength | cardio | flexibility
    muscle_groups = Column(Text, nullable=False)  # JSON array string
    equipment = Column(String(100), nullable=True)
    is_custom = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # NULL for seed data
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User")
    routine_exercises = relationship("RoutineExercise", back_populates="exercise")
    workout_sets = relationship("WorkoutSet", back_populates="exercise")


class Routine(Base):
    """Workout routine template — user-defined set of exercises."""

    __tablename__ = "routines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User")
    routine_exercises = relationship(
        "RoutineExercise", back_populates="routine", cascade="all, delete-orphan"
    )
    workout_sessions = relationship("WorkoutSession", back_populates="routine")


class RoutineExercise(Base):
    """Exercise within a routine — join table with ordering and target reps/sets."""

    __tablename__ = "routine_exercises"

    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(
        Integer, ForeignKey("routines.id", ondelete="CASCADE"), nullable=False
    )
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    target_sets = Column(Integer, nullable=False)
    target_reps = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)  # display order within routine

    routine = relationship("Routine", back_populates="routine_exercises")
    exercise = relationship("Exercise", back_populates="routine_exercises")


class WorkoutSession(Base):
    """A single workout session — started, then completed with notes."""

    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    routine_id = Column(Integer, ForeignKey("routines.id"), nullable=True)
    started_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User")
    routine = relationship("Routine", back_populates="workout_sessions")
    workout_sets = relationship(
        "WorkoutSet", back_populates="session", cascade="all, delete-orphan"
    )


class WorkoutSet(Base):
    """Individual set within a workout session — tracks weight, reps, RPE, and PR status."""

    __tablename__ = "workout_sets"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        Integer, ForeignKey("workout_sessions.id", ondelete="CASCADE"), nullable=False
    )
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    set_number = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False, default=0.0)
    reps = Column(Integer, nullable=False)
    rpe = Column(Float, nullable=True)
    is_pr = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    session = relationship("WorkoutSession", back_populates="workout_sets")
    exercise = relationship("Exercise", back_populates="workout_sets")


class UserStats(Base):
    """Gamification stats — 1:1 per user. Upserted on session complete."""

    __tablename__ = "user_stats"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    total_points = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    level = Column(Integer, default=1)
    last_workout_date = Column(DateTime, nullable=True)

    user = relationship("User")


class UserAchievement(Base):
    """Achievement unlock — unique per (user, achievement_key)."""

    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_key = Column(String(100), nullable=False)
    unlocked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("user_id", "achievement_key", name="uq_user_achievement"),
    )

    user = relationship("User")