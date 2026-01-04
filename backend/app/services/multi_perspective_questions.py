class MultiPerspectiveQuestionsService:
    @staticmethod
    def generate_questions(transcription: list, analysis_results: dict = None, topic: str = None) -> dict:
        """从多个视角生成关键问题
        
        Args:
            transcription: 带有说话人标记的转录结果
            analysis_results: 其他分析模块的结果
            topic: 特定主题（可选）
            
        Returns:
            dict: 从5个不同视角生成的关键问题
        """
        if not analysis_results:
            analysis_results = {}
        
        # 1. 提取核心主题
        core_topics = MultiPerspectiveQuestionsService._extract_core_topics(transcription, topic)
        
        # 2. 从5个视角生成问题
        perspectives = [
            "customer",      # 客户视角
            "competitor",    # 竞争对手视角
            "investor",      # 投资者视角
            "expert",        # 行业专家视角
            "future_user"    # 未来用户视角
        ]
        
        questions = {}
        for perspective in perspectives:
            questions[perspective] = MultiPerspectiveQuestionsService._generate_questions_from_perspective(
                perspective, core_topics, transcription, analysis_results
            )
        
        # 3. 评估问题质量
        questions_with_quality = MultiPerspectiveQuestionsService._evaluate_question_quality(questions)
        
        # 4. 生成可视化数据
        visualization_data = MultiPerspectiveQuestionsService._generate_visualization(questions_with_quality)
        
        return {
            "status": "success",
            "questions": questions_with_quality,
            "core_topics": core_topics,
            "visualization": visualization_data
        }
    
    @staticmethod
    def _extract_core_topics(transcription: list, topic: str = None) -> list:
        """提取核心主题
        
        Args:
            transcription: 带有说话人标记的转录结果
            topic: 特定主题（可选）
            
        Returns:
            list: 核心主题列表
        """
        core_topics = []
        
        if topic:
            # 如果指定了主题，直接添加
            core_topics.append({
                "topic": topic,
                "importance": 1.0,
                "source": "user_defined"
            })
        
        # 从转录文本中提取主题
        all_text = " ".join([item["text"] for item in transcription])
        
        # 简单实现：提取高频关键词作为主题
        from collections import Counter
        import re
        
        words = re.findall(r"\b\w+\b", all_text)
        filtered_words = [word for word in words if len(word) > 2]
        word_counts = Counter(filtered_words)
        
        # 提取前10个高频词作为潜在主题
        for word, count in word_counts.most_common(10):
            if word not in [topic["topic"] for topic in core_topics]:
                core_topics.append({
                    "topic": word,
                    "importance": round(count / len(filtered_words), 4),
                    "source": "transcription"
                })
        
        # 从分析结果中添加主题
        if "key_concepts" in analysis_results:
            for concept in analysis_results["key_concepts"]:
                if isinstance(concept, dict) and "concept" in concept:
                    concept_name = concept["concept"]
                else:
                    concept_name = str(concept)
                    
                if concept_name not in [topic["topic"] for topic in core_topics]:
                    core_topics.append({
                        "topic": concept_name,
                        "importance": concept.get("importance", 0.8) if isinstance(concept, dict) else 0.8,
                        "source": "analysis_results"
                    })
        
        # 按重要性排序
        core_topics.sort(key=lambda x: x["importance"], reverse=True)
        
        # 只保留前5个核心主题
        return core_topics[:5]
    
    @staticmethod
    def _generate_questions_from_perspective(perspective: str, core_topics: list, transcription: list, analysis_results: dict) -> list:
        """从特定视角生成问题
        
        Args:
            perspective: 视角类型
            core_topics: 核心主题列表
            transcription: 转录结果
            analysis_results: 分析结果
            
        Returns:
            list: 从该视角生成的问题列表
        """
        questions = []
        
        # 根据不同视角生成问题模板
        perspective_templates = {
            "customer": [
                "从用户角度来看，{topic}能解决什么具体问题？",
                "用户在使用{topic}时可能会遇到哪些痛点？",
                "{topic}如何提升用户的体验和满意度？",
                "用户最看重{topic}的哪些特性？",
                "{topic}是否符合用户的真实需求？"
            ],
            "competitor": [
                "竞争对手如何看待和评价{topic}？",
                "{topic}与竞争对手相比有哪些优势和劣势？",
                "竞争对手可能会如何应对{topic}的挑战？",
                "{topic}在市场竞争中的定位是什么？",
                "竞争对手的成功经验对{topic}有什么借鉴意义？"
            ],
            "investor": [
                "{topic}的商业价值和投资潜力是什么？",
                "{topic}的盈利模式是什么？",
                "{topic}的市场规模和增长空间有多大？",
                "投资{topic}存在哪些风险和机遇？",
                "{topic}的长期发展前景如何？"
            ],
            "expert": [
                "从行业专家的角度来看，{topic}的技术可行性如何？",
                "{topic}对行业的影响和变革是什么？",
                "{topic}符合行业发展的大趋势吗？",
                "{topic}存在哪些技术瓶颈和挑战？",
                "{topic}的创新点和突破点是什么？"
            ],
            "future_user": [
                "未来5-10年，用户对{topic}的需求会发生什么变化？",
                "{topic}如何适应未来用户的需求？",
                "未来用户会如何评价和使用{topic}？",
                "{topic}在未来的应用场景有哪些？",
                "技术发展会如何改变{topic}的形态和功能？"
            ]
        }
        
        # 获取该视角的模板
        templates = perspective_templates.get(perspective, [])
        
        # 为每个核心主题生成问题
        for topic in core_topics:
            topic_name = topic["topic"]
            
            for template in templates:
                # 填充模板生成问题
                question = template.format(topic=topic_name)
                
                # 计算问题与主题的相关性
                relevance = MultiPerspectiveQuestionsService._calculate_question_relevance(question, topic_name, transcription)
                
                questions.append({
                    "question": question,
                    "topic": topic_name,
                    "topic_importance": topic["importance"],
                    "relevance": relevance,
                    "template": template,
                    "source": perspective
                })
        
        # 每个视角只保留前5个最相关的问题
        questions.sort(key=lambda x: x["relevance"], reverse=True)
        return questions[:5]
    
    @staticmethod
    def _calculate_question_relevance(question: str, topic: str, transcription: list) -> float:
        """计算问题与主题的相关性
        
        Args:
            question: 问题
            topic: 主题
            transcription: 转录结果
            
        Returns:
            float: 相关性得分（0-1）
        """
        # 简单实现：基于关键词匹配计算相关性
        all_text = " ".join([item["text"] for item in transcription])
        
        # 计算问题中包含的主题关键词数量
        question_lower = question.lower()
        topic_lower = topic.lower()
        
        relevance = 0.0
        
        # 完全匹配
        if topic_lower in question_lower:
            relevance += 0.5
        
        # 计算主题在转录文本中的出现频率
        topic_count = all_text.lower().count(topic_lower)
        total_words = len(all_text.split())
        if total_words > 0:
            relevance += (topic_count / total_words) * 0.5
        
        return round(min(relevance, 1.0), 4)
    
    @staticmethod
    def _evaluate_question_quality(questions: dict) -> dict:
        """评估问题质量
        
        Args:
            questions: 从不同视角生成的问题
            
        Returns:
            dict: 包含质量评估的问题
        """
        questions_with_quality = {}
        
        for perspective, perspective_questions in questions.items():
            evaluated_questions = []
            
            for question in perspective_questions:
                # 计算问题质量得分
                # 质量 = 相关性 * 0.6 + 主题重要性 * 0.4
                quality = (question["relevance"] * 0.6) + (question["topic_importance"] * 0.4)
                
                # 确定问题类型
                question_type = MultiPerspectiveQuestionsService._classify_question_type(question["question"])
                
                evaluated_questions.append({
                    **question,
                    "quality": round(quality, 4),
                    "question_type": question_type
                })
            
            # 按质量排序
            evaluated_questions.sort(key=lambda x: x["quality"], reverse=True)
            questions_with_quality[perspective] = evaluated_questions
        
        return questions_with_quality
    
    @staticmethod
    def _classify_question_type(question: str) -> str:
        """分类问题类型
        
        Args:
            question: 问题
            
        Returns:
            str: 问题类型
        """
        # 根据问题关键词分类
        if any(keyword in question for keyword in ["什么", "哪些", "哪", "谁", "多少"]):
            return "what"
        elif any(keyword in question for keyword in ["如何", "怎么", "怎样", "如何"]):
            return "how"
        elif any(keyword in question for keyword in ["为什么", "为何", "原因", "理由"]):
            return "why"
        elif any(keyword in question for keyword in ["是否", "是不是", "能否", "会不会"]):
            return "yes_no"
        else:
            return "other"
    
    @staticmethod
    def _generate_visualization(questions: dict) -> dict:
        """生成可视化数据
        
        Args:
            questions: 包含质量评估的问题
            
        Returns:
            dict: 可视化数据
        """
        # 生成视角分布饼图数据
        perspective_counts = {
            "customer": len(questions.get("customer", [])),
            "competitor": len(questions.get("competitor", [])),
            "investor": len(questions.get("investor", [])),
            "expert": len(questions.get("expert", [])),
            "future_user": len(questions.get("future_user", []))
        }
        
        pie_data = {
            "labels": ["客户视角", "竞争对手视角", "投资者视角", "行业专家视角", "未来用户视角"],
            "values": [
                perspective_counts["customer"],
                perspective_counts["competitor"],
                perspective_counts["investor"],
                perspective_counts["expert"],
                perspective_counts["future_user"]
            ]
        }
        
        # 生成问题质量柱状图数据
        quality_data = {}
        for perspective, perspective_questions in questions.items():
            avg_quality = sum(q["quality"] for q in perspective_questions) / len(perspective_questions) if perspective_questions else 0
            quality_data[perspective] = round(avg_quality, 4)
        
        bar_data = {
            "labels": ["客户视角", "竞争对手视角", "投资者视角", "行业专家视角", "未来用户视角"],
            "values": [
                quality_data["customer"],
                quality_data["competitor"],
                quality_data["investor"],
                quality_data["expert"],
                quality_data["future_user"]
            ]
        }
        
        # 生成问题类型分布数据
        question_type_counts = {
            "what": 0,
            "how": 0,
            "why": 0,
            "yes_no": 0,
            "other": 0
        }
        
        for perspective_questions in questions.values():
            for question in perspective_questions:
                question_type_counts[question["question_type"]] += 1
        
        type_data = {
            "labels": ["是什么", "如何", "为什么", "是否", "其他"],
            "values": [
                question_type_counts["what"],
                question_type_counts["how"],
                question_type_counts["why"],
                question_type_counts["yes_no"],
                question_type_counts["other"]
            ]
        }
        
        return {
            "perspective_distribution": pie_data,
            "quality_by_perspective": bar_data,
            "question_type_distribution": type_data
        }
