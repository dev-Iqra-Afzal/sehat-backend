
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Any
from fastapi import Request
from fastcrud.paginated import PaginatedListResponse
import httpx

from ..core.db.database import async_get_db
from ..schemas.user import BaseUser, CreateUser, CreateUserInternal, UpdateUser
from ..crud.user import user_crud
from ..core.security import get_password_hash
from ..core.utils import paginated_response
from ..core.rabbitmq import publish_notification

router = APIRouter(tags=["users"])


@router.post("/users", response_model=BaseUser)
async def create_user(
    request: Request,
    user: CreateUser,
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> BaseUser:
    if await user_crud.get(db=db, email=user.email):
        raise HTTPException(status_code=400, detail="Email is already registered") 
    
    if await user_crud.get(db=db, username=user.username):
        raise HTTPException(status_code=400, detail="Username not available")
    
    user_internal_dict = user.model_dump()
    user_internal_dict["password_hash"] = await get_password_hash(user_internal_dict["password"])
    del user_internal_dict["password"]

    user_internal = CreateUserInternal(**user_internal_dict)
    created_user = await user_crud.create(db=db, obj_in=user_internal)


    if created_user.role == "hospital_professional":
        resource_payload = {
            "hospital_name": created_user.name,
            "hospital_username": created_user.username,
            "icu_beds": 0,
            "ventilators": 0,
            "monitors": 0,
            "defibrillators": 0,
            "infusion_pumps": 0,
            "oxygen_cylinders": 0,
            "xray_machines": 0,
            "ultrasound_machines": 0,
            "ct_scanners": 0,
            "mri_machines": 0,
            "ecg_machines": 0,
            "dialysis_machines": 0
        }

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "http://resource-service:8000/resource",
                    json=resource_payload,
                    timeout=10
                )
                resp.raise_for_status()

        except httpx.HTTPError as e:
            # Log error but don't block user creation
            print(f"⚠ Failed to create resource for hospital {created_user.username}: {e}")

    # Publish notification to RabbitMQ
    publish_notification(
        user_ids=[created_user.id],  
        title="Welcome!",
        message=f"Hello {created_user.username}, your account was created successfully."
    )

    return BaseUser.model_validate(created_user)


@router.get("/users", response_model=PaginatedListResponse[BaseUser])
async def get_users(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)]
)-> BaseUser:
    
    users = await user_crud.get_all(db)

    processed_users = []
    for user in users["users"]:
        processed_users.append(BaseUser.model_validate(user)) 

    response: dict[str, Any] = paginated_response(
        crud_data=processed_users,
        page=1,
        has_more = 20 * 1 < users["total"],
        total=users["total"],
        limit=20
    )
    return response


@router.get("/users/{username}", response_model=BaseUser)
async def get_user(
    request: Request,
    username: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
)-> BaseUser:
    
    user = await user_crud.get(db=db,username=username)
    if not user:
        raise HTTPException("User not found...!")
    
    return BaseUser.model_validate(user)


@router.patch("/users/{username}", response_model=BaseUser)
async def update_user(
    request: Request,
    username: str,
    user_in: UpdateUser,
    db: Annotated[AsyncSession, Depends(async_get_db)]
)-> BaseUser:
    
    user = user_crud.get(db=db, username=username)
    if not user:
        raise HTTPException("User not exists...!")
    
    updated_user = await user_crud.update(db=db, obj_in=user_in, username=username)

    return BaseUser.model_validate(updated_user)

    
@router.delete("/users/{username}")
async def delete_user(
    request: Request,
    username: str,
    db: Annotated[AsyncSession, Depends(async_get_db)]
)-> dict[str, Any]:
    
    user = await user_crud.get(db=db, username=username)

    if not user:
        HTTPException("User not found...!")

    deleted_user = await user_crud.delete(db=db, username=username)

    return {"message: ": "User deleted"}

    
