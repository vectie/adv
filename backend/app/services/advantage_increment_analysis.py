class AdvantageIncrementAnalysisService:
    @staticmethod
    def analyze_advantages_and_increments(transcription: list, historical_data: dict = None) -> dict:
        """分析优势与增量，识别核心竞争力和个人成长关键点
        
        Args:
            transcription: 带有说话人标记的转录结果
            historical_data: 个人/产品历史数据
            
        Returns:
            dict: 优势与增量分析报告
        """
        # 1. 提取关键概念和主题
        key_concepts = AdvantageIncrementAnalysisService._extract_key_concepts(transcription)
        
        # 2. 分析优势
        advantages = AdvantageIncrementAnalysisService._analyze_advantages(transcription, key_concepts)
        
        # 3. 分析增量机会
        increments = AdvantageIncrementAnalysisService._analyze_increments(transcription, key_concepts, historical_data)
        
        # 4. 生成优势矩阵
        advantage_matrix = AdvantageIncrementAnalysisService._generate_advantage_matrix(advantages, increments)
        
        # 5. 生成可视化数据
        visualization_data = AdvantageIncrementAnalysisService._generate_visualization(key_concepts, advantages, increments)
        
        return {
            "status": "success",
            "analysis": {
                "key_concepts": key_concepts,
                "advantages": advantages,
                "increments": increments,
                "advantage_matrix": advantage_matrix
            },
            "visualization": visualization_data
        }
    
    @staticmethod
    def _extract_key_concepts(transcription: list) -> list:
        """提取转录文本中的关键概念和主题
        
        Args:
            transcription: 带有说话人标记的转录结果
            
        Returns:
            list: 关键概念列表
        """
        # 简单实现：提取高频词汇作为关键概念
        # 实际应用中可以使用更复杂的NLP算法，如主题模型、命名实体识别等
        from collections import Counter
        import re
        
        all_text = " ".join([item["text"] for item in transcription])
        
        # 简单的分词和过滤
        words = re.findall(r"\b\w+\b", all_text)
        filtered_words = [word for word in words if len(word) > 2]
        
        # 计算词频
        word_counts = Counter(filtered_words)
        
        # 提取前20个高频词作为关键概念
        key_concepts = []
        for word, count in word_counts.most_common(20):
            key_concepts.append({
                "concept": word,
                "frequency": count,
                "importance": round(count / len(words), 4)
            })
        
        return key_concepts
    
    @staticmethod
    def _analyze_advantages(transcription: list, key_concepts: list) -> list:
        """分析优势
        
        Args:
            transcription: 带有说话人标记的转录结果
            key_concepts: 关键概念列表
            
        Returns:
            list: 优势分析结果
        """
        # 简单实现：基于关键概念在不同角色中的出现频率分析优势
        advantages = []
        
        # 统计不同说话人对每个关键概念的提及情况
        speaker_concepts = {}
        for item in transcription:
            speaker = item["speaker"]
            if speaker not in speaker_concepts:
                speaker_concepts[speaker] = {}
            
            for concept in key_concepts:
                if concept["concept"] in item["text"]:
                    if concept["concept"] not in speaker_concepts[speaker]:
                        speaker_concepts[speaker][concept["concept"]] = 0
                    speaker_concepts[speaker][concept["concept"]] += 1
        
        # 分析每个说话人的优势
        for speaker, concepts in speaker_concepts.items():
            # 找出该说话人最常提及的前5个概念作为优势
            sorted_concepts = sorted(concepts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for concept, count in sorted_concepts:
                # 计算优势强度（相对于其他说话人）
                strength = AdvantageIncrementAnalysisService._calculate_advantage_strength(
                    speaker, concept, speaker_concepts
                )
                
                advantages.append({
                    "speaker": speaker,
                    "concept": concept,
                    "strength": strength,
                    "mention_count": count,
                    "type": AdvantageIncrementAnalysisService._get_advantage_type(concept),
                    "description": AdvantageIncrementAnalysisService._get_advantage_description(concept)
                })
        
        return advantages
    
    @staticmethod
    def _calculate_advantage_strength(speaker: str, concept: str, speaker_concepts: dict) -> float:
        """计算优势强度
        
        Args:
            speaker: 说话人
            concept: 概念
            speaker_concepts: 说话人概念提及情况
            
        Returns:
            float: 优势强度（0-1）
        """
        # 简单实现：该说话人提及次数 / 所有说话人提及总次数
        total_count = 0
        for s, concepts in speaker_concepts.items():
            if concept in concepts:
                total_count += concepts[concept]
        
        if total_count == 0:
            return 0.0
        
        return round(speaker_concepts[speaker][concept] / total_count, 4)
    
    @staticmethod
    def _get_advantage_type(concept: str) -> str:
        """获取优势类型
        
        Args:
            concept: 概念
            
        Returns:
            str: 优势类型
        """
        # 简单实现：根据关键词判断优势类型
        technical_keywords = ["技术", "算法", "系统", "架构", "代码", "开发"]
        business_keywords = ["市场", "业务", "产品", "销售", "用户", "运营"]
        management_keywords = ["管理", "团队", "项目", "流程", "战略", "领导力"]
        
        for keyword in technical_keywords:
            if keyword in concept:
                return "技术优势"
        
        for keyword in business_keywords:
            if keyword in concept:
                return "业务优势"
        
        for keyword in management_keywords:
            if keyword in concept:
                return "管理优势"
        
        return "综合优势"
    
    @staticmethod
    def _get_advantage_description(concept: str) -> str:
        """获取优势描述
        
        Args:
            concept: 概念
            
        Returns:
            str: 优势描述
        """
        descriptions = {
            "技术": "在技术领域拥有深厚的知识和经验，能够解决复杂的技术问题",
            "市场": "对市场有深刻的理解，能够准确把握市场需求和趋势",
            "产品": "擅长产品设计和开发，能够创造出满足用户需求的产品",
            "团队": "具备优秀的团队管理能力，能够带领团队高效协作",
            "战略": "拥有清晰的战略思维，能够制定有效的长期规划",
            "创新": "具备创新思维，能够提出独特的观点和解决方案"
        }
        
        for key, desc in descriptions.items():
            if key in concept:
                return desc
        
        return f"在{concept}领域表现出色，具备较强的竞争力"
    
    @staticmethod
    def _analyze_increments(transcription: list, key_concepts: list, historical_data: dict = None) -> list:
        """分析增量机会
        
        Args:
            transcription: 带有说话人标记的转录结果
            key_concepts: 关键概念列表
            historical_data: 个人/产品历史数据
            
        Returns:
            list: 增量机会分析结果
        """
        increments = []
        
        # 简单实现：基于关键概念的增长潜力和市场需求分析增量机会
        for concept in key_concepts:
            # 计算增长潜力（基于概念的新颖性和重要性）
            growth_potential = AdvantageIncrementAnalysisService._calculate_growth_potential(concept)
            
            # 分析市场需求
            market_demand = AdvantageIncrementAnalysisService._analyze_market_demand(concept)
            
            # 评估个人契合度
            personal_fit = AdvantageIncrementAnalysisService._evaluate_personal_fit(concept, historical_data)
            
            # 计算综合得分
            composite_score = (growth_potential + market_demand + personal_fit) / 3
            
            increments.append({
                "concept": concept["concept"],
                "growth_potential": growth_potential,
                "market_demand": market_demand,
                "personal_fit": personal_fit,
                "composite_score": round(composite_score, 4),
                "type": AdvantageIncrementAnalysisService._get_increment_type(concept["concept"]),
                "description": AdvantageIncrementAnalysisService._get_increment_description(concept["concept"]),
                "actionable_steps": AdvantageIncrementAnalysisService._generate_actionable_steps(concept["concept"])
            })
        
        # 按综合得分排序
        increments.sort(key=lambda x: x["composite_score"], reverse=True)
        
        return increments
    
    @staticmethod
    def _calculate_growth_potential(concept: dict) -> float:
        """计算增长潜力
        
        Args:
            concept: 概念
            
        Returns:
            float: 增长潜力（0-1）
        """
        # 简单实现：基于概念的重要性和新颖性计算增长潜力
        # 实际应用中可以结合趋势数据、搜索量等指标
        return concept["importance"] * 0.7 + (1 - concept["frequency"] / 100) * 0.3
    
    @staticmethod
    def _analyze_market_demand(concept: str) -> float:
        """分析市场需求
        
        Args:
            concept: 概念
            
        Returns:
            float: 市场需求（0-1）
        """
        # 简单实现：基于关键词判断市场需求
        high_demand_keywords = ["人工智能", "大数据", "云原生", "区块链", "元宇宙", "可持续发展", "新能源"]
        medium_demand_keywords = ["管理", "营销", "设计", "用户体验", "数据分析", "产品经理"]
        
        for keyword in high_demand_keywords:
            if keyword in concept:
                return 0.9
        
        for keyword in medium_demand_keywords:
            if keyword in concept:
                return 0.7
        
        return 0.5
    
    @staticmethod
    def _evaluate_personal_fit(concept: str, historical_data: dict = None) -> float:
        """评估个人契合度
        
        Args:
            concept: 概念
            historical_data: 个人/产品历史数据
            
        Returns:
            float: 个人契合度（0-1）
        """
        if not historical_data:
            return 0.5
        
        # 简单实现：基于历史数据中的相关经验评估契合度
        if "experience" in historical_data:
            for exp in historical_data["experience"]:
                if concept in exp.get("description", ""):
                    return 0.8
        
        if "skills" in historical_data:
            if concept in historical_data["skills"]:
                return 0.7
        
        return 0.5
    
    @staticmethod
    def _get_increment_type(concept: str) -> str:
        """获取增量类型
        
        Args:
            concept: 概念
            
        Returns:
            str: 增量类型
        """
        # 简单实现：根据关键词判断增量类型
        technical_increments = ["技术", "算法", "系统", "架构", "代码", "开发"]
        business_increments = ["市场", "业务", "产品", "销售", "用户", "运营"]
        personal_increments = ["学习", "成长", "能力", "思维", "认知", "习惯"]
        
        for keyword in technical_increments:
            if keyword in concept:
                return "技术增量"
        
        for keyword in business_increments:
            if keyword in concept:
                return "业务增量"
        
        for keyword in personal_increments:
            if keyword in concept:
                return "个人成长增量"
        
        return "综合增量"
    
    @staticmethod
    def _get_increment_description(concept: str) -> str:
        """获取增量描述
        
        Args:
            concept: 概念
            
        Returns:
            str: 增量描述
        """
        return f"在{concept}领域有较大的增长空间，值得重点投入"
    
    @staticmethod
    def _generate_actionable_steps(concept: str) -> list:
        """生成可行动的步骤
        
        Args:
            concept: 概念
            
        Returns:
            list: 可行动的步骤
        """
        return [
            f"深入学习{concept}领域的基础知识",
            f"关注{concept}领域的最新趋势和发展动态",
            f"寻找{concept}领域的实践机会",
            f"与{concept}领域的专家交流和学习",
            f"制定{concept}领域的学习计划和目标"
        ]
    
    @staticmethod
    def _generate_advantage_matrix(advantages: list, increments: list) -> dict:
        """生成优势矩阵
        
        Args:
            advantages: 优势分析结果
            increments: 增量机会分析结果
            
        Returns:
            dict: 优势矩阵
        """
        # 简单实现：生成二维矩阵，行是优势，列是增量机会
        advantage_concepts = list(set([adv["concept"] for adv in advantages]))
        increment_concepts = [inc["concept"] for inc in increments[:10]]  # 取前10个增量机会
        
        matrix = []
        for advantage in advantage_concepts:
            row = {
                "advantage": advantage,
                "matches": []
            }
            
            for increment in increment_concepts:
                # 简单实现：如果优势概念和增量概念相关，则匹配度为1，否则为0
                match_score = 1.0 if advantage in increment or increment in advantage else 0.0
                row["matches"].append({
                    "increment": increment,
                    "match_score": match_score
                })
            
            matrix.append(row)
        
        return {
            "advantage_concepts": advantage_concepts,
            "increment_concepts": increment_concepts,
            "matrix": matrix
        }
    
    @staticmethod
    def _generate_visualization(key_concepts: list, advantages: list, increments: list) -> dict:
        """生成可视化数据
        
        Args:
            key_concepts: 关键概念列表
            advantages: 优势分析结果
            increments: 增量机会分析结果
            
        Returns:
            dict: 可视化数据
        """
        # 生成优势雷达图数据
        advantage_radar = AdvantageIncrementAnalysisService._generate_advantage_radar(advantages)
        
        # 生成增量柱状图数据
        increment_bar = AdvantageIncrementAnalysisService._generate_increment_bar(increments)
        
        # 生成优势矩阵热力图数据
        matrix_heatmap = AdvantageIncrementAnalysisService._generate_matrix_heatmap(advantages, increments)
        
        return {
            "radar_chart": advantage_radar,
            "bar_chart": increment_bar,
            "heatmap": matrix_heatmap
        }
    
    @staticmethod
    def _generate_advantage_radar(advantages: list) -> dict:
        """生成优势雷达图数据
        
        Args:
            advantages: 优势分析结果
            
        Returns:
            dict: 优势雷达图数据
        """
        # 简单实现：按优势类型分组统计
        technical_advantages = [adv for adv in advantages if adv["type"] == "技术优势"]
        business_advantages = [adv for adv in advantages if adv["type"] == "业务优势"]
        management_advantages = [adv for adv in advantages if adv["type"] == "管理优势"]
        
        return {
            "categories": ["技术优势", "业务优势", "管理优势", "综合优势"],
            "values": [
                len(technical_advantages) / 5 if technical_advantages else 0,
                len(business_advantages) / 5 if business_advantages else 0,
                len(management_advantages) / 5 if management_advantages else 0,
                len([adv for adv in advantages if adv["type"] == "综合优势"]) / 5
            ]
        }
    
    @staticmethod
    def _generate_increment_bar(increments: list) -> dict:
        """生成增量柱状图数据
        
        Args:
            increments: 增量机会分析结果
            
        Returns:
            dict: 增量柱状图数据
        """
        # 取前10个增量机会
        top_increments = increments[:10]
        
        return {
            "categories": [inc["concept"] for inc in top_increments],
            "values": [inc["composite_score"] for inc in top_increments]
        }
    
    @staticmethod
    def _generate_matrix_heatmap(advantages: list, increments: list) -> dict:
        """生成优势矩阵热力图数据
        
        Args:
            advantages: 优势分析结果
            increments: 增量机会分析结果
            
        Returns:
            dict: 优势矩阵热力图数据
        """
        # 取前5个优势和前5个增量机会
        top_advantages = list(set([adv["concept"] for adv in advantages]))[:5]
        top_increments = [inc["concept"] for inc in increments[:5]]
        
        heatmap_data = []
        for advantage in top_advantages:
            for increment in top_increments:
                # 简单实现：计算匹配度
                match_score = 1.0 if advantage in increment or increment in advantage else 0.0
                heatmap_data.append({
                    "advantage": advantage,
                    "increment": increment,
                    "value": match_score
                })
        
        return {
            "advantages": top_advantages,
            "increments": top_increments,
            "data": heatmap_data
        }
