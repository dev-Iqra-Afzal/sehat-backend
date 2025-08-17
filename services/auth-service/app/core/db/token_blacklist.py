from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import TIMESTAMP

from .database import Base

class TokenBlacklist(Base):
    __tablename__ = 'token_blacklist'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
