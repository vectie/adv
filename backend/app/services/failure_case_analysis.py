from typing import List, Dict, Any
from app.services.visualization_service import VisualizationService

class FailureCaseAnalysisService:
    """失败案例分析服务类"""
    
    @staticmethod
    def analyze_failure_cases(transcription: list, failure_database: dict = None) -> dict:
        """
        分析Podcast内容中的失败案例，提供风险规避策略
        
        Args:
            transcription: 转录文本列表
            failure_database: 失败案例数据库
            
        Returns:
            失败案例分析报告和风险规避策略
        """
        # 获取失败案例数据库
        if not failure_database:
            failure_database = FailureCaseAnalysisService._get_failure_database()
        
        # 从转录内容中识别失败模式
        identified_failures = FailureCaseAnalysisService._identify_failure_patterns(transcription, failure_database)
        
        # 分析失败原因和影响
        failure_analysis = FailureCaseAnalysisService._analyze_failure_causes(identified_failures)
        
        # 生成风险规避策略
        risk_mitigation = FailureCaseAnalysisService._generate_risk_mitigation_strategies(failure_analysis)
        
        # 生成可视化
        visualization_data = FailureCaseAnalysisService._generate_visualizations(failure_analysis, risk_mitigation)
        
        return {
            "identified_failures": identified_failures,
            "failure_analysis": failure_analysis,
            "risk_mitigation_strategies": risk_mitigation,
            "visualizations": visualization_data
        }
    
    @staticmethod
    def _get_failure_database() -> dict:
        """获取失败案例数据库"""
        # 模拟失败案例数据库
        return {
            "categories": ["市场定位", "产品开发", "营销策略", "团队管理", "资金管理", "技术选择"],
            "cases": [
                {
                    "id": "case_001",
                    "category": "市场定位",
                    "title": "定位模糊导致用户流失",
                    "description": "产品定位不明确，无法满足特定用户群体需求，导致用户流失率高",
                    "key_patterns": ["定位模糊", "用户需求不明确", "目标群体广泛", "缺乏差异化"],
                    "consequences": ["用户流失", "市场份额下降", "品牌认知度低"],
                    "lessons": ["明确目标用户", "聚焦核心需求", "打造差异化优势"]
                },
                {
                    "id": "case_002",
                    "category": "产品开发",
                    "title": "功能过度导致产品复杂",
                    "description": "试图满足所有用户需求，导致产品功能过度复杂，用户体验差",
                    "key_patterns": ["功能过多", "用户体验差", "学习曲线陡峭", "核心功能不突出"],
                    "consequences": ["用户活跃度低", "口碑差", "开发维护成本高"],
                    "lessons": ["聚焦核心功能", "保持简洁设计", "持续优化用户体验"]
                },
                {
                    "id": "case_003",
                    "category": "营销策略",
                    "title": "营销渠道选择失误",
                    "description": "选择了不适合目标用户的营销渠道，导致获客成本高，转化率低",
                    "key_patterns": ["渠道不匹配", "获客成本高", "转化率低", "营销预算浪费"],
                    "consequences": ["资金压力大", "增长缓慢", "市场拓展困难"],
                    "lessons": ["深入了解目标用户", "测试不同渠道", "优化营销漏斗"]
                },
                {
                    "id": "case_004",
                    "category": "团队管理",
                    "title": "团队沟通不畅导致项目延误",
                    "description": "团队成员之间沟通不畅，信息传递不及时，导致项目延误",
                    "key_patterns": ["沟通不畅", "信息不对称", "决策缓慢", "责任不明确"],
                    "consequences": ["项目延误", "团队士气低落", "产品质量下降"],
                    "lessons": ["建立有效的沟通机制", "明确角色责任", "采用敏捷开发方法"]
                },
                {
                    "id": "case_005",
                    "category": "资金管理",
                    "title": "资金链断裂导致企业倒闭",
                    "description": "资金规划不合理，现金流断裂，导致企业无法继续运营",
                    "key_patterns": ["资金规划不合理", "现金流紧张", "融资困难", "成本控制不力"],
                    "consequences": ["企业倒闭", "员工失业", "投资者损失"],
                    "lessons": ["合理规划资金", "严格控制成本", "多元化融资渠道"]
                },
                {
                    "id": "case_006",
                    "category": "技术选择",
                    "title": "技术选型失误导致系统崩溃",
                    "description": "选择了不适合业务需求的技术栈，导致系统性能差，频繁崩溃",
                    "key_patterns": ["技术选型失误", "系统性能差", "维护成本高", "扩展性不足"],
                    "consequences": ["用户流失", "品牌声誉受损", "开发成本增加"],
                    "lessons": ["充分评估技术需求", "选择成熟稳定的技术", "考虑未来扩展性"]
                }
            ]
        }
    
    @staticmethod
    def _identify_failure_patterns(transcription: list, failure_database: dict) -> list:
        """从转录内容中识别失败模式"""
        identified_failures = []
        
        # 提取转录文本中的所有关键词
        transcription_text = " ".join([segment.get("text", "").lower() for segment in transcription])
        
        # 匹配失败案例数据库中的模式
        for case in failure_database["cases"]:
            matched_patterns = []
            for pattern in case["key_patterns"]:
                if pattern in transcription_text:
                    matched_patterns.append(pattern)
            
            if matched_patterns:
                identified_failures.append({
                    "case_id": case["id"],
                    "category": case["category"],
                    "title": case["title"],
                    "matched_patterns": matched_patterns,
                    "match_score": len(matched_patterns) / len(case["key_patterns"])
                })
        
        # 按匹配分数排序
        identified_failures.sort(key=lambda x: x["match_score"], reverse=True)
        
        return identified_failures
    
    @staticmethod
    def _analyze_failure_causes(identified_failures: list) -> dict:
        """分析失败原因和影响"""
        if not identified_failures:
            return {
                "categories_analysis": {},
                "common_causes": [],
                "potential_consequences": [],
                "severity_assessment": "低"
            }
        
        # 按类别分析
        categories_analysis = {}
        for failure in identified_failures:
            category = failure["category"]
            if category not in categories_analysis:
                categories_analysis[category] = {
                    "count": 0,
                    "total_match_score": 0,
                    "average_match_score": 0,
                    "cases": []
                }
            categories_analysis[category]["count"] += 1
            categories_analysis[category]["total_match_score"] += failure["match_score"]
            categories_analysis[category]["cases"].append(failure["title"])
        
        # 计算平均匹配分数
        for category in categories_analysis:
            categories_analysis[category]["average_match_score"] = \
                categories_analysis[category]["total_match_score"] / categories_analysis[category]["count"]
        
        # 识别常见原因和潜在后果
        common_causes = ["市场定位不准确", "产品功能过度", "营销渠道选择失误", "团队沟通不畅"]
        potential_consequences = ["用户流失", "市场份额下降", "项目延误", "资金压力"]
        
        # 评估严重性
        severity = "低"
        max_match_score = max([f["match_score"] for f in identified_failures])
        if max_match_score > 0.8:
            severity = "高"
        elif max_match_score > 0.5:
            severity = "中"
        
        return {
            "categories_analysis": categories_analysis,
            "common_causes": common_causes,
            "potential_consequences": potential_consequences,
            "severity_assessment": severity
        }
    
    @staticmethod
    def _generate_risk_mitigation_strategies(failure_analysis: dict) -> dict:
        """生成风险规避策略"""
        strategies = {
            "prevention": [],
            "detection": [],
            "response": [],
            "recovery": []
        }
        
        # 预防策略
        strategies["prevention"].append({
            "category": "市场定位",
            "strategy": "明确目标用户群体，聚焦核心需求，打造差异化优势",
            "action_items": [
                "进行市场调研，深入了解目标用户",
                "定义清晰的产品定位和价值主张",
                "定期评估市场定位的有效性"
            ],
            "priority": "高"
        })
        
        strategies["prevention"].append({
            "category": "产品开发",
            "strategy": "采用敏捷开发方法，聚焦核心功能，持续优化用户体验",
            "action_items": [
                "进行用户需求调研，确定核心功能",
                "采用最小可行产品(MVP)策略",
                "定期收集用户反馈，持续迭代优化"
            ],
            "priority": "高"
        })
        
        # 检测策略
        strategies["detection"].append({
            "category": "项目管理",
            "strategy": "建立有效的监控和预警机制，及时发现潜在问题",
            "action_items": [
                "设置关键绩效指标(KPIs)",
                "建立定期检查机制",
                "使用项目管理工具跟踪进度"
            ],
            "priority": "中"
        })
        
        # 响应策略
        strategies["response"].append({
            "category": "危机管理",
            "strategy": "制定危机应对计划，快速响应和解决问题",
            "action_items": [
                "制定详细的危机应对预案",
                "建立跨部门响应团队",
                "定期进行危机演练"
            ],
            "priority": "高"
        })
        
        # 恢复策略
        strategies["recovery"].append({
            "category": "业务恢复",
            "strategy": "制定业务恢复计划，减少失败带来的影响",
            "action_items": [
                "建立业务连续性计划",
                "定期备份关键数据",
                "制定恢复时间表和优先级"
            ],
            "priority": "中"
        })
        
        return strategies
    
    @staticmethod
    def _generate_visualizations(failure_analysis: dict, risk_mitigation: dict) -> dict:
        """生成失败案例分析的可视化内容"""
        # 生成失败类别分布饼图
        if failure_analysis["categories_analysis"]:
            category_labels = list(failure_analysis["categories_analysis"].keys())
            category_values = [cat["count"] for cat in failure_analysis["categories_analysis"].values()]
        else:
            category_labels = ["无匹配失败模式"]
            category_values = [1]
        
        category_pie = VisualizationService.generate_pie_chart({"labels": category_labels, "values": category_values})
        
        # 生成风险等级雷达图
        risk_data = {
            "categories": ["市场风险", "产品风险", "营销风险", "团队风险", "资金风险", "技术风险"],
            "series": [{
                "name": "风险等级",
                "data": [85, 70, 65, 75, 60, 80]  # 模拟数据
            }]
        }
        risk_radar = VisualizationService.generate_radar_chart(risk_data)
        
        # 生成策略优先级柱状图
        strategy_counts = {
            "预防策略": len(risk_mitigation["prevention"]),
            "检测策略": len(risk_mitigation["detection"]),
            "响应策略": len(risk_mitigation["response"]),
            "恢复策略": len(risk_mitigation["recovery"])
        }
        
        strategy_bar = VisualizationService.generate_bar_chart({
            "labels": list(strategy_counts.keys()),
            "series": [{"name": "策略数量", "data": list(strategy_counts.values())}]
        })
        
        return {
            "failure_category_distribution": category_pie,
            "risk_level_assessment": risk_radar,
            "strategy_priority": strategy_bar
        }
    
    @staticmethod
    def compare_with_success_patterns(transcription: list, success_patterns: dict = None) -> dict:
        """
        对比成功模式和失败模式，提供改进建议
        
        Args:
            transcription: 转录文本列表
            success_patterns: 成功模式数据库
            
        Returns:
            成功与失败模式对比分析
        """
        if not success_patterns:
            success_patterns = {
                "key_patterns": ["明确的目标定位", "聚焦核心功能", "有效的营销策略", "良好的团队沟通", "合理的资金规划", "合适的技术选择"],
                "common_attributes": ["用户导向", "敏捷迭代", "数据驱动", "持续学习", "创新精神"]
            }
        
        # 分析转录内容中的成功和失败模式
        transcription_text = " ".join([segment.get("text", "").lower() for segment in transcription])
        
        # 匹配成功模式
        matched_success_patterns = []
        for pattern in success_patterns["key_patterns"]:
            if pattern in transcription_text:
                matched_success_patterns.append(pattern)
        
        # 获取失败模式（复用前面的方法）
        failure_database = FailureCaseAnalysisService._get_failure_database()
        identified_failures = FailureCaseAnalysisService._identify_failure_patterns(transcription, failure_database)
        
        # 生成对比分析
        comparison = {
            "success_patterns": {
                "total": len(success_patterns["key_patterns"]),
                "matched": len(matched_success_patterns),
                "matched_patterns": matched_success_patterns,
                "match_rate": len(matched_success_patterns) / len(success_patterns["key_patterns"])
            },
            "failure_patterns": {
                "total": len(identified_failures),
                "high_risk": len([f for f in identified_failures if f["match_score"] > 0.7]),
                "medium_risk": len([f for f in identified_failures if 0.3 < f["match_score"] <= 0.7]),
                "low_risk": len([f for f in identified_failures if f["match_score"] <= 0.3])
            },
            "gap_analysis": {
                "missing_success_patterns": [p for p in success_patterns["key_patterns"] if p not in matched_success_patterns],
                "priority_improvements": [p for p in success_patterns["key_patterns"] if p not in matched_success_patterns][:3]
            },
            "improvement_suggestions": [
                f"强化{pattern}，这是成功模式中的关键因素" for pattern in matched_success_patterns[:3]
            ] + [
                f"改进{pattern}，避免类似失败案例的后果" for f in identified_failures[:3] for pattern in f["matched_patterns"]
            ]
        }
        
        return comparison
    
    @staticmethod
    def generate_failure_case_studies(category: str = None, limit: int = 5) -> list:
        """
        生成失败案例研究报告
        
        Args:
            category: 失败类别
            limit: 返回的案例数量限制
            
        Returns:
            失败案例研究报告列表
        """
        # 获取失败案例数据库
        failure_database = FailureCaseAnalysisService._get_failure_database()
        
        # 过滤案例
        cases = failure_database["cases"]
        if category:
            cases = [case for case in cases if case["category"] == category]
        
        # 生成案例研究报告
        case_studies = []
        for case in cases[:limit]:
            case_studies.append({
                "case_id": case["id"],
                "title": case["title"],
                "category": case["category"],
                "description": case["description"],
                "key_failure_patterns": case["key_patterns"],
                "consequences": case["consequences"],
                "lessons_learned": case["lessons"],
                "risk_mitigation": [
                    f"避免{pattern}" for pattern in case["key_patterns"]
                ]
            })
        
        return case_studies
