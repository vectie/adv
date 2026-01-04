from fastapi import APIRouter, HTTPException
from app.services.future_prediction import FuturePredictionService

router = APIRouter()

future_service = FuturePredictionService()

@router.post("/predict")
async def predict_future(transcription: list, historical_data: dict = None):
    """基于转录内容预测未来趋势和潜在后果
    
    Args:
        transcription: 带有说话人标记的转录结果，格式为 [{"speaker": "主持人", "text": "xxx"}, ...]
        historical_data: 历史数据，用于增强预测准确性，可选
        
    Returns:
        dict: 未来预测结果，包含趋势预测、潜在后果、风险评估等
    """
    try:
        if not isinstance(transcription, list):
            raise HTTPException(status_code=400, detail="Transcription must be a list")
        
        # 调用未来预测服务
        result = future_service.predict_future(transcription, historical_data)
        
        return result
    except Exception as e:
        print(f"Future prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Future prediction failed: {str(e)}")