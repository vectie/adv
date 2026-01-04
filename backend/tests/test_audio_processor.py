import pytest
import tempfile
import os
from app.utils.audio_processor import AudioProcessor

class TestAudioProcessor:
    def setup_method(self):
        self.audio_processor = AudioProcessor()
    
    def test_convert_to_wav(self):
        """测试音频转换功能"""
        # 创建一个简单的测试音频文件（这里使用一个文本文件模拟，实际测试应该使用真实音频）
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(b"test audio content")
            temp_file_path = temp_file.name
        
        try:
            # 测试应该失败，因为输入不是有效的音频文件
            with pytest.raises(Exception):
                wav_path = self.audio_processor.convert_to_wav(temp_file_path)
        finally:
            # 清理测试文件
            os.unlink(temp_file_path)
    
    def test_cleanup_temp_files(self):
        """测试临时文件清理功能"""
        # 创建一些临时文件
        temp_files = []
        for _ in range(3):
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(b"test content")
                temp_files.append(temp_file.name)
        
        # 验证文件存在
        for file_path in temp_files:
            assert os.path.exists(file_path)
        
        # 调用清理函数
        self.audio_processor.cleanup_temp_files(temp_files)
        
        # 验证文件被删除
        for file_path in temp_files:
            assert not os.path.exists(file_path)
    
    def test_cleanup_nonexistent_files(self):
        """测试清理不存在的文件"""
        # 调用清理函数清理不存在的文件，应该不会抛出异常
        self.audio_processor.cleanup_temp_files(["nonexistent_file.txt"])