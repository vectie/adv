class ActionableAdviceService:
    @staticmethod
    def generate_advice(transcription: list, analysis_results: dict = None, user_goals: list = None) -> dict:
        """生成可行动的建议
        
        Args:
            transcription: 带有说话人标记的转录结果
            analysis_results: 其他分析模块的结果，如优势分析、增量分析等
            user_goals: 用户目标列表
            
        Returns:
            dict: 可行动的建议，包含时间线和优先级
        """
        if not analysis_results:
            analysis_results = {}
        
        if not user_goals:
            user_goals = []
        
        # 1. 提取关键洞察
        key_insights = ActionableAdviceService._extract_key_insights(transcription, analysis_results)
        
        # 2. 生成建议选项
        advice_options = ActionableAdviceService._generate_advice_options(key_insights, user_goals)
        
        # 3. 优先级排序
        prioritized_advice = ActionableAdviceService._prioritize_advice(advice_options)
        
        # 4. 生成时间线
        timeline = ActionableAdviceService._generate_timeline(prioritized_advice)
        
        # 5. 生成资源建议
        resources = ActionableAdviceService._generate_resource_suggestions(prioritized_advice)
        
        # 6. 生成可视化数据
        visualization_data = ActionableAdviceService._generate_visualization(prioritized_advice, timeline)
        
        return {
            "status": "success",
            "advice": {
                "key_insights": key_insights,
                "prioritized_advice": prioritized_advice,
                "timeline": timeline,
                "resources": resources
            },
            "visualization": visualization_data
        }
    
    @staticmethod
    def _extract_key_insights(transcription: list, analysis_results: dict) -> list:
        """提取关键洞察
        
        Args:
            transcription: 带有说话人标记的转录结果
            analysis_results: 其他分析模块的结果
            
        Returns:
            list: 关键洞察列表
        """
        insights = []
        
        # 从转录文本中提取关键洞察
        all_text = " ".join([item["text"] for item in transcription])
        
        # 示例：提取包含"建议"、"应该"、"需要"等关键词的句子
        import re
        sentences = re.split(r'[。！？；]', all_text)
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence for keyword in ["建议", "应该", "需要", "必须", "可以", "最好", "推荐"]):
                insights.append({
                    "type": "direct_advice",
                    "content": sentence,
                    "source": "transcription",
                    "confidence": 0.8
                })
        
        # 从优势分析结果中提取洞察
        if "advantages" in analysis_results:
            for advantage in analysis_results["advantages"]:
                insights.append({
                    "type": "strength",
                    "content": f"您在{advantage['concept']}方面具有优势，可以进一步发挥",
                    "source": "advantage_analysis",
                    "confidence": 0.9
                })
        
        # 从增量分析结果中提取洞察
        if "increments" in analysis_results:
            for increment in analysis_results["increments"][:5]:  # 取前5个增量机会
                insights.append({
                    "type": "opportunity",
                    "content": f"{increment['concept']}领域有较大增长空间，建议重点关注",
                    "source": "increment_analysis",
                    "confidence": increment["composite_score"]
                })
        
        # 从角色扮演分析结果中提取洞察
        if "role_play" in analysis_results:
            ecological_niches = analysis_results["role_play"].get("ecological_niches", [])
            for niche in ecological_niches:
                insights.append({
                    "type": "role_insight",
                    "content": f"{niche['participant_name']}在生态系统中扮演{niche['niche_type']}角色，您可以学习其{', '.join(niche['key_attributes'])}等属性",
                    "source": "role_play_analysis",
                    "confidence": 0.85
                })
        
        # 从未来预测结果中提取洞察
        if "future_prediction" in analysis_results:
            predictions = analysis_results["future_prediction"].get("predictions", [])
            for prediction in predictions:
                insights.append({
                    "type": "future_trend",
                    "content": f"未来{prediction['timeframe']}内，{prediction['trend']}，建议{prediction['suggestion']}",
                    "source": "future_prediction",
                    "confidence": prediction["confidence"]
                })
        
        # 从非共识观点中提取洞察
        if "non_consensus" in analysis_results:
            non_consensus_opinions = analysis_results["non_consensus"].get("non_consensus_opinions", [])
            for opinion in non_consensus_opinions:
                insights.append({
                    "type": "non_consensus",
                    "content": f"非共识观点：{opinion['content']}，这可能是一个突破点",
                    "source": "non_consensus_analysis",
                    "confidence": opinion["confidence"]
                })
        
        return insights
    
    @staticmethod
    def _generate_advice_options(key_insights: list, user_goals: list) -> list:
        """生成建议选项
        
        Args:
            key_insights: 关键洞察列表
            user_goals: 用户目标列表
            
        Returns:
            list: 建议选项列表
        """
        advice_options = []
        
        # 为每个关键洞察生成具体建议
        for insight in key_insights:
            if insight["type"] == "direct_advice":
                # 直接建议转换为可行动项
                advice_options.append({
                    "id": f"advice_{len(advice_options) + 1}",
                    "title": insight["content"].split("：")[-1] if "：" in insight["content"] else insight["content"],
                    "description": insight["content"],
                    "type": "action",
                    "source_insight": insight["id"] if "id" in insight else f"insight_{key_insights.index(insight) + 1}",
                    "confidence": insight["confidence"],
                    "estimated_effort": ActionableAdviceService._estimate_effort(insight["content"]),
                    "potential_impact": ActionableAdviceService._estimate_impact(insight["content"]),
                    "required_skills": ActionableAdviceService._identify_required_skills(insight["content"]),
                    "steps": ActionableAdviceService._break_down_into_steps(insight["content"])
                })
            elif insight["type"] == "strength":
                # 基于优势的建议
                advice_options.append({
                    "id": f"advice_{len(advice_options) + 1}",
                    "title": f"发挥{insight['content'].split('在')[-1].split('方面')[0]}优势",
                    "description": insight["content"],
                    "type": "development",
                    "source_insight": insight["id"] if "id" in insight else f"insight_{key_insights.index(insight) + 1}",
                    "confidence": insight["confidence"],
                    "estimated_effort": 3,
                    "potential_impact": 4,
                    "required_skills": [insight['content'].split('在')[-1].split('方面')[0]],
                    "steps": [
                        f"评估当前{insight['content'].split('在')[-1].split('方面')[0]}能力水平",
                        "设定具体的提升目标",
                        "寻找相关的实践机会",
                        "定期回顾和调整"
                    ]
                })
            elif insight["type"] == "opportunity":
                # 基于机会的建议
                concept = insight["content"].split('：')[-1].split('领域')[0]
                advice_options.append({
                    "id": f"advice_{len(advice_options) + 1}",
                    "title": f"探索{concept}领域机会",
                    "description": insight["content"],
                    "type": "exploration",
                    "source_insight": insight["id"] if "id" in insight else f"insight_{key_insights.index(insight) + 1}",
                    "confidence": insight["confidence"],
                    "estimated_effort": 4,
                    "potential_impact": 5,
                    "required_skills": [concept, "市场分析", "趋势判断"],
                    "steps": [
                        f"深入研究{concept}领域的现状和趋势",
                        "识别该领域的关键玩家和机会点",
                        "制定进入或合作策略",
                        "开始小规模试点"
                    ]
                })
            elif insight["type"] == "role_insight":
                # 基于角色洞察的建议
                role = insight["content"].split('扮演')[-1].split('角色')[0]
                attributes = insight["content"].split('学习其')[-1].split('等属性')[0]
                advice_options.append({
                    "id": f"advice_{len(advice_options) + 1}",
                    "title": f"学习{role}角色的{attributes}",
                    "description": insight["content"],
                    "type": "learning",
                    "source_insight": insight["id"] if "id" in insight else f"insight_{key_insights.index(insight) + 1}",
                    "confidence": insight["confidence"],
                    "estimated_effort": 3,
                    "potential_impact": 4,
                    "required_skills": ["观察学习", "自我反思"],
                    "steps": [
                        f"分析{role}角色的行为模式",
                        "学习和实践{attributes}",
                        "在实际场景中应用",
                        "寻求反馈和改进"
                    ]
                })
            elif insight["type"] == "future_trend":
                # 基于未来趋势的建议
                trend = insight["content"].split('内，')[-1].split('，建议')[0]
                suggestion = insight["content"].split('建议')[-1]
                advice_options.append({
                    "id": f"advice_{len(advice_options) + 1}",
                    "title": f"应对{trend}趋势",
                    "description": insight["content"],
                    "type": "strategy",
                    "source_insight": insight["id"] if "id" in insight else f"insight_{key_insights.index(insight) + 1}",
                    "confidence": insight["confidence"],
                    "estimated_effort": 5,
                    "potential_impact": 5,
                    "required_skills": ["战略规划", "风险评估"],
                    "steps": [
                        f"深入分析{trend}趋势的影响",
                        "制定应对策略和预案",
                        "分阶段实施",
                        "持续监控和调整"
                    ]
                })
            elif insight["type"] == "non_consensus":
                # 基于非共识观点的建议
                opinion = insight["content"].split('：')[-1].split('，这可能')[0]
                advice_options.append({
                    "id": f"advice_{len(advice_options) + 1}",
                    "title": f"探索非共识观点：{opinion[:20]}...",
                    "description": insight["content"],
                    "type": "innovation",
                    "source_insight": insight["id"] if "id" in insight else f"insight_{key_insights.index(insight) + 1}",
                    "confidence": insight["confidence"],
                    "estimated_effort": 4,
                    "potential_impact": 5,
                    "required_skills": ["批判性思维", "创新能力"],
                    "steps": [
                        f"深入研究{opinion}观点的依据",
                        "分析其与主流观点的差异",
                        "验证该观点的可行性",
                        "考虑如何应用或调整"
                    ]
                })
        
        # 根据用户目标调整建议
        for goal in user_goals:
            # 为每个目标生成特定建议
            advice_options.append({
                "id": f"advice_{len(advice_options) + 1}",
                "title": f"实现目标：{goal}",
                "description": f"针对您的目标 '{goal}' 生成的定制建议",
                "type": "goal_oriented",
                "source_insight": f"goal_{user_goals.index(goal) + 1}",
                "confidence": 0.9,
                "estimated_effort": 4,
                "potential_impact": 5,
                "required_skills": ["目标管理", "执行力"],
                "steps": [
                    f"将目标 '{goal}' 分解为具体的子目标",
                    "为每个子目标设定可衡量的指标",
                    "制定详细的行动计划",
                    "定期检查进度并调整"
                ]
            })
        
        return advice_options
    
    @staticmethod
    def _prioritize_advice(advice_options: list) -> list:
        """优先级排序建议
        
        Args:
            advice_options: 建议选项列表
            
        Returns:
            list: 按优先级排序的建议
        """
        # 使用RICE评分模型进行优先级排序
        # RICE = (Reach * Impact * Confidence) / Effort
        for advice in advice_options:
            # 计算Reach（影响范围）- 这里简化为基于建议类型
            reach = 10
            if advice["type"] == "action":
                reach = 8
            elif advice["type"] == "development":
                reach = 6
            elif advice["type"] == "exploration":
                reach = 7
            elif advice["type"] == "learning":
                reach = 5
            elif advice["type"] == "strategy":
                reach = 10
            elif advice["type"] == "innovation":
                reach = 9
            elif advice["type"] == "goal_oriented":
                reach = 10
            
            # Impact（影响程度）- 已经估算
            impact = advice["potential_impact"]
            
            # Confidence（置信度）- 已经计算
            confidence = advice["confidence"]
            
            # Effort（所需努力）- 已经估算
            effort = advice["estimated_effort"] if advice["estimated_effort"] > 0 else 1
            
            # 计算RICE分数
            rice_score = (reach * impact * confidence) / effort
            
            # 确定优先级
            priority = "low"
            if rice_score >= 20:
                priority = "high"
            elif rice_score >= 10:
                priority = "medium"
            
            advice["rice_score"] = round(rice_score, 2)
            advice["priority"] = priority
        
        # 按RICE分数降序排序
        prioritized_advice = sorted(advice_options, key=lambda x: x["rice_score"], reverse=True)
        
        # 添加排名
        for i, advice in enumerate(prioritized_advice):
            advice["rank"] = i + 1
        
        return prioritized_advice
    
    @staticmethod
    def _generate_timeline(prioritized_advice: list) -> dict:
        """生成时间线
        
        Args:
            prioritized_advice: 按优先级排序的建议
            
        Returns:
            dict: 时间线数据
        """
        # 简单实现：将建议分配到短期（1-2周）、中期（3-8周）、长期（9-24周）
        timeline = {
            "short_term": [],  # 1-2周
            "medium_term": [],  # 3-8周
            "long_term": []  # 9-24周
        }
        
        for advice in prioritized_advice:
            # 根据优先级和努力程度分配时间阶段
            if advice["priority"] == "high" and advice["estimated_effort"] <= 3:
                timeline["short_term"].append(advice["id"])
            elif advice["priority"] == "high" or (advice["priority"] == "medium" and advice["estimated_effort"] <= 4):
                timeline["medium_term"].append(advice["id"])
            else:
                timeline["long_term"].append(advice["id"])
        
        # 生成具体的时间线视图
        timeline_view = {
            "phases": [
                {
                    "name": "短期目标（1-2周）",
                    "duration": "1-2周",
                    "advice_ids": timeline["short_term"],
                    "total_effort": sum(advice["estimated_effort"] for advice in prioritized_advice if advice["id"] in timeline["short_term"])
                },
                {
                    "name": "中期目标（3-8周）",
                    "duration": "3-8周",
                    "advice_ids": timeline["medium_term"],
                    "total_effort": sum(advice["estimated_effort"] for advice in prioritized_advice if advice["id"] in timeline["medium_term"])
                },
                {
                    "name": "长期目标（9-24周）",
                    "duration": "9-24周",
                    "advice_ids": timeline["long_term"],
                    "total_effort": sum(advice["estimated_effort"] for advice in prioritized_advice if advice["id"] in timeline["long_term"])
                }
            ]
        }
        
        return timeline_view
    
    @staticmethod
    def _generate_resource_suggestions(prioritized_advice: list) -> list:
        """生成资源建议
        
        Args:
            prioritized_advice: 按优先级排序的建议
            
        Returns:
            list: 资源建议列表
        """
        resources = []
        
        # 基于建议的技能要求生成资源建议
        all_skills = set()
        for advice in prioritized_advice:
            all_skills.update(advice["required_skills"])
        
        for skill in all_skills:
            resources.append({
                "skill": skill,
                "suggestions": [
                    f"阅读关于{skill}的专业书籍",
                    f"参加{skill}相关的在线课程",
                    f"寻找{skill}领域的导师",
                    f"加入{skill}相关的社区或论坛",
                    f"实践{skill}并寻求反馈"
                ]
            })
        
        return resources
    
    @staticmethod
    def _extract_key_insights(transcription: list, analysis_results: dict) -> list:
        """提取关键洞察
        
        Args:
            transcription: 带有说话人标记的转录结果
            analysis_results: 其他分析模块的结果
            
        Returns:
            list: 关键洞察列表
        """
        # 这里简单实现，实际应用中可以使用更复杂的NLP算法
        insights = []
        
        # 从转录文本中提取关键句子
        all_text = " ".join([item["text"] for item in transcription])
        
        # 示例：提取包含"重要"、"关键"、"核心"等关键词的句子
        import re
        sentences = re.split(r'[。！？；]', all_text)
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence for keyword in ["重要", "关键", "核心", "本质", "根本", "关键是", "最重要的是"]):
                insights.append({
                    "id": f"insight_{len(insights) + 1}",
                    "type": "key_point",
                    "content": sentence,
                    "source": "transcription",
                    "confidence": 0.8
                })
        
        # 从分析结果中添加洞察
        if "advantages" in analysis_results:
            for advantage in analysis_results["advantages"]:
                insights.append({
                    "id": f"insight_{len(insights) + 1}",
                    "type": "strength",
                    "content": f"优势：{advantage['concept']}",
                    "source": "advantage_analysis",
                    "confidence": advantage["strength"]
                })
        
        if "increments" in analysis_results:
            for increment in analysis_results["increments"][:3]:
                insights.append({
                    "id": f"insight_{len(insights) + 1}",
                    "type": "opportunity",
                    "content": f"机会：{increment['concept']}",
                    "source": "increment_analysis",
                    "confidence": increment["composite_score"]
                })
        
        return insights
    
    @staticmethod
    def _estimate_effort(content: str) -> int:
        """估算所需努力
        
        Args:
            content: 建议内容
            
        Returns:
            int: 努力程度（1-5）
        """
        # 简单实现：基于内容长度和关键词估算
        if len(content) < 50:
            return 1
        elif len(content) < 100:
            return 2
        elif any(keyword in content for keyword in ["深入", "全面", "系统", "长期"]):
            return 5
        elif any(keyword in content for keyword in ["详细", "完整", "复杂"]):
            return 4
        else:
            return 3
    
    @staticmethod
    def _estimate_impact(content: str) -> int:
        """估算潜在影响
        
        Args:
            content: 建议内容
            
        Returns:
            int: 影响程度（1-5）
        """
        # 简单实现：基于关键词估算
        if any(keyword in content for keyword in ["战略", "长期", "根本", "核心"]):
            return 5
        elif any(keyword in content for keyword in ["重要", "关键", "显著"]):
            return 4
        elif any(keyword in content for keyword in ["有益", "有帮助", "改进"]):
            return 3
        else:
            return 2
    
    @staticmethod
    def _identify_required_skills(content: str) -> list:
        """识别所需技能
        
        Args:
            content: 建议内容
            
        Returns:
            list: 所需技能列表
        """
        # 简单实现：基于关键词识别
        skills = []
        
        skill_keywords = {
            "学习": ["学习", "研究", "阅读", "课程"],
            "分析": ["分析", "评估", "研究", "调研"],
            "实践": ["实践", "应用", "实施", "执行"],
            "创新": ["创新", "创意", "突破", "新颖"],
            "沟通": ["沟通", "交流", "表达", "演讲"],
            "管理": ["管理", "规划", "组织", "协调"],
            "技术": ["技术", "开发", "编程", "工程"]
        }
        
        for skill, keywords in skill_keywords.items():
            if any(keyword in content for keyword in keywords):
                skills.append(skill)
        
        return skills
    
    @staticmethod
    def _break_down_into_steps(content: str) -> list:
        """将建议分解为具体步骤
        
        Args:
            content: 建议内容
            
        Returns:
            list: 具体步骤列表
        """
        # 简单实现：生成通用的步骤模板
        return [
            "理解建议的核心内容和目标",
            "收集相关信息和资源",
            "制定详细的行动计划",
            "开始执行并记录过程",
            "定期评估和调整"
        ]
    
    @staticmethod
    def _generate_visualization(prioritized_advice: list, timeline: dict) -> dict:
        """生成可视化数据
        
        Args:
            prioritized_advice: 按优先级排序的建议
            timeline: 时间线数据
            
        Returns:
            dict: 可视化数据
        """
        # 生成优先级分布饼图数据
        priority_distribution = {
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for advice in prioritized_advice:
            priority_distribution[advice["priority"]] += 1
        
        pie_data = {
            "labels": ["高优先级", "中优先级", "低优先级"],
            "values": [priority_distribution["high"], priority_distribution["medium"], priority_distribution["low"]]
        }
        
        # 生成RICE分数柱状图数据
        top_10_advice = prioritized_advice[:10]
        bar_data = {
            "categories": [advice["title"] for advice in top_10_advice],
            "values": [advice["rice_score"] for advice in top_10_advice]
        }
        
        # 生成时间线甘特图数据
        gantt_data = {
            "tasks": [],
            "phases": [
                {
                    "name": "短期目标（1-2周）",
                    "start": 0,
                    "end": 2
                },
                {
                    "name": "中期目标（3-8周）",
                    "start": 3,
                    "end": 8
                },
                {
                    "name": "长期目标（9-24周）",
                    "start": 9,
                    "end": 24
                }
            ]
        }
        
        for phase in timeline["phases"]:
            for advice_id in phase["advice_ids"]:
                advice = next(a for a in prioritized_advice if a["id"] == advice_id)
                gantt_data["tasks"].append({
                    "id": advice_id,
                    "name": advice["title"],
                    "phase": phase["name"],
                    "priority": advice["priority"],
                    "estimated_effort": advice["estimated_effort"]
                })
        
        return {
            "priority_distribution": pie_data,
            "rice_scores": bar_data,
            "timeline_gantt": gantt_data
        }
