"""store doku invoice number on payments

Revision ID: 7e64e7cfb3e0
Revises: 88e152908a24
Create Date: 2026-09-13

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "7e64e7cfb3e0"
down_revision: str | None = "88e152908a24"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("payments", sa.Column("invoice_number", sa.String(60), nullable=True))
    op.create_index(
        "ix_payments_invoice_number", "payments", ["invoice_number"], unique=True
    )


def downgrade() -> None:
    op.drop_index("ix_payments_invoice_number", table_name="payments")
    op.drop_column("payments", "invoice_number")
