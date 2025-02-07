from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.users import UserCreate, UserUpdate
from app.core.security import get_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class UserService:
    @staticmethod
    def get_all_users(db: Session, page: int, limit: int, search: str = ""):
        return db.query(User).order_by(User.id.asc()).filter(User.user_name.contains(search)).limit(limit).offset((page-1)*limit).all()
    

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None
        return db_user
    

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(
            first_name = user.first_name,
            last_name = user.last_name,
            user_name = user.user_name,
            email = user.email,
            hashed_password = hashed_password,
            current_balance = user.current_balance
        )
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise ValueError("User with this email already exists")


    @staticmethod
    def update_user(db: Session, user_id: int, user: UserUpdate):
        try:
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user:
                for key, value in user.model_dump().items():
                    setattr(db_user, key, value)
                db.commit()
                db.refresh(db_user)
                return db_user
            return None

        except SQLAlchemyError as e:
            db.rollback()
            raise ValueError(f"Error updating user: {str(e)}")
        

    @staticmethod
    def delete_user(db: Session, user_id: int):
        try:
            db_user = db.query(User).filter(User.id == user_id).first()
            if not db_user:
                return None

            db.delete(db_user)
            db.commit()
            return db_user
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Error deleting user")