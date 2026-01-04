class MarketTrendService:
    @staticmethod
    def capture_market_trends(transcription: list, historical_trends: dict = None, real_time_data: dict = None) -> dict:
        """捕捉市场趋势
        
        Args:
            transcription: 带有说话人标记的转录结果
            historical_trends: 历史趋势数据（可选）
            real_time_data: 实时市场数据（可选）
            
        Returns:
            dict: 市场趋势分析结果，包含趋势识别、机会窗口和可视化数据
        """
        if not historical_trends:
            historical_trends = MarketTrendService._get_mock_historical_trends()
        
        if not real_time_data:
            real_time_data = MarketTrendService._get_mock_real_time_data()
        
        # 1. 提取关键概念和主题
        key_concepts = MarketTrendService._extract_key_concepts(transcription)
        
        # 2. 识别市场趋势
        identified_trends = MarketTrendService._identify_market_trends(key_concepts, historical_trends, real_time_data)
        
        # 3. 分析趋势强度和影响
        trend_analysis = MarketTrendService._analyze_trend_strength(identified_trends, real_time_data)
        
        # 4. 识别机会窗口
        opportunity_windows = MarketTrendService._identify_opportunity_windows(trend_analysis)
        
        # 5. 生成行动建议
        action_suggestions = MarketTrendService._generate_action_suggestions(opportunity_windows, trend_analysis)
        
        # 6. 生成可视化数据
        visualization_data = MarketTrendService._generate_visualization(identified_trends, trend_analysis, opportunity_windows)
        
        return {
            "status": "success",
            "trends": {
                "key_concepts": key_concepts,
                "identified_trends": identified_trends,
                "trend_analysis": trend_analysis,
                "opportunity_windows": opportunity_windows,
                "action_suggestions": action_suggestions
            },
            "visualization": visualization_data
        }
    
    @staticmethod
    def _extract_key_concepts(transcription: list) -> list:
        """提取关键概念
        
        Args:
            transcription: 转录结果
            
        Returns:
            list: 关键概念列表
        """
        # 简单实现：提取高频关键词
        from collections import Counter
        import re
        
        all_text = " ".join([item["text"] for item in transcription])
        words = re.findall(r"\b\w+\b", all_text)
        filtered_words = [word for word in words if len(word) > 2]
        word_counts = Counter(filtered_words)
        
        key_concepts = []
        for word, count in word_counts.most_common(20):
            key_concepts.append({
                "concept": word,
                "frequency": count,
                "importance": round(count / len(filtered_words), 4)
            })
        
        return key_concepts
    
    @staticmethod
    def _identify_market_trends(key_concepts: list, historical_trends: dict, real_time_data: dict) -> list:
        """识别市场趋势
        
        Args:
            key_concepts: 关键概念列表
            historical_trends: 历史趋势数据
            real_time_data: 实时市场数据
            
        Returns:
            list: 识别出的市场趋势列表
        """
        identified_trends = []
        
        # 遍历关键概念，识别相关趋势
        for concept in key_concepts:
            concept_lower = concept["concept"].lower()
            
            # 检查概念与历史趋势的匹配
            for trend in historical_trends.get("trends", []):
                if concept_lower in trend["name"].lower() or concept_lower in trend["description"].lower():
                    # 计算趋势与概念的相关性
                    relevance = MarketTrendService._calculate_trend_relevance(concept, trend, real_time_data)
                    
                    identified_trends.append({
                        "id": f"trend_{len(identified_trends) + 1}",
                        "concept": concept["concept"],
                        "trend_name": trend["name"],
                        "trend_description": trend["description"],
                        "trend_category": trend["category"],
                        "historical_growth_rate": trend["growth_rate"],
                        "relevance_score": round(relevance, 4),
                        "source": "historical_trend"
                    })
            
            # 检查概念与实时市场数据的匹配
            for real_time_trend in real_time_data.get("trending_topics", []):
                if concept_lower in real_time_trend["topic"].lower():
                    # 计算趋势与概念的相关性
                    relevance = MarketTrendService._calculate_trend_relevance(concept, real_time_trend, real_time_data)
                    
                    identified_trends.append({
                        "id": f"trend_{len(identified_trends) + 1}",
                        "concept": concept["concept"],
                        "trend_name": real_time_trend["topic"],
                        "trend_description": real_time_trend.get("description", ""),
                        "trend_category": real_time_trend.get("category", "实时热点"),
                        "historical_growth_rate": 0.0,
                        "relevance_score": round(relevance, 4),
                        "source": "real_time_data"
                    })
        
        # 去重并排序
        unique_trends = []
        seen_trend_names = set()
        for trend in identified_trends:
            if trend["trend_name"] not in seen_trend_names:
                seen_trend_names.add(trend["trend_name"])
                unique_trends.append(trend)
        
        # 按相关性分数排序
        unique_trends.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return unique_trends[:10]  # 只返回前10个最相关的趋势
    
    @staticmethod
    def _calculate_trend_relevance(concept: dict, trend: dict, real_time_data: dict) -> float:
        """计算趋势与概念的相关性
        
        Args:
            concept: 概念
            trend: 趋势
            real_time_data: 实时市场数据
            
        Returns:
            float: 相关性分数（0-1）
        """
        relevance = 0.0
        concept_lower = concept["concept"].lower()
        
        # 基于关键词匹配计算相关性
        if isinstance(trend, dict):
            trend_text = ""
            if "name" in trend:
                trend_text += trend["name"].lower() + " "
            if "description" in trend:
                trend_text += trend["description"].lower()
            if "topic" in trend:
                trend_text += trend["topic"].lower()
            
            if concept_lower in trend_text:
                relevance += 0.4
        
        # 基于概念重要性计算相关性
        relevance += concept["importance"] * 0.3
        
        # 基于实时数据热度计算相关性
        for real_time_trend in real_time_data.get("trending_topics", []):
            if isinstance(trend, dict) and "topic" in real_time_trend and "topic" in trend:
                if real_time_trend["topic"] == trend["topic"]:
                    relevance += real_time_trend.get("heat_score", 0) / 100 * 0.3
                    break
        
        return min(1.0, max(0.0, relevance))
    
    @staticmethod
    def _analyze_trend_strength(trends: list, real_time_data: dict) -> list:
        """分析趋势强度和影响
        
        Args:
            trends: 识别出的市场趋势列表
            real_time_data: 实时市场数据
            
        Returns:
            list: 趋势强度分析结果
        """
        trend_analysis = []
        
        for trend in trends:
            # 计算趋势强度
            trend_strength = MarketTrendService._calculate_trend_strength(trend, real_time_data)
            
            # 评估趋势影响范围
            impact_range = MarketTrendService._evaluate_impact_range(trend, real_time_data)
            
            # 预测趋势持续时间
            duration_forecast = MarketTrendService._forecast_trend_duration(trend, real_time_data)
            
            # 评估趋势风险
            trend_risk = MarketTrendService._evaluate_trend_risk(trend, real_time_data)
            
            trend_analysis.append({
                "trend_id": trend["id"],
                "trend_name": trend["trend_name"],
                "trend_strength": round(trend_strength, 4),
                "trend_strength_level": MarketTrendService._get_strength_level(trend_strength),
                "impact_range": impact_range,
                "duration_forecast": duration_forecast,
                "trend_risk": round(trend_risk, 4),
                "risk_level": MarketTrendService._get_risk_level(trend_risk),
                "potential_opportunity_score": round((trend_strength * (1 - trend_risk)) * 100, 2)
            })
        
        # 按潜在机会分数排序
        trend_analysis.sort(key=lambda x: x["potential_opportunity_score"], reverse=True)
        
        return trend_analysis
    
    @staticmethod
    def _calculate_trend_strength(trend: dict, real_time_data: dict) -> float:
        """计算趋势强度
        
        Args:
            trend: 趋势
            real_time_data: 实时市场数据
            
        Returns:
            float: 趋势强度分数（0-1）
        """
        strength = 0.0
        
        # 基于历史增长率计算
        if "historical_growth_rate" in trend and trend["historical_growth_rate"] > 0:
            strength += min(1.0, trend["historical_growth_rate"] / 0.3) * 0.4
        
        # 基于实时热度计算
        for real_time_trend in real_time_data.get("trending_topics", []):
            if real_time_trend["topic"] == trend["trend_name"]:
                strength += real_time_trend.get("heat_score", 0) / 100 * 0.4
                break
        
        # 基于相关性分数计算
        strength += trend["relevance_score"] * 0.2
        
        return min(1.0, max(0.0, strength))
    
    @staticmethod
    def _evaluate_impact_range(trend: dict, real_time_data: dict) -> str:
        """评估趋势影响范围
        
        Args:
            trend: 趋势
            real_time_data: 实时市场数据
            
        Returns:
            str: 影响范围描述
        """
        # 简单实现：基于趋势类别和热度评估影响范围
        for real_time_trend in real_time_data.get("trending_topics", []):
            if real_time_trend["topic"] == trend["trend_name"]:
                heat_score = real_time_trend.get("heat_score", 0)
                if heat_score > 80:
                    return "全球"
                elif heat_score > 50:
                    return "全国"
                elif heat_score > 30:
                    return "行业"
                else:
                    return "局部"
        
        # 默认基于趋势类别
        category = trend.get("trend_category", "")
        if category in ["技术", "人工智能", "云计算", "大数据"]:
            return "全球"
        elif category in ["金融", "投资", "市场"]:
            return "全国"
        else:
            return "行业"
    
    @staticmethod
    def _forecast_trend_duration(trend: dict, real_time_data: dict) -> str:
        """预测趋势持续时间
        
        Args:
            trend: 趋势
            real_time_data: 实时市场数据
            
        Returns:
            str: 持续时间预测
        """
        # 简单实现：基于趋势类别和增长率预测持续时间
        if "historical_growth_rate" in trend and trend["historical_growth_rate"] > 0.2:
            return "短期（1-6个月）"
        elif "historical_growth_rate" in trend and trend["historical_growth_rate"] > 0.1:
            return "中期（6-18个月）"
        else:
            return "长期（18个月以上）"
    
    @staticmethod
    def _evaluate_trend_risk(trend: dict, real_time_data: dict) -> float:
        """评估趋势风险
        
        Args:
            trend: 趋势
            real_time_data: 实时市场数据
            
        Returns:
            float: 风险分数（0-1）
        """
        risk = 0.0
        
        # 基于趋势类别评估风险
        category = trend.get("trend_category", "")
        if category in ["技术", "人工智能", "创新"]:
            risk += 0.3  # 新技术风险较高
        elif category in ["金融", "投资"]:
            risk += 0.4  # 金融市场风险较高
        
        # 基于实时波动率评估风险
        for market in real_time_data.get("markets", []):
            if category in market["sector"].lower():
                risk += market.get("volatility", 0) / 100 * 0.3
                break
        
        # 基于趋势强度评估风险（强度越高，风险可能越高）
        trend_strength = MarketTrendService._calculate_trend_strength(trend, real_time_data)
        risk += trend_strength * 0.3
        
        return min(1.0, max(0.0, risk))
    
    @staticmethod
    def _get_strength_level(strength: float) -> str:
        """获取趋势强度级别
        
        Args:
            strength: 趋势强度分数
            
        Returns:
            str: 强度级别描述
        """
        if strength >= 0.8:
            return "极强"
        elif strength >= 0.6:
            return "强"
        elif strength >= 0.4:
            return "中等"
        elif strength >= 0.2:
            return "弱"
        else:
            return "极弱"
    
    @staticmethod
    def _get_risk_level(risk: float) -> str:
        """获取风险级别
        
        Args:
            risk: 风险分数
            
        Returns:
            str: 风险级别描述
        """
        if risk >= 0.8:
            return "高风险"
        elif risk >= 0.6:
            return "中高风险"
        elif risk >= 0.4:
            return "中等风险"
        elif risk >= 0.2:
            return "低风险"
        else:
            return "极低风险"
    
    @staticmethod
    def _identify_opportunity_windows(trend_analysis: list) -> list:
        """识别机会窗口
        
        Args:
            trend_analysis: 趋势强度分析结果
            
        Returns:
            list: 机会窗口列表
        """
        opportunity_windows = []
        
        for analysis in trend_analysis:
            # 只考虑潜在机会分数较高的趋势
            if analysis["potential_opportunity_score"] >= 50:
                # 生成机会窗口描述
                window_description = MarketTrendService._generate_window_description(analysis)
                
                opportunity_windows.append({
                    "id": f"opportunity_{len(opportunity_windows) + 1}",
                    "trend_id": analysis["trend_id"],
                    "trend_name": analysis["trend_name"],
                    "window_description": window_description,
                    "opportunity_score": analysis["potential_opportunity_score"],
                    "window_type": MarketTrendService._get_window_type(analysis),
                    "timing_suggestion": MarketTrendService._get_timing_suggestion(analysis),
                    "estimated_duration": analysis["duration_forecast"]
                })
        
        # 按机会分数排序
        opportunity_windows.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        return opportunity_windows[:5]  # 只返回前5个最佳机会窗口
    
    @staticmethod
    def _generate_window_description(analysis: dict) -> str:
        """生成机会窗口描述
        
        Args:
            analysis: 趋势强度分析结果
            
        Returns:
            str: 机会窗口描述
        """
        return f"{analysis['trend_name']} 趋势当前处于{analysis['trend_strength_level']}强度，影响范围{analysis['impact_range']}，预计持续时间{analysis['duration_forecast']}，风险级别{analysis['risk_level']}，是一个潜在的机会窗口。"
    
    @staticmethod
    def _get_window_type(analysis: dict) -> str:
        """获取机会窗口类型
        
        Args:
            analysis: 趋势强度分析结果
            
        Returns:
            str: 机会窗口类型
        """
        if analysis["trend_strength_level"] in ["极强", "强"] and analysis["risk_level"] in ["低风险", "极低风险"]:
            return "黄金机会"
        elif analysis["trend_strength_level"] in ["极强", "强"] or analysis["risk_level"] in ["低风险", "极低风险"]:
            return "优质机会"
        else:
            return "普通机会"
    
    @staticmethod
    def _get_timing_suggestion(analysis: dict) -> str:
        """获取时机建议
        
        Args:
            analysis: 趋势强度分析结果
            
        Returns:
            str: 时机建议
        """
        if analysis["trend_strength_level"] == "极强":
            return "立即行动，当前是最佳时机"
        elif analysis["trend_strength_level"] == "强":
            return "尽快行动，时机良好"
        elif analysis["trend_strength_level"] == "中等":
            return "密切关注，准备行动"
        else:
            return "持续观察，等待时机"
    
    @staticmethod
    def _generate_action_suggestions(opportunity_windows: list, trend_analysis: list) -> list:
        """生成行动建议
        
        Args:
            opportunity_windows: 机会窗口列表
            trend_analysis: 趋势强度分析结果
            
        Returns:
            list: 行动建议列表
        """
        action_suggestions = []
        
        for window in opportunity_windows:
            # 查找对应的趋势分析
            trend = next((t for t in trend_analysis if t["trend_id"] == window["trend_id"]), None)
            if not trend:
                continue
            
            # 生成具体的行动步骤
            action_steps = MarketTrendService._generate_action_steps(window, trend)
            
            action_suggestions.append({
                "id": f"action_{len(action_suggestions) + 1}",
                "opportunity_id": window["id"],
                "trend_name": window["trend_name"],
                "action_description": f"针对{window['trend_name']}的{window['window_type']}，建议{window['timing_suggestion']}",
                "action_steps": action_steps,
                "required_resources": MarketTrendService._get_required_resources(window),
                "expected_outcome": MarketTrendService._get_expected_outcome(window)
            })
        
        return action_suggestions
    
    @staticmethod
    def _generate_action_steps(window: dict, trend: dict) -> list:
        """生成具体的行动步骤
        
        Args:
            window: 机会窗口
            trend: 趋势分析结果
            
        Returns:
            list: 行动步骤列表
        """
        steps = [
            f"深入研究{window['trend_name']}趋势的详细信息和影响范围",
            f"分析{window['trend_name']}趋势对自身业务或投资的具体影响",
            f"制定针对{window['trend_name']}趋势的具体行动计划",
            f"根据时机建议{window['timing_suggestion'].split('，')[0]}",
            f"持续监控{window['trend_name']}趋势的变化，及时调整策略"
        ]
        
        return steps
    
    @staticmethod
    def _get_required_resources(window: dict) -> list:
        """获取所需资源
        
        Args:
            window: 机会窗口
            
        Returns:
            list: 所需资源列表
        """
        return [
            "市场研究报告",
            "行业专家咨询",
            "资金储备",
            "技术支持",
            "团队协作"
        ]
    
    @staticmethod
    def _get_expected_outcome(window: dict) -> str:
        """获取预期结果
        
        Args:
            window: 机会窗口
            
        Returns:
            str: 预期结果描述
        """
        if window["window_type"] == "黄金机会":
            return "预期获得显著收益，建立市场领先地位"
        elif window["window_type"] == "优质机会":
            return "预期获得良好收益，提升市场竞争力"
        else:
            return "预期获得一定收益，拓展业务领域"
    
    @staticmethod
    def _generate_visualization(identified_trends: list, trend_analysis: list, opportunity_windows: list) -> dict:
        """生成可视化数据
        
        Args:
            identified_trends: 识别出的市场趋势列表
            trend_analysis: 趋势强度分析结果
            opportunity_windows: 机会窗口列表
            
        Returns:
            dict: 可视化数据
        """
        # 生成趋势强度雷达图数据
        radar_data = {
            "categories": ["趋势强度", "相关性", "机会分数", "风险", "影响范围"],
            "series": []
        }
        
        for analysis in trend_analysis[:5]:  # 取前5个趋势
            # 将影响范围转换为数值
            impact_value = 0.8
            if analysis["impact_range"] == "全球":
                impact_value = 1.0
            elif analysis["impact_range"] == "全国":
                impact_value = 0.8
            elif analysis["impact_range"] == "行业":
                impact_value = 0.6
            else:
                impact_value = 0.4
            
            # 查找对应的趋势
            trend = next((t for t in identified_trends if t["id"] == analysis["trend_id"]), None)
            if trend:
                radar_data["series"].append({
                    "name": analysis["trend_name"],
                    "values": [
                        analysis["trend_strength"],
                        trend["relevance_score"],
                        analysis["potential_opportunity_score"] / 100,
                        analysis["trend_risk"],
                        impact_value
                    ]
                })
        
        # 生成机会窗口柱状图数据
        bar_data = {
            "categories": [window["trend_name"] for window in opportunity_windows],
            "values": [window["opportunity_score"] for window in opportunity_windows]
        }
        
        # 生成趋势风险散点图数据
        scatter_data = {
            "points": []
        }
        
        for analysis in trend_analysis:
            # 查找对应的趋势
            trend = next((t for t in identified_trends if t["id"] == analysis["trend_id"]), None)
            if trend:
                scatter_data["points"].append({
                    "x": analysis["trend_strength"],
                    "y": analysis["trend_risk"],
                    "name": analysis["trend_name"],
                    "opportunity_score": analysis["potential_opportunity_score"]
                })
        
        return {
            "trend_strength_radar": radar_data,
            "opportunity_bar": bar_data,
            "risk_scatter": scatter_data
        }
    
    @staticmethod
    def _get_mock_historical_trends() -> dict:
        """获取模拟历史趋势数据
        
        Returns:
            dict: 模拟历史趋势数据
        """
        return {
            "trends": [
                {
                    "id": "hist_trend_1",
                    "name": "人工智能",
                    "description": "人工智能技术在各行业的应用不断扩大，市场规模持续增长",
                    "category": "技术",
                    "growth_rate": 0.30,
                    "start_date": "2020-01-01",
                    "current_status": "增长中"
                },
                {
                    "id": "hist_trend_2",
                    "name": "云计算",
                    "description": "企业和个人对云计算服务的需求持续增长",
                    "category": "技术",
                    "growth_rate": 0.20,
                    "start_date": "2018-01-01",
                    "current_status": "成熟中"
                },
                {
                    "id": "hist_trend_3",
                    "name": "远程工作",
                    "description": "远程工作模式成为常态，相关技术和服务需求增长",
                    "category": "社会",
                    "growth_rate": 0.15,
                    "start_date": "2020-03-01",
                    "current_status": "稳定"
                },
                {
                    "id": "hist_trend_4",
                    "name": "可持续发展",
                    "description": "企业和消费者对可持续发展的关注度不断提高",
                    "category": "环境",
                    "growth_rate": 0.25,
                    "start_date": "2019-01-01",
                    "current_status": "加速增长"
                },
                {
                    "id": "hist_trend_5",
                    "name": "数字经济",
                    "description": "数字经济在全球经济中的占比不断提高",
                    "category": "经济",
                    "growth_rate": 0.18,
                    "start_date": "2017-01-01",
                    "current_status": "稳定增长"
                }
            ]
        }
    
    @staticmethod
    def _get_mock_real_time_data() -> dict:
        """获取模拟实时市场数据
        
        Returns:
            dict: 模拟实时市场数据
        """
        return {
            "trending_topics": [
                {
                    "id": "real_trend_1",
                    "topic": "生成式AI",
                    "description": "生成式AI技术的最新进展和应用",
                    "heat_score": 95,
                    "category": "技术",
                    "trend_direction": "上升",
                    "growth_rate": 0.40
                },
                {
                    "id": "real_trend_2",
                    "topic": "量子计算",
                    "description": "量子计算技术的突破和商业应用",
                    "heat_score": 88,
                    "category": "技术",
                    "trend_direction": "上升",
                    "growth_rate": 0.35
                },
                {
                    "id": "real_trend_3",
                    "topic": "Web3.0",
                    "description": "Web3.0技术和去中心化应用的发展",
                    "heat_score": 75,
                    "category": "技术",
                    "trend_direction": "波动",
                    "growth_rate": 0.25
                },
                {
                    "id": "real_trend_4",
                    "topic": "新能源汽车",
                    "description": "新能源汽车市场的增长和技术创新",
                    "heat_score": 82,
                    "category": "交通",
                    "trend_direction": "上升",
                    "growth_rate": 0.28
                },
                {
                    "id": "real_trend_5",
                    "topic": "元宇宙",
                    "description": "元宇宙概念的发展和应用场景",
                    "heat_score": 65,
                    "category": "技术",
                    "trend_direction": "下降",
                    "growth_rate": 0.15
                }
            ],
            "markets": [
                {
                    "id": "market_1",
                    "sector": "技术",
                    "name": "科技股指数",
                    "current_value": 15000,
                    "change": 2.5,
                    "volatility": 18.5
                },
                {
                    "id": "market_2",
                    "sector": "金融",
                    "name": "金融股指数",
                    "current_value": 3500,
                    "change": -0.5,
                    "volatility": 12.3
                },
                {
                    "id": "market_3",
                    "sector": "新能源",
                    "name": "新能源指数",
                    "current_value": 8500,
                    "change": 3.2,
                    "volatility": 22.8
                }
            ],
            "sentiment_analysis": {
                "positive": 65.2,
                "neutral": 25.8,
                "negative": 9.0
            }
        }
