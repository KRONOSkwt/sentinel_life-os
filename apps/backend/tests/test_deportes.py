"""Integration tests for deportes router endpoints.

Tests HTTP status codes, auth requirements, CRUD operations,
stats aggregation, and PR detection.
Uses httpx TestClient with in-memory SQLite.
"""

import pytest
from datetime import datetime, timezone, timedelta

from src.models.db import Sport, SportActivity, TrainingPlan, TrainingPlanWeek, RaceEvent
from src.models.schemas import (
    SportCreate,
    SportActivityCreate,
    TrainingPlanCreate,
    RaceEventCreate,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_sport(db_session):
    """Create a sample sport for testing."""
    sport = Sport(name="Running", icon="🏃", is_custom=False)
    db_session.add(sport)
    db_session.commit()
    db_session.refresh(sport)
    return sport


@pytest.fixture
def sample_activity(db_session, test_user, sample_sport):
    """Create a sample activity for testing."""
    activity = SportActivity(
        user_id=test_user.id,
        sport_id=sample_sport.id,
        date=datetime(2026, 6, 29, tzinfo=timezone.utc),
        duration_seconds=3600,
        distance_km=10.5,
        calories=750,
        heart_rate_avg=145,
        notes="Morning run",
    )
    db_session.add(activity)
    db_session.commit()
    db_session.refresh(activity)
    return activity


@pytest.fixture
def sample_plan(db_session, test_user):
    """Create a sample training plan for testing."""
    plan = TrainingPlan(
        user_id=test_user.id,
        name="10K Plan",
        description="8-week 10K plan",
        start_date=datetime(2026, 7, 1, tzinfo=timezone.utc),
        end_date=datetime(2026, 8, 25, tzinfo=timezone.utc),
    )
    db_session.add(plan)
    db_session.flush()
    week = TrainingPlanWeek(
        plan_id=plan.id,
        week_number=1,
        target_sessions=3,
        completed_sessions=0,
    )
    db_session.add(week)
    db_session.commit()
    db_session.refresh(plan)
    return plan


@pytest.fixture
def sample_race(db_session, test_user, sample_sport):
    """Create a sample race event for testing."""
    race = RaceEvent(
        user_id=test_user.id,
        name="Buenos Aires Marathon",
        sport_id=sample_sport.id,
        event_date=datetime(2026, 10, 12, tzinfo=timezone.utc),
        distance_km=42.195,
        location="Buenos Aires",
        target_time_seconds=18000,
    )
    db_session.add(race)
    db_session.commit()
    db_session.refresh(race)
    return race


# ---------------------------------------------------------------------------
# Auth Tests
# ---------------------------------------------------------------------------


class TestDeportesAuthRequired:
    """All deportes endpoints should require JWT auth."""

    def test_sports_list_without_auth_returns_403(self, client):
        response = client.get("/deportes/sports")
        assert response.status_code in (401, 403)

    def test_activities_list_without_auth_returns_403(self, client):
        response = client.get("/deportes/activities")
        assert response.status_code in (401, 403)

    def test_plans_list_without_auth_returns_403(self, client):
        response = client.get("/deportes/plans")
        assert response.status_code in (401, 403)

    def test_races_list_without_auth_returns_403(self, client):
        response = client.get("/deportes/races")
        assert response.status_code in (401, 403)

    def test_stats_without_auth_returns_403(self, client):
        response = client.get("/deportes/stats/1")
        assert response.status_code in (401, 403)

    def test_prs_without_auth_returns_403(self, client):
        response = client.get("/deportes/prs/1")
        assert response.status_code in (401, 403)


# ---------------------------------------------------------------------------
# Sport CRUD Tests
# ---------------------------------------------------------------------------


class TestSportCRUD:
    """Tests for sport catalog endpoints."""

    def test_list_sports_empty(self, client, auth_headers):
        """GET /deportes/sports with no data returns empty list."""
        response = client.get("/deportes/sports", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_list_sports_with_data(self, client, auth_headers, sample_sport):
        """GET /deportes/sports returns seeded sports."""
        response = client.get("/deportes/sports", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == "Running"

    def test_create_custom_sport(self, client, auth_headers):
        """POST /deportes/sports creates a custom sport."""
        payload = {"name": "Surfing", "icon": "🏄"}
        response = client.post("/deportes/sports", json=payload, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Surfing"
        assert data["is_custom"] is True

    def test_create_sport_validation_error(self, client, auth_headers):
        """POST /deportes/sports with empty name returns 422."""
        payload = {"name": ""}
        response = client.post("/deportes/sports", json=payload, headers=auth_headers)
        assert response.status_code == 422

    def test_list_custom_only(self, client, auth_headers, sample_sport):
        """GET /deportes/sports?custom_only=true returns only custom."""
        # Create custom sport
        client.post(
            "/deportes/sports",
            json={"name": "Custom Sport"},
            headers=auth_headers,
        )
        response = client.get(
            "/deportes/sports?custom_only=true", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert all(s["is_custom"] is True for s in data)


# ---------------------------------------------------------------------------
# Activity CRUD Tests
# ---------------------------------------------------------------------------


class TestActivityCRUD:
    """Tests for activity endpoints."""

    def test_log_activity(self, client, auth_headers, sample_sport):
        """POST /deportes/activities logs an activity."""
        payload = {
            "sport_id": sample_sport.id,
            "date": "2026-06-29T10:00:00Z",
            "duration_seconds": 3600,
            "distance_km": 10.5,
            "calories": 750,
        }
        response = client.post(
            "/deportes/activities", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["sport_id"] == sample_sport.id
        assert data["duration_seconds"] == 3600
        assert data["distance_km"] == 10.5

    def test_list_activities(self, client, auth_headers, sample_activity):
        """GET /deportes/activities returns user activities."""
        response = client.get("/deportes/activities", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_get_activity(self, client, auth_headers, sample_activity):
        """GET /deportes/activities/:id returns activity detail."""
        response = client.get(
            f"/deportes/activities/{sample_activity.id}", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_activity.id
        assert data["notes"] == "Morning run"

    def test_get_activity_not_found(self, client, auth_headers):
        """GET /deportes/activities/9999 returns 404."""
        response = client.get("/deportes/activities/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_update_activity(self, client, auth_headers, sample_activity):
        """PUT /deportes/activities/:id updates activity."""
        payload = {"notes": "Updated notes", "calories": 800}
        response = client.put(
            f"/deportes/activities/{sample_activity.id}",
            json=payload,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["notes"] == "Updated notes"
        assert data["calories"] == 800

    def test_delete_activity(self, client, auth_headers, sample_activity):
        """DELETE /deportes/activities/:id returns 204."""
        response = client.delete(
            f"/deportes/activities/{sample_activity.id}", headers=auth_headers
        )
        assert response.status_code == 204

    def test_delete_activity_not_found(self, client, auth_headers):
        """DELETE /deportes/activities/9999 returns 404."""
        response = client.delete("/deportes/activities/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_list_activities_date_filter(self, client, auth_headers, sample_sport):
        """GET /deportes/activities with date range filter."""
        # Create activities on different dates
        for day in [10, 20, 25]:
            client.post(
                "/deportes/activities",
                json={
                    "sport_id": sample_sport.id,
                    "date": f"2026-06-{day:02d}T10:00:00Z",
                    "duration_seconds": 1800,
                },
                headers=auth_headers,
            )
        # Filter: June 15 to June 30 should include June 20 and 25
        response = client.get(
            "/deportes/activities?from_date=2026-06-15&to_date=2026-06-30",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_log_activity_validation_error(self, client, auth_headers, sample_sport):
        """POST /deportes/activities with invalid data returns 422."""
        payload = {
            "sport_id": sample_sport.id,
            "date": "2026-06-29T10:00:00Z",
            "duration_seconds": -1,
        }
        response = client.post(
            "/deportes/activities", json=payload, headers=auth_headers
        )
        assert response.status_code == 422

    def test_log_activity_with_extra_data(self, client, auth_headers, sample_sport):
        """POST /deportes/activities with extra_data JSON."""
        payload = {
            "sport_id": sample_sport.id,
            "date": "2026-06-29T10:00:00Z",
            "duration_seconds": 3600,
            "extra_data": {"elevation_gain": 200, "pace": "5:42/km"},
        }
        response = client.post(
            "/deportes/activities", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["extra_data"]["elevation_gain"] == 200


# ---------------------------------------------------------------------------
# Sport Stats & PRs Tests
# ---------------------------------------------------------------------------


class TestSportStats:
    """Tests for stats and PR endpoints."""

    def test_get_sport_stats_empty(self, client, auth_headers, sample_sport):
        """GET /deportes/stats/:sport_id returns zero stats."""
        response = client.get(
            f"/deportes/stats/{sample_sport.id}", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_activities"] == 0
        assert data["total_time_seconds"] == 0

    def test_get_sport_stats_with_data(
        self, client, auth_headers, sample_activity
    ):
        """GET /deportes/stats/:sport_id aggregates correctly."""
        response = client.get(
            f"/deportes/stats/{sample_activity.sport_id}", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_activities"] == 1
        assert data["total_time_seconds"] == 3600
        assert data["sport_name"] == "Running"

    def test_get_personal_records_empty(self, client, auth_headers, sample_sport):
        """GET /deportes/prs/:sport_id with no data."""
        response = client.get(
            f"/deportes/prs/{sample_sport.id}", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["best_time_seconds"] is None

    def test_get_personal_records_with_data(
        self, client, auth_headers, sample_activity
    ):
        """GET /deportes/prs/:sport_id returns PRs."""
        response = client.get(
            f"/deportes/prs/{sample_activity.sport_id}", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["best_time_seconds"] == 3600
        assert data["best_distance_km"] == 10.5

    def test_pr_detection_best_time(
        self, client, auth_headers, sample_sport
    ):
        """PR detection picks the fastest time."""
        # Log two activities
        for dur in [3600, 3000]:
            client.post(
                "/deportes/activities",
                json={
                    "sport_id": sample_sport.id,
                    "date": "2026-06-29T10:00:00Z",
                    "duration_seconds": dur,
                    "distance_km": 10.0,
                },
                headers=auth_headers,
            )
        response = client.get(
            f"/deportes/prs/{sample_sport.id}", headers=auth_headers
        )
        data = response.json()
        assert data["best_time_seconds"] == 3000

    def test_pr_detection_best_distance(
        self, client, auth_headers, sample_sport
    ):
        """PR detection picks the longest distance."""
        for dist in [5.0, 15.0, 10.0]:
            client.post(
                "/deportes/activities",
                json={
                    "sport_id": sample_sport.id,
                    "date": "2026-06-29T10:00:00Z",
                    "duration_seconds": 3600,
                    "distance_km": dist,
                },
                headers=auth_headers,
            )
        response = client.get(
            f"/deportes/prs/{sample_sport.id}", headers=auth_headers
        )
        data = response.json()
        assert data["best_distance_km"] == 15.0


# ---------------------------------------------------------------------------
# Training Plan CRUD Tests
# ---------------------------------------------------------------------------


class TestTrainingPlanCRUD:
    """Tests for training plan endpoints."""

    def test_create_plan(self, client, auth_headers):
        """POST /deportes/plans creates a plan with auto-weeks."""
        payload = {
            "name": "10K Plan",
            "description": "8-week plan",
            "start_date": "2026-07-01T00:00:00Z",
            "end_date": "2026-08-25T00:00:00Z",
        }
        response = client.post(
            "/deportes/plans", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "10K Plan"
        assert len(data["weeks"]) > 0

    def test_create_plan_with_explicit_weeks(self, client, auth_headers):
        """POST /deportes/plans with explicit weeks."""
        payload = {
            "name": "Custom Plan",
            "start_date": "2026-07-01T00:00:00Z",
            "end_date": "2026-07-14T00:00:00Z",
            "weeks": [
                {"week_number": 1, "target_sessions": 4, "completed_sessions": 0},
                {"week_number": 2, "target_sessions": 5, "completed_sessions": 0},
            ],
        }
        response = client.post(
            "/deportes/plans", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert len(data["weeks"]) == 2

    def test_list_plans(self, client, auth_headers, sample_plan):
        """GET /deportes/plans returns plan list."""
        response = client.get("/deportes/plans", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_get_plan(self, client, auth_headers, sample_plan):
        """GET /deportes/plans/:id returns plan with weeks."""
        response = client.get(
            f"/deportes/plans/{sample_plan.id}", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "10K Plan"
        assert len(data["weeks"]) >= 1

    def test_get_plan_not_found(self, client, auth_headers):
        """GET /deportes/plans/9999 returns 404."""
        response = client.get("/deportes/plans/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_update_plan(self, client, auth_headers, sample_plan):
        """PUT /deportes/plans/:id updates plan."""
        payload = {"name": "Updated Plan Name"}
        response = client.put(
            f"/deportes/plans/{sample_plan.id}",
            json=payload,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Plan Name"

    def test_delete_plan(self, client, auth_headers, sample_plan):
        """DELETE /deportes/plans/:id returns 204."""
        response = client.delete(
            f"/deportes/plans/{sample_plan.id}", headers=auth_headers
        )
        assert response.status_code == 204

    def test_delete_plan_not_found(self, client, auth_headers):
        """DELETE /deportes/plans/9999 returns 404."""
        response = client.delete("/deportes/plans/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_plan_validation_error(self, client, auth_headers):
        """POST /deportes/plans with empty name returns 422."""
        payload = {
            "name": "",
            "start_date": "2026-07-01T00:00:00Z",
            "end_date": "2026-08-25T00:00:00Z",
        }
        response = client.post(
            "/deportes/plans", json=payload, headers=auth_headers
        )
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# Race Event CRUD Tests
# ---------------------------------------------------------------------------


class TestRaceEventCRUD:
    """Tests for race event endpoints."""

    def test_create_race(self, client, auth_headers, sample_sport):
        """POST /deportes/races creates a race event."""
        payload = {
            "name": "Buenos Aires Marathon",
            "sport_id": sample_sport.id,
            "event_date": "2026-10-12T00:00:00Z",
            "distance_km": 42.195,
            "location": "Buenos Aires",
            "target_time_seconds": 18000,
        }
        response = client.post(
            "/deportes/races", json=payload, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Buenos Aires Marathon"
        assert data["distance_km"] == 42.195

    def test_list_races(self, client, auth_headers, sample_race):
        """GET /deportes/races returns race list."""
        response = client.get("/deportes/races", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_list_races_upcoming_filter(self, client, auth_headers, sample_sport):
        """GET /deportes/races?upcoming_only=true filters correctly."""
        # Create a past race
        client.post(
            "/deportes/races",
            json={
                "name": "Past Race",
                "sport_id": sample_sport.id,
                "event_date": "2020-01-01T00:00:00Z",
            },
            headers=auth_headers,
        )
        # Create a future race
        client.post(
            "/deportes/races",
            json={
                "name": "Future Race",
                "sport_id": sample_sport.id,
                "event_date": "2099-12-31T00:00:00Z",
            },
            headers=auth_headers,
        )
        response = client.get(
            "/deportes/races?upcoming_only=true", headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert all(r["name"] != "Past Race" for r in data)

    def test_update_race(self, client, auth_headers, sample_race):
        """PUT /deportes/races/:id updates race."""
        payload = {"location": "Updated Location"}
        response = client.put(
            f"/deportes/races/{sample_race.id}",
            json=payload,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["location"] == "Updated Location"

    def test_delete_race(self, client, auth_headers, sample_race):
        """DELETE /deportes/races/:id returns 204."""
        response = client.delete(
            f"/deportes/races/{sample_race.id}", headers=auth_headers
        )
        assert response.status_code == 204

    def test_delete_race_not_found(self, client, auth_headers):
        """DELETE /deportes/races/9999 returns 404."""
        response = client.delete("/deportes/races/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_race_validation_error(self, client, auth_headers, sample_sport):
        """POST /deportes/races with empty name returns 422."""
        payload = {
            "name": "",
            "sport_id": sample_sport.id,
            "event_date": "2026-10-12T00:00:00Z",
        }
        response = client.post(
            "/deportes/races", json=payload, headers=auth_headers
        )
        assert response.status_code == 422
