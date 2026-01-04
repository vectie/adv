class RolePlayAnalysisService:
    @staticmethod
    def analyze_ecological_niche(transcription: list, user_background: dict = None) -> dict:
        """分析生态位，理解参与者角色和关系，评估自身定位
        
        Args:
            transcription: 带有说话人标记的转录结果
            user_background: 用户背景信息
            
        Returns:
            dict: 生态位分析报告，包含角色关系图、参与者定位、用户定位建议等
        """
        # 1. 提取参与者和关系
        participants = RolePlayAnalysisService._extract_participants(transcription)
        relationships = RolePlayAnalysisService._extract_relationships(transcription, participants)
        
        # 2. 分析生态位
        ecological_niches = RolePlayAnalysisService._analyze_niches(participants, relationships)
        
        # 3. 评估用户定位
        user_positioning = RolePlayAnalysisService._evaluate_user_positioning(
            ecological_niches, 
            user_background
        )
        
        # 4. 生成可视化数据
        visualization_data = RolePlayAnalysisService._generate_visualization(
            participants, 
            relationships, 
            ecological_niches
        )
        
        return {
            "status": "success",
            "analysis": {
                "participants": participants,
                "relationships": relationships,
                "ecological_niches": ecological_niches,
                "user_positioning": user_positioning
            },
            "visualization": visualization_data
        }
    
    @staticmethod
    def _extract_participants(transcription: list) -> list:
        """提取参与者
        
        Args:
            transcription: 带有说话人标记的转录结果
            
        Returns:
            list: 参与者列表
        """
        participants = []
        speaker_set = set()
        
        # 提取所有不同的说话人
        for item in transcription:
            speaker = item["speaker"]
            if speaker not in speaker_set:
                speaker_set.add(speaker)
                participants.append({
                    "id": len(participants) + 1,
                    "name": speaker,
                    "type": "主持人" if speaker == "主持人" else "嘉宾",
                    "speaking_time": 0,
                    "influence_score": 0.0
                })
        
        # 计算说话时间（简单实现：按句子数量计算）
        for item in transcription:
            speaker = item["speaker"]
            for participant in participants:
                if participant["name"] == speaker:
                    participant["speaking_time"] += 1
        
        # 计算影响力分数（简单实现：基于说话时间）
        total_speaking_time = sum(p["speaking_time"] for p in participants)
        for participant in participants:
            participant["influence_score"] = round(participant["speaking_time"] / total_speaking_time, 2)
        
        return participants
    
    @staticmethod
    def _extract_relationships(transcription: list, participants: list) -> list:
        """提取参与者之间的关系
        
        Args:
            transcription: 带有说话人标记的转录结果
            participants: 参与者列表
            
        Returns:
            list: 关系列表
        """
        relationships = []
        relationship_set = set()
        
        # 简单实现：基于对话顺序提取关系
        for i in range(len(transcription) - 1):
            current_speaker = transcription[i]["speaker"]
            next_speaker = transcription[i+1]["speaker"]
            
            # 跳过同一说话人的连续发言
            if current_speaker == next_speaker:
                continue
            
            # 避免重复关系
            relationship_key = f"{current_speaker}->{next_speaker}"
            if relationship_key not in relationship_set:
                relationship_set.add(relationship_key)
                
                # 查找参与者ID
                current_id = next(p["id"] for p in participants if p["name"] == current_speaker)
                next_id = next(p["id"] for p in participants if p["name"] == next_speaker)
                
                relationships.append({
                    "id": len(relationships) + 1,
                    "source": current_id,
                    "target": next_id,
                    "type": "对话",
                    "strength": 1.0
                })
        
        return relationships
    
    @staticmethod
    def _analyze_niches(participants: list, relationships: list) -> list:
        """分析生态位
        
        Args:
            participants: 参与者列表
            relationships: 关系列表
            
        Returns:
            list: 生态位分析结果
        """
        niches = []
        
        for participant in participants:
            # 简单实现：基于影响力和角色类型分析生态位
            niche_type = ""
            if participant["type"] == "主持人":
                niche_type = "引导者"
            elif participant["influence_score"] > 0.5:
                niche_type = "主导者"
            elif participant["influence_score"] > 0.3:
                niche_type = "合作者"
            else:
                niche_type = "跟随者"
            
            niches.append({
                "participant_id": participant["id"],
                "participant_name": participant["name"],
                "niche_type": niche_type,
                "description": RolePlayAnalysisService._get_niche_description(niche_type),
                "influence_score": participant["influence_score"],
                "key_attributes": RolePlayAnalysisService._get_key_attributes(niche_type)
            })
        
        return niches
    
    @staticmethod
    def _get_niche_description(niche_type: str) -> str:
        """获取生态位描述
        
        Args:
            niche_type: 生态位类型
            
        Returns:
            str: 生态位描述
        """
        descriptions = {
            "引导者": "负责引导对话流程，控制话题走向，确保各方观点得到充分表达",
            "主导者": "在对话中占据主导地位，提供主要观点和方向，影响其他参与者",
            "合作者": "积极参与对话，提供有价值的观点和反馈，与其他参与者协作",
            "跟随者": "在对话中主要倾听和学习，较少主动提供观点，跟随其他参与者的思路"
        }
        
        return descriptions.get(niche_type, "")
    
    @staticmethod
    def _get_key_attributes(niche_type: str) -> list:
        """获取生态位关键属性
        
        Args:
            niche_type: 生态位类型
            
        Returns:
            list: 关键属性列表
        """
        attributes = {
            "引导者": ["沟通能力", "组织能力", "倾听能力", "中立性"],
            "主导者": ["专业知识", "说服力", "领导力", "创新性"],
            "合作者": ["协作能力", "分析能力", "适应性", "贡献精神"],
            "跟随者": ["学习能力", "倾听能力", "适应性", "执行力"]
        }
        
        return attributes.get(niche_type, [])
    
    @staticmethod
    def _evaluate_user_positioning(ecological_niches: list, user_background: dict = None) -> dict:
        """评估用户定位
        
        Args:
            ecological_niches: 生态位分析结果
            user_background: 用户背景信息
            
        Returns:
            dict: 用户定位评估结果
        """
        # 简单实现：基于用户背景和生态位分析提供定位建议
        if not user_background:
            user_background = {}
        
        # 确定用户最适合的生态位
        # 这里使用简单的规则，实际应用中可以使用更复杂的算法
        suitable_niche = "跟随者"
        if "经验丰富" in user_background.get("description", "") or user_background.get("expertise_level", "") == "高级":
            suitable_niche = "主导者"
        elif "擅长沟通" in user_background.get("description", "") or (user_background.get("skills", []) and "沟通" in user_background["skills"]):
            suitable_niche = "引导者"
        elif "团队协作" in user_background.get("description", "") or (user_background.get("skills", []) and "协作" in user_background["skills"]):
            suitable_niche = "合作者"
        
        return {
            "suitable_niche": suitable_niche,
            "reasoning": "基于您的背景和生态系统分析，建议您定位为{}".format(suitable_niche),
            "development_suggestions": RolePlayAnalysisService._get_development_suggestions(suitable_niche),
            "key_attributes_to_develop": RolePlayAnalysisService._get_key_attributes(suitable_niche)
        }
    
    @staticmethod
    def _get_development_suggestions(niche_type: str) -> list:
        """获取发展建议
        
        Args:
            niche_type: 生态位类型
            
        Returns:
            list: 发展建议列表
        """
        suggestions = {
            "引导者": [
                "提升对话引导技巧，学会更好地控制话题走向",
                "增强倾听能力，确保各方观点得到充分表达",
                "保持中立性，避免过度影响对话结果",
                "学习如何平衡不同参与者的发言时间"
            ],
            "主导者": [
                "深化专业知识，保持行业领先地位",
                "提升说服力和演讲技巧",
                "学会倾听和整合他人观点",
                "培养创新思维，提供独特价值"
            ],
            "合作者": [
                "增强协作能力，学会团队工作",
                "提升分析能力，提供有深度的见解",
                "培养适应性，应对不同的对话场景",
                "学会主动贡献，增加在对话中的影响力"
            ],
            "跟随者": [
                "培养主动学习意识，吸收他人经验",
                "提升倾听和总结能力",
                "逐步增加在对话中的参与度",
                "发展一两项核心技能，建立自己的独特价值"
            ]
        }
        
        return suggestions.get(niche_type, [])
    
    @staticmethod
    def _generate_visualization(participants: list, relationships: list, ecological_niches: list) -> dict:
        """生成可视化数据
        
        Args:
            participants: 参与者列表
            relationships: 关系列表
            ecological_niches: 生态位分析结果
            
        Returns:
            dict: 可视化数据，包含节点和连线
        """
        nodes = []
        edges = []
        
        # 添加参与者节点
        for participant in participants:
            # 查找对应的生态位
            niche = next(n for n in ecological_niches if n["participant_id"] == participant["id"])
            
            nodes.append({
                "id": f"participant_{participant['id']}",
                "label": participant["name"],
                "type": "participant",
                "niche_type": niche["niche_type"],
                "influence_score": participant["influence_score"],
                "speaking_time": participant["speaking_time"]
            })
        
        # 添加关系连线
        for relationship in relationships:
            edges.append({
                "source": f"participant_{relationship['source']}",
                "target": f"participant_{relationship['target']}",
                "type": relationship["type"],
                "strength": relationship["strength"]
            })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "layout": "force-directed"  # 力导向布局
        }