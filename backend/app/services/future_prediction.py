class FuturePredictionService:
    @staticmethod
    def predict_future(transcription: list, historical_data: dict = None) -> dict:
        """基于转录内容预测未来趋势和潜在后果
        
        Args:
            transcription: 带有说话人标记的转录结果
            historical_data: 历史数据，用于增强预测准确性
            
        Returns:
            dict: 未来预测结果，包含趋势预测、潜在后果、风险评估等
        """
        # 1. 提取关键预测点
        key_points = FuturePredictionService._extract_key_points(transcription)
        
        # 2. 预测未来趋势
        trends = FuturePredictionService._predict_trends(key_points, historical_data)
        
        # 3. 分析潜在后果
        consequences = FuturePredictionService._analyze_consequences(trends, key_points)
        
        # 4. 评估风险
        risks = FuturePredictionService._assess_risks(trends, consequences)
        
        # 5. 生成应对策略
        strategies = FuturePredictionService._generate_strategies(trends, risks)
        
        # 6. 生成可视化数据
        visualization_data = FuturePredictionService._generate_visualization(trends, consequences, risks)
        
        return {
            "status": "success",
            "prediction": {
                "key_points": key_points,
                "trends": trends,
                "consequences": consequences,
                "risks": risks,
                "strategies": strategies
            },
            "visualization": visualization_data
        }
    
    @staticmethod
    def _extract_key_points(transcription: list) -> list:
        """提取关键预测点
        
        Args:
            transcription: 带有说话人标记的转录结果
            
        Returns:
            list: 关键预测点列表
        """
        key_points = []
        
        # 关键词列表，用于识别关键预测点
        future_keywords = [
            "未来", "趋势", "预测", "可能", "将会", "将要", "预计", "展望",
            "发展", "变化", "转型", "创新", "革命", "颠覆", "突破",
            "机会", "挑战", "风险", "威胁", "机遇", "趋势", "方向"
        ]
        
        for i, item in enumerate(transcription):
            text = item["text"]
            speaker = item["speaker"]
            
            # 检查是否包含未来相关关键词
            has_future_keywords = any(keyword in text for keyword in future_keywords)
            
            if has_future_keywords:
                # 分类预测点类型
                point_type = FuturePredictionService._classify_point_type(text)
                
                key_points.append({
                    "id": i + 1,
                    "speaker": speaker,
                    "text": text,
                    "type": point_type,
                    "position": i,
                    "confidence": 0.8  # 简单实现，固定置信度
                })
        
        return key_points
    
    @staticmethod
    def _classify_point_type(text: str) -> str:
        """分类预测点类型
        
        Args:
            text: 预测点文本
            
        Returns:
            str: 预测点类型，如：技术趋势、市场趋势、风险预测等
        """
        # 技术趋势关键词
        tech_keywords = ["技术", "科技", "人工智能", "AI", "机器学习", "深度学习",
                        "自动化", "数字化", "智能化", "物联网", "区块链", "元宇宙"]
        
        # 市场趋势关键词
        market_keywords = ["市场", "行业", "需求", "用户", "竞争", "增长", "规模",
                          "份额", "市值", "投资", "融资", "估值"]
        
        # 风险预测关键词
        risk_keywords = ["风险", "威胁", "挑战", "问题", "危机", "风险", "障碍",
                       "限制", "瓶颈", "困难", "阻碍", "风险"]
        
        # 机会预测关键词
        opportunity_keywords = ["机会", "机遇", "潜力", "可能性", "优势", "利好",
                              "机会", "机遇", "前景", "潜力", "可能性"]
        
        # 分类预测点类型
        if any(keyword in text for keyword in tech_keywords):
            return "技术趋势"
        elif any(keyword in text for keyword in market_keywords):
            return "市场趋势"
        elif any(keyword in text for keyword in risk_keywords):
            return "风险预测"
        elif any(keyword in text for keyword in opportunity_keywords):
            return "机会预测"
        else:
            return "综合预测"
    
    @staticmethod
    def _predict_trends(key_points: list, historical_data: dict = None) -> list:
        """预测未来趋势
        
        Args:
            key_points: 关键预测点列表
            historical_data: 历史数据
            
        Returns:
            list: 未来趋势预测结果
        """
        trends = []
        
        # 按类型分组预测点
        points_by_type = {}
        for point in key_points:
            if point["type"] not in points_by_type:
                points_by_type[point["type"]] = []
            points_by_type[point["type"]].append(point)
        
        # 为每种类型生成趋势预测
        for type_name, points in points_by_type.items():
            # 简单实现：基于预测点数量和内容生成趋势
            trend_confidence = min(1.0, len(points) / 10 + 0.5)  # 简单计算置信度
            
            # 生成趋势描述
            if type_name == "技术趋势":
                trend_description = "技术将持续创新，人工智能、自动化等领域将迎来重大突破"
            elif type_name == "市场趋势":
                trend_description = "市场将继续增长，竞争加剧，用户需求将更加多样化"
            elif type_name == "风险预测":
                trend_description = "未来将面临多种风险和挑战，需要提前做好准备"
            elif type_name == "机会预测":
                trend_description = "将出现大量新机会，抓住机遇将带来巨大收益"
            else:
                trend_description = "未来将呈现多元化趋势，需要综合考虑各种因素"
            
            trends.append({
                "type": type_name,
                "description": trend_description,
                "confidence": round(trend_confidence, 2),
                "supporting_points": len(points),
                "timeframe": FuturePredictionService._determine_timeframe(points)
            })
        
        return trends
    
    @staticmethod
    def _determine_timeframe(points: list) -> str:
        """确定预测时间范围
        
        Args:
            points: 预测点列表
            
        Returns:
            str: 时间范围，如：短期（1-2年）、中期（3-5年）、长期（5年以上）
        """
        # 简单实现：随机分配时间范围
        import random
        timeframes = ["短期（1-2年）", "中期（3-5年）", "长期（5年以上）"]
        return random.choice(timeframes)
    
    @staticmethod
    def _analyze_consequences(trends: list, key_points: list) -> list:
        """分析潜在后果
        
        Args:
            trends: 未来趋势预测结果
            key_points: 关键预测点列表
            
        Returns:
            list: 潜在后果分析结果
        """
        consequences = []
        
        for trend in trends:
            # 为每个趋势生成潜在后果
            if trend["type"] == "技术趋势":
                consequences.append({
                    "trend_type": trend["type"],
                    "positive": [
                        "提高生产效率，降低成本",
                        "创造新的商业模式和机会",
                        "提升用户体验和满意度"
                    ],
                    "negative": [
                        "可能导致部分岗位失业",
                        "技术风险和安全隐患",
                        "需要大量投资和资源"
                    ],
                    "confidence": trend["confidence"]
                })
            elif trend["type"] == "市场趋势":
                consequences.append({
                    "trend_type": trend["type"],
                    "positive": [
                        "市场规模扩大，收入增长",
                        "吸引更多投资和人才",
                        "提升品牌影响力"
                    ],
                    "negative": [
                        "竞争加剧，利润空间压缩",
                        "用户需求变化快，难以跟上",
                        "市场饱和风险"
                    ],
                    "confidence": trend["confidence"]
                })
            elif trend["type"] == "风险预测":
                consequences.append({
                    "trend_type": trend["type"],
                    "positive": [
                        "提前识别风险，做好准备",
                        "提高应对风险的能力",
                        "从风险中发现机会"
                    ],
                    "negative": [
                        "可能导致损失和危机",
                        "影响企业声誉和形象",
                        "增加运营成本和压力"
                    ],
                    "confidence": trend["confidence"]
                })
            else:
                consequences.append({
                    "trend_type": trend["type"],
                    "positive": [
                        "综合考虑各种因素，做出更明智的决策",
                        "平衡风险和机会",
                        "提高长期竞争力"
                    ],
                    "negative": [
                        "可能错过一些机会",
                        "决策过程复杂，耗时长",
                        "需要大量数据和分析"
                    ],
                    "confidence": trend["confidence"]
                })
        
        return consequences
    
    @staticmethod
    def _assess_risks(trends: list, consequences: list) -> list:
        """评估风险
        
        Args:
            trends: 未来趋势预测结果
            consequences: 潜在后果分析结果
            
        Returns:
            list: 风险评估结果
        """
        risks = []
        
        for trend in trends:
            # 查找对应的后果
            consequence = next(c for c in consequences if c["trend_type"] == trend["type"])
            
            # 评估风险级别
            risk_level = "低"
            if trend["confidence"] > 0.8 and len(consequence["negative"]) > 2:
                risk_level = "高"
            elif trend["confidence"] > 0.6 or len(consequence["negative"]) > 1:
                risk_level = "中"
            
            # 计算风险分数（1-10）
            risk_score = min(10, int(trend["confidence"] * 10 * (0.5 + len(consequence["negative"]) * 0.1)))
            
            risks.append({
                "trend_type": trend["type"],
                "risk_level": risk_level,
                "risk_score": risk_score,
                "potential_impact": consequence["negative"],
                "likelihood": trend["confidence"]
            })
        
        return risks
    
    @staticmethod
    def _generate_strategies(trends: list, risks: list) -> list:
        """生成应对策略
        
        Args:
            trends: 未来趋势预测结果
            risks: 风险评估结果
            
        Returns:
            list: 应对策略列表
        """
        strategies = []
        
        for trend in trends:
            # 查找对应的风险
            risk = next(r for r in risks if r["trend_type"] == trend["type"])
            
            if trend["type"] == "技术趋势":
                strategies.append({
                    "trend_type": trend["type"],
                    "strategies": [
                        "加大技术研发投入，保持技术领先地位",
                        "建立技术风险评估机制，提前应对安全隐患",
                        "加强人才培养和引进，构建技术团队",
                        "探索新的商业模式，将技术优势转化为商业价值"
                    ],
                    "priority": "高" if risk["risk_level"] == "高" else "中"
                })
            elif trend["type"] == "市场趋势":
                strategies.append({
                    "trend_type": trend["type"],
                    "strategies": [
                        "加强市场调研，深入了解用户需求",
                        "优化产品和服务，提升竞争力",
                        "拓展新的市场渠道和客户群体",
                        "建立灵活的市场响应机制，快速适应变化"
                    ],
                    "priority": "高" if risk["risk_level"] == "高" else "中"
                })
            elif trend["type"] == "风险预测":
                strategies.append({
                    "trend_type": trend["type"],
                    "strategies": [
                        "建立全面的风险监控体系，提前识别风险",
                        "制定详细的风险应对预案，提高应对能力",
                        "分散风险，避免过度依赖单一市场或技术",
                        "加强危机公关和沟通能力，降低负面影响"
                    ],
                    "priority": "高" if risk["risk_level"] == "高" else "中"
                })
            else:
                strategies.append({
                    "trend_type": trend["type"],
                    "strategies": [
                        "建立综合决策机制，考虑各种因素",
                        "加强数据分析和预测能力，提高决策准确性",
                        "保持灵活性和适应性，快速调整策略",
                        "注重长期发展，平衡短期利益和长期目标"
                    ],
                    "priority": "中"
                })
        
        return strategies
    
    @staticmethod
    def _generate_visualization(trends: list, consequences: list, risks: list) -> dict:
        """生成可视化数据
        
        Args:
            trends: 未来趋势预测结果
            consequences: 潜在后果分析结果
            risks: 风险评估结果
            
        Returns:
            dict: 可视化数据，包含趋势图、风险矩阵等
        """
        # 生成趋势数据（用于折线图或柱状图）
        trend_data = []
        for trend in trends:
            trend_data.append({
                "type": trend["type"],
                "confidence": trend["confidence"] * 100,
                "supporting_points": trend["supporting_points"]
            })
        
        # 生成风险矩阵数据
        risk_matrix = []
        for risk in risks:
            # 将风险分数映射到1-5的评分
            severity = min(5, int(risk["risk_score"] / 2))
            likelihood = min(5, int(risk["likelihood"] * 5))
            
            risk_matrix.append({
                "type": risk["trend_type"],
                "severity": severity,
                "likelihood": likelihood,
                "risk_level": risk["risk_level"]
            })
        
        return {
            "trend_data": trend_data,
            "risk_matrix": risk_matrix,
            "consequence_data": consequences
        }