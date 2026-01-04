import pytest
from app.services.speaker_diarization import SpeakerDiarizationService

class TestSpeakerDiarizationService:
    def setup_method(self):
        self.speaker_service = SpeakerDiarizationService()
    
    def test_separate_speakers(self):
        """测试说话人分离功能"""
        # 准备测试数据
        text = "主持人：欢迎收听今天的节目。嘉宾：很高兴来到这里。主持人：请介绍一下你的项目。嘉宾：我们正在开发一个语音识别应用。"
        
        # 调用说话人分离服务
        result = self.speaker_service.separate_speakers(text)
        
        # 验证结果
        assert isinstance(result, list)
        assert len(result) > 0
        
        # 验证每个元素的格式
        for item in result:
            assert "speaker" in item
            assert "text" in item
            assert item["speaker"] in ["主持人", "嘉宾"]
            assert isinstance(item["text"], str)
            assert len(item["text"]) > 0
    
    def test_improve_diarization(self):
        """测试改进说话人分离结果功能"""
        # 准备测试数据
        transcription = [
            {"speaker": "主持人", "text": "欢迎收听今天的节目。"},
            {"speaker": "嘉宾", "text": "很高兴来到这里。"},
            {"speaker": "主持人", "text": "请介绍一下你的项目。"}
        ]
        
        # 调用改进说话人分离结果服务
        result = self.speaker_service.improve_diarization(transcription)
        
        # 验证结果
        assert isinstance(result, list)
        assert len(result) == len(transcription)
        
        # 验证结果格式保持不变
        for i, item in enumerate(result):
            assert item["speaker"] == transcription[i]["speaker"]
            assert item["text"] == transcription[i]["text"]
    
    def test_separate_speakers_with_short_text(self):
        """测试短文本的说话人分离"""
        # 准备测试数据（短文本）
        text = "主持人：你好。嘉宾：你好。"
        
        # 调用说话人分离服务
        result = self.speaker_service.separate_speakers(text)
        
        # 验证结果
        assert isinstance(result, list)
        assert len(result) == 2
        for item in result:
            assert "speaker" in item
            assert "text" in item
    
    def test_separate_speakers_with_empty_text(self):
        """测试空文本的说话人分离"""
        # 准备测试数据（空文本）
        text = ""
        
        # 调用说话人分离服务
        result = self.speaker_service.separate_speakers(text)
        
        # 验证结果
        assert isinstance(result, list)
        assert len(result) == 0