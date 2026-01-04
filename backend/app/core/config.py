import os

class Settings:
    # 模型配置
    MODEL_DIR: str = "FunAudioLLM/Fun-ASR-Nano-2512"
    TRUST_REMOTE_CODE: bool = True
    REMOTE_CODE: bool = None
    DISABLE_UPDATE: bool = True
    
    # 设备配置
    DEVICE: str = "cuda:0" if os.environ.get("USE_GPU", "False").lower() == "true" else "cpu"
    
    # 服务配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Podcast Transcription API"
    VERSION: str = "1.0.0"
    
    # 音频处理配置
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHANNELS: int = 1
    AUDIO_FORMAT: str = "wav"
    
    # 转录配置
    BATCH_SIZE: int = 1
    HOTWORDS: list = ["开放时间"]
    LANGUAGE: str = "中文"
    ITN: bool = True  # 数字转换

settings = Settings()