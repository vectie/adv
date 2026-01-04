from fastapi import APIRouter, HTTPException
from app.services.fact_opinion_distinction import FactOpinionDistinctionService
from typing import List, Dict, Any

router = APIRouter()

@router.post("/distinguish", response_model=Dict[str, Any])
async def distinguish_fact_opinion(transcription: List[Dict[str, Any]]):
    """区分转录内容中的事实陈述和主观观点"""
    try:
        result = FactOpinionDistinctionService.distinguish_fact_opinion(transcription)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-evidence", response_model=Dict[str, Any])
async def extract_evidence(transcription: List[Dict[str, Any]]):
    """从转录内容中提取证据支持"""
    try:
        result = FactOpinionDistinctionService.extract_evidence(transcription)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-report", response_model=Dict[str, Any])
async def generate_fact_check_report(transcription: List[Dict[str, Any]]):
    """生成事实核查报告"""
    try:
        result = FactOpinionDistinctionService.generate_fact_check_report(transcription)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
