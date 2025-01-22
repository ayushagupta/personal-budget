from sqlalchemy.orm import Session
from app.models.models import Category
from app.schemas.categories import CategoryCreate, CategoryUpdate, CategoryResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class CategoryService:
    @staticmethod
    def get_all_categories(db: Session, page: int, limit: int, search: str = ""):
        return db.query(Category).order_by(Category.id.asc()).filter(Category.name.contains(search)).limit(limit).offset((page-1)*limit).all()


    @staticmethod
    def get_category_by_id(db: Session, category_id: int):
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return None
        return db_category
    

    @staticmethod
    def create_category(db: Session, category: CategoryCreate):
        db_category = Category(
            name = category.name,
            description = category.description
        )
        try:
            db.add(db_category)
            db.commit()
            db.refresh(db_category)
            return db_category
        except IntegrityError:
            db.rollback()
            raise ValueError("Category with this name already exists")
        

    @staticmethod
    def update_category(db: Session, category_id: int, category: CategoryUpdate):
        try:
            db_category = db.query(Category).filter(Category.id == category_id).first()
            if db_category:
                for key, value in category.model_dump().items():
                    setattr(db_category, key, value)
                db.commit()
                db.refresh(db_category)
                return db_category
            return None
        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Error updating category: {str(e)}")
    

    @staticmethod
    def delete_category(db: Session, category_id: int):
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
            return db_category
        return None