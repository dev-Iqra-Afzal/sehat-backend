from typing import Optional
from fastapi import APIRouter, Cookie, Depends, Response, HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db.database import async_get_db
from ..core.security import blacklist_tokens, oauth2_scheme

router = APIRouter(tags=["login"])

#------------------------------------------------------------
# ------> Logout route
#------------------------------------------------------------
# @router.post("/logout")
# async def logout(
#     response: Response,
#     access_token: str = Depends(oauth2_scheme),
#     refresh_token: Optional[str] = Cookie(None, alias="refresh_token"),
# ) -> dict[str, str]:

#     try:
#         if not refresh_token:
#             raise HTTPException("Refresh token not found")

#         await blacklist_tokens(access_token=access_token, refresh_token=refresh_token)
#         response.delete_cookie(key="refresh_token")

#         return {"message": "Logged out successfully"}

#     except JWTError:
#         raise HTTPException("Invalid token.")

@router.post("/logout")
async def logout(
    response: Response,
    access_token: str = Depends(oauth2_scheme),
    refresh_token: Optional[str] = Cookie(None, alias="refresh_token"),
) -> dict[str, str]:

    try:
        # If we have both tokens, blacklist them
        if refresh_token:
            await blacklist_tokens(access_token=access_token, refresh_token=refresh_token)
            response.delete_cookie(key="refresh_token")
        else:
            # Still delete cookie in case it's there under a different state
            response.delete_cookie(key="refresh_token")

        # Always return a success message
        return {"message": "Logged out successfully"}

    except JWTError:
        # Invalid token — still return success to avoid exposing details
        return {"message": "Logged out successfully"}
