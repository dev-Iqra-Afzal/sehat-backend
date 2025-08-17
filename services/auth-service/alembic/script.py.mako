
# The message you pass when running alembic revision -m "Your message".
# ${up_revision}: A unique ID for this migration, usually a hash  
# ${down_revision}: The ID(s) of the parent migration(s). Alembic uses this to understand the migration history chain.
# ${create_date}: Timestamp of when the migration was generated.

"""${message}
Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
# These lines act as metadata — telling Alembic where this migration belongs in the overall database version history.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade schema."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade schema."""
    ${downgrades if downgrades else "pass"}
