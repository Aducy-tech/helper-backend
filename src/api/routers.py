from src.api.endpoints.users import router as auth_router
from src.api.endpoints.ai import router as ai_router

routers = [
    auth_router,
    ai_router,
]
