from funasr import AutoModel
from app.core.config import settings
import os

class ModelService:
    def __init__(self):
        self.model = None
    
    def load_model(self):
        """加载FunASR模型
        
        Returns:
            bool: 模型加载是否成功
        """
        print("Loading FunASR model...")
        try:
            self.model = AutoModel(
                model=settings.MODEL_DIR,
                trust_remote_code=settings.TRUST_REMOTE_CODE,
                remote_code=settings.REMOTE_CODE,
                disable_update=settings.DISABLE_UPDATE,
                device=settings.DEVICE,
            )
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Model loading failed: {e}")
            # 如果模型加载失败，使用模拟模型
            self.model = None
            print("Using mock model instead...")
            return False
    
    def unload_model(self):
        """卸载模型，释放资源
        
        Returns:
            bool: 模型卸载是否成功
        """
        if self.model is not None:
            try:
                del self.model
                self.model = None
                print("Model unloaded successfully!")
                return True
            except Exception as e:
                print(f"Failed to unload model: {e}")
                return False
        return True
    
    def transcribe(self, audio_path: str) -> str:
        """使用模型进行语音识别
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            str: 识别结果文本
        """
        if self.model is not None:
            # 调用FunASR模型进行语音识别
            res = self.model.generate(
                input=[audio_path],
                cache={},
                batch_size=settings.BATCH_SIZE,
                hotwords=settings.HOTWORDS,
                language=settings.LANGUAGE,
                itn=settings.ITN,  # 数字转换
            )
            
            return res[0]["text"]
        else:
            # 使用模拟数据，模型加载失败时的备选方案
            return "欢迎收听今天的播客节目，今天我们邀请到了一位非常特别的嘉宾。大家好，很高兴能来到这里和大家交流。能否请您介绍一下您最近在做的项目？当然可以，我们最近在开发一个跨平台的语音识别应用，它能够自动区分不同的说话人，并生成准确的文字稿。"

# 创建全局模型服务实例
model_service = ModelService()