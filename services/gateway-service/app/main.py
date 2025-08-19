from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .routers import auth, hospital, resource, blood, ngo, notification, ai

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API Gateway for Sehat-Iqra services",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Add CORS middleware to the FastAPI application
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all service routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(hospital.router, prefix=f"{settings.API_V1_STR}/hospital", tags=["hospital"])
app.include_router(resource.router, prefix=f"{settings.API_V1_STR}/resource", tags=["resource"])
app.include_router(blood.router, prefix=f"{settings.API_V1_STR}/blood", tags=["blood"])
app.include_router(ngo.router, prefix=f"{settings.API_V1_STR}/ngo", tags=["ngo"])
app.include_router(notification.router, prefix=f"{settings.API_V1_STR}/notification", tags=["notification"])
app.include_router(ai.router, prefix=f"{settings.API_V1_STR}/ai", tags=["ai"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Sehat-Iqra API Gateway",
        "services": [
            "Auth Service",
            "Hospital Service",
            "Resource Service",
            "Blood Service",
            "NGO Service",
            "Notification Service",
            "AI Service"
        ]
    }
