from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from ..models.user import User
from ..schemas.user import CreateUserInternal, UpdateUser

class CRUDUser:

    """
    Create a new user
    """
    async def create(self, db: AsyncSession, obj_in: CreateUserInternal)-> User:
        db_obj = User(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        # Refresh the instance to get the updated state from the database
        await db.refresh(db_obj)
        return db_obj
    
    """
    Get users with pagination
    """
    async def get_all(self, db: AsyncSession, offset: int = 0, limit: int = 10) -> dict:
        # offset means how many records to skip, limit means how many records to return
        if offset < 0 or limit <= 0:
            raise ValueError("Offset must be non-negative and limit must be positive.")
        
        query = select(User).offset(offset).limit(limit)
        result = await db.execute(query)
        users = result.scalars().all()
        return {"users": users, "total": len(users)}
    
    """
    Get a user by username, id, or email
    """
    async def get(self, db: AsyncSession, username: str|None = None, id: int|None = None, email: str|None = None) -> User | None:
        query = select(User)
        if username:
            query = query.where(User.username == username)
        elif id:
            query = query.where(User.id == id)
        elif email:
            query = query.where(User.email == email)
        else:
            raise ValueError("At least one parameter (username, id, or email) must be provided.")
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    """
    update a user by username, id, or email
    """
    async def update(self, db: AsyncSession, obj_in: UpdateUser, username: str|None = None, id: int|None = None, email: str|None = None) -> User | None: 
        if not (username or id or email):
            raise ValueError("At least one parameter (username, id, or email) must be provided.")
        
        user = None
        if username:
            user = await self.get(db, username=username)
        elif id:
            user = await self.get(db, id=id)
        elif email:
            user = await self.get(db, email=email)

        if not user:
            raise ValueError("User not found.")

        query = (
            update(User)
            .where(User.id == user.id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await db.commit()
        return user
    
    """
    Delete a user by username, id, or email
    """
    async def delete(self, db: AsyncSession, username: str|None = None, id: int|None = None, email: str|None = None) -> User | None:
        user = None
        if username:
            user = await self.get(db, username=username)
        elif id:
            user = await self.get(db, id=id)
        elif email:
            user = await self.get(db, email=email)

        if not user:
            raise ValueError("User not found.")
        
        query = (
            delete(User)
            .where(User.id == user.id)
        )

        await db.execute(query)
        await db.commit()
        return user

user_crud = CRUDUser()