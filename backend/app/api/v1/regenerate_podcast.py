from fastapi import APIRouter, HTTPException
from app.services.regenerate_podcast import RegeneratePodcastService
from typing import List, Dict, Any

router = APIRouter()

@router.post("/regenerate", response_model=Dict[str, Any])
async def regenerate_podcast(transcription: List[Dict[str, Any]], improvements: Dict[str, Any] = None):
    """基于原Podcast内容生成改进版本"""
    try:
        result = RegeneratePodcastService.regenerate_podcast(transcription, improvements)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/content-calendar", response_model=Dict[str, Any])
async def generate_content_calendar(transcription: List[Dict[str, Any]], frequency: str = "weekly"):
    """基于原内容生成内容日历"""
    try:
        result = RegeneratePodcastService.generate_content_calendar(transcription, frequency)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-performance", response_model=Dict[str, Any])
async def analyze_content_performance(transcription: List[Dict[str, Any]], performance_data: Dict[str, Any] = None):
    """分析Podcast内容表现"""
    try:
        result = RegeneratePodcastService.analyze_content_performance(transcription, performance_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
