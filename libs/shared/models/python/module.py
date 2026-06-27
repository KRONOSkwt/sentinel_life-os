from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ModuleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=500)

class ModuleCreate(ModuleBase):
    pass

class ModuleResponse(ModuleBase):
    id: int
    enabled: bool = True
    created_at: datetime

    class Config:
        from_attributes = True