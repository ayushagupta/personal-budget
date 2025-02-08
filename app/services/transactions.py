from sqlalchemy.orm import Session
from app.models.models import Transaction
from app.schemas.transactions import TransactionCreate, TransactionUpdate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.security import get_current_user
from fastapi import HTTPException

class TransactionService:
    @staticmethod
    def get_all_transactions(db: Session, page: int, limit: int, token: str):
        try:
            user = get_current_user(token, db)
            return db.query(Transaction).filter(Transaction.user_id == user.id).order_by(Transaction.id.asc()).limit(limit).offset((page-1)*limit).all()
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise ValueError(f"Error fetching transactions: {str(e)}")


    @staticmethod
    def get_transaction_by_id(db: Session, transaction_id: int, token: str):
        try:
            user = get_current_user(token, db)
            db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user.id).first()
            if not db_transaction:
                return None
            return db_transaction
        except HTTPException as http_exc:
            raise http_exc
    

    @staticmethod
    def create_transaction(db: Session, transaction: TransactionCreate, token: str):
        try:
            user = get_current_user(token, db)
            db_transaction = Transaction(
                amount = transaction.amount,
                is_expense = transaction.is_expense,
                transaction_date = transaction.transaction_date,
                user_id = user.id,
                category_id = transaction.category_id
            )
            db.add(db_transaction)
            db.commit()
            db.refresh(db_transaction)
            return db_transaction
        except HTTPException as http_exc:
            raise http_exc
        except IntegrityError:
            db.rollback()
            raise ValueError("Error creating transaction")


    @staticmethod
    def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate, token: str):
        try:
            user = get_current_user(token, db)
            db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user.id).first()
            if not db_transaction:
                return None
            for key, value in transaction.model_dump().items():
                setattr(db_transaction, key, value)
            db.commit()
            db.refresh(db_transaction)
            return db_transaction
        except HTTPException as http_exc:
            raise http_exc
        except IntegrityError:
            db.rollback()
            raise ValueError("Error updating transaction")


    @staticmethod
    def delete_transaction(db: Session, transaction_id: int, token: str):
        try:
            user = get_current_user(token, db)
            db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user.id).first()
            if not db_transaction:
                return None
            db.delete(db_transaction)
            db.commit()
            return {"transaction_id": transaction_id }
        except HTTPException as http_exc:
            raise http_exc
        except IntegrityError:
            db.rollback()
            raise ValueError("Error deleting transaction")