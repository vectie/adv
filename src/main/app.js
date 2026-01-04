const { app, BrowserWindow } = require('electron');
const path = require('path');
const remote = require('@electron/remote/main');
const { registerIpcHandlers } = require('./ipcHandlers');

remote.initialize();

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, '../../preload.js'),
      contextIsolation: false,
      nodeIntegration: true
    }
  });

  remote.enable(mainWindow.webContents);
  mainWindow.loadFile('index.html');
  mainWindow.webContents.openDevTools();
  
  return mainWindow;
}

app.whenReady().then(() => {
  const win = createWindow();
  registerIpcHandlers(win);

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

module.exports = { createWindow };