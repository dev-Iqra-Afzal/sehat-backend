from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.resource import Resource
from ..schemas.resource import CreateResource, UpdateResource

class CRUDResource:

    async def create(self, db: AsyncSession, obj_in: CreateResource)-> Resource:
        db_obj = Resource(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj


    async def get_all(self, db: AsyncSession, offset: int = 0, limit: int = 10)-> dict:
        if offset<0 or limit<0:
            raise ValueError("Offset must be non-negative and limit must be positive.")

        query = select(Resource).offset(offset).limit(limit)
        result = await db.execute(query)
        resources = result.scalars().all()

        return {"resources":resources, "total":len(resources)}


    async def get(self, db: AsyncSession, id: int|None = None, hospital_name: str|None = None, hospital_username: str|None = None)-> Resource:

        query = select(Resource)
        if id is not None:
            query = query.where(Resource.id==id)
        elif hospital_name is not None:
            query = query.where(Resource.hospital_name==hospital_name)
        elif hospital_username is not None:
            query = query.where(Resource.hospital_username==hospital_username)
        
        
        result = await db.execute(query)

        return result.scalar_one_or_none()


    async def update(self, db: AsyncSession, obj_in: UpdateResource, id: int)-> Resource|None:
        resource = await self.get(db, id)

        if not resource:
            raise ValueError("Resource not found")

        query = (
            update(Resource)
            .where(Resource.id==id)
            .values(**obj_in.model_dump(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )

        await db.execute(query)
        await db.commit()
        return resource

    
    async def delete(self, db: AsyncSession, id: int)-> Resource | None:

        resource = await self.get(db,id)
        if not resource:
            raise ValueError("Resource not found")

        query = (
            delete(Resource)
            .where(Resource.id==id)
        )

        await db.execute(query)
        await db.commit()

        return resource

resource_crud = CRUDResource()

        

