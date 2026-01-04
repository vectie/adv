from fastapi import APIRouter, HTTPException
from app.services.thinking_process import ThinkingProcessService

router = APIRouter()

thinking_process_service = ThinkingProcessService()

@router.post("/analyze")
async def analyze_thinking_process(transcription: list, successful_speakers: list = None):
    """分析思考过程
    
    Args:
        transcription: 带有说话人标记的转录结果，格式为 [{"speaker": "主持人", "text": "xxx"}, ...]
        successful_speakers: 成功人士列表，可选，用于区分成功人士和普通人士的思考过程
        
    Returns:
        dict: 思考过程分析结果，包含思维链、因果关系、思维模型图谱、可模仿的思考框架和可视化数据
    """
    try:
        if not isinstance(transcription, list):
            raise HTTPException(status_code=400, detail="Transcription must be a list")
        
        if successful_speakers and not isinstance(successful_speakers, list):
            raise HTTPException(status_code=400, detail="Successful speakers must be a list")
        
        # 调用思考过程分析服务
        result = thinking_process_service.analyze_thinking_process(transcription, successful_speakers)
        
        return result
    except Exception as e:
        print(f"Thinking process analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Thinking process analysis failed: {str(e)}")
