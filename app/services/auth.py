from sqlalchemy.orm import Session
from app.schemas.auth import Signup, Login
from app.core.security import get_password_hash, verify_password, get_user_token
from app.models.models import User
from fastapi import HTTPException, status

class AuthService:
    @staticmethod
    def signup(db: Session, signup_data: Signup):
        if db.query(User).filter(User.user_name == signup_data.user_name).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists."
            )
        hashed_password = get_password_hash(signup_data.password)

        new_user = User(
            first_name = signup_data.first_name,
            last_name = signup_data.last_name,
            user_name = signup_data.user_name,
            email = signup_data.email,
            hashed_password = hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    

    @staticmethod
    def login(db: Session, login_data: Login):
        user = db.query(User).filter(User.user_name == login_data.user_name).first()
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password."
            )
        
        return get_user_token(user_id=user.id)
