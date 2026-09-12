"""create slots table

Revision ID: 3aedc811d045
Revises: 838d6949cfbe
Create Date: 2026-09-13

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "3aedc811d045"
down_revision: str | None = "838d6949cfbe"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "slots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.Uuid(), nullable=False),
        sa.Column("court_id", sa.Integer(), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
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
        sa.CheckConstraint("ends_at > starts_at", name="ck_slots_ends_after_starts"),
        sa.ForeignKeyConstraint(["court_id"], ["courts.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_id"),
    )
    op.create_index("ix_slots_public_id", "slots", ["public_id"], unique=True)
    op.create_index("ix_slots_court_starts", "slots", ["court_id", "starts_at"])


def downgrade() -> None:
    op.drop_index("ix_slots_court_starts", table_name="slots")
    op.drop_index("ix_slots_public_id", table_name="slots")
    op.drop_table("slots")
