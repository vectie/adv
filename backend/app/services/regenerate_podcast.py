from typing import List, Dict, Any
from app.services.visualization_service import VisualizationService

class RegeneratePodcastService:
    """再生Podcast服务类"""
    
    @staticmethod
    def regenerate_podcast(transcription: list, improvements: dict = None) -> dict:
        """
        基于原Podcast内容生成改进版本
        
        Args:
            transcription: 原转录文本列表
            improvements: 改进建议，包含需要优化的方面
            
        Returns:
            优化后的Podcast脚本和改进建议
        """
        # 分析原内容
        original_analysis = RegeneratePodcastService._analyze_original_content(transcription)
        
        # 生成改进建议
        if not improvements:
            improvements = RegeneratePodcastService._generate_improvement_suggestions(original_analysis)
        
        # 生成优化后的脚本
        optimized_script = RegeneratePodcastService._generate_optimized_script(transcription, improvements)
        
        # 生成内容迭代循环建议
        iteration_loop = RegeneratePodcastService._generate_iteration_loop(original_analysis, improvements)
        
        # 生成可视化
        visualization_data = RegeneratePodcastService._generate_visualizations(original_analysis, improvements)
        
        return {
            "original_analysis": original_analysis,
            "improvements": improvements,
            "optimized_script": optimized_script,
            "iteration_loop": iteration_loop,
            "visualizations": visualization_data
        }
    
    @staticmethod
    def _analyze_original_content(transcription: list) -> dict:
        """分析原Podcast内容"""
        # 统计基本信息
        total_duration = len(transcription) * 5  # 假设每个片段5分钟
        total_speakers = len(set(segment.get("speaker", "Unknown") for segment in transcription))
        
        # 分析内容结构
        content_structure = {
            "introduction": 0,
            "main_content": 0,
            "conclusion": 0
        }
        
        # 简单的结构划分（前10%为引言，中间80%为主内容，后10%为结论）
        segment_count = len(transcription)
        for i, segment in enumerate(transcription):
            if i < segment_count * 0.1:
                content_structure["introduction"] += 1
            elif i < segment_count * 0.9:
                content_structure["main_content"] += 1
            else:
                content_structure["conclusion"] += 1
        
        # 分析主题分布
        topics = RegeneratePodcastService._extract_topics(transcription)
        
        return {
            "total_duration": total_duration,
            "total_speakers": total_speakers,
            "segment_count": segment_count,
            "content_structure": content_structure,
            "topics": topics,
            "average_segment_length": total_duration / segment_count if segment_count > 0 else 0
        }
    
    @staticmethod
    def _extract_topics(transcription: list) -> dict:
        """从转录内容中提取主题"""
        # 模拟主题提取
        topics = {
            "创新": 0,
            "市场趋势": 0,
            "战略规划": 0,
            "竞争优势": 0,
            "技术发展": 0,
            "团队管理": 0,
            "用户体验": 0
        }
        
        for segment in transcription:
            text = segment.get("text", "").lower()
            if "创新" in text or "innovation" in text:
                topics["创新"] += 1
            if "趋势" in text or "trend" in text:
                topics["市场趋势"] += 1
            if "策略" in text or "strategy" in text:
                topics["战略规划"] += 1
            if "竞争" in text or "competition" in text:
                topics["竞争优势"] += 1
            if "技术" in text or "technology" in text:
                topics["技术发展"] += 1
            if "团队" in text or "team" in text:
                topics["团队管理"] += 1
            if "用户" in text or "user" in text:
                topics["用户体验"] += 1
        
        # 过滤掉没有出现的主题
        return {topic: count for topic, count in topics.items() if count > 0}
    
    @staticmethod
    def _generate_improvement_suggestions(original_analysis: dict) -> dict:
        """生成改进建议"""
        suggestions = {
            "structure": [],
            "content": [],
            "delivery": [],
            "engagement": []
        }
        
        # 基于结构分析生成建议
        structure = original_analysis["content_structure"]
        total_segments = sum(structure.values())
        
        if structure["introduction"] / total_segments < 0.05:
            suggestions["structure"].append("增加引言部分的长度，更好地引入主题")
        if structure["conclusion"] / total_segments < 0.05:
            suggestions["structure"].append("增加结论部分，总结核心观点")
        if structure["main_content"] / total_segments > 0.9:
            suggestions["structure"].append("考虑将主内容拆分为更清晰的小节，提高可理解性")
        
        # 基于主题分布生成建议
        topics = original_analysis["topics"]
        if len(topics) < 3:
            suggestions["content"].append("增加主题多样性，引入更多相关话题")
        elif len(topics) > 7:
            suggestions["content"].append("聚焦核心主题，减少主题切换频率")
        
        # 生成其他方面的建议
        suggestions["delivery"].append("增加对话互动，提高内容生动性")
        suggestions["delivery"].append("调整语速，确保关键信息清晰传达")
        suggestions["engagement"].append("增加听众参与环节，如提问、调查等")
        suggestions["engagement"].append("添加案例分析，增强内容实用性")
        
        return suggestions
    
    @staticmethod
    def _generate_optimized_script(transcription: list, improvements: dict) -> dict:
        """生成优化后的Podcast脚本"""
        # 基于改进建议生成优化后的脚本结构
        optimized_segments = []
        
        # 1. 优化引言
        intro_improvements = [s for s in improvements["structure"] if "引言" in s]
        if intro_improvements:
            optimized_segments.append({
                "id": "optimized-intro",
                "speaker": "主持人",
                "text": "欢迎收听本期Podcast！今天我们将深入探讨\"创新与市场趋势\"这一话题。在节目中，我们将分析当前行业现状，分享成功案例，并探讨未来发展方向。希望通过本期节目，您能获得有价值的 insights 和可行动的建议。",
                "improvement": "优化了引言部分，更清晰地引入主题和节目结构"
            })
        
        # 2. 优化主内容
        main_content = transcription[1:-1] if len(transcription) > 2 else transcription
        for i, segment in enumerate(main_content):
            optimized_text = segment["text"]
            improvement_note = ""
            
            # 添加更多案例分析
            if any("案例" in s for s in improvements["engagement"]):
                optimized_text += " 举个例子，苹果公司通过持续创新，从一家电脑公司发展成为全球科技巨头，其成功经验值得我们深入研究和借鉴。"
                improvement_note = "添加了案例分析，增强内容实用性"
            
            optimized_segments.append({
                "id": f"optimized-main-{i}",
                "speaker": segment.get("speaker", "Unknown"),
                "text": optimized_text,
                "improvement": improvement_note
            })
        
        # 3. 优化结论
        conclusion_improvements = [s for s in improvements["structure"] if "结论" in s]
        if conclusion_improvements:
            optimized_segments.append({
                "id": "optimized-conclusion",
                "speaker": "主持人",
                "text": "感谢您收听本期节目！总结一下，我们探讨了创新的重要性、市场趋势的变化以及企业如何在竞争中保持优势。希望这些内容能对您有所启发，帮助您在工作和生活中更好地应对挑战和机遇。如果您有任何想法或建议，欢迎在评论区留言与我们交流。",
                "improvement": "优化了结论部分，总结核心观点并鼓励听众互动"
            })
        
        return {
            "segments": optimized_segments,
            "total_segments": len(optimized_segments),
            "estimated_duration": len(optimized_segments) * 5  # 假设每个片段5分钟
        }
    
    @staticmethod
    def _generate_iteration_loop(original_analysis: dict, improvements: dict) -> dict:
        """生成内容迭代循环建议"""
        return {
            "cycle": [
                {
                    "phase": "内容创建",
                    "description": "基于优化建议生成新的Podcast脚本",
                    "actions": [
                        "编写详细的脚本大纲",
                        "准备相关案例和数据",
                        "设计互动环节"
                    ]
                },
                {
                    "phase": "录制与发布",
                    "description": "录制并发布改进后的Podcast",
                    "actions": [
                        "按照优化后的脚本进行录制",
                        "进行音频后期处理",
                        "发布到各大平台"
                    ]
                },
                {
                    "phase": "反馈收集",
                    "description": "收集听众反馈和数据分析",
                    "actions": [
                        "分析听众评论和评分",
                        "统计下载量和收听时长",
                        "收集社交媒体反馈"
                    ]
                },
                {
                    "phase": "优化迭代",
                    "description": "基于反馈优化下一期内容",
                    "actions": [
                        "分析反馈数据，识别改进点",
                        "调整内容策略和形式",
                        "更新优化建议库"
                    ]
                }
            ],
            "key_metrics": [
                "下载量",
                "收听完成率",
                "听众评论数",
                "社交媒体分享数",
                "听众留存率"
            ],
            "optimization_goals": [
                "提高收听完成率10%",
                "增加听众评论数20%",
                "提高听众留存率15%"
            ]
        }
    
    @staticmethod
    def _generate_visualizations(original_analysis: dict, improvements: dict) -> dict:
        """生成可视化内容"""
        # 生成结构对比柱状图
        structure_data = {
            "labels": ["引言", "主内容", "结论"],
            "series": [
                {
                    "name": "原内容",
                    "data": [
                        original_analysis["content_structure"]["introduction"],
                        original_analysis["content_structure"]["main_content"],
                        original_analysis["content_structure"]["conclusion"]
                    ]
                },
                {
                    "name": "优化建议",
                    "data": [
                        max(original_analysis["content_structure"]["introduction"] * 2, 2),
                        original_analysis["content_structure"]["main_content"],
                        max(original_analysis["content_structure"]["conclusion"] * 3, 2)
                    ]
                }
            ]
        }
        structure_bar = VisualizationService.generate_bar_chart(structure_data)
        
        # 生成主题分布雷达图
        topic_categories = list(original_analysis["topics"].keys())[:5]  # 最多显示5个主题
        topic_data = {
            "categories": topic_categories,
            "series": [{
                "name": "主题分布",
                "data": [original_analysis["topics"][cat] for cat in topic_categories]
            }]
        }
        topic_radar = VisualizationService.generate_radar_chart(topic_data)
        
        # 生成改进建议热力图
        suggestion_types = list(improvements.keys())
        suggestion_counts = [len(improvements[key]) for key in suggestion_types]
        
        heatmap_data = {
            "x_labels": suggestion_types,
            "y_labels": ["改进建议数量"],
            "values": [[count] for count in suggestion_counts]
        }
        suggestion_heatmap = VisualizationService.generate_heatmap(heatmap_data)
        
        return {
            "structure_comparison": structure_bar,
            "topic_distribution": topic_radar,
            "suggestion_heatmap": suggestion_heatmap
        }
    
    @staticmethod
    def generate_content_calendar(transcription: list, frequency: str = "weekly") -> dict:
        """
        基于原内容生成内容日历
        
        Args:
            transcription: 原转录文本列表
            frequency: 发布频率，可选值：daily, weekly, monthly
            
        Returns:
            内容日历和主题规划
        """
        # 提取核心主题
        topics = RegeneratePodcastService._extract_topics(transcription)
        core_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # 生成内容日历
        content_calendar = {
            "frequency": frequency,
            "core_topics": [topic[0] for topic in core_topics],
            "episodes": []
        }
        
        # 生成未来8期的内容规划
        for i in range(8):
            episode = {
                "episode_number": i + 1,
                "title": f"{core_topics[i % 3][0]}深度探讨 - 第{i + 1}期",
                "topic": core_topics[i % 3][0],
                "subtopics": [
                    f"{core_topics[i % 3][0]}的最新趋势",
                    f"{core_topics[i % 3][0]}的实践案例",
                    f"{core_topics[i % 3][0]}的未来发展"
                ],
                "target_audience": "专业人士和爱好者",
                "estimated_duration": 30,  # 分钟
                "production_tasks": [
                    "脚本编写",
                    "嘉宾邀请（如需要）",
                    "音频录制",
                    "后期制作",
                    "发布准备"
                ]
            }
            content_calendar["episodes"].append(episode)
        
        return content_calendar
    
    @staticmethod
    def analyze_content_performance(transcription: list, performance_data: dict = None) -> dict:
        """
        分析Podcast内容表现
        
        Args:
            transcription: 转录文本列表
            performance_data: 表现数据，如下载量、收听时长等
            
        Returns:
            内容表现分析报告
        """
        if not performance_data:
            # 生成模拟数据
            performance_data = {
                "downloads": 1500,
                "average_listen_duration": 22,
                "completion_rate": 0.65,
                "ratings": 4.2,
                "reviews": 85,
                "social_shares": 230
            }
        
        # 分析内容结构对表现的影响
        structure_analysis = {
            "segment_count": len(transcription),
            "estimated_total_duration": len(transcription) * 5,
            "average_segment_engagement": performance_data["completion_rate"] * 100
        }
        
        # 生成改进建议
        performance_suggestions = []
        if performance_data["completion_rate"] < 0.7:
            performance_suggestions.append("考虑缩短内容长度或增加互动环节，提高完成率")
        if performance_data["ratings"] < 4.5:
            performance_suggestions.append("收集听众反馈，优化内容质量和相关性")
        if performance_data["social_shares"] < 300:
            performance_suggestions.append("增加分享激励机制，提高内容传播性")
        
        return {
            "performance_metrics": performance_data,
            "structure_analysis": structure_analysis,
            "engagement_insights": [
                f"平均收听时长为{performance_data['average_listen_duration']}分钟，完成率{performance_data['completion_rate'] * 100:.1f}%",
                f"获得{performance_data['reviews']}条评论，平均评分{performance_data['ratings']}星",
                f"社交媒体分享{performance_data['social_shares']}次，传播范围较广"
            ],
            "improvement_suggestions": performance_suggestions
        }
