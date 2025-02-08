from pydantic import BaseModel, Field
from typing import List
from datetime import date
from app.schemas.categories import CategoryBase

class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount must be positive.")
    is_expense: bool
    transaction_date: date
    category_id: int

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    category: CategoryBase
    transaction_date: str

    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj, *, from_attributes=False):
        obj.transaction_date = obj.transaction_date.isoformat()
        return super().model_validate(obj, from_attributes=from_attributes)

class TransactionsResponse(BaseModel):
    total_count: int = Field(..., ge=0, description="Total count must be non-negative.")
    data: List[TransactionResponse]

    class Config:
        from_attributes = True