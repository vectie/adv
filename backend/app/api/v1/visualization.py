from fastapi import APIRouter, HTTPException
from app.services.visualization_service import VisualizationService

router = APIRouter()

visualization_service = VisualizationService()

@router.post("/generate")
async def generate_visualization(data: dict, viz_type: str, config: dict = None):
    """生成可视化数据
    
    Args:
        data: 要可视化的数据
        viz_type: 可视化类型，支持：
            - radar: 雷达图
            - bar: 柱状图
            - line: 折线图
            - pie: 饼图
            - heatmap: 热力图
            - network: 网络图
            - table: 表格
        config: 可视化配置参数
        
    Returns:
        dict: 可视化数据
    """
    try:
        if not isinstance(data, dict):
            raise HTTPException(status_code=400, detail="Data must be a dictionary")
        
        if not isinstance(viz_type, str):
            raise HTTPException(status_code=400, detail="Visualization type must be a string")
        
        # 调用可视化服务
        result = visualization_service.generate_visualization(data, viz_type, config)
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Visualization error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Visualization failed: {str(e)}")

@router.post("/dashboard")
async def generate_dashboard(dashboard_config: dict):
    """生成仪表盘数据
    
    Args:
        dashboard_config: 仪表盘配置，包含多个可视化组件
        
    Returns:
        dict: 仪表盘数据
    """
    try:
        if not isinstance(dashboard_config, dict):
            raise HTTPException(status_code=400, detail="Dashboard config must be a dictionary")
        
        # 调用仪表盘生成服务
        result = visualization_service.generate_dashboard(dashboard_config)
        
        return result
    except Exception as e:
        print(f"Dashboard generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dashboard generation failed: {str(e)}")
