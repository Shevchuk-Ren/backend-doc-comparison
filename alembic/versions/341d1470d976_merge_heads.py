"""merge heads

Revision ID: 341d1470d976
Revises: eff1cc2b9e6f
Create Date: 2026-03-17 17:07:24.075363

"""

from typing import Sequence, Union

from alembic import op  # noqa: F401
import sqlalchemy as sa  # noqa: F401

# revision identifiers, used by Alembic.
revision: str = "341d1470d976"
down_revision: Union[str, None] = "eff1cc2b9e6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
