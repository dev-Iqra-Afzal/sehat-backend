from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.ngo import router as ngo_router

app = FastAPI(
    title="NGO Service",
    description="API for NGO service",
    version="1.0.0"
)

app.include_router(ngo_router, tags=["ngo"])

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
