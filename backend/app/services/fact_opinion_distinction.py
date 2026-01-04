from typing import List, Dict, Any
from app.services.visualization_service import VisualizationService

class FactOpinionDistinctionService:
    """事实与观点区分服务类"""
    
    @staticmethod
    def distinguish_fact_opinion(transcription: list) -> dict:
        """
        区分转录内容中的事实陈述和主观观点
        
        Args:
            transcription: 转录文本列表
            
        Returns:
            事实与观点区分结果，包含标记和证据支持
        """
        # 分析转录内容，区分事实和观点
        analyzed_segments = []
        for segment in transcription:
            analyzed_segment = FactOpinionDistinctionService._analyze_segment(segment)
            analyzed_segments.append(analyzed_segment)
        
        # 统计事实与观点分布
        statistics = FactOpinionDistinctionService._calculate_statistics(analyzed_segments)
        
        # 生成可信度评估
        credibility_assessment = FactOpinionDistinctionService._assess_credibility(analyzed_segments)
        
        # 生成可视化
        visualization_data = FactOpinionDistinctionService._generate_visualizations(statistics, credibility_assessment)
        
        return {
            "analyzed_segments": analyzed_segments,
            "statistics": statistics,
            "credibility_assessment": credibility_assessment,
            "visualizations": visualization_data
        }
    
    @staticmethod
    def _analyze_segment(segment: dict) -> dict:
        """分析单个转录片段，区分事实和观点"""
        text = segment.get("text", "").lower()
        speaker = segment.get("speaker", "Unknown")
        
        # 定义事实和观点的关键词和模式
        fact_keywords = [
            "数据", "统计", "研究", "报告", "调查", "结果", "事实", "实际", "已经", "曾经", "现在", "未来",
            "数字", "百分比", "比例", "时间", "日期", "地点", "事件", "人物", "机构", "组织"
        ]
        
        opinion_keywords = [
            "认为", "觉得", "应该", "可能", "也许", "大概", "似乎", "好像", "显然", "确实", "肯定",
            "重要", "关键", "必要", "必须", "建议", "推荐", "希望", "期望", "相信", "信任", "怀疑",
            "好", "坏", "优", "劣", "强", "弱", "高", "低", "大", "小", "多", "少"
        ]
        
        # 检测事实和观点标记
        is_fact = False
        is_opinion = False
        evidence = []
        
        # 检查事实关键词
        for keyword in fact_keywords:
            if keyword in text:
                is_fact = True
                evidence.append(f"包含事实关键词：{keyword}")
                break
        
        # 检查观点关键词
        for keyword in opinion_keywords:
            if keyword in text:
                is_opinion = True
                evidence.append(f"包含观点关键词：{keyword}")
                break
        
        # 检查特殊句式
        if "是" in text and "的" in text and len(text) > 5:
            is_fact = True
            evidence.append("包含判断句式")
        
        if "应该" in text or "必须" in text:
            is_opinion = True
            evidence.append("包含建议或命令句式")
        
        # 确定类型（可能同时包含事实和观点）
        content_type = []
        if is_fact:
            content_type.append("事实")
        if is_opinion:
            content_type.append("观点")
        if not content_type:
            content_type.append("不确定")
        
        # 评估可信度
        credibility = "高"
        if len(evidence) < 2:
            credibility = "中"
        if "不确定" in content_type:
            credibility = "低"
        
        return {
            "id": segment.get("id", ""),
            "speaker": speaker,
            "text": segment.get("text", ""),
            "content_type": content_type,
            "evidence": evidence,
            "credibility": credibility
        }
    
    @staticmethod
    def _calculate_statistics(analyzed_segments: list) -> dict:
        """计算事实与观点分布统计"""
        total_segments = len(analyzed_segments)
        fact_count = 0
        opinion_count = 0
        mixed_count = 0
        uncertain_count = 0
        
        # 按类型统计
        for segment in analyzed_segments:
            content_type = segment["content_type"]
            if len(content_type) == 2:
                mixed_count += 1
                fact_count += 1
                opinion_count += 1
            elif "事实" in content_type:
                fact_count += 1
            elif "观点" in content_type:
                opinion_count += 1
            else:
                uncertain_count += 1
        
        # 按可信度统计
        credibility_stats = {
            "高": 0,
            "中": 0,
            "低": 0
        }
        for segment in analyzed_segments:
            credibility_stats[segment["credibility"]] += 1
        
        # 按发言人统计
        speaker_stats = {}
        for segment in analyzed_segments:
            speaker = segment["speaker"]
            if speaker not in speaker_stats:
                speaker_stats[speaker] = {
                    "total": 0,
                    "fact": 0,
                    "opinion": 0,
                    "mixed": 0
                }
            speaker_stats[speaker]["total"] += 1
            
            content_type = segment["content_type"]
            if len(content_type) == 2:
                speaker_stats[speaker]["mixed"] += 1
            elif "事实" in content_type:
                speaker_stats[speaker]["fact"] += 1
            elif "观点" in content_type:
                speaker_stats[speaker]["opinion"] += 1
        
        return {
            "total_segments": total_segments,
            "fact_count": fact_count,
            "opinion_count": opinion_count,
            "mixed_count": mixed_count,
            "uncertain_count": uncertain_count,
            "fact_ratio": fact_count / total_segments if total_segments > 0 else 0,
            "opinion_ratio": opinion_count / total_segments if total_segments > 0 else 0,
            "credibility_distribution": credibility_stats,
            "speaker_distribution": speaker_stats
        }
    
    @staticmethod
    def _assess_credibility(analyzed_segments: list) -> dict:
        """
        评估事实陈述的可信度
        
        Args:
            analyzed_segments: 分析后的片段列表
            
        Returns:
            可信度评估结果
        """
        # 提取所有事实陈述
        fact_segments = [s for s in analyzed_segments if "事实" in s["content_type"]]
        
        # 评估可信度
        high_credibility = [s for s in fact_segments if s["credibility"] == "高"]
        medium_credibility = [s for s in fact_segments if s["credibility"] == "中"]
        low_credibility = [s for s in fact_segments if s["credibility"] == "低"]
        
        # 生成可信度报告
        credibility_report = {
            "total_facts": len(fact_segments),
            "high_credibility_facts": len(high_credibility),
            "medium_credibility_facts": len(medium_credibility),
            "low_credibility_facts": len(low_credibility),
            "high_credibility_examples": [s["text"] for s in high_credibility[:3]],
            "low_credibility_examples": [s["text"] for s in low_credibility[:3]],
            "credibility_score": {
                "overall": (len(high_credibility) * 3 + len(medium_credibility) * 2 + len(low_credibility)) / \
                           (len(fact_segments) * 3) if len(fact_segments) > 0 else 0,
                "by_evidence_count": {
                    "1": 0.6,
                    "2": 0.8,
                    "3+": 0.95
                }
            }
        }
        
        return credibility_report
    
    @staticmethod
    def _generate_visualizations(statistics: dict, credibility_assessment: dict) -> dict:
        """
        生成事实与观点区分的可视化内容
        
        Args:
            statistics: 统计数据
            credibility_assessment: 可信度评估
            
        Returns:
            可视化数据
        """
        # 生成事实与观点分布饼图
        distribution_data = {
            "labels": ["事实", "观点", "混合", "不确定"],
            "values": [
                statistics["fact_count"],
                statistics["opinion_count"],
                statistics["mixed_count"],
                statistics["uncertain_count"]
            ]
        }
        distribution_pie = VisualizationService.generate_pie_chart(distribution_data)
        
        # 生成可信度分布柱状图
        credibility_data = {
            "labels": ["高可信度", "中可信度", "低可信度"],
            "series": [{
                "name": "事实数量",
                "data": [
                    credibility_assessment["high_credibility_facts"],
                    credibility_assessment["medium_credibility_facts"],
                    credibility_assessment["low_credibility_facts"]
                ]
            }]
        }
        credibility_bar = VisualizationService.generate_bar_chart(credibility_data)
        
        # 生成发言人观点分布雷达图
        if statistics["speaker_distribution"]:
            speaker_names = list(statistics["speaker_distribution"].keys())[:5]  # 最多显示5个发言人
            radar_data = {
                "categories": ["事实占比", "观点占比", "混合占比"],
                "series": []
            }
            
            for speaker in speaker_names:
                speaker_stats = statistics["speaker_distribution"][speaker]
                total = speaker_stats["total"]
                series_item = {
                    "name": speaker,
                    "data": [
                        speaker_stats["fact"] / total * 100 if total > 0 else 0,
                        speaker_stats["opinion"] / total * 100 if total > 0 else 0,
                        speaker_stats["mixed"] / total * 100 if total > 0 else 0
                    ]
                }
                radar_data["series"].append(series_item)
            
            speaker_radar = VisualizationService.generate_radar_chart(radar_data)
        else:
            speaker_radar = {}
        
        return {
            "fact_opinion_distribution": distribution_pie,
            "credibility_distribution": credibility_bar,
            "speaker_opinion_distribution": speaker_radar
        }
    
    @staticmethod
    def extract_evidence(transcription: list) -> dict:
        """
        从转录内容中提取证据支持
        
        Args:
            transcription: 转录文本列表
            
        Returns:
            证据提取结果
        """
        # 分析转录内容，提取证据
        evidence_segments = []
        for segment in transcription:
            text = segment.get("text", "")
            speaker = segment.get("speaker", "Unknown")
            
            # 简单的证据提取逻辑
            evidence = []
            
            # 检查是否包含数据或研究支持
            if any(keyword in text.lower() for keyword in ["数据", "统计", "研究", "报告", "调查", "结果"]):
                evidence.append({
                    "type": "数据支持",
                    "content": text,
                    "confidence": 0.85
                })
            
            # 检查是否包含引用
            if any(keyword in text.lower() for keyword in ["引用", "根据", "据", "表示", "指出"]):
                evidence.append({
                    "type": "引用支持",
                    "content": text,
                    "confidence": 0.75
                })
            
            # 检查是否包含具体例子
            if any(keyword in text.lower() for keyword in ["例如", "比如", "举例来说", "像", "比如"]):
                evidence.append({
                    "type": "例子支持",
                    "content": text,
                    "confidence": 0.65
                })
            
            if evidence:
                evidence_segments.append({
                    "speaker": speaker,
                    "text": text,
                    "evidence": evidence
                })
        
        # 统计证据类型分布
        evidence_types = {}
        for segment in evidence_segments:
            for ev in segment["evidence"]:
                ev_type = ev["type"]
                if ev_type not in evidence_types:
                    evidence_types[ev_type] = 0
                evidence_types[ev_type] += 1
        
        return {
            "evidence_segments": evidence_segments,
            "evidence_count": len(evidence_segments),
            "evidence_type_distribution": evidence_types,
            "average_confidence": sum(
                ev["confidence"] for segment in evidence_segments for ev in segment["evidence"]
            ) / sum(
                len(segment["evidence"]) for segment in evidence_segments
            ) if evidence_segments else 0
        }
    
    @staticmethod
    def generate_fact_check_report(transcription: list) -> dict:
        """
        生成事实核查报告
        
        Args:
            transcription: 转录文本列表
            
        Returns:
            事实核查报告
        """
        # 首先区分事实和观点
        distinction_result = FactOpinionDistinctionService.distinguish_fact_opinion(transcription)
        
        # 提取事实陈述
        fact_segments = [s for s in distinction_result["analyzed_segments"] if "事实" in s["content_type"]]
        
        # 生成事实核查报告
        fact_check_report = {
            "total_facts": len(fact_segments),
            "credibility_summary": distinction_result["credibility_assessment"],
            "high_credibility_facts": [
                s["text"] for s in fact_segments if s["credibility"] == "高"
            ],
            "medium_credibility_facts": [
                s["text"] for s in fact_segments if s["credibility"] == "中"
            ],
            "low_credibility_facts": [
                s["text"] for s in fact_segments if s["credibility"] == "低"
            ],
            "fact_opinion_ratio": {
                "fact": distinction_result["statistics"]["fact_ratio"],
                "opinion": distinction_result["statistics"]["opinion_ratio"]
            },
            "recommendations": [
                "进一步核实低可信度事实",
                "为关键事实添加更多证据支持",
                "在引用他人观点时明确标注",
                "平衡事实陈述和主观观点的比例"
            ]
        }
        
        return fact_check_report
