from fastapi import APIRouter, HTTPException
from app.services.feedback import FeedbackService

router = APIRouter()

feedback_service = FeedbackService()

@router.post("/update-progress")
async def update_progress(user_id: str, progress_data: dict):
    """更新用户进度
    
    Args:
        user_id: 用户ID
        progress_data: 进度数据，包含 transcription_count, analysis_count, duration 等
        
    Returns:
        dict: 更新后的进度信息和新解锁的成就
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        # 调用反馈服务更新进度
        result = feedback_service.update_progress(user_id, progress_data)
        
        return result
    except Exception as e:
        print(f"Feedback update error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Feedback update failed: {str(e)}")

@router.get("/get-feedback")
async def get_feedback(user_id: str, activity_type: str):
    """获取用户反馈
    
    Args:
        user_id: 用户ID
        activity_type: 活动类型，如 transcription, analysis 等
        
    Returns:
        dict: 反馈信息，包含激励、成就和进度可视化数据
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        if not activity_type:
            raise HTTPException(status_code=400, detail="Activity type is required")
        
        # 调用反馈服务获取反馈
        result = feedback_service.get_user_feedback(user_id, activity_type)
        
        return result
    except Exception as e:
        print(f"Get feedback error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Get feedback failed: {str(e)}")

@router.get("/get-stats")
async def get_stats(user_id: str):
    """获取用户统计信息
    
    Args:
        user_id: 用户ID
        
    Returns:
        dict: 用户统计信息
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        # 调用反馈服务获取统计信息
        result = feedback_service.get_user_stats(user_id)
        
        return result
    except Exception as e:
        print(f"Get stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Get stats failed: {str(e)}")