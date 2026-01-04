from fastapi import APIRouter, HTTPException
from app.services.academic_paper_expansion import AcademicPaperExpansionService
from typing import List, Dict, Any

router = APIRouter()

@router.post("/expand", response_model=Dict[str, Any])
async def expand_to_academic_paper(transcription: List[Dict[str, Any]], analysis_results: Dict[str, Any] = None):
    """将转录内容扩展为学术风格的分析报告"""
    try:
        result = AcademicPaperExpansionService.expand_to_academic_paper(transcription, analysis_results)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/research-proposals", response_model=List[Dict[str, Any]])
async def generate_research_proposals(transcription: List[Dict[str, Any]]):
    """基于转录内容生成研究提案"""
    try:
        result = AcademicPaperExpansionService.generate_research_proposals(transcription)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend-literature", response_model=List[Dict[str, Any]])
async def recommend_related_literature(key_concepts: List[str], field: str = None):
    """推荐相关文献"""
    try:
        result = AcademicPaperExpansionService.recommend_related_literature(key_concepts, field)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
