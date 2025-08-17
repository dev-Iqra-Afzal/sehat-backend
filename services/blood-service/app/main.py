from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.blood import router as blood_router

app = FastAPI(
    title="Blood Service",
    description="API for Blood service",
    version="1.0.0"
)

app.include_router(blood_router, tags=["blood"])

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
