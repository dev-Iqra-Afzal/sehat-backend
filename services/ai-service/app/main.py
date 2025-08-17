from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.chat import router as chat_router

app = FastAPI(
    title="AI Service",
    description="API for AI service",
    version="1.0.0"
)

app.include_router(chat_router, tags=["chat"])

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
