from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Enum, Date, func
from sqlalchemy.orm import relationship
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    user_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    current_balance = Column(Float, nullable=False, default=0.0, server_default="0.0")

    transactions = relationship("Transaction", back_populates="user")
    budgets = relationship("Budget", back_populates="user")


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    is_expense = Column(Boolean, nullable=False, default=True, server_default="true")
    transaction_date = Column(Date, server_default=func.now())

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="transactions")

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="transactions")


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    limit = Column(Float, nullable=False)
    period = Column(Enum("daily", "weekly", "monthly", name="budget_period", create_type=True), nullable=False, server_default="monthly")

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="budgets")

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Category", back_populates="budgets")
