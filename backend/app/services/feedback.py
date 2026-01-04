import json
import os
import time
from datetime import datetime

class FeedbackService:
    def __init__(self):
        self.progress_db = self._load_progress_db()
        self.achievements = self._define_achievements()
    
    def _load_progress_db(self):
        """加载或初始化进度数据库"""
        db_path = os.path.join(os.getcwd(), "progress_db.json")
        if os.path.exists(db_path):
            try:
                with open(db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load progress DB: {e}")
                return {}
        return {}
    
    def _save_progress_db(self):
        """保存进度数据库"""
        db_path = os.path.join(os.getcwd(), "progress_db.json")
        try:
            with open(db_path, "w", encoding="utf-8") as f:
                json.dump(self.progress_db, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save progress DB: {e}")
            return False
    
    def _define_achievements(self):
        """定义成就列表"""
        return [
            {
                "id": "first_transcription",
                "name": "初试锋芒",
                "description": "完成第一次转录",
                "icon": "🌟",
                "condition_type": "transcription_count",
                "condition_value": 1,
                "reward": "解锁基础分析功能",
                "level": "beginner"
            },
            {
                "id": "five_transcriptions",
                "name": "熟能生巧",
                "description": "完成5次转录",
                "icon": "🏆",
                "condition_type": "transcription_count",
                "condition_value": 5,
                "reward": "解锁高级可视化功能",
                "level": "intermediate"
            },
            {
                "id": "ten_transcriptions",
                "name": "转录达人",
                "description": "完成10次转录",
                "icon": "👑",
                "condition_type": "transcription_count",
                "condition_value": 10,
                "reward": "解锁所有高级功能",
                "level": "advanced"
            },
            {
                "id": "first_analysis",
                "name": "思考者",
                "description": "完成第一次思考过程分析",
                "icon": "🤔",
                "condition_type": "analysis_count",
                "condition_value": 1,
                "reward": "获得思考模型推荐",
                "level": "beginner"
            },
            {
                "id": "five_analyses",
                "name": "分析大师",
                "description": "完成5次思考过程分析",
                "icon": "🧠",
                "condition_type": "analysis_count",
                "condition_value": 5,
                "reward": "获得个性化思维模型",
                "level": "advanced"
            },
            {
                "id": "long_transcription",
                "name": "耐心倾听者",
                "description": "转录时长超过30分钟的内容",
                "icon": "⏱️",
                "condition_type": "total_duration",
                "condition_value": 30,
                "reward": "获得高级音频处理功能",
                "level": "intermediate"
            }
        ]
    
    def _get_user_progress(self, user_id):
        """获取用户进度"""
        if user_id not in self.progress_db:
            self.progress_db[user_id] = {
                "user_id": user_id,
                "transcription_count": 0,
                "analysis_count": 0,
                "total_duration": 0,
                "achievements_unlocked": [],
                "last_activity": datetime.now().isoformat(),
                "progress_history": []
            }
        return self.progress_db[user_id]
    
    def update_progress(self, user_id, progress_data):
        """更新用户进度
        
        Args:
            user_id: 用户ID
            progress_data: 进度数据，包含 transcription_count, analysis_count, duration 等
            
        Returns:
            dict: 更新后的进度信息和新解锁的成就
        """
        user_progress = self._get_user_progress(user_id)
        
        # 更新基本进度
        if "transcription_count" in progress_data:
            user_progress["transcription_count"] += progress_data["transcription_count"]
        
        if "analysis_count" in progress_data:
            user_progress["analysis_count"] += progress_data["analysis_count"]
        
        if "duration" in progress_data:
            user_progress["total_duration"] += progress_data["duration"]
        
        # 更新最后活动时间
        user_progress["last_activity"] = datetime.now().isoformat()
        
        # 记录进度历史
        user_progress["progress_history"].append({
            "timestamp": datetime.now().isoformat(),
            **progress_data
        })
        
        # 检查新解锁的成就
        new_achievements = self._check_achievements(user_progress)
        
        # 保存进度
        self.progress_db[user_id] = user_progress
        self._save_progress_db()
        
        return {
            "status": "success",
            "user_progress": user_progress,
            "new_achievements": new_achievements,
            "all_achievements": self.achievements
        }
    
    def _check_achievements(self, user_progress):
        """检查并解锁成就"""
        new_achievements = []
        
        for achievement in self.achievements:
            if achievement["id"] not in user_progress["achievements_unlocked"]:
                unlocked = False
                
                # 检查条件
                if achievement["condition_type"] == "transcription_count":
                    if user_progress["transcription_count"] >= achievement["condition_value"]:
                        unlocked = True
                
                elif achievement["condition_type"] == "analysis_count":
                    if user_progress["analysis_count"] >= achievement["condition_value"]:
                        unlocked = True
                
                elif achievement["condition_type"] == "total_duration":
                    if user_progress["total_duration"] >= achievement["condition_value"]:
                        unlocked = True
                
                # 解锁成就
                if unlocked:
                    user_progress["achievements_unlocked"].append(achievement["id"])
                    new_achievements.append(achievement)
        
        return new_achievements
    
    def get_user_feedback(self, user_id, activity_type, activity_data=None):
        """获取用户反馈
        
        Args:
            user_id: 用户ID
            activity_type: 活动类型，如 transcription, analysis 等
            activity_data: 活动数据
            
        Returns:
            dict: 反馈信息，包含激励、成就和进度可视化数据
        """
        user_progress = self._get_user_progress(user_id)
        
        # 生成个性化激励
        motivation = self._generate_motivation(activity_type, user_progress)
        
        # 计算进度百分比
        progress_percentage = self._calculate_progress_percentage(user_progress)
        
        # 生成可视化数据
        visualization_data = self._generate_progress_visualization(user_progress)
        
        return {
            "status": "success",
            "feedback": {
                "motivation": motivation,
                "user_progress": user_progress,
                "progress_percentage": progress_percentage,
                "visualization": visualization_data,
                "next_achievements": self._get_next_achievements(user_progress)
            }
        }
    
    def _generate_motivation(self, activity_type, user_progress):
        """生成个性化激励
        
        Args:
            activity_type: 活动类型
            user_progress: 用户进度
            
        Returns:
            dict: 激励信息
        """
        motivations = {
            "transcription": [
                f"太棒了！你已经完成了 {user_progress['transcription_count']} 次转录，继续保持！",
                f"优秀！每一次转录都是一次学习的机会，你已经累积了 {user_progress['total_duration']} 分钟的学习时间。",
                f"加油！你离下一个成就越来越近了！",
                f"了不起！你正在建立自己的知识宝库，坚持下去！"
            ],
            "analysis": [
                f"精彩的分析！你已经完成了 {user_progress['analysis_count']} 次思考过程分析，思维正在不断提升！",
                f"深入的思考会带来巨大的进步，你做得非常好！",
                f"每一次分析都是一次思维的锻炼，继续挑战自己！",
                f"你的思考能力正在快速提升，期待看到你更多的精彩分析！"
            ]
        }
        
        # 随机选择一条激励语
        import random
        return {
            "text": random.choice(motivations.get(activity_type, motivations["transcription"])),
            "type": activity_type,
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_progress_percentage(self, user_progress):
        """计算整体进度百分比
        
        Args:
            user_progress: 用户进度
            
        Returns:
            dict: 各维度的进度百分比
        """
        # 计算转录进度 (目标10次)
        transcription_progress = min(100, (user_progress["transcription_count"] / 10) * 100)
        
        # 计算分析进度 (目标5次)
        analysis_progress = min(100, (user_progress["analysis_count"] / 5) * 100)
        
        # 计算总时长进度 (目标60分钟)
        duration_progress = min(100, (user_progress["total_duration"] / 60) * 100)
        
        # 计算成就解锁进度
        total_achievements = len(self.achievements)
        unlocked_achievements = len(user_progress["achievements_unlocked"])
        achievement_progress = min(100, (unlocked_achievements / total_achievements) * 100)
        
        return {
            "transcription": transcription_progress,
            "analysis": analysis_progress,
            "duration": duration_progress,
            "achievements": achievement_progress,
            "overall": (transcription_progress + analysis_progress + duration_progress + achievement_progress) / 4
        }
    
    def _generate_progress_visualization(self, user_progress):
        """生成进度可视化数据
        
        Args:
            user_progress: 用户进度
            
        Returns:
            dict: 可视化数据，包含历史趋势等
        """
        # 提取最近7天的进度数据
        recent_history = user_progress["progress_history"][-7:]
        
        # 生成趋势数据
        trend_data = []
        for entry in recent_history:
            date = entry["timestamp"].split("T")[0]
            trend_data.append({
                "date": date,
                "transcriptions": entry.get("transcription_count", 0),
                "analyses": entry.get("analysis_count", 0),
                "duration": entry.get("duration", 0)
            })
        
        # 生成成就统计
        achievement_stats = {
            "total": len(self.achievements),
            "unlocked": len(user_progress["achievements_unlocked"]),
            "by_level": {
                "beginner": 0,
                "intermediate": 0,
                "advanced": 0
            }
        }
        
        for achievement_id in user_progress["achievements_unlocked"]:
            achievement = next(a for a in self.achievements if a["id"] == achievement_id)
            achievement_stats["by_level"][achievement["level"]] += 1
        
        return {
            "trend_data": trend_data,
            "achievement_stats": achievement_stats
        }
    
    def _get_next_achievements(self, user_progress):
        """获取用户即将解锁的成就
        
        Args:
            user_progress: 用户进度
            
        Returns:
            list: 即将解锁的成就列表
        """
        next_achievements = []
        
        for achievement in self.achievements:
            if achievement["id"] not in user_progress["achievements_unlocked"]:
                # 计算距离解锁的进度
                if achievement["condition_type"] == "transcription_count":
                    progress = min(100, (user_progress["transcription_count"] / achievement["condition_value"]) * 100)
                elif achievement["condition_type"] == "analysis_count":
                    progress = min(100, (user_progress["analysis_count"] / achievement["condition_value"]) * 100)
                elif achievement["condition_type"] == "total_duration":
                    progress = min(100, (user_progress["total_duration"] / achievement["condition_value"]) * 100)
                else:
                    progress = 0
                
                next_achievements.append({
                    **achievement,
                    "progress": progress,
                    "remaining": max(0, achievement["condition_value"] - 
                                     user_progress.get(achievement["condition_type"].replace("_count", ""), 0))
                })
        
        # 按进度排序，即将解锁的排在前面
        next_achievements.sort(key=lambda x: x["progress"], reverse=True)
        
        return next_achievements[:3]  # 返回前3个即将解锁的成就
    
    def get_user_stats(self, user_id):
        """获取用户统计信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            dict: 用户统计信息
        """
        user_progress = self._get_user_progress(user_id)
        
        return {
            "status": "success",
            "stats": {
                "total_transcriptions": user_progress["transcription_count"],
                "total_analyses": user_progress["analysis_count"],
                "total_duration": user_progress["total_duration"],
                "achievements_unlocked": len(user_progress["achievements_unlocked"]),
                "total_achievements": len(self.achievements),
                "last_activity": user_progress["last_activity"],
                "progress_history": user_progress["progress_history"][-30:]  # 返回最近30条历史记录
            }
        }