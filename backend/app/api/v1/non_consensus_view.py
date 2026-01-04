from fastapi import APIRouter, HTTPException
from app.services.non_consensus_view import NonConsensusViewService
from typing import List, Dict, Any

router = APIRouter()

@router.post("/identify", response_model=Dict[str, Any])
async def identify_non_consensus_views(transcription: List[Dict[str, Any]], industry_benchmark: Dict[str, Any] = None):
    """识别转录内容中的非共识观点，并评估其影响力"""
    try:
        result = NonConsensusViewService.identify_non_consensus_views(transcription, industry_benchmark)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clusters", response_model=Dict[str, Any])
async def analyze_view_clusters(transcription: List[Dict[str, Any]]):
    """对转录内容中的观点进行聚类分析"""
    try:
        result = NonConsensusViewService.analyze_view_clusters(transcription)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
