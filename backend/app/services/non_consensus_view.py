from typing import List, Dict, Any
from app.services.visualization_service import VisualizationService

class NonConsensusViewService:
    """非共识观点识别服务类"""
    
    @staticmethod
    def identify_non_consensus_views(transcription: list, industry_benchmark: dict = None) -> dict:
        """
        识别转录内容中的非共识观点，并评估其影响力
        
        Args:
            transcription: 转录文本列表
            industry_benchmark: 行业基准数据
            
        Returns:
            非共识观点列表和影响力评估
        """
        # 提取所有观点
        all_views = NonConsensusViewService._extract_views(transcription)
        
        # 识别非共识观点
        non_consensus_views = NonConsensusViewService._detect_non_consensus(all_views, industry_benchmark)
        
        # 评估观点影响力
        influence_assessment = NonConsensusViewService._assess_influence(non_consensus_views)
        
        # 生成可视化
        visualization_data = NonConsensusViewService._generate_visualizations(non_consensus_views, influence_assessment)
        
        return {
            "total_views": len(all_views),
            "non_consensus_views": non_consensus_views,
            "influence_assessment": influence_assessment,
            "visualizations": visualization_data
        }
    
    @staticmethod
    def _extract_views(transcription: list) -> list:
        """从转录内容中提取所有观点"""
        views = []
        
        for segment in transcription:
            text = segment.get("text", "").lower()
            speaker = segment.get("speaker", "Unknown")
            
            # 识别观点标记词
            opinion_markers = ["认为", "觉得", "应该", "可能", "也许", "大概", "似乎", "好像", "显然", "确实", "肯定"]
            has_opinion = any(marker in text for marker in opinion_markers)
            
            # 识别判断性语句
            if has_opinion or any(keyword in text for keyword in ["好", "坏", "优", "劣", "强", "弱", "高", "低"]):
                views.append({
                    "id": f"view_{len(views) + 1}",
                    "speaker": speaker,
                    "text": text,
                    "original_text": segment.get("text", ""),
                    "timestamp": segment.get("timestamp", 0)
                })
        
        return views
    
    @staticmethod
    def _detect_non_consensus(views: list, industry_benchmark: dict = None) -> list:
        """识别非共识观点"""
        if not industry_benchmark:
            industry_benchmark = NonConsensusViewService._get_industry_benchmark()
        
        non_consensus_views = []
        
        for view in views:
            text = view["text"]
            
            # 检查是否与行业共识相反
            is_non_consensus = False
            consensus_contradictions = []
            
            for consensus in industry_benchmark["consensus_views"]:
                if any(keyword in text for keyword in consensus["keywords"]):
                    # 检查是否包含相反含义
                    if any(opposite in text for opposite in consensus["opposite_keywords"]):
                        is_non_consensus = True
                        consensus_contradictions.append(consensus["view"])
            
            # 检查是否包含创新或颠覆关键词
            if any(keyword in text for keyword in ["创新", "颠覆", "打破", "全新", "革命性", "反其道而行之"]):
                is_non_consensus = True
            
            if is_non_consensus:
                non_consensus_views.append({
                    **view,
                    "is_non_consensus": True,
                    "contradicts": consensus_contradictions,
                    "confidence": 0.85
                })
        
        return non_consensus_views
    
    @staticmethod
    def _get_industry_benchmark() -> dict:
        """获取行业基准数据"""
        return {
            "industry": "科技行业",
            "consensus_views": [
                {
                    "id": "consensus_1",
                    "view": "人工智能将改变所有行业",
                    "keywords": ["人工智能", "AI", "机器学习", "深度学习"],
                    "opposite_keywords": ["不会改变", "影响有限", "被高估", "炒作"]
                },
                {
                    "id": "consensus_2",
                    "view": "数字化转型是企业必由之路",
                    "keywords": ["数字化转型", "数字化", "数字化战略"],
                    "opposite_keywords": ["不需要", "没必要", "风险太大", "成本太高"]
                },
                {
                    "id": "consensus_3",
                    "view": "用户体验是产品成功的关键",
                    "keywords": ["用户体验", "UX", "用户中心"],
                    "opposite_keywords": ["不重要", "次要", "技术更重要"]
                },
                {
                    "id": "consensus_4",
                    "view": "数据是新的石油",
                    "keywords": ["数据", "大数据", "数据驱动"],
                    "opposite_keywords": ["被夸大", "不是关键", "隐私更重要"]
                }
            ]
        }
    
    @staticmethod
    def _assess_influence(non_consensus_views: list) -> dict:
        """评估非共识观点的影响力"""
        if not non_consensus_views:
            return {
                "high_influence": [],
                "medium_influence": [],
                "low_influence": [],
                "overall_influence_score": 0
            }
        
        # 简单的影响力评估算法
        influence_assessment = {
            "high_influence": [],
            "medium_influence": [],
            "low_influence": []
        }
        
        for view in non_consensus_views:
            # 基于观点长度、关键词和矛盾程度评估影响力
            influence_score = len(view["text"]) / 100  # 观点长度
            
            # 创新关键词加分
            innovation_keywords = ["创新", "颠覆", "打破", "全新", "革命性"]
            for keyword in innovation_keywords:
                if keyword in view["text"]:
                    influence_score += 0.3
            
            # 矛盾共识数量加分
            influence_score += len(view["contradicts"]) * 0.2
            
            # 分类
            if influence_score > 0.8:
                influence_assessment["high_influence"].append(view)
            elif influence_score > 0.5:
                influence_assessment["medium_influence"].append(view)
            else:
                influence_assessment["low_influence"].append(view)
        
        # 计算总体影响力评分
        total_score = (
            len(influence_assessment["high_influence"]) * 3 + 
            len(influence_assessment["medium_influence"]) * 2 + 
            len(influence_assessment["low_influence"])
        ) / (len(non_consensus_views) * 3) if non_consensus_views else 0
        
        influence_assessment["overall_influence_score"] = total_score
        
        return influence_assessment
    
    @staticmethod
    def _generate_visualizations(non_consensus_views: list, influence_assessment: dict) -> dict:
        """生成非共识观点的可视化内容"""
        # 生成影响力分布饼图
        influence_data = {
            "labels": ["高影响力", "中影响力", "低影响力"],
            "values": [
                len(influence_assessment["high_influence"]),
                len(influence_assessment["medium_influence"]),
                len(influence_assessment["low_influence"])
            ]
        }
        influence_pie = VisualizationService.generate_pie_chart(influence_data)
        
        # 生成观点数量趋势图
        # 简单的时间分布，基于转录片段索引
        time_distribution = [0] * 10  # 分为10个时间段
        for i, view in enumerate(non_consensus_views):
            time_slot = int((i / len(non_consensus_views)) * 10)
            time_distribution[time_slot] += 1
        
        trend_data = {
            "labels": [f"时段{i+1}" for i in range(10)],
            "series": [{
                "name": "非共识观点数量",
                "data": time_distribution
            }]
        }
        trend_line = VisualizationService.generate_line_chart(trend_data)
        
        # 生成矛盾共识分布柱状图
        contradiction_data = {}
        for view in non_consensus_views:
            for consensus in view["contradicts"]:
                contradiction_data[consensus] = contradiction_data.get(consensus, 0) + 1
        
        contradiction_chart = VisualizationService.generate_bar_chart({
            "labels": list(contradiction_data.keys()),
            "series": [{
                "name": "矛盾次数",
                "data": list(contradiction_data.values())
            }]
        })
        
        return {
            "influence_distribution": influence_pie,
            "time_trend": trend_line,
            "contradiction_analysis": contradiction_chart
        }
    
    @staticmethod
    def analyze_view_clusters(transcription: list) -> dict:
        """
        对转录内容中的观点进行聚类分析
        
        Args:
            transcription: 转录文本列表
            
        Returns:
            观点聚类分析结果
        """
        # 提取所有观点
        all_views = NonConsensusViewService._extract_views(transcription)
        
        # 简单的聚类分析（基于关键词）
        clusters = {
            "技术趋势": [],
            "商业模式": [],
            "用户体验": [],
            "市场策略": [],
            "其他": []
        }
        
        for view in all_views:
            text = view["text"]
            
            if any(keyword in text for keyword in ["技术", "AI", "人工智能", "机器学习", "数字化", "转型"]):
                clusters["技术趋势"].append(view)
            elif any(keyword in text for keyword in ["商业模式", "盈利", "变现", "收入"]):
                clusters["商业模式"].append(view)
            elif any(keyword in text for keyword in ["用户", "体验", "UX", "产品", "设计"]):
                clusters["用户体验"].append(view)
            elif any(keyword in text for keyword in ["市场", "营销", "推广", "销售", "竞争"]):
                clusters["市场策略"].append(view)
            else:
                clusters["其他"].append(view)
        
        # 统计聚类结果
        cluster_stats = {
            cluster_name: len(views) for cluster_name, views in clusters.items()
        }
        
        return {
            "clusters": clusters,
            "cluster_statistics": cluster_stats,
            "total_clusters": len(clusters),
            "average_cluster_size": sum(cluster_stats.values()) / len(cluster_stats) if cluster_stats else 0
        }
