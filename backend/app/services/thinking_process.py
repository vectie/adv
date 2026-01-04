class ThinkingProcessService:
    @staticmethod
    def analyze_thinking_process(transcription: list, successful_speakers: list = None) -> dict:
        """分析思考过程
        
        Args:
            transcription: 带有说话人标记的转录结果
            successful_speakers: 成功人士列表（可选）
            
        Returns:
            dict: 思考过程分析结果，包含思维链、因果关系、可视化数据和可模仿的思考框架
        """
        if not successful_speakers:
            successful_speakers = []
        
        # 1. 抽取思维链
        thought_chains = ThinkingProcessService._extract_thought_chains(transcription, successful_speakers)
        
        # 2. 构建因果关系模型
        causal_relations = ThinkingProcessService._build_causal_relations(thought_chains)
        
        # 3. 生成思维模型图谱
        thought_model = ThinkingProcessService._generate_thought_model(thought_chains, causal_relations)
        
        # 4. 总结可模仿的思考框架
        thinking_frameworks = ThinkingProcessService._summarize_thinking_frameworks(thought_chains, thought_model)
        
        # 5. 生成可视化数据
        visualization_data = ThinkingProcessService._generate_visualization(thought_chains, causal_relations, thought_model)
        
        return {
            "status": "success",
            "thinking_process": {
                "thought_chains": thought_chains,
                "causal_relations": causal_relations,
                "thought_model": thought_model,
                "thinking_frameworks": thinking_frameworks
            },
            "visualization": visualization_data
        }
    
    @staticmethod
    def _extract_thought_chains(transcription: list, successful_speakers: list) -> list:
        """抽取思维链
        
        Args:
            transcription: 转录结果
            successful_speakers: 成功人士列表
            
        Returns:
            list: 思维链列表
        """
        thought_chains = []
        
        # 遍历转录文本，提取思维链
        for i, item in enumerate(transcription):
            speaker = item["speaker"]
            text = item["text"]
            
            # 判断是否为成功人士
            is_successful = speaker in successful_speakers
            
            # 提取思维标记词
            if any(marker in text for marker in ["因为", "所以", "因此", "之所以", "由于", "导致", "结果", "从而", "进而", "使得"]):
                # 识别因果关系
                thought_chain = ThinkingProcessService._parse_causal_chain(text, speaker, i, is_successful)
                thought_chains.append(thought_chain)
            elif any(marker in text for marker in ["首先", "其次", "然后", "最后", "第一步", "第二步", "第三步", "首先是", "接下来", "最终"]):
                # 识别步骤关系
                thought_chain = ThinkingProcessService._parse_step_chain(text, speaker, i, is_successful)
                thought_chains.append(thought_chain)
            elif any(marker in text for marker in ["如果", "假设", "假如", "要是", "倘若", "一旦"]):
                # 识别假设关系
                thought_chain = ThinkingProcessService._parse_hypothetical_chain(text, speaker, i, is_successful)
                thought_chains.append(thought_chain)
            elif any(marker in text for marker in ["虽然", "但是", "然而", "不过", "尽管", "可是"]):
                # 识别转折关系
                thought_chain = ThinkingProcessService._parse_contrast_chain(text, speaker, i, is_successful)
                thought_chains.append(thought_chain)
        
        return thought_chains
    
    @staticmethod
    def _parse_causal_chain(text: str, speaker: str, index: int, is_successful: bool) -> dict:
        """解析因果关系思维链
        
        Args:
            text: 文本内容
            speaker: 说话人
            index: 索引
            is_successful: 是否为成功人士
            
        Returns:
            dict: 因果关系思维链
        """
        # 简单实现：提取原因和结果
        causes = []
        effects = []
        
        # 分割因果关系
        if "因为" in text:
            parts = text.split("因为")
            if len(parts) > 1:
                effects.append(parts[0].strip())
                causes.append(parts[1].strip())
        elif "所以" in text:
            parts = text.split("所以")
            if len(parts) > 1:
                causes.append(parts[0].strip())
                effects.append(parts[1].strip())
        elif "因此" in text:
            parts = text.split("因此")
            if len(parts) > 1:
                causes.append(parts[0].strip())
                effects.append(parts[1].strip())
        
        return {
            "id": f"thought_chain_{len(causes) + len(effects) + 1}",
            "speaker": speaker,
            "is_successful": is_successful,
            "type": "causal",
            "content": text,
            "causes": causes,
            "effects": effects,
            "position": index,
            "confidence": 0.8
        }
    
    @staticmethod
    def _parse_step_chain(text: str, speaker: str, index: int, is_successful: bool) -> dict:
        """解析步骤关系思维链
        
        Args:
            text: 文本内容
            speaker: 说话人
            index: 索引
            is_successful: 是否为成功人士
            
        Returns:
            dict: 步骤关系思维链
        """
        # 简单实现：提取步骤
        import re
        
        # 提取步骤标记
        step_markers = re.findall(r"(首先|其次|然后|最后|第一步|第二步|第三步|首先是|接下来|最终)", text)
        
        # 分割步骤
        steps = []
        current_step = 1
        for marker in step_markers:
            if marker in text:
                parts = text.split(marker, 1)
                if len(parts) > 1:
                    steps.append({
                        "step": current_step,
                        "marker": marker,
                        "content": parts[1].strip()
                    })
                    current_step += 1
                    text = parts[1]
        
        return {
            "id": f"thought_chain_{len(steps) + 1}",
            "speaker": speaker,
            "is_successful": is_successful,
            "type": "step",
            "content": text,
            "steps": steps,
            "position": index,
            "confidence": 0.85
        }
    
    @staticmethod
    def _parse_hypothetical_chain(text: str, speaker: str, index: int, is_successful: bool) -> dict:
        """解析假设关系思维链
        
        Args:
            text: 文本内容
            speaker: 说话人
            index: 索引
            is_successful: 是否为成功人士
            
        Returns:
            dict: 假设关系思维链
        """
        # 简单实现：提取假设和结论
        hypotheticals = []
        conclusions = []
        
        if "如果" in text:
            parts = text.split("如果")
            if len(parts) > 1:
                hypothetical_part = parts[1].split("，")[0] if "，" in parts[1] else parts[1]
                conclusion_part = parts[1].split("，")[1] if len(parts[1].split("，")) > 1 else ""
                hypotheticals.append(hypothetical_part.strip())
                conclusions.append(conclusion_part.strip())
        
        return {
            "id": f"thought_chain_{len(hypotheticals) + len(conclusions) + 1}",
            "speaker": speaker,
            "is_successful": is_successful,
            "type": "hypothetical",
            "content": text,
            "hypotheticals": hypotheticals,
            "conclusions": conclusions,
            "position": index,
            "confidence": 0.75
        }
    
    @staticmethod
    def _parse_contrast_chain(text: str, speaker: str, index: int, is_successful: bool) -> dict:
        """解析转折关系思维链
        
        Args:
            text: 文本内容
            speaker: 说话人
            index: 索引
            is_successful: 是否为成功人士
            
        Returns:
            dict: 转折关系思维链
        """
        # 简单实现：提取对比双方
        contrasts = []
        
        if "虽然" in text and "但是" in text:
            parts = text.split("虽然")[1].split("但是")
            if len(parts) == 2:
                contrasts.append({
                    "contrast1": parts[0].strip(),
                    "contrast2": parts[1].strip(),
                    "relation": "转折"
                })
        elif "但是" in text:
            parts = text.split("但是")
            if len(parts) == 2:
                contrasts.append({
                    "contrast1": parts[0].strip(),
                    "contrast2": parts[1].strip(),
                    "relation": "转折"
                })
        
        return {
            "id": f"thought_chain_{len(contrasts) + 1}",
            "speaker": speaker,
            "is_successful": is_successful,
            "type": "contrast",
            "content": text,
            "contrasts": contrasts,
            "position": index,
            "confidence": 0.7
        }
    
    @staticmethod
    def _build_causal_relations(thought_chains: list) -> list:
        """构建因果关系模型
        
        Args:
            thought_chains: 思维链列表
            
        Returns:
            list: 因果关系列表
        """
        causal_relations = []
        relation_id = 1
        
        # 从因果思维链中提取直接因果关系
        for chain in thought_chains:
            if chain["type"] == "causal":
                for cause in chain["causes"]:
                    for effect in chain["effects"]:
                        causal_relations.append({
                            "id": f"causal_{relation_id}",
                            "cause": cause,
                            "effect": effect,
                            "source_chain": chain["id"],
                            "confidence": chain["confidence"],
                            "strength": 0.8
                        })
                        relation_id += 1
        
        # 从步骤思维链中提取间接因果关系
        for chain in thought_chains:
            if chain["type"] == "step" and len(chain["steps"]) > 1:
                for i in range(len(chain["steps"]) - 1):
                    current_step = chain["steps"][i]
                    next_step = chain["steps"][i + 1]
                    causal_relations.append({
                        "id": f"causal_{relation_id}",
                        "cause": current_step["content"],
                        "effect": next_step["content"],
                        "source_chain": chain["id"],
                        "confidence": chain["confidence"] * 0.7,
                        "strength": 0.6
                    })
                    relation_id += 1
        
        # 从假设思维链中提取假设因果关系
        for chain in thought_chains:
            if chain["type"] == "hypothetical":
                for hypothetical in chain["hypotheticals"]:
                    for conclusion in chain["conclusions"]:
                        causal_relations.append({
                            "id": f"causal_{relation_id}",
                            "cause": hypothetical,
                            "effect": conclusion,
                            "source_chain": chain["id"],
                            "confidence": chain["confidence"] * 0.6,
                            "strength": 0.5
                        })
                        relation_id += 1
        
        return causal_relations
    
    @staticmethod
    def _generate_thought_model(thought_chains: list, causal_relations: list) -> dict:
        """生成思维模型图谱
        
        Args:
            thought_chains: 思维链列表
            causal_relations: 因果关系列表
            
        Returns:
            dict: 思维模型图谱
        """
        # 构建节点（概念）
        concepts = {}
        concept_id = 1
        
        # 从因果关系中提取概念
        for relation in causal_relations:
            if relation["cause"] not in concepts:
                concepts[relation["cause"]] = {
                    "id": f"concept_{concept_id}",
                    "name": relation["cause"],
                    "type": "cause",
                    "occurrences": 1,
                    "confidence": relation["confidence"]
                }
                concept_id += 1
            else:
                concepts[relation["cause"]]["occurrences"] += 1
                concepts[relation["cause"]]["confidence"] = max(concepts[relation["cause"]]["confidence"], relation["confidence"])
            
            if relation["effect"] not in concepts:
                concepts[relation["effect"]] = {
                    "id": f"concept_{concept_id}",
                    "name": relation["effect"],
                    "type": "effect",
                    "occurrences": 1,
                    "confidence": relation["confidence"]
                }
                concept_id += 1
            else:
                concepts[relation["effect"]]["occurrences"] += 1
                concepts[relation["effect"]]["confidence"] = max(concepts[relation["effect"]]["confidence"], relation["confidence"])
        
        # 构建边（关系）
        edges = []
        for relation in causal_relations:
            cause_concept = concepts[relation["cause"]]
            effect_concept = concepts[relation["effect"]]
            
            edges.append({
                "id": relation["id"],
                "source": cause_concept["id"],
                "target": effect_concept["id"],
                "type": "causal",
                "strength": relation["strength"],
                "confidence": relation["confidence"],
                "source_chain": relation["source_chain"]
            })
        
        return {
            "concepts": list(concepts.values()),
            "edges": edges,
            "central_concepts": ThinkingProcessService._identify_central_concepts(list(concepts.values()), edges)
        }
    
    @staticmethod
    def _identify_central_concepts(concepts: list, edges: list) -> list:
        """识别中心概念
        
        Args:
            concepts: 概念列表
            edges: 关系列表
            
        Returns:
            list: 中心概念列表
        """
        # 计算概念的度中心性
        concept_degrees = {}
        for concept in concepts:
            concept_degrees[concept["id"]] = 0
        
        for edge in edges:
            concept_degrees[edge["source"]] += 1
            concept_degrees[edge["target"]] += 1
        
        # 按度中心性排序，取前5个
        sorted_concepts = sorted(concepts, key=lambda x: concept_degrees[x["id"]], reverse=True)
        return sorted_concepts[:5]
    
    @staticmethod
    def _summarize_thinking_frameworks(thought_chains: list, thought_model: dict) -> list:
        """总结可模仿的思考框架
        
        Args:
            thought_chains: 思维链列表
            thought_model: 思维模型图谱
            
        Returns:
            list: 可模仿的思考框架列表
        """
        frameworks = []
        
        # 从成功人士的思维链中提取思考框架
        successful_chains = [chain for chain in thought_chains if chain["is_successful"]]
        
        # 提取因果分析框架
        causal_chains = [chain for chain in successful_chains if chain["type"] == "causal"]
        if causal_chains:
            frameworks.append({
                "id": "framework_1",
                "name": "因果分析框架",
                "description": "通过分析事物之间的因果关系，理解问题的本质和发展规律",
                "steps": [
                    "识别问题的根本原因",
                    "分析原因可能产生的各种影响",
                    "验证因果关系的可靠性",
                    "基于因果关系制定解决方案"
                ],
                "example_chains": [chain["id"] for chain in causal_chains[:3]],
                "applicability": "适用于问题分析、决策制定和预测未来趋势"
            })
        
        # 提取步骤规划框架
        step_chains = [chain for chain in successful_chains if chain["type"] == "step"]
        if step_chains:
            frameworks.append({
                "id": "framework_2",
                "name": "步骤规划框架",
                "description": "将复杂问题分解为有序的步骤，逐步解决",
                "steps": [
                    "明确目标和最终结果",
                    "分解为具体、可执行的步骤",
                    "确定步骤之间的依赖关系",
                    "按照顺序执行并调整"
                ],
                "example_chains": [chain["id"] for chain in step_chains[:3]],
                "applicability": "适用于项目管理、任务执行和复杂问题解决"
            })
        
        # 提取假设验证框架
        hypothetical_chains = [chain for chain in successful_chains if chain["type"] == "hypothetical"]
        if hypothetical_chains:
            frameworks.append({
                "id": "framework_3",
                "name": "假设验证框架",
                "description": "通过提出假设并验证，探索问题的多种可能性",
                "steps": [
                    "基于现有信息提出假设",
                    "分析假设成立的条件和影响",
                    "设计验证方法和实验",
                    "根据结果调整或放弃假设"
                ],
                "example_chains": [chain["id"] for chain in hypothetical_chains[:3]],
                "applicability": "适用于创新思考、风险评估和科学研究"
            })
        
        # 提取对比分析框架
        contrast_chains = [chain for chain in successful_chains if chain["type"] == "contrast"]
        if contrast_chains:
            frameworks.append({
                "id": "framework_4",
                "name": "对比分析框架",
                "description": "通过对比不同观点或方案，找出优劣和差异",
                "steps": [
                    "确定对比的维度和标准",
                    "收集不同观点或方案的信息",
                    "进行全面的对比分析",
                    "综合评估并做出选择"
                ],
                "example_chains": [chain["id"] for chain in contrast_chains[:3]],
                "applicability": "适用于决策制定、方案评估和观点分析"
            })
        
        # 从中心概念中提取核心思考模型
        if thought_model["central_concepts"]:
            central_concept_names = [concept["name"] for concept in thought_model["central_concepts"]]
            frameworks.append({
                "id": "framework_5",
                "name": "核心概念模型",
                "description": f"围绕核心概念 {', '.join(central_concept_names[:3])} 构建的思考模型",
                "steps": [
                    f"以{central_concept_names[0]}为核心展开思考",
                    f"关联{central_concept_names[1]}和{central_concept_names[2]}等相关概念",
                    "构建概念之间的关系网络",
                    "基于概念网络进行决策和创新"
                ],
                "example_chains": [chain["id"] for chain in successful_chains[:3]],
                "applicability": "适用于系统思考、创新设计和战略规划"
            })
        
        return frameworks
    
    @staticmethod
    def _generate_visualization(thought_chains: list, causal_relations: list, thought_model: dict) -> dict:
        """生成可视化数据
        
        Args:
            thought_chains: 思维链列表
            causal_relations: 因果关系列表
            thought_model: 思维模型图谱
            
        Returns:
            dict: 可视化数据
        """
        # 生成思维模型网络图数据
        network_data = {
            "nodes": [],
            "edges": []
        }
        
        # 添加概念节点
        for concept in thought_model["concepts"]:
            # 计算节点大小（基于出现次数和置信度）
            node_size = concept["occurrences"] * concept["confidence"]
            
            # 确定节点颜色（基于概念类型）
            node_color = "#3498db"  # 默认蓝色
            if concept["type"] == "cause":
                node_color = "#e74c3c"  # 红色表示原因
            elif concept["type"] == "effect":
                node_color = "#2ecc71"  # 绿色表示结果
            
            network_data["nodes"].append({
                "id": concept["id"],
                "label": concept["name"],
                "type": "concept",
                "size": node_size,
                "color": node_color,
                "occurrences": concept["occurrences"],
                "confidence": concept["confidence"]
            })
        
        # 添加思维链节点
        for chain in thought_chains:
            network_data["nodes"].append({
                "id": chain["id"],
                "label": chain["content"][:30] + "..." if len(chain["content"]) > 30 else chain["content"],
                "type": "thought_chain",
                "size": 5,
                "color": "#f39c12" if chain["is_successful"] else "#95a5a6",
                "chain_type": chain["type"],
                "confidence": chain["confidence"]
            })
        
        # 添加因果关系边
        for relation in causal_relations:
            # 查找对应的概念节点
            cause_concept = next(c for c in thought_model["concepts"] if c["name"] == relation["cause"])
            effect_concept = next(c for c in thought_model["concepts"] if c["name"] == relation["effect"])
            
            network_data["edges"].append({
                "id": relation["id"],
                "source": cause_concept["id"],
                "target": effect_concept["id"],
                "type": "causal",
                "strength": relation["strength"],
                "confidence": relation["confidence"],
                "width": relation["strength"] * 2
            })
        
        # 添加思维链与概念的关联边
        for chain in thought_chains:
            if chain["type"] == "causal":
                for cause in chain["causes"]:
                    cause_concept = next(c for c in thought_model["concepts"] if c["name"] == cause)
                    network_data["edges"].append({
                        "id": f"assoc_{chain['id']}_{cause_concept['id']}",
                        "source": chain["id"],
                        "target": cause_concept["id"],
                        "type": "association",
                        "strength": 0.5,
                        "width": 1,
                        "color": "#95a5a6"
                    })
                for effect in chain["effects"]:
                    effect_concept = next(c for c in thought_model["concepts"] if c["name"] == effect)
                    network_data["edges"].append({
                        "id": f"assoc_{chain['id']}_{effect_concept['id']}",
                        "source": chain["id"],
                        "target": effect_concept["id"],
                        "type": "association",
                        "strength": 0.5,
                        "width": 1,
                        "color": "#95a5a6"
                    })
        
        # 生成思维链类型分布饼图数据
        chain_type_counts = {
            "causal": 0,
            "step": 0,
            "hypothetical": 0,
            "contrast": 0
        }
        
        for chain in thought_chains:
            chain_type_counts[chain["type"]] += 1
        
        pie_data = {
            "labels": ["因果关系", "步骤规划", "假设分析", "对比思考"],
            "values": [
                chain_type_counts["causal"],
                chain_type_counts["step"],
                chain_type_counts["hypothetical"],
                chain_type_counts["contrast"]
            ]
        }
        
        # 生成成功人士与普通人士思维链对比柱状图数据
        successful_vs_normal = {
            "successful": {
                "causal": len([c for c in thought_chains if c["is_successful"] and c["type"] == "causal"]),
                "step": len([c for c in thought_chains if c["is_successful"] and c["type"] == "step"]),
                "hypothetical": len([c for c in thought_chains if c["is_successful"] and c["type"] == "hypothetical"]),
                "contrast": len([c for c in thought_chains if c["is_successful"] and c["type"] == "contrast"])
            },
            "normal": {
                "causal": len([c for c in thought_chains if not c["is_successful"] and c["type"] == "causal"]),
                "step": len([c for c in thought_chains if not c["is_successful"] and c["type"] == "step"]),
                "hypothetical": len([c for c in thought_chains if not c["is_successful"] and c["type"] == "hypothetical"]),
                "contrast": len([c for c in thought_chains if not c["is_successful"] and c["type"] == "contrast"])
            }
        }
        
        bar_data = {
            "categories": ["因果关系", "步骤规划", "假设分析", "对比思考"],
            "series": [
                {
                    "name": "成功人士",
                    "values": [
                        successful_vs_normal["successful"]["causal"],
                        successful_vs_normal["successful"]["step"],
                        successful_vs_normal["successful"]["hypothetical"],
                        successful_vs_normal["successful"]["contrast"]
                    ]
                },
                {
                    "name": "普通人士",
                    "values": [
                        successful_vs_normal["normal"]["causal"],
                        successful_vs_normal["normal"]["step"],
                        successful_vs_normal["normal"]["hypothetical"],
                        successful_vs_normal["normal"]["contrast"]
                    ]
                }
            ]
        }
        
        return {
            "network_graph": network_data,
            "chain_type_distribution": pie_data,
            "successful_vs_normal": bar_data
        }
