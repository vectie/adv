const { ipcRenderer } = require('electron');

console.log('preload.js loaded');

// 确保window对象存在
if (typeof window !== 'undefined') {
  // 直接挂载到window对象，因为contextIsolation为false
  window.electronAPI = {
    selectFile: async () => {
      console.log('preload: selectFile called');
      try {
        const result = await ipcRenderer.invoke('select-file');
        console.log('preload: selectFile result:', result);
        return result;
      } catch (error) {
        console.error('preload: selectFile error:', error);
        throw error;
      }
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
}