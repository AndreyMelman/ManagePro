"""Create teams table

Revision ID: 857f57b91bcd
Revises: e301f65cdbaa
Create Date: 2025-05-07 11:49:18.677252

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "857f57b91bcd"
down_revision: Union[str, None] = "e301f65cdbaa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("admin_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["admin_id"], ["users.id"], name=op.f("fk_teams_admin_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teams")),
        sa.UniqueConstraint("code", name=op.f("uq_teams_code")),
        sa.UniqueConstraint("name", name=op.f("uq_teams_name")),
    )
    op.add_column("users", sa.Column("team_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_users_team_id_teams"),
        "users",
        "teams",
        ["team_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_users_team_id_teams"), "users", type_="foreignkey"
    )
    op.drop_column("users", "team_id")
    op.drop_table("teams")

