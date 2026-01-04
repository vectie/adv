from fastapi import APIRouter, HTTPException
from app.services.market_trend import MarketTrendService
from typing import List, Dict, Any

router = APIRouter()

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_market_trends(transcription: List[Dict[str, Any]], historical_data: Dict[str, Any] = None):
    """分析市场趋势"""
    try:
        result = MarketTrendService.analyze_market_trends(transcription, historical_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/opportunity-windows", response_model=Dict[str, Any])
async def identify_opportunity_windows(trends: Dict[str, Any], user_context: Dict[str, Any] = None):
    """识别机会窗口"""
    try:
        result = MarketTrendService.identify_opportunity_windows(trends, user_context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trend-strength", response_model=Dict[str, Any])
async def analyze_trend_strength(trends: Dict[str, Any]):
    """分析趋势强度"""
    try:
        result = MarketTrendService.analyze_trend_strength(trends)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
