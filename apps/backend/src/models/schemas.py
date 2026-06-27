"""Pydantic request/response schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


class UserCreate(BaseModel):
    """Request body for user registration."""

    email: EmailStr
    password: str = Field(..., min_length=8)
    display_name: str = Field(..., min_length=1, max_length=50)


class UserLogin(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Public user representation."""

    id: int
    email: str
    display_name: str
    created_at: datetime


class TokenResponse(BaseModel):
    """JWT token pair returned after login/register."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Request body for token refresh."""

    refresh_token: str


# ---------------------------------------------------------------------------
# Module
# ---------------------------------------------------------------------------


class ModuleCreate(BaseModel):
    """Request body for creating a module."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=500)


class ModuleUpdate(BaseModel):
    """Request body for updating a module (all optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    enabled: Optional[bool] = None


class ModuleResponse(BaseModel):
    """Public module representation."""

    id: int
    name: str
    description: str
    enabled: bool
    created_at: datetime


# ---------------------------------------------------------------------------
# Activity
# ---------------------------------------------------------------------------


class ActivityCreate(BaseModel):
    """Request body for logging an activity."""

    module_id: int
    type: str = Field(..., min_length=1, max_length=50)
    value: float = Field(ge=0)
    metadata: Optional[dict] = None


class ActivityResponse(BaseModel):
    """Public activity representation."""

    id: int
    module_id: int
    type: str
    value: float
    metadata: Optional[dict]
    created_at: datetime
