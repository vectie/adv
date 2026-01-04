import pytest
from fastapi.testclient import TestClient
from app.main import app
import tempfile
import os

client = TestClient(app)

class TestIntegration:
    def test_health_check(self):
        """测试健康检查端点"""
        response = client.get("/api/v1/transcription/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_health_check(self):
        """测试根路径健康检查端点"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_thinking_process_analyze(self):
        """测试思考过程分析端点"""
        # 准备测试数据
        transcription_data = [
            {
                "speaker": "主持人",
                "text": "首先，我认为我们需要分析当前的市场状况。因为市场变化很快，所以我们必须及时调整策略。"
            },
            {
                "speaker": "嘉宾",
                "text": "我同意你的观点。如果我们不做出改变，可能会面临很大的挑战。核心问题是如何平衡短期利益和长期发展。"
            }
        ]
        
        # 调用思考过程分析端点
        response = client.post("/api/v1/thinking-process/analyze", json=transcription_data)
        
        # 验证结果
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "thinking_steps" in response.json()
        assert "thinking_models" in response.json()
        assert "visualization" in response.json()
    
    def test_feedback_update_progress(self):
        """测试反馈进度更新端点"""
        # 准备测试数据
        test_user_id = "test_integration_user"
        progress_data = {
            "transcription_count": 1,
            "analysis_count": 0,
            "duration": 5
        }
        
        # 调用进度更新端点
        response = client.post(
            f"/api/v1/feedback/update-progress?user_id={test_user_id}",
            json=progress_data
        )
        
        # 验证结果
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["user_progress"]["user_id"] == test_user_id
        assert response.json()["user_progress"]["transcription_count"] == 1
    
    def test_feedback_get_feedback(self):
        """测试获取反馈端点"""
        # 先更新用户进度
        test_user_id = "test_integration_user_2"
        progress_data = {
            "transcription_count": 1,
            "analysis_count": 0,
            "duration": 5
        }
        client.post(
            f"/api/v1/feedback/update-progress?user_id={test_user_id}",
            json=progress_data
        )
        
        # 调用获取反馈端点
        response = client.get(
            f"/api/v1/feedback/get-feedback?user_id={test_user_id}&activity_type=transcription"
        )
        
        # 验证结果
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "feedback" in response.json()
        assert "motivation" in response.json()["feedback"]
    
    def test_feedback_get_stats(self):
        """测试获取统计信息端点"""
        # 先更新用户进度
        test_user_id = "test_integration_user_3"
        progress_data = {
            "transcription_count": 2,
            "analysis_count": 1,
            "duration": 8
        }
        client.post(
            f"/api/v1/feedback/update-progress?user_id={test_user_id}",
            json=progress_data
        )
        
        # 调用获取统计信息端点
        response = client.get(f"/api/v1/feedback/get-stats?user_id={test_user_id}")
        
        # 验证结果
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "stats" in response.json()
        assert response.json()["stats"]["total_transcriptions"] == 2
    
    def test_transcribe_endpoint(self):
        """测试转录端点（模拟文件上传）"""
        # 创建一个临时文本文件（不是有效的音频文件，但用于测试端点响应）
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(b"test audio content")
            temp_file_path = temp_file.name
        
        try:
            # 模拟文件上传
            with open(temp_file_path, "rb") as f:
                response = client.post(
                    "/api/v1/transcription/transcribe",
                    files={"file": ("test.txt", f, "text/plain")}
                )
            
            # 验证响应状态码（应该是500，因为输入不是有效的音频文件）
            assert response.status_code == 500
        finally:
            # 清理测试文件
            os.unlink(temp_file_path)