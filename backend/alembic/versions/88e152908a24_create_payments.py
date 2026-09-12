"""create payments table

Revision ID: 88e152908a24
Revises: 4533a006b998
Create Date: 2026-09-13

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "88e152908a24"
down_revision: str | None = "4533a006b998"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.Uuid(), nullable=False),
        sa.Column("booking_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=20), nullable=False),
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
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_index("ix_payments_public_id", "payments", ["public_id"], unique=True)
    op.create_index("ix_payments_booking_id", "payments", ["booking_id"])


def downgrade() -> None:
    op.drop_index("ix_payments_booking_id", table_name="payments")
    op.drop_index("ix_payments_public_id", table_name="payments")
    op.drop_table("payments")
