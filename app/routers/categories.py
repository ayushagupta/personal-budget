from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryResponse, CategoriesResponse
from app.services.categories import CategoryService
from app.database.database import get_db
from app.utils.responses import ResponseHandler

router = APIRouter(tags=["Categories"], prefix="/categories")

@router.get("/", response_model=CategoriesResponse)
def get_all_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page Number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query("", description="Search based on name of categories")
    ):
    try:
        categories = CategoryService.get_all_categories(db, page, limit, search)
        categories_response = [CategoryResponse.model_validate(category, from_attributes=True).model_dump()
                               for category in categories]
        response = CategoriesResponse(total_count=len(categories_response), data=categories_response)
        return ResponseHandler.success_response(data=response.model_dump(), status_code=200)
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db)
    ):
    try:
        category = CategoryService.get_category_by_id(db, category_id)
        if not category:
            return ResponseHandler.not_found_response(f"Category with id {category_id} not found")
        
        category_response = CategoryResponse.model_validate(category, from_attributes=True)
        return ResponseHandler.success_response(data=category_response.model_dump(), message="Category found successfully", status_code=200)
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)
    

@router.post("/", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
    ):
    try:
        created_category = CategoryService.create_category(db, category)
        created_category_response = CategoryResponse.model_validate(created_category, from_attributes=True)
        return ResponseHandler.success_response(data=created_category_response.model_dump(), message="Category created successfully", status_code=201)
    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
    ):
    try:
        updated_category = CategoryService.update_category(db, category_id, category)
        if not updated_category:
            ResponseHandler.not_found_response(f"Category with id {category_id} not found")

        update_category_response = CategoryResponse.model_validate(updated_category, from_attributes=True)
        return ResponseHandler.success_response(data=update_category_response.model_dump(), message="Category updated successfully", status_code=200)

    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)
    

@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
    ):
    try:
        deleted_category = CategoryService.delete_category(db, category_id)
        if not deleted_category:
            ResponseHandler.not_found_response(f"Category with id {category_id} not found")

        deleted_category_response = CategoryResponse.model_validate(deleted_category, from_attributes=True)
        return ResponseHandler.success_response(data=deleted_category_response.model_dump(), message="Category deleted successfully", status_code=200)

    except Exception as e:
        return ResponseHandler.error_response(message=f"Internal server error: {str(e)}", status_code=500)