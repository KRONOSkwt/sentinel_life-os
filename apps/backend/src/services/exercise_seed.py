"""Exercise seed data — 50 common exercises (strength, cardio, flexibility).

Run `seed_exercises(db)` on app startup. Idempotent — skips if exercises exist.
"""

import json
from sqlalchemy.orm import Session

from src.models.db import Exercise

# ---------------------------------------------------------------------------
# Seed data — 50 exercises
# ---------------------------------------------------------------------------

EXERCISES: list[dict] = [
    # ── Strength — Upper Body ──────────────────────────────────────────────
    {"name": "Bench Press", "category": "strength", "muscle_groups": ["chest", "triceps", "front_delts"], "equipment": "barbell"},
    {"name": "Incline Dumbbell Press", "category": "strength", "muscle_groups": ["upper_chest", "triceps"], "equipment": "dumbbells"},
    {"name": "Dumbbell Flyes", "category": "strength", "muscle_groups": ["chest"], "equipment": "dumbbells"},
    {"name": "Overhead Press", "category": "strength", "muscle_groups": ["shoulders", "triceps"], "equipment": "barbell"},
    {"name": "Lateral Raises", "category": "strength", "muscle_groups": ["side_delts"], "equipment": "dumbbells"},
    {"name": "Barbell Row", "category": "strength", "muscle_groups": ["back", "biceps"], "equipment": "barbell"},
    {"name": "Pull-Up", "category": "strength", "muscle_groups": ["lats", "biceps"], "equipment": "bodyweight"},
    {"name": "Lat Pulldown", "category": "strength", "muscle_groups": ["lats", "biceps"], "equipment": "cable"},
    {"name": "Seated Cable Row", "category": "strength", "muscle_groups": ["back", "biceps"], "equipment": "cable"},
    {"name": "Dumbbell Curl", "category": "strength", "muscle_groups": ["biceps"], "equipment": "dumbbells"},
    {"name": "Tricep Pushdown", "category": "strength", "muscle_groups": ["triceps"], "equipment": "cable"},
    {"name": "Skull Crushers", "category": "strength", "muscle_groups": ["triceps"], "equipment": "ez_bar"},
    {"name": "Face Pulls", "category": "strength", "muscle_groups": ["rear_delts", "rotator_cuff"], "equipment": "cable"},

    # ── Strength — Lower Body ──────────────────────────────────────────────
    {"name": "Barbell Squat", "category": "strength", "muscle_groups": ["quads", "glutes", "hamstrings"], "equipment": "barbell"},
    {"name": "Front Squat", "category": "strength", "muscle_groups": ["quads", "core"], "equipment": "barbell"},
    {"name": "Leg Press", "category": "strength", "muscle_groups": ["quads", "glutes"], "equipment": "machine"},
    {"name": "Romanian Deadlift", "category": "strength", "muscle_groups": ["hamstrings", "glutes"], "equipment": "barbell"},
    {"name": "Conventional Deadlift", "category": "strength", "muscle_groups": ["back", "hamstrings", "glutes"], "equipment": "barbell"},
    {"name": "Leg Curl", "category": "strength", "muscle_groups": ["hamstrings"], "equipment": "machine"},
    {"name": "Leg Extension", "category": "strength", "muscle_groups": ["quads"], "equipment": "machine"},
    {"name": "Calf Raises", "category": "strength", "muscle_groups": ["calves"], "equipment": "machine"},
    {"name": "Bulgarian Split Squat", "category": "strength", "muscle_groups": ["quads", "glutes"], "equipment": "dumbbells"},
    {"name": "Hip Thrust", "category": "strength", "muscle_groups": ["glutes", "hamstrings"], "equipment": "barbell"},

    # ── Strength — Core ────────────────────────────────────────────────────
    {"name": "Plank", "category": "strength", "muscle_groups": ["core"], "equipment": "bodyweight"},
    {"name": "Cable Crunch", "category": "strength", "muscle_groups": ["abs"], "equipment": "cable"},
    {"name": "Hanging Leg Raise", "category": "strength", "muscle_groups": ["lower_abs", "hip_flexors"], "equipment": "bodyweight"},
    {"name": "Ab Wheel Rollout", "category": "strength", "muscle_groups": ["core", "lats"], "equipment": "ab_wheel"},

    # ── Strength — Full Body / Compound ────────────────────────────────────
    {"name": "Dumbbell Thruster", "category": "strength", "muscle_groups": ["quads", "shoulders", "triceps"], "equipment": "dumbbells"},
    {"name": "Kettlebell Swing", "category": "strength", "muscle_groups": ["glutes", "hamstrings", "core"], "equipment": "kettlebell"},
    {"name": "Clean and Press", "category": "strength", "muscle_groups": ["full_body"], "equipment": "barbell"},

    # ── Strength — Other ───────────────────────────────────────────────────
    {"name": "Farmer's Walk", "category": "strength", "muscle_groups": ["forearms", "traps", "core"], "equipment": "dumbbells"},
    {"name": "Shrugs", "category": "strength", "muscle_groups": ["traps"], "equipment": "dumbbells"},

    # ── Cardio ─────────────────────────────────────────────────────────────
    {"name": "Treadmill Run", "category": "cardio", "muscle_groups": ["legs", "cardiovascular"], "equipment": "treadmill"},
    {"name": "Stationary Bike", "category": "cardio", "muscle_groups": ["quads", "cardiovascular"], "equipment": "bike"},
    {"name": "Rowing Machine", "category": "cardio", "muscle_groups": ["full_body", "cardiovascular"], "equipment": "rower"},
    {"name": "Jump Rope", "category": "cardio", "muscle_groups": ["calves", "cardiovascular"], "equipment": "jump_rope"},
    {"name": "Stair Climber", "category": "cardio", "muscle_groups": ["glutes", "quads", "cardiovascular"], "equipment": "machine"},
    {"name": "Elliptical", "category": "cardio", "muscle_groups": ["full_body", "cardiovascular"], "equipment": "machine"},
    {"name": "Burpees", "category": "cardio", "muscle_groups": ["full_body", "cardiovascular"], "equipment": "bodyweight"},
    {"name": "Mountain Climbers", "category": "cardio", "muscle_groups": ["core", "cardiovascular"], "equipment": "bodyweight"},
    {"name": "Battle Ropes", "category": "cardio", "muscle_groups": ["shoulders", "core", "cardiovascular"], "equipment": "battle_ropes"},
    {"name": "Assault Bike", "category": "cardio", "muscle_groups": ["full_body", "cardiovascular"], "equipment": "bike"},

    # ── Flexibility / Mobility ─────────────────────────────────────────────
    {"name": "Foam Rolling", "category": "flexibility", "muscle_groups": ["full_body"], "equipment": "foam_roller"},
    {"name": "Cat-Cow Stretch", "category": "flexibility", "muscle_groups": ["spine", "core"], "equipment": "bodyweight"},
    {"name": "Pigeon Pose", "category": "flexibility", "muscle_groups": ["hip_flexors", "glutes"], "equipment": "bodyweight"},
    {"name": "Hamstring Stretch", "category": "flexibility", "muscle_groups": ["hamstrings"], "equipment": "bodyweight"},
    {"name": "Hip Flexor Stretch", "category": "flexibility", "muscle_groups": ["hip_flexors"], "equipment": "bodyweight"},
    {"name": "Shoulder Dislocates", "category": "flexibility", "muscle_groups": ["shoulders"], "equipment": "band"},
    {"name": "Thoracic Rotation", "category": "flexibility", "muscle_groups": ["spine"], "equipment": "bodyweight"},
    {"name": "Downward Dog", "category": "flexibility", "muscle_groups": ["hamstrings", "calves", "shoulders"], "equipment": "bodyweight"},
    {"name": "Child's Pose", "category": "flexibility", "muscle_groups": ["back", "hips"], "equipment": "bodyweight"},
    {"name": "90/90 Stretch", "category": "flexibility", "muscle_groups": ["hips", "glutes"], "equipment": "bodyweight"},
]


def seed_exercises(db: Session) -> int:
    """Insert seed exercises if the table is empty. Returns count inserted."""
    existing = db.query(Exercise).count()
    if existing > 0:
        return 0

    exercises = []
    for data in EXERCISES:
        exercises.append(
            Exercise(
                name=data["name"],
                category=data["category"],
                muscle_groups=json.dumps(data["muscle_groups"]),
                equipment=data.get("equipment"),
                is_custom=False,
                user_id=None,
            )
        )

    db.add_all(exercises)
    db.commit()
    return len(exercises)
