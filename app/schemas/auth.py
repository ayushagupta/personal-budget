from pydantic import BaseModel, EmailStr, Field
from typing import List
from app.schemas.transactions import TransactionBase
from app.schemas.budgets import BudgetBase

class BaseConfig:
    from_attributes = True


class AuthUserBase(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr


class Signup(AuthUserBase):
    password: str


class Login(BaseModel):
    user_name: str
    password: str


class UserOut(BaseModel):
    message: str
    data: AuthUserBase


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'
    expires_in: int

