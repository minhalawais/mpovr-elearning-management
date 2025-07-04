"""Update application status enum type

Revision ID: 8e8edf3c4b11
Revises: e8def53fa06d
Create Date: 2024-12-15 23:20:38.358226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8e8edf3c4b11'
down_revision: Union[str, None] = 'e8def53fa06d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add start_date column with a default value
    op.add_column('programs', 
        sa.Column('start_date', sa.Date(), nullable=False, server_default=sa.text("CURRENT_DATE"))
    )

def downgrade():
    # Remove start_date column
    op.drop_column('programs', 'start_date')