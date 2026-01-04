from fastapi import APIRouter
from app.api.v1 import router as v1_router
from app.core.config import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

# 包含v1版本的路由
api_router.include_router(v1_router)