from fastapi import APIRouter, HTTPException
from app.services.advantage_increment_analysis import AdvantageIncrementAnalysisService

router = APIRouter()

advantage_increment_service = AdvantageIncrementAnalysisService()

@router.post("/analyze")
async def analyze_advantages_and_increments(transcription: list, historical_data: dict = None):
    """分析优势与增量，识别核心竞争力和个人成长关键点
    
    Args:
        transcription: 带有说话人标记的转录结果，格式为 [{"speaker": "主持人", "text": "xxx"}, ...]
        historical_data: 个人/产品历史数据，可选，包含经验、技能等信息
        
    Returns:
        dict: 优势与增量分析报告，包含关键概念、优势分析、增量机会、优势矩阵和可视化数据
    """
    try:
        if not isinstance(transcription, list):
            raise HTTPException(status_code=400, detail="Transcription must be a list")
        
        # 调用优势与增量分析服务
        result = advantage_increment_service.analyze_advantages_and_increments(transcription, historical_data)
        
        return result
    except Exception as e:
        print(f"Advantage increment analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Advantage increment analysis failed: {str(e)}")
