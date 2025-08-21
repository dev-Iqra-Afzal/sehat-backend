from app.core.config import settings
from .proxy import create_proxy_router

router = create_proxy_router("/notification", settings.NOTIFICATION_SERVICE_URL, tags=["notification"])