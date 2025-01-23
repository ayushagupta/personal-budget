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
    transactions: List[TransactionBase]
    budgets: List[BudgetBase]

class UserCreate(UserBase):
    password: SecretStr = Field(..., min_length=8, description="Password must have at least 8 characters.")
    transactions: List[TransactionBase] = []
    budgets: List[BudgetBase] = []

class UserUpdate(BaseModel):
    first_name: str
    last_name: str

class PasswordUpdate(BaseModel):
    current_password: SecretStr = Field(..., description="The current password of the user.")
    new_password: SecretStr = Field(..., min_length=8, description="The new password must be at least 8 characters long.")

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UsersResoponse(BaseModel):
    total_count: int
    data: List[UserResponse]

    class Config:
        from_attributes = True