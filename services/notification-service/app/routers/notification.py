from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from typing import Dict, List

from sqlalchemy.orm import NotExtension
import aio_pika
import json
import asyncio
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import async_get_db
from ..models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

# Store connected clients: {user_id: [WebSocket, WebSocket, ...]}
connected_clients: Dict[int, List[WebSocket]] = {}

# ---------------------- DB Helpers ----------------------

async def save_notification(db: AsyncSession, user_id: int, title: str, message: str) -> Notification:
    """Create and save a notification asynchronously."""
    note = Notification(
        user_id=user_id,
        title=title,
        message=message,
        created_at=datetime.utcnow(),
        is_read=False
    )
    print("saved note", note)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note

async def broadcast_notification(user_id: int, note: Notification):
    """Send notification to all connected WebSocket clients for a user."""
    if user_id in connected_clients:
        for ws in connected_clients[user_id]:
            await ws.send_json(note.to_dict())

# ---------------------- REST Endpoints ----------------------

@router.get("/{user_id}")
async def get_notifications(user_id: int, db: AsyncSession = Depends(async_get_db)):
    """Fetch all notifications for a user asynchronously."""
    result = await db.execute(
        select(Notification)
        .filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc())
    )
    notifications = result.scalars().all()
    return [n.to_dict() for n in notifications]

@router.post("/{notification_id}/read")
async def mark_as_read(notification_id: int, db: AsyncSession = Depends(async_get_db)):
    """Mark a notification as read."""
    result = await db.execute(select(Notification).filter_by(id=notification_id))
    note = result.scalars().first()
    if note:
        note.is_read = True
        await db.commit()
    return {"status": "success"}

# ---------------------- WebSocket ----------------------

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """
    WebSocket endpoint for clients to receive real-time notifications.

    - Accepts connection.
    - Adds client WebSocket to connected clients list.
    - Keeps connection alive by awaiting messages.
    - Removes client on disconnect.
    """
    await websocket.accept()
    connected_clients.setdefault(user_id, []).append(websocket)
    try:
        while True:
            print("hi")
            await websocket.receive_text()  # Keep connection alive by waiting for incoming messages (even if unused)
            print("received")
    except WebSocketDisconnect:
        connected_clients[user_id].remove(websocket)
        if not connected_clients[user_id]:
            del connected_clients[user_id]

# ---------------------- RabbitMQ Async Consumer ----------------------

async def rabbitmq_consumer():
    print("Connecting to RabbitMQ...")
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    print("Connected!")

    channel = await connection.channel()
    print("Channel created")

    queue = await channel.declare_queue("notifications", durable=True)
    print("Queue declared")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    print("Message received:", message.body)
                    payload = json.loads(message.body)
                    async for db in async_get_db():
                        for uid in payload.get("user_ids", []):
                            note = await save_notification(db, uid, payload["title"], payload["message"])
                            print(f"Notification saved for user {uid}: {note}")
                            # await broadcast_notification(uid, note)  # optional
                except Exception as e:
                    print("Error processing message:", e)


# ---------------------- Startup Event ----------------------

from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Run RabbitMQ consumer as a background asyncio task on app startup
    asyncio.create_task(rabbitmq_consumer())
