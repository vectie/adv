from fastapi import APIRouter, HTTPException
from app.services.actionable_advice import ActionableAdviceService

router = APIRouter()

actionable_advice_service = ActionableAdviceService()

@router.post("/generate")
async def generate_actionable_advice(transcription: list, analysis_results: dict = None, user_goals: list = None):
    """生成可行动的建议
    
    Args:
        transcription: 带有说话人标记的转录结果，格式为 [{"speaker": "主持人", "text": "xxx"}, ...]
        analysis_results: 其他分析模块的结果，可选，包含优势分析、增量分析等
        user_goals: 用户目标列表，可选
        
    Returns:
        dict: 可行动的建议，包含时间线和优先级
    """
    try:
        if not isinstance(transcription, list):
            raise HTTPException(status_code=400, detail="Transcription must be a list")
        
        # 调用可行动建议服务
        result = actionable_advice_service.generate_advice(transcription, analysis_results, user_goals)
        
        return result
    except Exception as e:
        print(f"Actionable advice generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Actionable advice generation failed: {str(e)}")
