from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import Signup, Login, TokenResponse
from app.database.database import get_db
from app.services.auth import AuthService
from app.utils.responses import ResponseHandler

router = APIRouter(tags=["Auth"], prefix="/auth")

@router.post("/signup")
def signup(signup_data: Signup, db: Session = Depends(get_db)):
    try:
        new_user = AuthService.signup(db, signup_data)
        return ResponseHandler.success_response(
            data={
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "user_name": new_user.user_name,
                "email": new_user.email
            },
            message="User registered successfully."
        )
    except HTTPException as e:
        if e.status_code == 401:
            return ResponseHandler.unauthorized_response(message=e.detail)
        return ResponseHandler.error_response(message="Failed to register user.")
    

@router.post("/login")
def login(login_data: Login, db: Session = Depends(get_db)):
    try:
        tokens = AuthService.login(db, login_data)
        token_response = TokenResponse.model_validate(tokens, from_attributes=True)
        return ResponseHandler.success_response(
            data=token_response.model_dump(),
            message="Login successful."
        )
    except HTTPException as e:
        if e.status_code == 401:
            return ResponseHandler.unauthorized_response(message=e.detail)
        return ResponseHandler.error_response(message="Login failed.")