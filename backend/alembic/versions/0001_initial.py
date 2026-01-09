"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-01-09
"""

from alembic import op
from sqlmodel import SQLModel

import app.models  # noqa: F401
from app.db.session import engine

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Use SQLModel metadata to create all tables as initial migration
    SQLModel.metadata.create_all(bind=engine)


def downgrade() -> None:
    # Drop all tables on downgrade
    SQLModel.metadata.drop_all(bind=engine)


