"""add column uuid and name to users table

Revision ID: ede60e1a6391
Revises: 7f4f9f9a8712
Create Date: 2025-06-06 01:43:24.063654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ede60e1a6391'
down_revision: Union[str, None] = '7f4f9f9a8712'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column(
        'uuid',
        sa.UUID(as_uuid=True),
        nullable=True,
        server_default=sa.text("gen_random_uuid()"),
    ))
    op.add_column('users', sa.Column(
        'name',
        sa.String(length=255),
        nullable=True
    ))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'name')
    op.drop_column('users', 'uuid')
