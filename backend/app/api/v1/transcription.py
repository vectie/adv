from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.model_service import model_service
from app.services.speaker_diarization import SpeakerDiarizationService
from app.utils.audio_processor import AudioProcessor
from app.core.config import settings
import tempfile
import os
import shutil

router = APIRouter()

speaker_service = SpeakerDiarizationService()
audio_processor = AudioProcessor()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """语音识别API，将音频文件转录为文本并区分说话人
    
    Args:
        file: 上传的音频文件
        
    Returns:
        dict: 转录结果，格式为 {"status": "success", "transcription": [{"speaker": "主持人", "text": "xxx"}, ...]}
    """
    try:
        # 保存上传的文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        # 转换为WAV格式
        wav_path = audio_processor.convert_to_wav(
            temp_file_path,
            sample_rate=settings.AUDIO_SAMPLE_RATE,
            channels=settings.AUDIO_CHANNELS
        )
        
        try:
            # 使用模型进行转录
            text = model_service.transcribe(wav_path)
            
            # 分离说话人
            transcription = speaker_service.separate_speakers(text)
            
            return {
                "status": "success",
                "transcription": transcription
            }
        finally:
            # 清理临时文件
            audio_processor.cleanup_temp_files([temp_file_path, wav_path])
    
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@router.get("/health")
async def health_check():
    """健康检查接口，用于检查服务是否正常运行
    
    Returns:
        dict: 健康状态，格式为 {"status": "healthy", "model_loaded": True, "service": "xxx"}
    """
    return {
        "status": "healthy",
        "model_loaded": model_service.model is not None,
        "service": settings.PROJECT_NAME
    }