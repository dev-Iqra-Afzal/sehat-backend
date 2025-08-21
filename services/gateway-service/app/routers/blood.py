from app.core.config import settings
from .proxy import create_proxy_router

router = create_proxy_router("/blood", settings.BLOOD_SERVICE_URL, tags=["blood"])