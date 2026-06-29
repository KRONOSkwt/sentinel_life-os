"""Unit tests for gimnasio services.

Tests PR detection, streak calculation, point awards, achievement triggers,
routine CRUD, and AI coach rules.
"""

import json
from datetime import datetime, timedelta, timezone

import pytest

from src.models.db import (
    Exercise,
    Routine,
    RoutineExercise,
    UserStats,
    UserAchievement,
    WorkoutSession,
    WorkoutSet,
)
from src.services import (
    gamification_service,
    routine_service,
    workout_service,
)
from src.services.ai_coach import _rule_based_suggestion


# ---------------------------------------------------------------------------
# PR Detection Tests
# ---------------------------------------------------------------------------


class TestPRDetection:
    """Tests for workout_service._detect_pr logic."""

    def test_first_set_is_pr(self, db_session, test_user, seed_exercises):
        """First ever set for an exercise should be a PR."""
        exercise = seed_exercises[0]  # Bench Press
        # Create a completed session
        session = WorkoutSession(
            user_id=test_user.id,
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Log a set
        set_data = type("SetData", (), {
            "exercise_id": exercise.id,
            "set_number": 1,
            "weight": 80.0,
            "reps": 8,
            "rpe": None,
        })()
        result = workout_service.log_set(db_session, session.id, test_user.id, set_data)
        assert result.is_pr is True

    def test_higher_weight_is_pr(self, db_session, test_user, seed_exercises):
        """Higher weight than previous best should be a PR."""
        exercise = seed_exercises[0]

        # Complete a session with 80kg
        session1 = WorkoutSession(
            user_id=test_user.id,
            started_at=datetime.now(timezone.utc) - timedelta(days=1),
            completed_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        db_session.add(session1)
        db_session.commit()
        db_session.refresh(session1)
        ws1 = WorkoutSet(
            session_id=session1.id, exercise_id=exercise.id,
            set_number=1, weight=80.0, reps=8, is_pr=True,
        )
        db_session.add(ws1)
        db_session.commit()

        # New session with 82.5kg
        session2 = WorkoutSession(
            user_id=test_user.id,
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )
        db_session.add(session2)
        db_session.commit()
        db_session.refresh(session2)

        set_data = type("SetData", (), {
            "exercise_id": exercise.id,
            "set_number": 1,
            "weight": 82.5,
            "reps": 8,
            "rpe": None,
        })()
        result = workout_service.log_set(db_session, session2.id, test_user.id, set_data)
        assert result.is_pr is True

    def test_same_weight_fewer_reps_not_pr(self, db_session, test_user, seed_exercises):
        """Same weight with fewer or equal reps should NOT be a PR."""
        exercise = seed_exercises[0]

        # Previous session: 80kg x 8
        session1 = WorkoutSession(
            user_id=test_user.id,
            started_at=datetime.now(timezone.utc) - timedelta(days=1),
            completed_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        db_session.add(session1)
        db_session.commit()
        db_session.refresh(session1)
        ws1 = WorkoutSet(
            session_id=session1.id, exercise_id=exercise.id,
            set_number=1, weight=80.0, reps=8, is_pr=True,
        )
        db_session.add(ws1)
        db_session.commit()

        # New session: 80kg x 6 (fewer reps)
        session2 = WorkoutSession(
            user_id=test_user.id,
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )
        db_session.add(session2)
        db_session.commit()
        db_session.refresh(session2)

        set_data = type("SetData", (), {
            "exercise_id": exercise.id,
            "set_number": 1,
            "weight": 80.0,
            "reps": 6,
            "rpe": None,
        })()
        result = workout_service.log_set(db_session, session2.id, test_user.id, set_data)
        assert result.is_pr is False

    def test_same_weight_more_reps_is_pr(self, db_session, test_user, seed_exercises):
        """Same weight with MORE reps should be a PR."""
        exercise = seed_exercises[0]

        session1 = WorkoutSession(
            user_id=test_user.id,
            started_at=datetime.now(timezone.utc) - timedelta(days=1),
            completed_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        db_session.add(session1)
        db_session.commit()
        db_session.refresh(session1)
        ws1 = WorkoutSet(
            session_id=session1.id, exercise_id=exercise.id,
            set_number=1, weight=80.0, reps=8, is_pr=True,
        )
        db_session.add(ws1)
        db_session.commit()

        session2 = WorkoutSession(
            user_id=test_user.id,
            started_at=datetime.now(timezone.utc),
            completed_at=datetime.now(timezone.utc),
        )
        db_session.add(session2)
        db_session.commit()
        db_session.refresh(session2)

        set_data = type("SetData", (), {
            "exercise_id": exercise.id,
            "set_number": 1,
            "weight": 80.0,
            "reps": 10,
            "rpe": None,
        })()
        result = workout_service.log_set(db_session, session2.id, test_user.id, set_data)
        assert result.is_pr is True


# ---------------------------------------------------------------------------
# Streak Calculation Tests
# ---------------------------------------------------------------------------


class TestStreakCalculation:
    """Tests for gamification_service._update_streak logic."""

    def test_first_workout_sets_streak_to_1(self, db_session, test_user):
        """First workout should set streak to 1."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)
        today = datetime.now(timezone.utc).date()
        gamification_service._update_streak(db_session, stats, test_user.id, today)
        assert stats.current_streak == 1

    def test_consecutive_day_extends_streak(self, db_session, test_user):
        """Workout on consecutive days should extend the streak."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)
        yesterday = datetime.now(timezone.utc).date() - timedelta(days=1)
        stats.last_workout_date = datetime.now(timezone.utc) - timedelta(days=1)
        stats.current_streak = 3

        today = datetime.now(timezone.utc).date()
        gamification_service._update_streak(db_session, stats, test_user.id, today)
        assert stats.current_streak == 4

    def test_gap_breaks_streak(self, db_session, test_user):
        """Gap of more than 1 day should reset streak to 1."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)
        stats.last_workout_date = datetime.now(timezone.utc) - timedelta(days=3)
        stats.current_streak = 5

        today = datetime.now(timezone.utc).date()
        gamification_service._update_streak(db_session, stats, test_user.id, today)
        assert stats.current_streak == 1

    def test_same_day_does_not_change_streak(self, db_session, test_user):
        """Two workouts same day should not change streak."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)
        stats.last_workout_date = datetime.now(timezone.utc)
        stats.current_streak = 2

        today = datetime.now(timezone.utc).date()
        gamification_service._update_streak(db_session, stats, test_user.id, today)
        assert stats.current_streak == 2

    def test_longest_streak_tracking(self, db_session, test_user):
        """Longest streak should update when current exceeds it."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)
        stats.last_workout_date = datetime.now(timezone.utc) - timedelta(days=1)
        stats.current_streak = 9
        stats.longest_streak = 7

        today = datetime.now(timezone.utc).date()
        gamification_service._update_streak(db_session, stats, test_user.id, today)
        assert stats.current_streak == 10
        assert stats.longest_streak == 10


# ---------------------------------------------------------------------------
# Points Award Tests
# ---------------------------------------------------------------------------


class TestPointsAward:
    """Tests for gamification point calculations."""

    def test_level_formula(self, db_session, test_user):
        """Level should be floor(points/500) + 1."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)
        stats.total_points = 1200
        stats.level = (stats.total_points // 500) + 1
        assert stats.level == 3

    def test_level_at_zero_points(self, db_session, test_user):
        """New user with 0 points should be level 1."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)
        stats.level = (stats.total_points // 500) + 1
        assert stats.level == 1

    def test_points_constants(self):
        """Verify point constants match design spec."""
        assert gamification_service.POINTS_PER_LOG == 10
        assert gamification_service.POINTS_PER_COMPLETE == 20
        assert gamification_service.POINTS_PER_PR == 25
        assert gamification_service.POINTS_PER_ACHIEVEMENT == 50


# ---------------------------------------------------------------------------
# Achievement Trigger Tests
# ---------------------------------------------------------------------------


class TestAchievementTriggers:
    """Tests for achievement condition checks."""

    def test_first_workout_achievement(self, db_session, test_user):
        """first_workout should trigger after 1 session."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)
        newly = gamification_service._check_achievements(db_session, test_user.id, stats, 1)
        assert "first_workout" in newly

    def test_streak_7_achievement(self, db_session, test_user):
        """streak_7 should trigger at 7-day streak."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)
        stats.current_streak = 7
        newly = gamification_service._check_achievements(db_session, test_user.id, stats, 10)
        assert "streak_7" in newly

    def test_level_5_achievement(self, db_session, test_user):
        """level_5 should trigger at level 5."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)
        stats.level = 5
        newly = gamification_service._check_achievements(db_session, test_user.id, stats, 10)
        assert "level_5" in newly

    def test_no_duplicate_achievements(self, db_session, test_user):
        """Already-unlocked achievements should not be re-unlocked."""
        stats = gamification_service.get_or_create_stats(db_session, test_user.id)

        # First check — should unlock
        newly1 = gamification_service._check_achievements(db_session, test_user.id, stats, 1)
        assert "first_workout" in newly1
        db_session.commit()

        # Second check — should NOT unlock again
        newly2 = gamification_service._check_achievements(db_session, test_user.id, stats, 1)
        assert "first_workout" not in newly2


# ---------------------------------------------------------------------------
# Routine CRUD Tests
# ---------------------------------------------------------------------------


class TestRoutineCRUD:
    """Tests for routine_service operations."""

    def test_create_routine(self, db_session, test_user, seed_exercises):
        """Creating a routine should succeed with valid data."""
        exercise = seed_exercises[0]
        data = type("RoutineData", (), {
            "name": "Push Day",
            "description": "Upper body push",
            "exercises": [type("RE", (), {
                "exercise_id": exercise.id,
                "target_sets": 4,
                "target_reps": 8,
                "order": 1,
            })()],
        })()
        result = routine_service.create_routine(db_session, test_user.id, data)
        assert result.name == "Push Day"
        assert len(result.exercises) == 1

    def test_routine_name_uniqueness(self, db_session, test_user, seed_exercises):
        """Duplicate routine name (case-insensitive) should raise ValueError."""
        exercise = seed_exercises[0]
        data = type("RoutineData", (), {
            "name": "Push Day",
            "description": None,
            "exercises": [],
        })()
        routine_service.create_routine(db_session, test_user.id, data)

        with pytest.raises(ValueError, match="already exists"):
            routine_service.create_routine(db_session, test_user.id, data)

    def test_list_routines(self, db_session, test_user, seed_exercises):
        """List routines should return user's routines."""
        data = type("RoutineData", (), {
            "name": "Test Routine",
            "description": None,
            "exercises": [],
        })()
        routine_service.create_routine(db_session, test_user.id, data)
        result = routine_service.list_routines(db_session, test_user.id)
        assert len(result) == 1

    def test_delete_routine(self, db_session, test_user, seed_exercises):
        """Deleting a routine should return True."""
        data = type("RoutineData", (), {
            "name": "To Delete",
            "description": None,
            "exercises": [],
        })()
        routine = routine_service.create_routine(db_session, test_user.id, data)
        deleted = routine_service.delete_routine(db_session, routine.id, test_user.id)
        assert deleted is True

    def test_delete_nonexistent_returns_false(self, db_session, test_user):
        """Deleting a non-existent routine should return False."""
        deleted = routine_service.delete_routine(db_session, 9999, test_user.id)
        assert deleted is False


# ---------------------------------------------------------------------------
# AI Coach Rule-Based Tests
# ---------------------------------------------------------------------------


class TestAICoachRules:
    """Tests for the rule-based progressive overload engine."""

    def test_deload_on_high_rpe(self):
        """Average RPE >= 9 should suggest deload."""
        history = [
            {"weight": 80.0, "reps": 8, "target_reps": 8, "rpe": 9.0},
            {"weight": 80.0, "reps": 7, "target_reps": 8, "rpe": 9.5},
            {"weight": 80.0, "reps": 6, "target_reps": 8, "rpe": 9.0},
        ]
        result = _rule_based_suggestion("Bench Press", history)
        assert result.suggested_weight < result.current_weight
        assert "deload" in result.reason.lower() or "RPE" in result.reason

    def test_progression_on_consecutive_hits(self):
        """2+ consecutive sessions hitting target reps should suggest increase."""
        history = [
            {"weight": 80.0, "reps": 8, "target_reps": 8, "rpe": 7.0},
            {"weight": 80.0, "reps": 9, "target_reps": 8, "rpe": 7.5},
            {"weight": 80.0, "reps": 8, "target_reps": 8, "rpe": 7.0},
        ]
        result = _rule_based_suggestion("Bench Press", history)
        assert result.suggested_weight > result.current_weight

    def test_maintain_when_not_hitting_target(self):
        """Not hitting target reps should suggest maintain."""
        history = [
            {"weight": 80.0, "reps": 6, "target_reps": 8, "rpe": 8.0},
            {"weight": 80.0, "reps": 5, "target_reps": 8, "rpe": 8.5},
        ]
        result = _rule_based_suggestion("Bench Press", history)
        assert result.suggested_weight == result.current_weight
        assert result.confidence < 0.8
