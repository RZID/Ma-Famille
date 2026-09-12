"""create courts table

Revision ID: 838d6949cfbe
Revises: 895af8a4ec9e
Create Date: 2026-09-13

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "838d6949cfbe"
down_revision: str | None = "895af8a4ec9e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "courts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.Uuid(), nullable=False),
        sa.Column("venue_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("sport", sa.String(length=20), nullable=False),
        sa.Column("price_weekday", sa.Integer(), nullable=False),
        sa.Column("price_weekend", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
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
        sa.ForeignKeyConstraint(["venue_id"], ["venues.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_index("ix_courts_public_id", "courts", ["public_id"], unique=True)
    op.create_index("ix_courts_venue_id", "courts", ["venue_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_courts_venue_id", table_name="courts")
    op.drop_index("ix_courts_public_id", table_name="courts")
    op.drop_table("courts")
