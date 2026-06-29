"""Sport seed data — 10 default sports.

Run `seed_sports(db)` on app startup. Idempotent — skips if sports exist.
"""

from sqlalchemy.orm import Session

from src.models.db import Sport

# ---------------------------------------------------------------------------
# Seed data — 10 sports
# ---------------------------------------------------------------------------

SPORTS: list[dict] = [
    {"name": "Running", "icon": "🏃"},
    {"name": "Cycling", "icon": "🚴"},
    {"name": "Swimming", "icon": "🏊"},
    {"name": "Hiking", "icon": "🥾"},
    {"name": "Walking", "icon": "🚶"},
    {"name": "Yoga", "icon": "🧘"},
    {"name": "Strength Training", "icon": "🏋️"},
    {"name": "Rowing", "icon": "🚣"},
    {"name": "Jump Rope", "icon": "🤸"},
    {"name": "Calisthenics", "icon": "💪"},
]


def seed_sports(db: Session) -> int:
    """Insert seed sports if the table is empty. Returns count inserted."""
    existing = db.query(Sport).count()
    if existing > 0:
        return 0

    sports = []
    for data in SPORTS:
        sports.append(
            Sport(
                name=data["name"],
                icon=data.get("icon"),
                is_custom=False,
                user_id=None,
            )
        )

    db.add_all(sports)
    db.commit()
    return len(sports)
