from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.resource import router as resource_router

app = FastAPI(
    title="Resource Service",
    description="API for resource management",
    version="1.0.0"
)

app.include_router(resource_router, tags=["resources"])

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


