from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.notification import router as notification_router, rabbitmq_consumer
import asyncio

app = FastAPI(
    title="Notifications Service",
    description="API for notifications service",
    version="1.0.0"
)

app.include_router(notification_router, tags=["notifications"])

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

@app.on_event("startup")
async def on_startup():
    # Run RabbitMQ consumer in background
    asyncio.create_task(rabbitmq_consumer())
    print("[APP] RabbitMQ consumer task started")