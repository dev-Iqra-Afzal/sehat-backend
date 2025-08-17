from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Any
from fastcrud.paginated import PaginatedListResponse
import urllib.parse
import httpx

from ..core.database import async_get_db
from ..schemas.resource import CreateResource, UpdateResource, ReadResource
from ..crud.resource import resource_crud
from ..core.utils import paginated_response
from ..core.rabbitmq import publish_notification


router = APIRouter(tags=["resources"])

@router.post("/resource")
async def create_resource(
    resource: CreateResource,
    db: Annotated[AsyncSession, Depends(async_get_db)]
)-> ReadResource:
    
    resource = await resource_crud.create(db, resource)

    # Send GET request to http://auth-service:8001/users
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://auth-service:8000/users",
            timeout=20
        )

    # Parse JSON
    resp_json = response.json()
    users = resp_json["data"]

    # Iterate and publish notifications
    for user in users:
        publish_notification(
            user_ids=[user["id"]],
            title="New Resource Added",
            message=f"Resource for {resource.hospital_name} has been added."
        )

    return ReadResource.model_validate(resource)


@router.get("/resources", response_model=PaginatedListResponse[ReadResource])
async def get_resources(
    request: Request,
    db: Annotated[AsyncSession, Depends(async_get_db)]
)-> ReadResource:
    
    resources = await resource_crud.get_all(db)

    processed_resources = []
    for resource in resources["resources"]:
        processed_resources.append(ReadResource.model_validate(resource)) 

    response: dict[str, Any] = paginated_response(
        crud_data=processed_resources,
        page=1,
        has_more = 20 * 1 < resources["total"],
        total=resources["total"],
        limit=20
    )
    return response


@router.get("/resources/{hospital_name}")
async def get_user(
    request: Request,
    hospital_name: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
):

    decoded_name = urllib.parse.unquote(hospital_name)
    resource = await resource_crud.get(db=db, hospital_name=decoded_name)
    
    if not resource:
        return ReadResource(
            id = "Unknown",
            icu_beds="Unknown",
            ventilators="Unknown",
            monitors="Unknown",
            defibrillators="Unknown",
            infusion_pumps="Unknown",
            oxygen_cylinders="Unknown",
            xray_machines="Unknown",
            ultrasound_machines="Unknown",
            ct_scanners="Unknown",
            mri_machines="Unknown",
            ecg_machines="Unknown",
            dialysis_machines="Unknown",
        )
    
    return ReadResource.model_validate(resource)


@router.get("/resources/username/{hospital_username}")
async def get_user(
    request: Request,
    hospital_username: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
):

    decoded_name = urllib.parse.unquote(hospital_username)
    resource = await resource_crud.get(db=db, hospital_username=decoded_name)
    
    if not resource:
        return ReadResource(
            id = "Unknown",
            icu_beds="Unknown",
            ventilators="Unknown",
            monitors="Unknown",
            defibrillators="Unknown",
            infusion_pumps="Unknown",
            oxygen_cylinders="Unknown",
            xray_machines="Unknown",
            ultrasound_machines="Unknown",
            ct_scanners="Unknown",
            mri_machines="Unknown",
            ecg_machines="Unknown",
            dialysis_machines="Unknown",
        )
    
    return ReadResource.model_validate(resource)


@router.get("/resources/{id}", response_model=ReadResource)
async def get_user(
    request: Request,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
)-> ReadResource:
    
    resource = await resource_crud.get(db=db,id=id)
    if not resource:
        raise HTTPException("Resource not found...!")
    
    return ReadResource.model_validate(resource)




@router.patch("/resources/{id}", response_model=ReadResource)
async def update_user(
    request: Request,
    id: int,
    resource_in: UpdateResource,
    db: Annotated[AsyncSession, Depends(async_get_db)]
)-> ReadResource:
    
    resource = await resource_crud.get(db=db, id=id)
    if not resource:
        raise HTTPException("Resource not exists...!")
    
    updated_user = await resource_crud.update(db=db, obj_in=resource_in, id=id)

    # Send GET request to http://auth-service:8001/users
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://auth-service:8000/users",
            timeout=20
        )

    # Parse JSON
    resp_json = response.json()
    users = resp_json["data"]

    # Iterate and publish notifications
    for user in users:
        publish_notification(
            user_ids=[user["id"]],
            title="A Resource Updated",
            message=f"Resource for {resource.hospital_name} has been Updated."
        )


    return ReadResource.model_validate(updated_user)

    
@router.delete("/resources/{id}")
async def delete_user(
    request: Request,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)]
)-> dict[str, Any]:
    
    resource = await resource_crud.get(db=db, id=id)

    if not resource:
        HTTPException("Resource not found...!")

    deleted_user = await resource_crud.delete(db=db, id=id)

    return {"message: ": "Resource deleted"}

    

