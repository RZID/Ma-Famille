"""create bookings table

Revision ID: 4533a006b998
Revises: 3aedc811d045
Create Date: 2026-09-13

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "4533a006b998"
down_revision: str | None = "3aedc811d045"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.Uuid(), nullable=False),
        sa.Column("slot_id", sa.Integer(), nullable=False),
        sa.Column("customer_name", sa.String(length=120), nullable=False),
        sa.Column("customer_contact", sa.String(length=60), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
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
        sa.ForeignKeyConstraint(["slot_id"], ["slots.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_index("ix_bookings_public_id", "bookings", ["public_id"], unique=True)
    op.create_index(
        "ix_bookings_slot_active",
        "bookings",
        ["slot_id"],
        unique=True,
        postgresql_where=sa.text("status <> 'cancelled'"),
    )


def downgrade() -> None:
    op.drop_index("ix_bookings_slot_active", table_name="bookings")
    op.drop_index("ix_bookings_public_id", table_name="bookings")
    op.drop_table("bookings")
