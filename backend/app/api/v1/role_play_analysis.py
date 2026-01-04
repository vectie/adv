from fastapi import APIRouter, HTTPException
from app.services.role_play_analysis import RolePlayAnalysisService

router = APIRouter()

role_play_service = RolePlayAnalysisService()

@router.post("/analyze-niche")
async def analyze_ecological_niche(transcription: list, user_background: dict = None):
    """分析生态位，理解参与者角色和关系，评估自身定位
    
    Args:
        transcription: 带有说话人标记的转录结果，格式为 [{"speaker": "主持人", "text": "xxx"}, ...]
        user_background: 用户背景信息，可选，包含描述、技能、专业水平等
        
    Returns:
        dict: 生态位分析报告，包含角色关系图、参与者定位、用户定位建议等
    """
    try:
        if not isinstance(transcription, list):
            raise HTTPException(status_code=400, detail="Transcription must be a list")
        
        # 调用角色扮演分析服务
        result = role_play_service.analyze_ecological_niche(transcription, user_background)
        
        return result
    except Exception as e:
        print(f"Role play analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Role play analysis failed: {str(e)}")