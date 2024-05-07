"""create hero table

Revision ID: 968206a51bc2
Revises: ac42dfa6e929
Create Date: 2024-04-30 11:00:28.947710

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa
import sqlmodel



# revision identifiers, used by Alembic.
revision: str = '968206a51bc2'
down_revision: str | None = 'ac42dfa6e929'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workouts')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workouts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('set', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rep', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('weight', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='workouts_pkey')
    )
    # ### end Alembic commands ###