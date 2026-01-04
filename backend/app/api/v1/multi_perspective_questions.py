from fastapi import APIRouter, HTTPException
from app.services.multi_perspective_questions import MultiPerspectiveQuestionsService

router = APIRouter()

multi_perspective_questions_service = MultiPerspectiveQuestionsService()

@router.post("/generate")
async def generate_multi_perspective_questions(transcription: list, analysis_results: dict = None, topic: str = None):
    """从多个视角生成关键问题
    
    Args:
        transcription: 带有说话人标记的转录结果，格式为 [{"speaker": "主持人", "text": "xxx"}, ...]
        analysis_results: 其他分析模块的结果，可选，包含优势分析、增量分析等
        topic: 特定主题，可选
        
    Returns:
        dict: 从5个不同视角生成的关键问题，包括客户视角、竞争对手视角、投资者视角、行业专家视角和未来用户视角
    """
    try:
        if not isinstance(transcription, list):
            raise HTTPException(status_code=400, detail="Transcription must be a list")
        
        # 调用多角度提问服务
        result = multi_perspective_questions_service.generate_questions(transcription, analysis_results, topic)
        
        return result
    except Exception as e:
        print(f"Multi-perspective questions generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Multi-perspective questions generation failed: {str(e)}")
