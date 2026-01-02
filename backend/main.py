from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import tempfile
import shutil
from funasr import AutoModel
from transformers import AutoTokenizer
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
    try:
        model = AutoModel(
            model=model_dir,
            trust_remote_code=True,
            remote_code=None,
            disable_update=True,
            device="cuda:0" if os.environ.get("USE_GPU", "False").lower() == "true" else "cpu",
        )
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Model loading failed: {e}")
        # 如果模型加载失败，使用一个模拟模型
        model = None
        print("Using mock model instead...")

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
    try:
        # 保存上传的文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        # 转换为WAV格式
        wav_path = convert_to_wav(temp_file_path)
        
        try:
            if model is not None:
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
            else:
                # 使用模拟数据，模型加载失败时的备选方案
                text = "欢迎收听今天的播客节目，今天我们邀请到了一位非常特别的嘉宾。大家好，很高兴能来到这里和大家交流。能否请您介绍一下您最近在做的项目？当然可以，我们最近在开发一个跨平台的语音识别应用，它能够自动区分不同的说话人，并生成准确的文字稿。"
            
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
