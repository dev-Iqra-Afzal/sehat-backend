# from sqlalchemy.ext.asyncio gives you asynchronous (non-blocking) versions of SQLAlchemy’s database tools
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from collections.abc import AsyncGenerator

from ..config import settings

# DeclarativeBase – the base for mapping Python classes to database tables
# MappedAsDataclass - it makes SQLAlchemy model classes behave like Python dataclasses — automatically.
# A dataclass is a convenient way to create classes that are mainly used to store data.
# Normally, when you create a class to store data, you have to write a lot of code (like __init__, __repr__, __eq__, etc). 
# The @dataclass decorator automatically adds that for you.
class Base(DeclarativeBase, MappedAsDataclass):
    pass


DATABASE_URI = settings.POSTGRES_URI
DATABASE_PREFIX = settings.POSTGRES_ASYNC_PREFIX
DATABASE_URL = f"{DATABASE_PREFIX}{DATABASE_URI}"

# It creates a special object that serves as manager for database connections.
# when this object is created, it creates a connection pool to the database.
# echo - If True, logs all SQL statements (for debugging).
# future - Should always be True for SQLAlchemy 2.0+ compatibility.
async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# It's a factory to create async sessions for talking to the database.
local_session = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# It's a generator function that creates a session and yields it for use in the application.
async def async_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with local_session() as db:  # It's a context manager that creates a session and yields it for use in the application.
        yield db 
