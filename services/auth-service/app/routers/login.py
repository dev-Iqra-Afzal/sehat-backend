from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Any
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from enum import Enum
from datetime import datetime

from ..core.db.database import async_get_db
from ..core.security import authenticate_user
from ..core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, create_refresh_token, verify_token
from ..core.config import settings
from ..schemas.user import BaseUser
from ..core.rabbitmq import publish_notification


router = APIRouter(tags=["authentication"])

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"



@router.post("/login")
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(async_get_db)]
)-> dict[str, Any]:
    
    user = await authenticate_user(username_or_email=form_data.username, password=form_data.password, db=db)
    user_model = BaseUser.model_validate(user)

    if not user:
        raise HTTPException("Wrong username, email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)

    refresh_token = await create_refresh_token(data={"sub":user.username})
    max_age = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60

    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="lax", max_age=max_age
    )
    
    print("login user id: ", user.id)
    # Notify user of login
    publish_notification(
        user_ids=[user.id],
        title="Login Alert",
        message=f"Your account was accessed on {datetime.utcnow().isoformat()} UTC."
    )

    print("Message published to RabbitMQ: ")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_model
    }

#------------------------------------------------------------
# ------> Refresh route
#------------------------------------------------------------
@router.post("/refresh")
async def refresh_access_token(request: Request, db: AsyncSession = Depends(async_get_db)) -> dict[str, str]:

    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException("Refresh token missing.")

        user_data = await verify_token(refresh_token, TokenType.REFRESH, db)
        if not user_data:
            raise HTTPException("Invalid refresh token.")

        new_access_token = await create_access_token(data={"sub": user_data.username_or_email})
        return {"access_token": new_access_token, "token_type": "bearer"}

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")