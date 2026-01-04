class NonConsensusService:
    @staticmethod
    def identify_non_consensus(transcription: list, industry_benchmark: dict = None) -> dict:
        """识别非共识观点，发现打破常规的思考角度
        
        Args:
            transcription: 带有说话人标记的转录结果
            industry_benchmark: 行业基准数据，用于对比分析
            
        Returns:
            dict: 非共识观点分析结果，包含非共识观点列表、观点影响力评估等
        """
        # 1. 提取所有观点
        all_opinions = NonConsensusService._extract_opinions(transcription)
        
        # 2. 识别共识观点
        consensus_opinions = NonConsensusService._identify_consensus(all_opinions, industry_benchmark)
        
        # 3. 识别非共识观点
        non_consensus_opinions = NonConsensusService._identify_non_consensus(all_opinions, consensus_opinions)
        
        # 4. 评估观点影响力
        non_consensus_opinions = NonConsensusService._evaluate_influence(non_consensus_opinions, all_opinions)
        
        # 5. 生成可视化数据
        visualization_data = NonConsensusService._generate_visualization(non_consensus_opinions, consensus_opinions)
        
        return {
            "status": "success",
            "analysis": {
                "total_opinions": len(all_opinions),
                "consensus_opinions": consensus_opinions,
                "non_consensus_opinions": non_consensus_opinions
            },
            "visualization": visualization_data
        }
    
    @staticmethod
    def _extract_opinions(transcription: list) -> list:
        """提取所有观点
        
        Args:
            transcription: 带有说话人标记的转录结果
            
        Returns:
            list: 观点列表
        """
        opinions = []
        
        # 观点关键词列表，用于识别观点
        opinion_keywords = [
            "我认为", "我觉得", "我的观点是", "我相信", "我坚信", "我怀疑",
            "应该", "必须", "不应该", "不应该", "建议", "推荐",
            "可能", "或许", "大概", "很可能", "很有可能", "不太可能",
            "好的", "不好的", "有利的", "不利的", "积极的", "消极的"
        ]
        
        for i, item in enumerate(transcription):
            text = item["text"]
            speaker = item["speaker"]
            
            # 检查是否包含观点关键词
            has_opinion_keywords = any(keyword in text for keyword in opinion_keywords)
            
            if has_opinion_keywords:
                # 分类观点类型
                opinion_type = NonConsensusService._classify_opinion_type(text)
                
                opinions.append({
                    "id": i + 1,
                    "speaker": speaker,
                    "text": text,
                    "type": opinion_type,
                    "position": i,
                    "sentiment": NonConsensusService._analyze_sentiment(text)
                })
        
        return opinions
    
    @staticmethod
    def _classify_opinion_type(text: str) -> str:
        """分类观点类型
        
        Args:
            text: 观点文本
            
        Returns:
            str: 观点类型，如：技术观点、市场观点、产品观点等
        """
        # 技术观点关键词
        tech_keywords = ["技术", "科技", "人工智能", "AI", "机器学习", "深度学习",
                        "自动化", "数字化", "智能化", "物联网", "区块链", "元宇宙"]
        
        # 市场观点关键词
        market_keywords = ["市场", "行业", "需求", "用户", "竞争", "增长", "规模",
                          "份额", "市值", "投资", "融资", "估值"]
        
        # 产品观点关键词
        product_keywords = ["产品", "服务", "功能", "设计", "体验", "质量",
                          "性能", "价格", "性价比", "创新", "差异化"]
        
        # 战略观点关键词
        strategy_keywords = ["战略", "策略", "规划", "方向", "目标", "愿景",
                           "使命", "价值观", "定位", "转型", "升级"]
        
        # 分类观点类型
        if any(keyword in text for keyword in tech_keywords):
            return "技术观点"
        elif any(keyword in text for keyword in market_keywords):
            return "市场观点"
        elif any(keyword in text for keyword in product_keywords):
            return "产品观点"
        elif any(keyword in text for keyword in strategy_keywords):
            return "战略观点"
        else:
            return "综合观点"
    
    @staticmethod
    def _analyze_sentiment(text: str) -> str:
        """分析观点情感
        
        Args:
            text: 观点文本
            
        Returns:
            str: 情感类型，如：积极、中性、消极
        """
        # 积极情感关键词
        positive_keywords = ["好", "很好", "非常好", "优秀", "出色", "完美",
                           "棒", "精彩", "厉害", "强大", "创新", "突破",
                           "机会", "机遇", "潜力", "希望", "乐观", "看好"]
        
        # 消极情感关键词
        negative_keywords = ["不好", "很差", "非常差", "糟糕", "差劲", "失败",
                           "烂", "垃圾", "弱", "差劲", "风险", "威胁",
                           "挑战", "问题", "危机", "悲观", "不看好", "担忧"]
        
        # 分析情感
        positive_count = sum(1 for keyword in positive_keywords if keyword in text)
        negative_count = sum(1 for keyword in negative_keywords if keyword in text)
        
        if positive_count > negative_count:
            return "积极"
        elif negative_count > positive_count:
            return "消极"
        else:
            return "中性"
    
    @staticmethod
    def _identify_consensus(all_opinions: list, industry_benchmark: dict = None) -> list:
        """识别共识观点
        
        Args:
            all_opinions: 所有观点列表
            industry_benchmark: 行业基准数据
            
        Returns:
            list: 共识观点列表
        """
        consensus_opinions = []
        
        # 简单实现：基于观点类型和情感的共识识别
        # 统计每种类型和情感组合的观点数量
        opinion_counts = {}
        for opinion in all_opinions:
            key = f"{opinion['type']}_{opinion['sentiment']}"
            if key not in opinion_counts:
                opinion_counts[key] = 0
            opinion_counts[key] += 1
        
        # 找出占比超过50%的观点类型和情感组合作为共识
        total_opinions = len(all_opinions)
        consensus_threshold = 0.5
        
        for key, count in opinion_counts.items():
            if count / total_opinions > consensus_threshold:
                opinion_type, sentiment = key.split('_')
                consensus_opinions.append({
                    "type": opinion_type,
                    "sentiment": sentiment,
                    "count": count,
                    "percentage": round(count / total_opinions, 2)
                })
        
        # 如果有行业基准数据，结合行业基准分析
        if industry_benchmark:
            consensus_opinions = NonConsensusService._integrate_benchmark(consensus_opinions, industry_benchmark)
        
        return consensus_opinions
    
    @staticmethod
    def _integrate_benchmark(consensus_opinions: list, industry_benchmark: dict) -> list:
        """结合行业基准数据调整共识观点
        
        Args:
            consensus_opinions: 共识观点列表
            industry_benchmark: 行业基准数据
            
        Returns:
            list: 调整后的共识观点列表
        """
        # 简单实现：将行业基准观点添加到共识观点中
        if "consensus_opinions" in industry_benchmark:
            for benchmark_opinion in industry_benchmark["consensus_opinions"]:
                # 检查是否已经存在
                exists = any(
                    o["type"] == benchmark_opinion["type"] and o["sentiment"] == benchmark_opinion["sentiment"]
                    for o in consensus_opinions
                )
                if not exists:
                    consensus_opinions.append({
                        "type": benchmark_opinion["type"],
                        "sentiment": benchmark_opinion["sentiment"],
                        "count": 0,
                        "percentage": 0.0,
                        "from_benchmark": True
                    })
        
        return consensus_opinions
    
    @staticmethod
    def _identify_non_consensus(all_opinions: list, consensus_opinions: list) -> list:
        """识别非共识观点
        
        Args:
            all_opinions: 所有观点列表
            consensus_opinions: 共识观点列表
            
        Returns:
            list: 非共识观点列表
        """
        non_consensus_opinions = []
        
        # 将共识观点转换为字典，便于查找
        consensus_dict = {}
        for consensus in consensus_opinions:
            key = f"{consensus['type']}_{consensus['sentiment']}"
            consensus_dict[key] = consensus
        
        # 找出与共识观点不同的观点作为非共识观点
        for opinion in all_opinions:
            key = f"{opinion['type']}_{opinion['sentiment']}"
            if key not in consensus_dict:
                non_consensus_opinions.append(opinion)
        
        return non_consensus_opinions
    
    @staticmethod
    def _evaluate_influence(non_consensus_opinions: list, all_opinions: list) -> list:
        """评估观点影响力
        
        Args:
            non_consensus_opinions: 非共识观点列表
            all_opinions: 所有观点列表
            
        Returns:
            list: 带有影响力评估的非共识观点列表
        """
        # 简单实现：基于说话人角色和观点在对话中的位置评估影响力
        for opinion in non_consensus_opinions:
            # 基于说话人角色评估影响力
            speaker_influence = 1.0
            if opinion["speaker"] == "主持人":
                speaker_influence = 1.5  # 主持人影响力更高
            
            # 基于观点在对话中的位置评估影响力（越靠近中间影响力越高）
            position_score = 1.0 - abs(opinion["position"] - len(all_opinions) / 2) / (len(all_opinions) / 2)
            
            # 计算总影响力分数
            influence_score = round(speaker_influence * position_score, 2)
            
            # 分类影响力等级
            if influence_score > 1.2:
                influence_level = "高"
            elif influence_score > 0.8:
                influence_level = "中"
            else:
                influence_level = "低"
            
            # 添加影响力评估
            opinion["influence_score"] = influence_score
            opinion["influence_level"] = influence_level
        
        # 按影响力分数降序排序
        non_consensus_opinions.sort(key=lambda x: x["influence_score"], reverse=True)
        
        return non_consensus_opinions
    
    @staticmethod
    def _generate_visualization(non_consensus_opinions: list, consensus_opinions: list) -> dict:
        """生成可视化数据
        
        Args:
            non_consensus_opinions: 非共识观点列表
            consensus_opinions: 共识观点列表
            
        Returns:
            dict: 可视化数据，包含观点分布、影响力评估等
        """
        # 生成观点分布数据
        opinion_distribution = {
            "total": len(non_consensus_opinions) + sum(c["count"] for c in consensus_opinions),
            "consensus": sum(c["count"] for c in consensus_opinions),
            "non_consensus": len(non_consensus_opinions)
        }
        
        # 生成非共识观点影响力分布
        influence_distribution = {
            "high": 0,
            "medium": 0,
            "low": 0
        }
        for opinion in non_consensus_opinions:
            influence_distribution[opinion["influence_level"]] += 1
        
        # 生成观点类型分布
        type_distribution = {}
        for opinion in non_consensus_opinions:
            if opinion["type"] not in type_distribution:
                type_distribution[opinion["type"]] = 0
            type_distribution[opinion["type"]] += 1
        
        return {
            "opinion_distribution": opinion_distribution,
            "influence_distribution": influence_distribution,
            "type_distribution": type_distribution
        }