from app.core.config import settings
from .proxy import create_proxy_router

router = create_proxy_router("/ai", settings.AI_SERVICE_URL, tags=["ai"])