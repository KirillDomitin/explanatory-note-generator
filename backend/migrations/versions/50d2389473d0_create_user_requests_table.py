"""create user_requests table

Revision ID: 50d2389473d0
Revises:
Create Date: 2026-03-17 00:30:10.428848
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "50d2389473d0"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_requests",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("inn", sa.String(length=12), nullable=False),
        sa.Column("name", sa.String(length=512), nullable=True),
        sa.Column(
            "status",
            postgresql.ENUM("success", "failed", name="request_status_enum"),
            nullable=False,
        ),
        sa.Column("error_message", sa.Text(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_requests")),
    )

    op.create_index(
        "ix_user_requests_user_id_created_at",
        "user_requests",
        ["user_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_user_requests_user_id_created_at", table_name="user_requests")
    op.drop_table("user_requests")
    postgresql.ENUM(name="request_status_enum").drop(op.get_bind(), checkfirst=True)