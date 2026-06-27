from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class ActivityBase(BaseModel):
    module_id: int
    type: str = Field(..., min_length=1, max_length=50)
    value: float = Field(ge=0)
    metadata: Optional[Dict[str, Any]] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True