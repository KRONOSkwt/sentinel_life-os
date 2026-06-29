"""Integration tests for gimnasio router endpoints.

Tests HTTP status codes, auth requirements, and full request/response cycles.
Uses httpx TestClient with in-memory SQLite.
"""

import pytest


# ---------------------------------------------------------------------------
# Auth Tests
# ---------------------------------------------------------------------------


class TestAuthRequired:
    """All gimnasio endpoints should require JWT auth."""

    def test_exercises_without_auth_returns_403(self, client):
        """GET /gimnasio/exercises without token should return 403."""
        response = client.get("/gimnasio/exercises")
        assert response.status_code in (401, 403)

    def test_routines_without_auth_returns_403(self, client):
        """GET /gimnasio/routines without token should return 403."""
        response = client.get("/gimnasio/routines")
        assert response.status_code in (401, 403)

    def test_sessions_without_auth_returns_403(self, client):
        """GET /gimnasio/sessions without token should return 403."""
        response = client.get("/gimnasio/sessions")
        assert response.status_code in (401, 403)

    def test_gamification_without_auth_returns_403(self, client):
        """GET /gimnasio/gamification/stats without token should return 403."""
        response = client.get("/gimnasio/gamification/stats")
        assert response.status_code in (401, 403)

    def test_heatmap_without_auth_returns_403(self, client):
        """GET /gimnasio/heatmap without token should return 403."""
        response = client.get("/gimnasio/heatmap")
        assert response.status_code in (401, 403)


# ---------------------------------------------------------------------------
# Exercise Catalog Tests
# ---------------------------------------------------------------------------


class TestExerciseCatalog:
    """Tests for GET/POST /gimnasio/exercises."""

    def test_list_exercises_empty(self, client, auth_headers):
        """GET /gimnasio/exercises with no seed data returns empty list."""
        response = client.get("/gimnasio/exercises", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_list_exercises_with_data(self, client, auth_headers, seed_exercises):
        """GET /gimnasio/exercises returns seeded exercises."""
        response = client.get("/gimnasio/exercises", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_filter_by_category(self, client, auth_headers, seed_exercises):
        """GET /gimnasio/exercises?category=cardio filters correctly."""
        response = client.get("/gimnasio/exercises?category=cardio", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert all(ex["category"] == "cardio" for ex in data)

    def test_create_custom_exercise(self, client, auth_headers):
        """POST /gimnasio/exercises creates a custom exercise."""
        payload = {
            "name": "My Custom Exercise",
            "category": "strength",
            "muscle_groups": ["chest"],
            "equipment": "dumbbells",
        }
        response = client.post("/gimnasio/exercises", json=payload, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "My Custom Exercise"
        assert data["is_custom"] is True


# ---------------------------------------------------------------------------
# Routine CRUD Tests
# ---------------------------------------------------------------------------


class TestRoutineCRUD:
    """Tests for routine endpoints."""

    def test_create_routine(self, client, auth_headers, seed_exercises):
        """POST /gimnasio/routines creates a routine."""
        exercise = seed_exercises[0]
        payload = {
            "name": "Push Day",
            "description": "Upper body",
            "exercises": [{
                "exercise_id": exercise.id,
                "target_sets": 4,
                "target_reps": 8,
                "order": 1,
            }],
        }
        response = client.post("/gimnasio/routines", json=payload, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Push Day"
        assert len(data["exercises"]) == 1

    def test_list_routines(self, client, auth_headers):
        """GET /gimnasio/routines returns user's routines."""
        response = client.get("/gimnasio/routines", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_routine_not_found(self, client, auth_headers):
        """GET /gimnasio/routines/9999 returns 404."""
        response = client.get("/gimnasio/routines/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_routine(self, client, auth_headers, seed_exercises):
        """DELETE /gimnasio/routines/{id} returns 204."""
        # Create first
        payload = {"name": "To Delete", "exercises": []}
        create_resp = client.post("/gimnasio/routines", json=payload, headers=auth_headers)
        routine_id = create_resp.json()["id"]

        # Delete
        response = client.delete(f"/gimnasio/routines/{routine_id}", headers=auth_headers)
        assert response.status_code == 204

    def test_delete_routine_not_found(self, client, auth_headers):
        """DELETE /gimnasio/routines/9999 returns 404."""
        response = client.delete("/gimnasio/routines/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_routine_name_conflict(self, client, auth_headers):
        """POST /gimnasio/routines with duplicate name returns 409."""
        payload = {"name": "Duplicate", "exercises": []}
        client.post("/gimnasio/routines", json=payload, headers=auth_headers)
        response = client.post("/gimnasio/routines", json=payload, headers=auth_headers)
        assert response.status_code == 409


# ---------------------------------------------------------------------------
# Session Lifecycle Tests
# ---------------------------------------------------------------------------


class TestSessionLifecycle:
    """Tests for session start → log sets → complete flow."""

    def test_start_session(self, client, auth_headers):
        """POST /gimnasio/sessions starts a session."""
        response = client.post("/gimnasio/sessions", json={}, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] > 0
        assert data["completed_at"] is None

    def test_list_sessions(self, client, auth_headers):
        """GET /gimnasio/sessions returns session list."""
        response = client.get("/gimnasio/sessions", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_session_not_found(self, client, auth_headers):
        """GET /gimnasio/sessions/9999 returns 404."""
        response = client.get("/gimnasio/sessions/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_full_session_lifecycle(self, client, auth_headers, seed_exercises):
        """Full lifecycle: start → log set → complete."""
        exercise = seed_exercises[0]

        # Start session
        start_resp = client.post("/gimnasio/sessions", json={}, headers=auth_headers)
        assert start_resp.status_code == 201
        session_id = start_resp.json()["id"]

        # Log a set
        set_payload = {
            "exercise_id": exercise.id,
            "set_number": 1,
            "weight": 80.0,
            "reps": 8,
        }
        set_resp = client.post(
            f"/gimnasio/sessions/{session_id}/sets",
            json=set_payload,
            headers=auth_headers,
        )
        assert set_resp.status_code == 201
        set_data = set_resp.json()
        assert set_data["is_pr"] is True  # First set = PR

        # Complete session
        complete_resp = client.post(
            f"/gimnasio/sessions/{session_id}/complete",
            json={"notes": "Good session"},
            headers=auth_headers,
        )
        assert complete_resp.status_code == 200
        completed = complete_resp.json()
        assert completed["completed_at"] is not None
        assert completed["notes"] == "Good session"

    def test_complete_already_completed_returns_400(self, client, auth_headers):
        """Completing an already-completed session returns 400."""
        # Start + complete
        start_resp = client.post("/gimnasio/sessions", json={}, headers=auth_headers)
        session_id = start_resp.json()["id"]
        client.post(
            f"/gimnasio/sessions/{session_id}/complete",
            json={},
            headers=auth_headers,
        )
        # Try again
        response = client.post(
            f"/gimnasio/sessions/{session_id}/complete",
            json={},
            headers=auth_headers,
        )
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# Gamification Tests
# ---------------------------------------------------------------------------


class TestGamification:
    """Tests for gamification endpoints."""

    def test_get_stats(self, client, auth_headers):
        """GET /gimnasio/gamification/stats returns stats."""
        response = client.get("/gimnasio/gamification/stats", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_points" in data
        assert "current_streak" in data
        assert "level" in data

    def test_get_achievements(self, client, auth_headers):
        """GET /gimnasio/gamification/achievements returns list."""
        response = client.get("/gimnasio/gamification/achievements", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# ---------------------------------------------------------------------------
# Heatmap Tests
# ---------------------------------------------------------------------------


class TestHeatmap:
    """Tests for heatmap endpoint."""

    def test_get_heatmap(self, client, auth_headers):
        """GET /gimnasio/heatmap returns heatmap data."""
        response = client.get("/gimnasio/heatmap", headers=auth_headers)
        assert response.status_code == 200

    def test_get_heatmap_with_year(self, client, auth_headers):
        """GET /gimnasio/heatmap?year=2026 accepts year param."""
        response = client.get("/gimnasio/heatmap?year=2026", headers=auth_headers)
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# Weight Chart Tests
# ---------------------------------------------------------------------------


class TestWeightChart:
    """Tests for weight chart endpoint."""

    def test_weight_chart_returns_data(self, client, auth_headers, seed_exercises):
        """GET /gimnasio/weight-chart/{exercise_id} returns chart data."""
        exercise = seed_exercises[0]
        response = client.get(
            f"/gimnasio/weight-chart/{exercise.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "exercise_id" in data
        assert "data" in data


# ---------------------------------------------------------------------------
# AI Coach Tests
# ---------------------------------------------------------------------------


class TestAICoach:
    """Tests for AI suggestion endpoints."""

    def test_ai_suggestions(self, client, auth_headers):
        """GET /gimnasio/ai-suggestions returns list."""
        response = client.get("/gimnasio/ai-suggestions", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_ai_suggestion_for_exercise_not_found(self, client, auth_headers):
        """GET /gimnasio/ai-suggestions/9999 returns 404."""
        response = client.get("/gimnasio/ai-suggestions/9999", headers=auth_headers)
        assert response.status_code == 404
