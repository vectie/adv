# FunASR 语音识别后端

本地语音识别服务，基于 FunASR 模型实现，替代云端 API 调用。

## 功能特性

- 🎤 基于 FunASR 模型的本地语音识别
- 🌐 提供 HTTP API 接口
- ⚡ 支持多种音频格式（MP3、MP4、M4A、WAV 等）
- 📱 自动音频格式转换
- 👥 模拟说话人分离
- 💻 支持 CPU 和 GPU 运行

## 技术栈

- **框架**: FastAPI
- **语音识别**: FunASR
- **音频处理**: ffmpeg
- **语言**: Python 3.8+

## 快速开始

### 1. 启动后端服务

```bash
# 进入后端目录
cd backend

# 运行启动脚本
python run_server.py
```

启动脚本会自动：
- 安装所需依赖
- 启动 FastAPI 服务器
- 加载 FunASR 模型

### 2. 验证服务

服务启动成功后，可以通过以下方式验证：

- 健康检查: http://localhost:8000/health
- Swagger 文档: http://localhost:8000/docs

### 3. 使用 API

#### 转录接口

```
POST /transcribe
Content-Type: multipart/form-data

file: <音频文件>
```

**响应示例**:

```json
{
  "status": "success",
  "transcription": [
    {
      "speaker": "主持人",
      "text": "欢迎收听今天的播客节目。"
    },
    {
      "speaker": "嘉宾",
      "text": "大家好，很高兴能来到这里。"
    }
  ]
}
```

## 环境配置

### GPU 支持

默认使用 CPU 运行，如需使用 GPU，请修改 `run_server.py` 中的环境变量：

```python
env["USE_GPU"] = "true"
```

### 模型配置

目前使用的模型是 `FunAudioLLM/Fun-ASR-Nano-2512`，支持中文、英文、日文识别。

可以在 `main.py` 中修改模型配置：

```python
model_dir = "FunAudioLLM/Fun-ASR-Nano-2512"
```

## 前端集成

前端应用已自动配置为使用本地 API，无需额外修改。

### 启动前端应用

```bash
# 回到项目根目录
cd ..

# 启动 Electron 应用
npm start
```

## 注意事项

1. **首次启动**: 首次启动时会自动下载 FunASR 模型，可能需要较长时间
2. **内存需求**: 模型加载需要约 1-2GB 内存
3. **性能**: CPU 模式下，识别速度可能较慢，建议使用 GPU 加速
4. **音频长度**: 建议音频文件长度不超过 60 秒，过长可能导致内存不足

## 故障排除

### 服务启动失败

- 检查 Python 版本是否为 3.8+（推荐 3.10+）
- 检查网络连接，首次启动需要下载模型
- 查看控制台输出的错误信息

### 识别结果不准确

- 确保音频文件清晰，无明显噪音
- 可以调整模型参数，如增加 hotwords
- 尝试使用更精确的模型

## 开发说明

### 依赖安装

```bash
pip install -r requirements.txt
```

### 手动启动服务

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

### API 测试

使用 Swagger 文档进行测试：
http://localhost:8000/docs

## 许可证

MIT License
