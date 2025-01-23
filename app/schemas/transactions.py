from pydantic import BaseModel, Field
from typing import List
from datetime import date
from app.schemas.users import UserBase
from app.schemas.categories import CategoryBase

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount must be positive.")
    is_expense: bool
    transaction_date: date
    user_id: int
    category_id: int

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: float | None = Field(None, gt=0, description="Transaction amount must be positive.")
    is_expense: bool | None = None
    transaction_date: date | None = None
    category_id: int | None = None

class TransactionResponse(TransactionBase):
    id: int
    user: UserBase
    category: CategoryBase

    class Config:
        from_attributes = True

class TransactionsResponse(BaseModel):
    total_count: int = Field(..., ge=0, description="Total count must be non-negative.")
    data: List[TransactionResponse]

    class Config:
        from_attributes = True