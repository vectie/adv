from fastapi import APIRouter, HTTPException
from app.services.cost_optimization import CostOptimizationService
from typing import Dict, Any

router = APIRouter()

@router.post("/optimize", response_model=Dict[str, Any])
async def optimize_computation_cost(resource_usage: Dict[str, Any] = None, goals: Dict[str, Any] = None):
    """优化计算成本，实现计算成本大于通信成本的高效学习"""
    try:
        result = CostOptimizationService.optimize_computation_cost(resource_usage, goals)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/monitor", response_model=Dict[str, Any])
async def monitor_resource_usage(metrics: Dict[str, Any] = None):
    """监控资源使用情况"""
    try:
        result = CostOptimizationService.monitor_resource_usage(metrics)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-report", response_model=Dict[str, Any])
async def generate_cost_report(historical_data: list = None, time_range: str = "monthly"):
    """生成成本报告"""
    try:
        result = CostOptimizationService.generate_cost_report(historical_data, time_range)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
