"""create venues table

Revision ID: 895af8a4ec9e
Revises:
Create Date: 2026-09-13

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "895af8a4ec9e"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "venues",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_index("ix_venues_public_id", "venues", ["public_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_venues_public_id", table_name="venues")
    op.drop_table("venues")
