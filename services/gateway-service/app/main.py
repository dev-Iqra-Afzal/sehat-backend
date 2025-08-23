from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.routers import auth, hospital, blood, ngo, resource, notification, ai

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip('"') for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(hospital.router, prefix=settings.API_V1_STR)
app.include_router(blood.router, prefix=settings.API_V1_STR)
app.include_router(ngo.router, prefix=settings.API_V1_STR)
app.include_router(resource.router, prefix=settings.API_V1_STR)
app.include_router(notification.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to Sehat-Iqra API Gateway"}

@app.get(f"/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "gateway"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
