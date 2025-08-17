
# sqlalchemy.orm: is Object Relational Mapper, which lets you interact with database tables using Python classes.
# Mapped: A typing hint used to declare attributes in ORM models.
# mapped_column: A function used to declare columns for ORM models.
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(autoincrement=True,nullable=False, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False, index=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column()
