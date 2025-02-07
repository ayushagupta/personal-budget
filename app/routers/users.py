from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.users import UserResponse, UsersResponse, UserCreate, UserUpdate
from app.services.users import UserService
from app.database.database import get_db
from app.utils.responses import ResponseHandler

router = APIRouter(tags=["Users"], prefix="/users")

@router.get("/", response_model=UsersResponse)
def get_all_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page Number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based on username")
    ):
    try:
        users = UserService.get_all_users(db, page, limit, search)
        users_response = [UserResponse.model_validate(user, from_attributes=True).model_dump()
                          for user in users]
        response = UsersResponse(total_count=len(users_response), data=users_response)
        return ResponseHandler.success_response(data=response.model_dump(), status_code=200)

    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)
    

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return ResponseHandler.not_found_response(message=f"User with id {user_id} not found")
        
        user_response = UserResponse.model_validate(user, from_attributes=True)
        return ResponseHandler.success_response(data=user_response.model_dump(), message="User found successfully", status_code=200)
    
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)
    

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = UserService.create_user(db, user)
        created_user_response = UserResponse.model_validate(created_user, from_attributes=True)
        return ResponseHandler.success_response(data=created_user_response.model_dump(), message="User created successfully", status_code=201)
    
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)
    

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        updated_user = UserService.update_user(db, user_id, user)
        if not updated_user:
            ResponseHandler.not_found_response(f"User with id {user_id} not found")

        updated_user_response = UserResponse.model_validate(updated_user, from_attributes=True)
        return ResponseHandler.success_response(data=updated_user_response.model_dump(), message="User updated successfully", status_code=200)
    
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)
    
    
@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        deleted_user = UserService.delete_user(db, user_id)
        if not deleted_user:
            return ResponseHandler.not_found_response(f"User with id {user_id} not found")
        
        deleted_user_response = UserResponse.model_validate(deleted_user, from_attributes=True)
        return ResponseHandler.success_response(data=deleted_user_response.model_dump(), message="User deleted successfully", status_code=200)
    
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)