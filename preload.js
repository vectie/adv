const { ipcRenderer } = require('electron');

console.log('preload.js loaded');

// 当contextIsolation为false时，直接挂载到window对象
window.electronAPI = {
  selectFile: () => {
    console.log('preload: selectFile called');
    return ipcRenderer.invoke('select-file');
  },
  downloadPodcast: (url) => {
    console.log('preload: downloadPodcast called with url:', url);
    return ipcRenderer.invoke('download-podcast', url);
  },
  transcribe: (path) => {
    console.log('preload: transcribe called with path:', path);
    return ipcRenderer.invoke('transcribe', path);
  }
};

console.log('electronAPI mounted to window:', !!window.electronAPI);