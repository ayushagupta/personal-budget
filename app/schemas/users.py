from pydantic import BaseModel, EmailStr, Field, SecretStr
from typing import List
from app.schemas.transactions import TransactionBase
from app.schemas.budgets import BudgetBase

class UserBase(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    current_balance: float = Field(..., ge=0, description="Balance should be non-negative.")

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: str
    last_name: str

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

class UserResponse(UserBase):
    id: int
    transactions: List[TransactionBase]
    budgets: List[BudgetBase]
    
    class Config:
        from_attributes = True

class UsersResponse(BaseModel):
    total_count: int
    data: List[UserResponse]

    class Config:
        from_attributes = True