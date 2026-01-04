from fastapi import APIRouter, HTTPException
from app.services.failure_case_analysis import FailureCaseAnalysisService
from typing import List, Dict, Any

router = APIRouter()

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_failure_cases(transcription: List[Dict[str, Any]], failure_database: Dict[str, Any] = None):
    """分析Podcast内容中的失败案例，提供风险规避策略"""
    try:
        result = FailureCaseAnalysisService.analyze_failure_cases(transcription, failure_database)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare-with-success", response_model=Dict[str, Any])
async def compare_with_success_patterns(transcription: List[Dict[str, Any]], success_patterns: Dict[str, Any] = None):
    """对比成功模式和失败模式，提供改进建议"""
    try:
        result = FailureCaseAnalysisService.compare_with_success_patterns(transcription, success_patterns)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/case-studies", response_model=List[Dict[str, Any]])
async def generate_failure_case_studies(category: str = None, limit: int = 5):
    """生成失败案例研究报告"""
    try:
        result = FailureCaseAnalysisService.generate_failure_case_studies(category, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
