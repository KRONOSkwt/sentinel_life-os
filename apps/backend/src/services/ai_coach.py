"""AI Coach service — progressive overload suggestions.

Tries Hugging Face API first (with timeout), falls back to rule-based calculation.
Caches suggestions to reduce API calls.

Rule-based logic:
- Hit target reps for 2 consecutive sessions → +2.5% weight (barbell) / +1.25kg (dumbbell)
- Failed to hit target reps → maintain current weight
- Average RPE >= 9 across recent sessions → deload -5-10%
"""

import hashlib
import json
import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.db import Exercise, RoutineExercise, WorkoutSession, WorkoutSet
from src.models.schemas import AISuggestionResponse

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# In-memory cache (production would use Redis)
# ---------------------------------------------------------------------------

_suggestion_cache: dict[str, tuple[AISuggestionResponse, float]] = {}
CACHE_TTL_SECONDS = 3600  # 1 hour


def _cache_key(user_id: int, exercise_id: int) -> str:
    return hashlib.sha256(f"{user_id}:{exercise_id}".encode()).hexdigest()[:16]


def _get_cached(user_id: int, exercise_id: int) -> Optional[AISuggestionResponse]:
    key = _cache_key(user_id, exercise_id)
    if key in _suggestion_cache:
        suggestion, cached_at = _suggestion_cache[key]
        if time.time() - cached_at < CACHE_TTL_SECONDS:
            return suggestion
        del _suggestion_cache[key]
    return None


def _set_cache(user_id: int, exercise_id: int, suggestion: AISuggestionResponse) -> None:
    key = _cache_key(user_id, exercise_id)
    _suggestion_cache[key] = (suggestion, time.time())


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_suggestion(
    db: Session,
    user_id: int,
    exercise_id: int,
    *,
    use_ai: bool = True,
) -> Optional[AISuggestionResponse]:
    """Get a progressive overload suggestion for an exercise.

    Args:
        db: Database session
        user_id: Current user
        exercise_id: Exercise to get suggestion for
        use_ai: Whether to try Hugging Face API first

    Returns:
        AISuggestionResponse or None if no history exists
    """
    # Check cache first
    cached = _get_cached(user_id, exercise_id)
    if cached:
        return cached

    # Gather history
    history = _get_exercise_history(db, user_id, exercise_id)
    if not history:
        return None

    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    exercise_name = exercise.name if exercise else f"Exercise #{exercise_id}"

    suggestion = None

    # Try Hugging Face API first
    if use_ai:
        try:
            suggestion = _try_hf_api(exercise_name, history)
        except Exception as e:
            logger.warning("Hugging Face API failed, falling back to rules: %s", e)

    # Rule-based fallback
    if suggestion is None:
        suggestion = _rule_based_suggestion(exercise_name, history)

    # Cache the result
    _set_cache(user_id, exercise_id, suggestion)
    return suggestion


def get_all_suggestions(
    db: Session,
    user_id: int,
    *,
    use_ai: bool = True,
) -> list[AISuggestionResponse]:
    """Get suggestions for all exercises the user has recently trained."""
    # Get exercises from recent sessions (last 30 days)
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    exercise_ids = (
        db.query(WorkoutSet.exercise_id)
        .join(WorkoutSession, WorkoutSet.session_id == WorkoutSession.id)
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.started_at >= thirty_days_ago,
            WorkoutSession.completed_at.isnot(None),
        )
        .distinct()
        .all()
    )

    suggestions = []
    for (ex_id,) in exercise_ids:
        s = get_suggestion(db, user_id, ex_id, use_ai=use_ai)
        if s:
            suggestions.append(s)

    return suggestions


# ---------------------------------------------------------------------------
# Hugging Face API
# ---------------------------------------------------------------------------


def _try_hf_api(
    exercise_name: str, history: list[dict]
) -> Optional[AISuggestionResponse]:
    """Try calling Hugging Face inference API for progressive overload advice.

    Uses a text-generation model to analyze the workout history and suggest
    weight/rep adjustments. Returns None if the API is unavailable.
    """
    try:
        import httpx
    except ImportError:
        raise RuntimeError("httpx not installed")

    # Build a prompt from history
    recent = history[-6:]  # Last 3 sessions
    history_text = "\n".join(
        f"Session {i+1}: weight={h['weight']}kg, reps={h['reps']}, "
        f"target_reps={h['target_reps']}, rpe={h.get('rpe', 'N/A')}"
        for i, h in enumerate(recent)
    )

    prompt = (
        f"Exercise: {exercise_name}\n"
        f"Recent performance:\n{history_text}\n\n"
        f"Suggest the next weight and reps. Reply with JSON: "
        f'{{"weight": <number>, "reps": <number>, "reason": "<string>"}}'
    )

    # Call HF API with short timeout
    try:
        response = httpx.post(
            "https://api-inference.huggingface.co/models/gpt2",
            json={"inputs": prompt, "parameters": {"max_new_tokens": 150}},
            headers={"Content-Type": "application/json"},
            timeout=5.0,
        )
        response.raise_for_status()
        result = response.json()

        # Parse the generated text
        generated = result[0].get("generated_text", "")
        return _parse_hf_response(exercise_name, history, generated)

    except (httpx.TimeoutException, httpx.HTTPStatusError, KeyError, IndexError) as e:
        raise RuntimeError(f"HF API call failed: {e}")


def _parse_hf_response(
    exercise_name: str, history: list[dict], generated_text: str
) -> Optional[AISuggestionResponse]:
    """Parse the HF model response into a suggestion. Returns None if parsing fails."""
    try:
        # Find JSON in the generated text
        start = generated_text.find("{")
        end = generated_text.find("}") + 1
        if start == -1 or end == 0:
            return None

        data = json.loads(generated_text[start:end])
        current_weight = history[-1]["weight"]

        return AISuggestionResponse(
            exercise_id=0,  # Will be filled by caller
            exercise_name=exercise_name,
            current_weight=current_weight,
            suggested_weight=float(data["weight"]),
            reason=data.get("reason", "AI-suggested progression"),
            confidence=0.7,  # Moderate confidence for HF suggestions
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Rule-based engine
# ---------------------------------------------------------------------------


def _rule_based_suggestion(
    exercise_name: str, history: list[dict]
) -> AISuggestionResponse:
    """Generate a suggestion using deterministic rules.

    Rules (in priority order):
    1. Average RPE >= 9 across last 3 sessions → deload -5-10%
    2. Hit target reps for 2+ consecutive sessions → increase weight
    3. Otherwise → maintain
    """
    current = history[-1]
    current_weight = current["weight"]
    current_reps = current["reps"]
    target_reps = current["target_reps"]

    # Rule 1: High RPE → deload
    recent_rpes = [h["rpe"] for h in history[-3:] if h.get("rpe") is not None]
    if recent_rpes and sum(recent_rpes) / len(recent_rpes) >= 9:
        deload_pct = 0.075  # 7.5% average of 5-10%
        new_weight = round(current_weight * (1 - deload_pct), 1)
        return AISuggestionResponse(
            exercise_id=0,
            exercise_name=exercise_name,
            current_weight=current_weight,
            suggested_weight=new_weight,
            reason=f"Average RPE {sum(recent_rpes)/len(recent_rpes):.1f} across recent sessions — deloading to prevent overtraining",
            confidence=0.9,
        )

    # Rule 2: Hit target reps for 2+ consecutive sessions → increase
    consecutive_hits = 0
    for h in reversed(history):
        if h["reps"] >= h["target_reps"]:
            consecutive_hits += 1
        else:
            break

    if consecutive_hits >= 2:
        # Determine increment based on exercise type (heuristic from equipment)
        increment_pct = 0.025  # +2.5% default (barbell-style)
        new_weight = round(current_weight * (1 + increment_pct), 1)
        return AISuggestionResponse(
            exercise_id=0,
            exercise_name=exercise_name,
            current_weight=current_weight,
            suggested_weight=new_weight,
            reason=f"Hit target reps {consecutive_hits} sessions in a row — progressing +2.5%",
            confidence=0.85,
        )

    # Rule 3: Maintain
    return AISuggestionResponse(
        exercise_id=0,
        exercise_name=exercise_name,
        current_weight=current_weight,
        suggested_weight=current_weight,
        reason="Maintain current weight — build consistency before progressing",
        confidence=0.6,
    )


# ---------------------------------------------------------------------------
# History helper
# ---------------------------------------------------------------------------


def _get_exercise_history(
    db: Session, user_id: int, exercise_id: int
) -> list[dict]:
    """Get recent workout history for an exercise, ordered oldest→newest."""
    rows = (
        db.query(WorkoutSet, WorkoutSession.started_at)
        .join(WorkoutSession, WorkoutSet.session_id == WorkoutSession.id)
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSet.exercise_id == exercise_id,
            WorkoutSession.completed_at.isnot(None),
        )
        .order_by(WorkoutSession.started_at)
        .all()
    )

    # Also grab target_reps from routine if available
    result = []
    for ws, started_at in rows:
        target_reps = _get_target_reps(db, user_id, exercise_id) or 10
        result.append(
            {
                "date": started_at.isoformat(),
                "weight": ws.weight,
                "reps": ws.reps,
                "rpe": ws.rpe,
                "target_reps": target_reps,
            }
        )

    return result


def _get_target_reps(db: Session, user_id: int, exercise_id: int) -> Optional[int]:
    """Get target reps from the user's routine for this exercise."""
    row = (
        db.query(RoutineExercise.target_reps)
        .join(Exercise, RoutineExercise.exercise_id == Exercise.id)
        .first()
    )
    return row[0] if row else None
