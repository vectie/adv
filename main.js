const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const remote = require('@electron/remote/main');
const FormData = require('form-data');

remote.initialize();

// 本地FunASR后端API地址
const LOCAL_API_URL = 'http://localhost:8000';

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: false,
      nodeIntegration: true
    }
  });

  remote.enable(mainWindow.webContents);
  mainWindow.loadFile('index.html');
  mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

ipcMain.handle('select-file', async () => {
  console.log('select-file called');
  try {
    console.log('mainWindow exists:', !!mainWindow);
    // 使用最简化的配置尝试打开对话框
    const result = await dialog.showOpenDialog(mainWindow);
    console.log('dialog result:', result);
    return result.filePaths[0] || null;
  } catch (error) {
    console.error('dialog error:', error);
    return null;
  }
});

ipcMain.handle('download-podcast', async (event, url) => {
  try {
    const response = await axios.get(url, { responseType: 'stream' });
    const ext = url.split('.').pop().split('?')[0];
    const filename = path.join(app.getPath('temp'), `${uuidv4()}.${ext}`);
    const writer = fs.createWriteStream(filename);
    
    response.data.pipe(writer);
    
    return new Promise((resolve, reject) => {
      writer.on('finish', () => resolve(filename));
      writer.on('error', reject);
    });
  } catch (error) {
    console.error('Download error:', error);
    throw error;
  }
});

ipcMain.handle('transcribe', async (event, audioPath) => {
  console.log('Starting transcription for:', audioPath);
  
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
    
    console.log('Local API result:', response.data);
    
    return response.data;
  } catch (error) {
    console.error('Transcription error:', error);
    return {
      status: 'error',
      message: error.response?.data?.detail || error.message
    };
  }
});