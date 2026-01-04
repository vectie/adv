class MarketBenchmarkService:
    @staticmethod
    def benchmark_against_market(transcription: list, product_info: dict = None, financial_data: dict = None) -> dict:
        """基于市场数据进行基准测试
        
        Args:
            transcription: 带有说话人标记的转录结果
            product_info: 产品/服务信息
            financial_data: 金融市场数据（可选）
            
        Returns:
            dict: 市场基准测试结果，包含市场对比报告、竞争力排名和可视化数据
        """
        if not product_info:
            product_info = {}
        
        if not financial_data:
            financial_data = MarketBenchmarkService._get_mock_financial_data()
        
        # 1. 提取关键概念和主题
        key_concepts = MarketBenchmarkService._extract_key_concepts(transcription)
        
        # 2. 分析市场相关性
        market_relevance = MarketBenchmarkService._analyze_market_relevance(key_concepts, financial_data)
        
        # 3. 计算竞争力排名
        competitive_ranking = MarketBenchmarkService._calculate_competitive_ranking(product_info, financial_data)
        
        # 4. 生成市场对比报告
        market_comparison = MarketBenchmarkService._generate_market_comparison(market_relevance, competitive_ranking)
        
        # 5. 结合预测市场数据进行验证
        prediction_market_validation = MarketBenchmarkService._validate_with_prediction_market(key_concepts, financial_data)
        
        # 6. 生成可视化数据
        visualization_data = MarketBenchmarkService._generate_visualization(market_relevance, competitive_ranking, market_comparison)
        
        return {
            "status": "success",
            "benchmark": {
                "key_concepts": key_concepts,
                "market_relevance": market_relevance,
                "competitive_ranking": competitive_ranking,
                "market_comparison": market_comparison,
                "prediction_market_validation": prediction_market_validation
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
    def _analyze_market_relevance(key_concepts: list, financial_data: dict) -> list:
        """分析市场相关性
        
        Args:
            key_concepts: 关键概念列表
            financial_data: 金融市场数据
            
        Returns:
            list: 市场相关性分析结果
        """
        market_relevance = []
        
        # 遍历关键概念，分析每个概念与市场的相关性
        for concept in key_concepts:
            concept_lower = concept["concept"].lower()
            relevance_score = 0.0
            
            # 检查概念与行业关键词的匹配
            industry_keywords = ["技术", "市场", "产品", "销售", "用户", "增长", "创新", "竞争", "趋势", "策略", "投资", "收益", "风险", "回报", "估值"]
            for keyword in industry_keywords:
                if keyword in concept_lower:
                    relevance_score += 0.2
                    break
            
            # 检查概念与金融指标的相关性
            financial_metrics = ["市值", "股价", "营收", "利润", "增长率", "市盈率", "市销率", "市净率", "ROE", "ROA", "利润率", "负债率"]
            for metric in financial_metrics:
                if metric in concept_lower:
                    relevance_score += 0.3
                    break
            
            # 计算概念在市场中的重要性
            market_importance = MarketBenchmarkService._calculate_market_importance(concept_lower, financial_data)
            relevance_score += market_importance * 0.5
            
            # 限制相关性分数在0-1之间
            relevance_score = min(1.0, max(0.0, relevance_score))
            
            market_relevance.append({
                "concept": concept["concept"],
                "relevance_score": round(relevance_score, 4),
                "market_importance": round(market_importance, 4),
                "industry_relevance": round(relevance_score - market_importance * 0.5, 4),
                "description": MarketBenchmarkService._get_relevance_description(relevance_score)
            })
        
        # 按相关性分数排序
        market_relevance.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return market_relevance
    
    @staticmethod
    def _calculate_market_importance(concept: str, financial_data: dict) -> float:
        """计算概念在市场中的重要性
        
        Args:
            concept: 概念
            financial_data: 金融市场数据
            
        Returns:
            float: 市场重要性分数（0-1）
        """
        # 简单实现：基于概念与金融数据的匹配程度计算重要性
        importance = 0.0
        
        # 检查概念在行业板块中的出现
        for sector in financial_data.get("sectors", []):
            if concept in sector["name"].lower() or concept in sector["description"].lower():
                importance += 0.2
                break
        
        # 检查概念在股票数据中的出现
        for stock in financial_data.get("stocks", []):
            if concept in stock["name"].lower() or concept in stock["ticker"].lower():
                importance += 0.1
        
        # 检查概念在市场趋势中的出现
        for trend in financial_data.get("market_trends", []):
            if concept in trend["name"].lower() or concept in trend["description"].lower():
                importance += 0.3
                break
        
        return min(1.0, importance)
    
    @staticmethod
    def _calculate_competitive_ranking(product_info: dict, financial_data: dict) -> dict:
        """计算竞争力排名
        
        Args:
            product_info: 产品/服务信息
            financial_data: 金融市场数据
            
        Returns:
            dict: 竞争力排名结果
        """
        # 简单实现：基于产品信息和市场数据计算竞争力分数
        # 实际应用中可以结合更多维度和数据源
        
        # 提取相关行业板块
        relevant_sectors = []
        product_name = product_info.get("name", "").lower()
        
        for sector in financial_data.get("sectors", []):
            if any(keyword in product_name for keyword in [sector["name"].lower(), sector["description"].lower()]):
                relevant_sectors.append(sector)
        
        if not relevant_sectors:
            relevant_sectors = financial_data.get("sectors", [])[:3]
        
        # 计算竞争力分数
        competitive_score = 0.0
        
        # 基于市场规模计算
        total_market_size = sum(sector["market_size"] for sector in relevant_sectors)
        if total_market_size > 0:
            competitive_score += 0.3
        
        # 基于增长潜力计算
        avg_growth_rate = sum(sector["growth_rate"] for sector in relevant_sectors) / len(relevant_sectors)
        competitive_score += min(1.0, avg_growth_rate / 0.2) * 0.4
        
        # 基于竞争强度计算
        avg_competition = sum(sector["competition_level"] for sector in relevant_sectors) / len(relevant_sectors)
        competitive_score += (1 - min(1.0, avg_competition / 10)) * 0.3
        
        # 生成排名
        ranking = {
            "score": round(competitive_score, 4),
            "percentile": round(min(100, competitive_score * 100), 2),
            "relevant_sectors": relevant_sectors,
            "ranking_position": MarketBenchmarkService._get_ranking_position(competitive_score),
            "comparison_metrics": {
                "market_size": total_market_size,
                "growth_rate": avg_growth_rate,
                "competition_level": avg_competition
            }
        }
        
        return ranking
    
    @staticmethod
    def _get_ranking_position(score: float) -> str:
        """获取排名位置
        
        Args:
            score: 竞争力分数
            
        Returns:
            str: 排名位置描述
        """
        if score >= 0.8:
            return "行业领先"
        elif score >= 0.6:
            return "行业前列"
        elif score >= 0.4:
            return "行业中游"
        elif score >= 0.2:
            return "行业后进"
        else:
            return "需要改进"
    
    @staticmethod
    def _generate_market_comparison(market_relevance: list, competitive_ranking: dict) -> dict:
        """生成市场对比报告
        
        Args:
            market_relevance: 市场相关性分析结果
            competitive_ranking: 竞争力排名结果
            
        Returns:
            dict: 市场对比报告
        """
        # 提取高相关性概念
        high_relevance_concepts = [concept for concept in market_relevance if concept["relevance_score"] >= 0.7]
        medium_relevance_concepts = [concept for concept in market_relevance if 0.4 <= concept["relevance_score"] < 0.7]
        low_relevance_concepts = [concept for concept in market_relevance if concept["relevance_score"] < 0.4]
        
        # 生成优势和劣势分析
        strengths = []
        weaknesses = []
        opportunities = []
        threats = []
        
        # 基于相关性分析生成SWOT
        for sector in competitive_ranking["relevant_sectors"]:
            if sector["growth_rate"] > 0.15:
                opportunities.append(f"{sector['name']}行业增长迅速，增长率达到{sector['growth_rate']*100:.1f}%")
            
            if sector["competition_level"] < 5:
                opportunities.append(f"{sector['name']}行业竞争强度较低，有较大市场空间")
            else:
                threats.append(f"{sector['name']}行业竞争激烈，需要差异化竞争")
            
            if sector["profit_margin"] > 0.2:
                strengths.append(f"{sector['name']}行业利润率较高，盈利能力强")
            else:
                weaknesses.append(f"{sector['name']}行业利润率较低，盈利压力大")
        
        return {
            "relevance_summary": {
                "high_relevance_count": len(high_relevance_concepts),
                "medium_relevance_count": len(medium_relevance_concepts),
                "low_relevance_count": len(low_relevance_concepts),
                "total_concepts": len(market_relevance)
            },
            "swot_analysis": {
                "strengths": strengths[:5],
                "weaknesses": weaknesses[:5],
                "opportunities": opportunities[:5],
                "threats": threats[:5]
            },
            "competitive_position": competitive_ranking["ranking_position"],
            "market_size": competitive_ranking["comparison_metrics"]["market_size"],
            "growth_rate": competitive_ranking["comparison_metrics"]["growth_rate"],
            "competition_level": competitive_ranking["comparison_metrics"]["competition_level"]
        }
    
    @staticmethod
    def _validate_with_prediction_market(key_concepts: list, financial_data: dict) -> dict:
        """结合预测市场数据进行验证
        
        Args:
            key_concepts: 关键概念列表
            financial_data: 金融市场数据
            
        Returns:
            dict: 预测市场验证结果
        """
        # 简单实现：基于预测市场数据验证关键概念
        # 实际应用中可以集成Polymarket等预测市场API
        
        prediction_market_data = financial_data.get("prediction_market", [])
        
        validation_results = []
        
        for concept in key_concepts[:10]:  # 取前10个关键概念
            concept_lower = concept["concept"].lower()
            matching_predictions = []
            
            for prediction in prediction_market_data:
                if concept_lower in prediction["question"].lower():
                    matching_predictions.append(prediction)
            
            if matching_predictions:
                # 计算平均置信度
                avg_confidence = sum(pred["confidence"] for pred in matching_predictions) / len(matching_predictions)
                
                validation_results.append({
                    "concept": concept["concept"],
                    "matching_predictions": matching_predictions,
                    "avg_confidence": round(avg_confidence, 4),
                    "validation_status": "validated" if avg_confidence >= 0.6 else "needs_further_validation"
                })
        
        return {
            "validation_results": validation_results,
            "total_validated_concepts": len([res for res in validation_results if res["validation_status"] == "validated"]),
            "total_concepts_checked": len(validation_results),
            "prediction_market_summary": {
                "total_predictions": len(prediction_market_data),
                "avg_prediction_confidence": sum(pred["confidence"] for pred in prediction_market_data) / len(prediction_market_data) if prediction_market_data else 0
            }
        }
    
    @staticmethod
    def _generate_visualization(market_relevance: list, competitive_ranking: dict, market_comparison: dict) -> dict:
        """生成可视化数据
        
        Args:
            market_relevance: 市场相关性分析结果
            competitive_ranking: 竞争力排名结果
            market_comparison: 市场对比报告
            
        Returns:
            dict: 可视化数据
        """
        # 生成相关性分布柱状图数据
        relevance_data = {
            "categories": ["高相关性", "中相关性", "低相关性"],
            "values": [
                market_comparison["relevance_summary"]["high_relevance_count"],
                market_comparison["relevance_summary"]["medium_relevance_count"],
                market_comparison["relevance_summary"]["low_relevance_count"]
            ]
        }
        
        # 生成竞争力雷达图数据
        radar_data = {
            "categories": ["市场规模", "增长潜力", "竞争强度", "盈利能力"],
            "values": [
                0.8 if competitive_ranking["comparison_metrics"]["market_size"] > 1000000000 else 0.5,
                min(1.0, competitive_ranking["comparison_metrics"]["growth_rate"] / 0.2),
                1.0 - min(1.0, competitive_ranking["comparison_metrics"]["competition_level"] / 10),
                0.7  # 模拟盈利能力
            ]
        }
        
        # 生成SWOT分析表格数据
        swot_data = {
            "columns": [
                {"id": "type", "label": "类型", "type": "string"},
                {"id": "description", "label": "描述", "type": "string"}
            ],
            "rows": []
        }
        
        for strength in market_comparison["swot_analysis"]["strengths"]:
            swot_data["rows"].append({"type": "优势", "description": strength})
        
        for weakness in market_comparison["swot_analysis"]["weaknesses"]:
            swot_data["rows"].append({"type": "劣势", "description": weakness})
        
        for opportunity in market_comparison["swot_analysis"]["opportunities"]:
            swot_data["rows"].append({"type": "机会", "description": opportunity})
        
        for threat in market_comparison["swot_analysis"]["threats"]:
            swot_data["rows"].append({"type": "威胁", "description": threat})
        
        return {
            "relevance_distribution": relevance_data,
            "competitive_radar": radar_data,
            "swot_analysis": swot_data,
            "competitive_score": {
                "score": competitive_ranking["score"],
                "percentile": competitive_ranking["percentile"]
            }
        }
    
    @staticmethod
    def _get_mock_financial_data() -> dict:
        """获取模拟金融数据
        
        Returns:
            dict: 模拟金融市场数据
        """
        return {
            "sectors": [
                {
                    "id": "tech",
                    "name": "科技",
                    "description": "科技行业包括软件开发、硬件制造、人工智能等领域",
                    "market_size": 1000000000000,
                    "growth_rate": 0.15,
                    "competition_level": 8,
                    "profit_margin": 0.25
                },
                {
                    "id": "finance",
                    "name": "金融",
                    "description": "金融行业包括银行、保险、投资等领域",
                    "market_size": 1500000000000,
                    "growth_rate": 0.08,
                    "competition_level": 7,
                    "profit_margin": 0.20
                },
                {
                    "id": "healthcare",
                    "name": "医疗健康",
                    "description": "医疗健康行业包括制药、医疗设备、医疗服务等领域",
                    "market_size": 800000000000,
                    "growth_rate": 0.12,
                    "competition_level": 6,
                    "profit_margin": 0.30
                }
            ],
            "stocks": [
                {
                    "ticker": "AAPL",
                    "name": "苹果公司",
                    "sector": "tech",
                    "market_cap": 2500000000000,
                    "price": 180,
                    "pe_ratio": 28,
                    "growth_rate": 0.10
                },
                {
                    "ticker": "MSFT",
                    "name": "微软公司",
                    "sector": "tech",
                    "market_cap": 2200000000000,
                    "price": 370,
                    "pe_ratio": 32,
                    "growth_rate": 0.15
                },
                {
                    "ticker": "JPM",
                    "name": "摩根大通",
                    "sector": "finance",
                    "market_cap": 450000000000,
                    "price": 150,
                    "pe_ratio": 12,
                    "growth_rate": 0.07
                }
            ],
            "market_trends": [
                {
                    "id": "ai_growth",
                    "name": "人工智能增长",
                    "description": "人工智能技术在各行业的应用不断扩大，市场规模持续增长",
                    "growth_rate": 0.30,
                    "confidence": 0.85
                },
                {
                    "id": "cloud_adoption",
                    "name": "云计算普及",
                    "description": "企业和个人对云计算服务的需求持续增长",
                    "growth_rate": 0.20,
                    "confidence": 0.90
                },
                {
                    "id": "remote_work",
                    "name": "远程工作趋势",
                    "description": "远程工作模式成为常态，相关技术和服务需求增长",
                    "growth_rate": 0.15,
                    "confidence": 0.75
                }
            ],
            "prediction_market": [
                {
                    "id": "pred_1",
                    "question": "人工智能技术在未来5年内会成为主流吗？",
                    "yes_probability": 0.85,
                    "no_probability": 0.15,
                    "confidence": 0.85,
                    "expiration_date": "2028-12-31"
                },
                {
                    "id": "pred_2",
                    "question": "云计算市场规模会在2025年突破1万亿美元吗？",
                    "yes_probability": 0.75,
                    "no_probability": 0.25,
                    "confidence": 0.80,
                    "expiration_date": "2025-12-31"
                },
                {
                    "id": "pred_3",
                    "question": "远程工作会成为大多数企业的标准选项吗？",
                    "yes_probability": 0.70,
                    "no_probability": 0.30,
                    "confidence": 0.75,
                    "expiration_date": "2026-12-31"
                }
            ]
        }
    
    @staticmethod
    def _get_relevance_description(relevance_score: float) -> str:
        """获取相关性描述
        
        Args:
            relevance_score: 相关性分数
            
        Returns:
            str: 相关性描述
        """
        if relevance_score >= 0.8:
            return "与市场高度相关，对市场分析有重要价值"
        elif relevance_score >= 0.6:
            return "与市场中度相关，对市场分析有一定价值"
        elif relevance_score >= 0.4:
            return "与市场低度相关，对市场分析价值有限"
        else:
            return "与市场相关性较低，对市场分析价值较小"
