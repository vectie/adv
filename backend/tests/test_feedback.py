import pytest
import json
import os
from app.services.feedback import FeedbackService

class TestFeedbackService:
    def setup_method(self):
        self.feedback_service = FeedbackService()
        # 保存原始进度数据库以便测试后恢复
        self.original_db = self.feedback_service.progress_db.copy()
    
    def teardown_method(self):
        # 恢复原始进度数据库
        self.feedback_service.progress_db = self.original_db
        # 删除测试生成的数据库文件
        db_path = os.path.join(os.getcwd(), "progress_db.json")
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    def test_update_progress(self):
        """测试进度更新功能"""
        # 准备测试数据
        user_id = "test_user_1"
        progress_data = {
            "transcription_count": 1,
            "analysis_count": 0,
            "duration": 5
        }
        
        # 调用进度更新服务
        result = self.feedback_service.update_progress(user_id, progress_data)
        
        # 验证结果
        assert result["status"] == "success"
        assert result["user_progress"]["user_id"] == user_id
        assert result["user_progress"]["transcription_count"] == 1
        assert result["user_progress"]["analysis_count"] == 0
        assert result["user_progress"]["total_duration"] == 5
        
        # 验证成就解锁
        assert len(result["new_achievements"]) > 0
        assert any(achievement["id"] == "first_transcription" for achievement in result["new_achievements"])
    
    def test_get_user_feedback(self):
        """测试获取用户反馈功能"""
        # 先更新用户进度
        user_id = "test_user_2"
        progress_data = {
            "transcription_count": 1,
            "analysis_count": 0,
            "duration": 5
        }
        self.feedback_service.update_progress(user_id, progress_data)
        
        # 调用获取反馈服务
        result = self.feedback_service.get_user_feedback(user_id, "transcription")
        
        # 验证结果
        assert result["status"] == "success"
        assert "feedback" in result
        assert "motivation" in result["feedback"]
        assert "user_progress" in result["feedback"]
        assert "progress_percentage" in result["feedback"]
        assert "visualization" in result["feedback"]
        assert "next_achievements" in result["feedback"]
        
        # 验证激励信息
        assert "text" in result["feedback"]["motivation"]
        assert len(result["feedback"]["motivation"]["text"]) > 0
    
    def test_get_next_achievements(self):
        """测试获取即将解锁的成就功能"""
        # 先更新用户进度
        user_id = "test_user_3"
        progress_data = {
            "transcription_count": 3,
            "analysis_count": 0,
            "duration": 10
        }
        self.feedback_service.update_progress(user_id, progress_data)
        
        # 获取用户进度
        user_progress = self.feedback_service._get_user_progress(user_id)
        
        # 调用获取即将解锁的成就
        next_achievements = self.feedback_service._get_next_achievements(user_progress)
        
        # 验证结果
        assert len(next_achievements) > 0
        # 应该返回最多3个即将解锁的成就
        assert len(next_achievements) <= 3
        # 按进度排序，进度高的在前
        for i in range(len(next_achievements) - 1):
            assert next_achievements[i]["progress"] >= next_achievements[i+1]["progress"]
    
    def test_get_user_stats(self):
        """测试获取用户统计信息功能"""
        # 先更新用户进度
        user_id = "test_user_4"
        progress_data = {
            "transcription_count": 2,
            "analysis_count": 1,
            "duration": 8
        }
        self.feedback_service.update_progress(user_id, progress_data)
        
        # 调用获取统计信息服务
        result = self.feedback_service.get_user_stats(user_id)
        
        # 验证结果
        assert result["status"] == "success"
        assert "stats" in result
        assert result["stats"]["total_transcriptions"] == 2
        assert result["stats"]["total_analyses"] == 1
        assert result["stats"]["total_duration"] == 8
        assert result["stats"]["achievements_unlocked"] >= 0
        assert result["stats"]["total_achievements"] > 0
    
    def test_check_achievements(self):
        """测试成就检查功能"""
        # 准备测试数据
        user_progress = {
            "user_id": "test_user_5",
            "transcription_count": 5,
            "analysis_count": 0,
            "total_duration": 0,
            "achievements_unlocked": [],
            "last_activity": "2024-01-01T00:00:00",
            "progress_history": []
        }
        
        # 调用成就检查功能
        new_achievements = self.feedback_service._check_achievements(user_progress)
        
        # 验证结果
        assert len(new_achievements) > 0
        # 应该解锁多个成就
        assert any(achievement["id"] == "first_transcription" for achievement in new_achievements)
        assert any(achievement["id"] == "five_transcriptions" for achievement in new_achievements)