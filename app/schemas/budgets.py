from pydantic import BaseModel, field_validator
from typing import Optional, List, Literal
from app.schemas.categories import CategoryBase

class BudgetBase(BaseModel):
    @field_validator("limit")
    def validate_limit(cls, v: float) -> float:
        if v < 0:
            raise ValueError("limit must be non-negative value")
        return v

    limit: float
    period: Literal["daily", "weekly", "monthly"]
    user_id: int
    category_id: int

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    limit: float
    period: Literal["daily", "weekly", "monthly"]


class BudgetResponse(BudgetBase):
    id: int
    category: CategoryBase
    
    class Config:
        from_attributes = True

class BudgetsResponse(BaseModel):
    total_count: int
    data: List[BudgetResponse]

    class Config:
        from_attributes = True