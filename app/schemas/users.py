from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    user_name: str
    email: EmailStr
    