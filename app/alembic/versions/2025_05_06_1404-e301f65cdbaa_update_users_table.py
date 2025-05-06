"""update users table

Revision ID: e301f65cdbaa
Revises: ac0f0fe4f412
Create Date: 2025-05-06 14:04:16.285766

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e301f65cdbaa"
down_revision: Union[str, None] = "ac0f0fe4f412"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "role")
