"""Initial migration

Revision ID: c5ee3ac69981
Revises: 
Create Date: 2025-01-21 18:26:51.312225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5ee3ac69981'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('current_balance', sa.Float(), server_default='0.0', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('budgets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('limit', sa.Float(), nullable=False),
    sa.Column('period', sa.Enum('daily', 'weekly', 'monthly', name='budget_period'), server_default='monthly', nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('is_expense', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('date', sa.Date(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('budgets')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###
