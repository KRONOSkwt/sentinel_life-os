"""Auth service — business logic for authentication."""

from sqlalchemy.orm import Session

from src.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    validate_password_strength,
)
from src.models.db import User


def register_user(db: Session, email: str, password: str, display_name: str) -> User:
    """Register a new user. Raises ValueError on validation failure."""
    errors = validate_password_strength(password)
    if errors:
        raise ValueError("; ".join(errors))
    if db.query(User).filter(User.email == email).first():
        raise ValueError("Email already registered")
    user = User(
        email=email,
        password_hash=hash_password(password),
        display_name=display_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> dict:
    """Authenticate user and return token pair. Raises ValueError on failure."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }