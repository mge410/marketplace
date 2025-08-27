"""empty message

Revision ID: 94c1a406fe7e
Revises: e07fc0ac1257
Create Date: 2025-08-26 21:32:34.854488

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "94c1a406fe7e"
down_revision: Union[str, Sequence[str], None] = "e07fc0ac1257"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "categories", sa.Column("title", sa.String(length=100), nullable=False)
    )
    op.drop_constraint(op.f("uq_categories_name"), "categories", type_="unique")
    op.drop_constraint(op.f("uq_categories_slug"), "categories", type_="unique")
    op.create_unique_constraint(op.f("uq_categories_title"), "categories", ["title"])
    op.drop_column("categories", "name")
    op.drop_column("categories", "slug")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "categories",
        sa.Column("slug", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    )
    op.add_column(
        "categories",
        sa.Column("name", sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    )
    op.drop_constraint(op.f("uq_categories_title"), "categories", type_="unique")
    op.create_unique_constraint(
        op.f("uq_categories_slug"),
        "categories",
        ["slug"],
        postgresql_nulls_not_distinct=False,
    )
    op.create_unique_constraint(
        op.f("uq_categories_name"),
        "categories",
        ["name"],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_column("categories", "title")
