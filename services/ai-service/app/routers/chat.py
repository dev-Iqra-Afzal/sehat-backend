from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest
from app.routers.openrouter import ask_groq
import logging

router = APIRouter(tags=["Chat"])

@router.post("/chat")
def chat(request: ChatRequest):
    try:
        # Ensure prompt is not empty or whitespace
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

        response = ask_groq(request.prompt)

        # If ask_groq returns None or empty string
        if not response:
            raise HTTPException(status_code=500, detail="No response received from Groq.")

        return {"response": response}

    except HTTPException as http_err:
        # Let FastAPI handle the HTTPException
        raise http_err

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error.")
