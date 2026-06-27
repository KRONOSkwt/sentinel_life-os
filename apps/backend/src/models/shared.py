"""Bridge to shared models in libs/shared/models.

This module re-exports the canonical Pydantic schemas so the backend
can import from ``src.models.shared`` instead of reaching into
``libs/`` directly.
"""

import sys
from pathlib import Path

# Ensure the libs tree is importable at runtime.
_libs_root = str(Path(__file__).resolve().parents[3] / "libs")
if _libs_root not in sys.path:
    sys.path.insert(0, _libs_root)

from shared.models.python import (  # noqa: E402
    ActivityBase,
    ActivityCreate,
    ActivityResponse,
    ModuleBase,
    ModuleCreate,
    ModuleResponse,
    UserBase,
    UserCreate,
    UserResponse,
)

__all__ = [
    "ActivityBase", "ActivityCreate", "ActivityResponse",
    "ModuleBase", "ModuleCreate", "ModuleResponse",
    "UserBase", "UserCreate", "UserResponse",
]
