from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.login import router as login_router
from .routers.user import router as user_router
from .routers.logout import router as logout_router
from .routers.email import router as verification_router

app = FastAPI(
    title="Auth Service",
    description="API for authentication and user management",
    version="1.0.0"
)

app.include_router(login_router, tags=["login"])
app.include_router(user_router, tags=["users"])
app.include_router(logout_router, tags=["logout"])
app.include_router(verification_router, tags=["verification"])

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
