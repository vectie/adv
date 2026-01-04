// 渲染进程主入口文件
const AppController = require('./appController');

// 初始化应用控制器
window.appController = new AppController();

console.log('Podcast Transcriber App Initialized');