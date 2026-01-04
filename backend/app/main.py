from fastapi import FastAPI
from app.api import api_router
from app.core.config import settings
from app.services.model_service import model_service

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Local speech recognition API using FunASR",
    version=settings.VERSION
)

# 包含API路由
app.include_router(api_router)

# 健康检查端点（根路径）
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

# 启动事件：加载模型
@app.on_event("startup")
async def load_model():
    model_service.load_model()

# 关闭事件：卸载模型
@app.on_event("shutdown")
async def unload_model():
    model_service.unload_model()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1
    )