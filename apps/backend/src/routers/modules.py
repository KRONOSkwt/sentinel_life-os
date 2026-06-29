"""Modules CRUD routes."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.deps import get_current_user
from src.models.db import Module, User
from src.models.schemas import ModuleCreate, ModuleResponse, ModuleUpdate

router = APIRouter(prefix="/modules", tags=["modules"])


# ---------------------------------------------------------------------------
# List modules (current user)
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[ModuleResponse])
def list_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return all modules owned by the current user."""
    return db.query(Module).filter(Module.owner_id == current_user.id).all()


# ---------------------------------------------------------------------------
# Get module by ID
# ---------------------------------------------------------------------------

@router.get("/{module_id}", response_model=ModuleResponse)
def get_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return a single module by ID (must be owned by current user)."""
    module = (
        db.query(Module)
        .filter(Module.id == module_id, Module.owner_id == current_user.id)
        .first()
    )
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found",
        )
    return module


# ---------------------------------------------------------------------------
# Create module
# ---------------------------------------------------------------------------

@router.post("/", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
def create_module(
    body: ModuleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new module for the current user."""
    module = Module(
        name=body.name,
        description=body.description,
        owner_id=current_user.id,
    )
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


# ---------------------------------------------------------------------------
# Update module
# ---------------------------------------------------------------------------

@router.patch("/{module_id}", response_model=ModuleResponse)
def update_module(
    module_id: int,
    body: ModuleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Partially update a module (must be owned by current user)."""
    module = (
        db.query(Module)
        .filter(Module.id == module_id, Module.owner_id == current_user.id)
        .first()
    )
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found",
        )

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(module, field, value)

    db.commit()
    db.refresh(module)
    return module


# ---------------------------------------------------------------------------
# Delete module
# ---------------------------------------------------------------------------

@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a module and its cascade activities (must be owned by current user)."""
    module = (
        db.query(Module)
        .filter(Module.id == module_id, Module.owner_id == current_user.id)
        .first()
    )
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found",
        )
    db.delete(module)
    db.commit()
