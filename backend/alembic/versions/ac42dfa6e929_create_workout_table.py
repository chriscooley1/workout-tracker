"""create_workout_table

Revision ID: ac42dfa6e929
Revises: 
Create Date: 2024-04-26 10:19:42.396015

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac42dfa6e929'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table("workouts",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column("name", sa.String),
                    sa.Column("set", sa.Integer),
                    sa.Column("rep", sa.Integer),
                    sa.Column("weight", sa.Integer))
    

def downgrade() -> None:
    op.drop_table("workouts")