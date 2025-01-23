from pydantic import BaseModel, Field
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class CategoriesResponse(BaseModel):
    total_count: int = Field(..., ge=0, description="Total count must be non-negative.")
    data: List[CategoryResponse]

    class Config:
        from_attributes = True