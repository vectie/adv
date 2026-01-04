const { ipcMain, dialog } = require('electron');
const { downloadPodcast } = require('./downloader');
const { transcribeAudio } = require('./transcriber');

function registerIpcHandlers(win) {
  // 文件选择处理
  ipcMain.handle('select-file', async () => {
    console.log('select-file called');
    try {
      const result = await dialog.showOpenDialog(win, {
        filters: [{ name: 'Audio/Video Files', extensions: ['mp3', 'mp4', 'm4a', 'wav', 'aac'] }],
        properties: ['openFile']
      });
      console.log('dialog result:', result);
      return result.filePaths[0] || null;
    } catch (error) {
      console.error('dialog error:', error);
      return null;
    }
  });

  // Podcast下载处理
  ipcMain.handle('download-podcast', async (event, url) => {
    try {
      return await downloadPodcast(url);
    } catch (error) {
      console.error('Download error:', error);
      throw error;
    }
  });

  // 转录处理
  ipcMain.handle('transcribe', async (event, audioPath) => {
    console.log('Starting transcription for:', audioPath);
    try {
      return await transcribeAudio(audioPath);
    } catch (error) {
      console.error('Transcription error:', error);
      return {
        status: 'error',
        message: error.response?.data?.detail || error.message
      };
    }
  });
}

module.exports = { registerIpcHandlers };