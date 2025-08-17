from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from ..core.utils_funcs.email import send_verification_email, send_query_email

router = APIRouter(tags=["email"])

class EmailRequest(BaseModel):
    to_email: EmailStr
    code: str

class EmailRequestMsg(BaseModel):
    to_email: EmailStr
    msg: str

@router.post("/send-verification-code")
async def send_verification_code(email_request: EmailRequest):
    try:
        await send_verification_email(email_request.to_email, email_request.code)
        return {"message": "Verification code sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-query")
async def send_query_code(email_request: EmailRequestMsg):
    try:
        await send_query_email(email_request.to_email, email_request.msg)
        return {"message": "Message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
