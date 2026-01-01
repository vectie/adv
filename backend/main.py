from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import tempfile
import shutil
from funasr import AutoModel
import numpy as np
import ffmpeg

app = FastAPI(title="Podcast Transcription API", description="Local speech recognition API using FunASR", version="1.0.0")

# 初始化FunASR模型
model_dir = "FunAudioLLM/Fun-ASR-Nano-2512"
model = None

@app.on_event("startup")
async def load_model():
    global model
    print("Loading FunASR model...")
    model = AutoModel(
        model=model_dir,
        trust_remote_code=True,
        # remote_code="./model.py",  # 如需要自定义模型代码，取消注释并提供路径
        device="cuda:0" if os.environ.get("USE_GPU", "False").lower() == "true" else "cpu",
    )
    print("Model loaded successfully!")

@app.on_event("shutdown")
async def unload_model():
    global model
    del model
    print("Model unloaded successfully!")

# 音频格式转换函数
def convert_to_wav(input_path):
    """将音频文件转换为WAV格式"""
    output_path = tempfile.mktemp(suffix=".wav")
    
    try:
        # 使用ffmpeg进行格式转换
        (ffmpeg
         .input(input_path)
         .output(output_path, ac=1, ar=16000, format='wav')
         .overwrite_output()
         .run(capture_stdout=True, capture_stderr=True))
        
        return output_path
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
        raise HTTPException(status_code=500, detail="Audio conversion failed")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """语音识别API"""
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # 保存上传的文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        # 转换为WAV格式
        wav_path = convert_to_wav(temp_file_path)
        
        try:
            # 调用FunASR模型进行语音识别
            res = model.generate(
                input=[wav_path],
                cache={},
                batch_size=1,
                hotwords=["开放时间"],
                language="中文",
                itn=True,  # 数字转换
            )
            
            text = res[0]["text"]
            
            # 模拟说话人分离（简单实现，交替分配主持人和嘉宾）
            sentences = text.split('。')
            transcription = []
            for i, sentence in enumerate(sentences):
                if sentence.strip():
                    transcription.append({
                        "speaker": "主持人" if i % 2 == 0 else "嘉宾",
                        "text": sentence.strip() + "。"
                    })
            
            return {
                "status": "success",
                "transcription": transcription
            }
        finally:
            # 清理临时文件
            os.unlink(temp_file_path)
            os.unlink(wav_path)
    
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "service": "Podcast Transcription API"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        workers=1
    )
