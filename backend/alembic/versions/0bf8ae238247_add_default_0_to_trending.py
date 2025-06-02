"""Add default 0 to trending column in agents table

Revision ID: 0bf8ae238247
Revises: 9fc7de7517f6
Create Date: 2025-06-02 14:18:59.204016
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0bf8ae238247"
down_revision = "9fc7de7517f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Set default value to 0 on trending column
    op.alter_column(
        "agents",
        "trending",
        server_default=sa.text("0"),
        existing_type=sa.INTEGER(),
        existing_nullable=True,
    )

    # Optionally, set existing NULL trending values to 0
    op.execute("UPDATE agents SET trending = 0 WHERE trending IS NULL")


def downgrade() -> None:
    # Remove default value on trending column
    op.alter_column(
        "agents",
        "trending",
        server_default=None,
        existing_type=sa.INTEGER(),
        existing_nullable=True,
    )
