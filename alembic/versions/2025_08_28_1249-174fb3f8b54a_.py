"""empty message

Revision ID: 174fb3f8b54a
Revises: a3b5f4216a62
Create Date: 2025-08-28 12:49:50.820338

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "174fb3f8b54a"
down_revision: Union[str, Sequence[str], None] = "a3b5f4216a62"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users",
        "uuid",
        existing_type=sa.VARCHAR(length=36),
        type_=sa.UUID(),
        postgresql_using="uuid::uuid",
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users",
        "uuid",
        existing_type=sa.UUID(),
        type_=sa.VARCHAR(length=36),
        postgresql_using="uuid::text",
        existing_nullable=False,
    )
