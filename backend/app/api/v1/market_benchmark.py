from fastapi import APIRouter, HTTPException
from app.services.market_benchmark import MarketBenchmarkService

router = APIRouter()

market_benchmark_service = MarketBenchmarkService()

@router.post("/benchmark")
async def benchmark_against_market(transcription: list, product_info: dict = None, financial_data: dict = None):
    """基于市场数据进行基准测试
    
    Args:
        transcription: 带有说话人标记的转录结果，格式为 [{"speaker": "主持人", "text": "xxx"}, ...]
        product_info: 产品/服务信息，可选，包含名称、描述等
        financial_data: 金融市场数据，可选，包含行业、股票、市场趋势等信息
        
    Returns:
        dict: 市场基准测试结果，包含市场对比报告、竞争力排名和可视化数据
    """
    try:
        if not isinstance(transcription, list):
            raise HTTPException(status_code=400, detail="Transcription must be a list")
        
        if product_info and not isinstance(product_info, dict):
            raise HTTPException(status_code=400, detail="Product info must be a dictionary")
        
        if financial_data and not isinstance(financial_data, dict):
            raise HTTPException(status_code=400, detail="Financial data must be a dictionary")
        
        # 调用市场基准测试服务
        result = market_benchmark_service.benchmark_against_market(transcription, product_info, financial_data)
        
        return result
    except Exception as e:
        print(f"Market benchmark error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Market benchmark failed: {str(e)}")
