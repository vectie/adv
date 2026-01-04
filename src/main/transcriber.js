const axios = require('axios');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');

// 本地FunASR后端API地址
const LOCAL_API_URL = 'http://localhost:8000';

async function transcribeAudio(audioPath) {
  try {
    // 检查本地API是否可用
    try {
      await axios.get(`${LOCAL_API_URL}/health`);
    } catch (error) {
      return {
        status: 'error',
        message: '本地语音识别服务未启动，请先运行backend/run_server.py'
      };
    }
    
    // 调用本地FunASR API进行语音识别
    const formData = new FormData();
    const fileStream = fs.createReadStream(audioPath);
    formData.append('file', fileStream, { filename: path.basename(audioPath) });
    
    const response = await axios.post(`${LOCAL_API_URL}/transcribe`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  } catch (error) {
    console.error('Transcription error:', error);
    return {
      status: 'error',
      message: error.response?.data?.detail || error.message
    };
  }
}

module.exports = { transcribeAudio };