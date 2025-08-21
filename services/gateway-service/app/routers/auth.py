from app.core.config import settings
from .proxy import create_proxy_router

router = create_proxy_router("/auth", settings.AUTH_SERVICE_URL, tags=["auth"])