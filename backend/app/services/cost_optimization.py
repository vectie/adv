from typing import List, Dict, Any
from app.services.visualization_service import VisualizationService

class CostOptimizationService:
    """计算成本优化服务类"""
    
    @staticmethod
    def optimize_computation_cost(resource_usage: dict = None, goals: dict = None) -> dict:
        """
        优化计算成本，实现计算成本大于通信成本的高效学习
        
        Args:
            resource_usage: 资源使用数据，包含CPU、内存、存储等使用情况
            goals: 优化目标，如成本降低百分比、性能提升要求等
            
        Returns:
            成本优化建议和资源分配方案
        """
        # 收集资源使用数据
        if not resource_usage:
            resource_usage = CostOptimizationService._generate_mock_resource_usage()
        
        # 分析当前资源使用情况
        usage_analysis = CostOptimizationService._analyze_resource_usage(resource_usage)
        
        # 确定优化目标
        if not goals:
            goals = {
                "cost_reduction": 0.2,  # 降低20%成本
                "performance_improvement": 0.1,  # 提升10%性能
                "target_compute_communication_ratio": 1.5  # 计算成本/通信成本 > 1.5
            }
        
        # 生成优化建议
        optimization_suggestions = CostOptimizationService._generate_optimization_suggestions(usage_analysis, goals)
        
        # 生成资源智能分配方案
        resource_allocation = CostOptimizationService._generate_resource_allocation(usage_analysis, optimization_suggestions)
        
        # 计算成本效益分析
        cost_benefit = CostOptimizationService._calculate_cost_benefit(usage_analysis, optimization_suggestions)
        
        # 生成可视化
        visualization_data = CostOptimizationService._generate_visualizations(usage_analysis, optimization_suggestions, cost_benefit)
        
        return {
            "resource_usage": resource_usage,
            "usage_analysis": usage_analysis,
            "optimization_goals": goals,
            "optimization_suggestions": optimization_suggestions,
            "resource_allocation": resource_allocation,
            "cost_benefit_analysis": cost_benefit,
            "visualizations": visualization_data
        }
    
    @staticmethod
    def _generate_mock_resource_usage() -> dict:
        """生成模拟资源使用数据"""
        return {
            "cpu_usage": {
                "average": 75.5,
                "peak": 92.3,
                "low": 45.8,
                "unit": "%"
            },
            "memory_usage": {
                "average": 82.1,
                "peak": 95.7,
                "low": 55.3,
                "unit": "%"
            },
            "storage_usage": {
                "total": 1000,  # GB
                "used": 785,
                "free": 215,
                "unit": "GB"
            },
            "network_usage": {
                "incoming": 1250,  # MB/s
                "outgoing": 980,
                "unit": "MB/s"
            },
            "compute_cost": {
                "current": 1500,  # 元/月
                "communication_cost": 800,  # 元/月
                "ratio": 1.875
            },
            "model_inference": {
                "average_latency": 2.3,  # 秒
                "throughput": 45,  # 请求/秒
                "model_sizes": {
                    "funasr": 1.2,  # GB
                    "speaker_diarization": 0.8,
                    "nlp_models": 2.5
                }
            },
            "workload_distribution": {
                "transcription": 45,
                "speaker_diarization": 25,
                "nlp_analysis": 20,
                "visualization": 10,
                "unit": "%"
            }
        }
    
    @staticmethod
    def _analyze_resource_usage(resource_usage: dict) -> dict:
        """分析资源使用情况"""
        # 计算资源使用效率
        cpu_efficiency = resource_usage["cpu_usage"]["average"] / 100
        memory_efficiency = resource_usage["memory_usage"]["average"] / 100
        storage_efficiency = resource_usage["storage_usage"]["used"] / resource_usage["storage_usage"]["total"]
        
        # 识别瓶颈
        bottlenecks = []
        if resource_usage["cpu_usage"]["peak"] > 90:
            bottlenecks.append("CPU峰值使用率过高")
        if resource_usage["memory_usage"]["peak"] > 90:
            bottlenecks.append("内存峰值使用率过高")
        if storage_efficiency > 0.8:
            bottlenecks.append("存储使用率过高")
        if resource_usage["model_inference"]["average_latency"] > 3:
            bottlenecks.append("模型推理延迟过高")
        
        # 分析工作负载分布
        workload_analysis = {
            "highest_workload": max(resource_usage["workload_distribution"].items(), key=lambda x: x[1] if x[0] != "unit" else 0)[0],
            "lowest_workload": min(resource_usage["workload_distribution"].items(), key=lambda x: x[1] if x[0] != "unit" else 100)[0],
            "balanced": all(20 <= v <= 30 for k, v in resource_usage["workload_distribution"].items() if k != "unit")
        }
        
        # 计算成本效益比
        cost_benefit_ratio = resource_usage["compute_cost"]["current"] / (resource_usage["model_inference"]["throughput"] * 3600 * 24 * 30)
        
        return {
            "resource_efficiency": {
                "cpu": cpu_efficiency,
                "memory": memory_efficiency,
                "storage": storage_efficiency
            },
            "bottlenecks": bottlenecks,
            "workload_analysis": workload_analysis,
            "cost_benefit_ratio": cost_benefit_ratio,
            "compute_communication_ratio": resource_usage["compute_cost"]["ratio"]
        }
    
    @staticmethod
    def _generate_optimization_suggestions(usage_analysis: dict, goals: dict) -> dict:
        """生成成本优化建议"""
        suggestions = {
            "model_optimization": [],
            "resource_allocation": [],
            "workload_optimization": [],
            "infrastructure_improvements": []
        }
        
        # 模型优化建议
        if usage_analysis["compute_communication_ratio"] < goals["target_compute_communication_ratio"]:
            suggestions["model_optimization"].append("优化模型结构，提高计算密集度")
        suggestions["model_optimization"].append("考虑模型蒸馏，减少模型大小")
        suggestions["model_optimization"].append("实现模型自动选择，根据任务复杂度动态调整")
        
        # 资源分配建议
        if "CPU峰值使用率过高" in usage_analysis["bottlenecks"]:
            suggestions["resource_allocation"].append("优化CPU调度策略，避免资源争用")
        if "内存峰值使用率过高" in usage_analysis["bottlenecks"]:
            suggestions["resource_allocation"].append("实现内存动态分配，减少空闲资源占用")
        if usage_analysis["resource_efficiency"]["storage"] > 0.8:
            suggestions["resource_allocation"].append("清理过期数据，优化存储结构")
        
        # 工作负载优化建议
        if not usage_analysis["workload_analysis"]["balanced"]:
            suggestions["workload_optimization"].append("重新分配工作负载，平衡各模块资源使用")
        suggestions["workload_optimization"].append("实现异步处理，提高系统吞吐量")
        suggestions["workload_optimization"].append("添加缓存机制，减少重复计算")
        
        # 基础设施改进建议
        suggestions["infrastructure_improvements"].append("考虑边缘计算，减少网络通信成本")
        suggestions["infrastructure_improvements"].append("实现资源弹性伸缩，根据负载动态调整")
        suggestions["infrastructure_improvements"].append("优化网络架构，降低通信延迟")
        
        return suggestions
    
    @staticmethod
    def _generate_resource_allocation(usage_analysis: dict, suggestions: dict) -> dict:
        """生成资源智能分配方案"""
        # 基于当前资源使用情况和优化建议，生成新的资源分配方案
        return {
            "cpu_allocation": {
                "transcription": 35,  # 减少转录模块CPU分配
                "speaker_diarization": 20,  # 减少发言人识别CPU分配
                "nlp_analysis": 30,  # 增加NLP分析CPU分配
                "visualization": 15,  # 增加可视化CPU分配
                "strategy": "动态调整，根据实时负载优化"
            },
            "memory_allocation": {
                "model_caching": 40,  # 40%内存用于模型缓存
                "data_processing": 35,  # 35%用于数据处理
                "visualization": 15,  # 15%用于可视化
                "system_overhead": 10,  # 10%系统开销
                "strategy": "分层内存管理，优先级调度"
            },
            "storage_allocation": {
                "model_files": 25,  # 25%存储模型文件
                "transcription_data": 45,  # 45%存储转录数据
                "analysis_results": 20,  # 20%存储分析结果
                "logs": 10,  # 10%存储日志
                "strategy": "冷热数据分离，定期清理过期数据"
            },
            "inference_optimization": {
                "batch_processing": True,
                "quantization": "int8",  # 使用INT8量化减少模型大小
                "model_pruning": 0.3,  # 修剪30%的模型参数
                "dynamic_batching": True  # 动态批处理
            },
            "expected_improvements": {
                "cost_reduction": 0.25,  # 预期降低25%成本
                "performance_improvement": 0.15,  # 预期提升15%性能
                "compute_communication_ratio": 2.2  # 预期计算通信比达到2.2
            }
        }
    
    @staticmethod
    def _calculate_cost_benefit(usage_analysis: dict, optimization_suggestions: dict) -> dict:
        """计算成本效益分析"""
        # 模拟成本效益计算
        return {
            "current_state": {
                "monthly_cost": 1500,  # 元/月
                "performance_score": 75,  # 性能评分
                "compute_communication_ratio": 1.875
            },
            "optimized_state": {
                "monthly_cost": 1125,  # 降低25%
                "performance_score": 86,  # 提升15%
                "compute_communication_ratio": 2.2
            },
            "benefits": {
                "annual_cost_savings": (1500 - 1125) * 12,  # 元/年
                "performance_improvement": 11,
                "ratio_improvement": 0.325
            },
            "implementation_effort": {
                "model_optimization": 3,  # 1-5分，5分为最高
                "resource_allocation": 2,
                "workload_optimization": 2,
                "infrastructure_improvements": 4
            },
            "return_on_investment": {
                "break_even_point": 3,  # 个月
                "annual_roi": 0.8  # 80%
            }
        }
    
    @staticmethod
    def _generate_visualizations(usage_analysis: dict, optimization_suggestions: dict, cost_benefit: dict) -> dict:
        """生成成本优化的可视化内容"""
        # 生成资源使用饼图
        resource_usage_data = {
            "labels": ["CPU", "内存", "存储", "网络"],
            "values": [
                usage_analysis["resource_efficiency"]["cpu"] * 100,
                usage_analysis["resource_efficiency"]["memory"] * 100,
                usage_analysis["resource_efficiency"]["storage"] * 100,
                65  # 模拟网络使用率
            ]
        }
        resource_pie = VisualizationService.generate_pie_chart(resource_usage_data)
        
        # 生成成本效益对比柱状图
        cost_benefit_data = {
            "labels": ["月成本", "性能评分", "计算通信比"],
            "series": [
                {
                    "name": "当前状态",
                    "data": [
                        cost_benefit["current_state"]["monthly_cost"],
                        cost_benefit["current_state"]["performance_score"],
                        cost_benefit["current_state"]["compute_communication_ratio"]
                    ]
                },
                {
                    "name": "优化后",
                    "data": [
                        cost_benefit["optimized_state"]["monthly_cost"],
                        cost_benefit["optimized_state"]["performance_score"],
                        cost_benefit["optimized_state"]["compute_communication_ratio"]
                    ]
                }
            ]
        }
        cost_benefit_bar = VisualizationService.generate_bar_chart(cost_benefit_data)
        
        # 生成优化建议优先级雷达图
        suggestion_counts = {
            "model_optimization": len(optimization_suggestions["model_optimization"]),
            "resource_allocation": len(optimization_suggestions["resource_allocation"]),
            "workload_optimization": len(optimization_suggestions["workload_optimization"]),
            "infrastructure_improvements": len(optimization_suggestions["infrastructure_improvements"])
        }
        
        priority_data = {
            "categories": list(suggestion_counts.keys()),
            "series": [{
                "name": "建议数量",
                "data": list(suggestion_counts.values())
            }]
        }
        priority_radar = VisualizationService.generate_radar_chart(priority_data)
        
        # 生成投资回报率折线图
        roi_data = {
            "labels": ["第1月", "第2月", "第3月", "第4月", "第5月", "第6月"],
            "series": [{
                "name": "累计收益",
                "data": [0, 0, 0, 125, 250, 375]
            }, {
                "name": "累计成本",
                "data": [500, 500, 500, 500, 500, 500]
            }]
        }
        roi_line = VisualizationService.generate_line_chart(roi_data)
        
        return {
            "resource_usage_distribution": resource_pie,
            "cost_benefit_comparison": cost_benefit_bar,
            "suggestion_priority": priority_radar,
            "roi_analysis": roi_line
        }
    
    @staticmethod
    def monitor_resource_usage(metrics: dict = None) -> dict:
        """
        监控资源使用情况
        
        Args:
            metrics: 实时监控指标
            
        Returns:
            资源使用监控报告
        """
        if not metrics:
            # 生成模拟监控数据
            metrics = {
                "timestamp": "2024-01-15T14:30:00",
                "cpu": {
                    "usage": 78.2,
                    "temperature": 65,
                    "cores": [72, 85, 70, 81]
                },
                "memory": {
                    "usage": 81.5,
                    "available": 19.5,
                    "swap": 12.3
                },
                "disk": {
                    "usage": 78.5,
                    "read_speed": 125,
                    "write_speed": 95
                },
                "network": {
                    "download": 1120,
                    "upload": 890,
                    "latency": 15
                },
                "model_inference": {
                    "current_latency": 2.1,
                    "throughput": 48,
                    "active_models": 3
                }
            }
        
        # 分析监控数据
        alerts = []
        if metrics["cpu"]["usage"] > 90:
            alerts.append("CPU使用率过高")
        if metrics["memory"]["usage"] > 90:
            alerts.append("内存使用率过高")
        if metrics["disk"]["usage"] > 90:
            alerts.append("磁盘使用率过高")
        if metrics["model_inference"]["current_latency"] > 3:
            alerts.append("模型推理延迟过高")
        
        # 生成健康评分
        health_score = 100
        if alerts:
            health_score -= len(alerts) * 10
        health_score -= (metrics["cpu"]["usage"] - 70) if metrics["cpu"]["usage"] > 70 else 0
        health_score -= (metrics["memory"]["usage"] - 70) if metrics["memory"]["usage"] > 70 else 0
        health_score = max(0, min(100, health_score))
        
        return {
            "metrics": metrics,
            "alerts": alerts,
            "health_score": health_score,
            "status": "正常" if health_score > 70 else "警告" if health_score > 50 else "异常"
        }
    
    @staticmethod
    def generate_cost_report(historical_data: list = None, time_range: str = "monthly") -> dict:
        """
        生成成本报告
        
        Args:
            historical_data: 历史成本数据
            time_range: 时间范围，可选值：daily, weekly, monthly
            
        Returns:
            成本报告和趋势分析
        """
        if not historical_data:
            # 生成模拟历史数据
            historical_data = [
                {"date": "2024-01-01", "compute_cost": 1450, "communication_cost": 780, "total_cost": 2230},
                {"date": "2024-01-02", "compute_cost": 1480, "communication_cost": 810, "total_cost": 2290},
                {"date": "2024-01-03", "compute_cost": 1420, "communication_cost": 760, "total_cost": 2180},
                {"date": "2024-01-04", "compute_cost": 1500, "communication_cost": 820, "total_cost": 2320},
                {"date": "2024-01-05", "compute_cost": 1470, "communication_cost": 790, "total_cost": 2260},
                {"date": "2024-01-06", "compute_cost": 1430, "communication_cost": 770, "total_cost": 2200},
                {"date": "2024-01-07", "compute_cost": 1490, "communication_cost": 800, "total_cost": 2290}
            ]
        
        # 计算统计数据
        total_cost = sum(item["total_cost"] for item in historical_data)
        avg_daily_cost = total_cost / len(historical_data)
        max_cost = max(item["total_cost"] for item in historical_data)
        min_cost = min(item["total_cost"] for item in historical_data)
        
        # 分析成本趋势
        cost_trend = "稳定"  # 简单判断，实际应使用更复杂的趋势分析
        if historical_data[-1]["total_cost"] > historical_data[0]["total_cost"] * 1.1:
            cost_trend = "上升"
        elif historical_data[-1]["total_cost"] < historical_data[0]["total_cost"] * 0.9:
            cost_trend = "下降"
        
        # 生成成本分布
        compute_cost_ratio = sum(item["compute_cost"] for item in historical_data) / total_cost
        communication_cost_ratio = sum(item["communication_cost"] for item in historical_data) / total_cost
        
        return {
            "time_range": time_range,
            "period": f"{historical_data[0]['date']} 至 {historical_data[-1]['date']}",
            "statistics": {
                "total_cost": total_cost,
                "average_daily_cost": avg_daily_cost,
                "max_daily_cost": max_cost,
                "min_daily_cost": min_cost,
                "compute_cost_ratio": compute_cost_ratio,
                "communication_cost_ratio": communication_cost_ratio
            },
            "trend_analysis": {
                "cost_trend": cost_trend,
                "compute_communication_ratio_trend": "上升"  # 模拟趋势
            },
            "historical_data": historical_data,
            "recommendations": [
                f"基于{time_range}成本趋势，建议{'控制' if cost_trend == '上升' else '保持'}资源使用",
                "考虑优化模型推理，降低计算成本",
                "实现动态资源分配，提高资源利用率"
            ]
        }
