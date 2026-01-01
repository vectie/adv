# Podcast转录工具

一个支持本地文件和在线链接的Podcast转录桌面应用，能够自动区分主持人与嘉宾。

## 功能特性

- 📁 **支持本地文件**：MP3、MP4、M4A、WAV、AAC格式
- 🔗 **支持在线链接**：直接输入Podcast URL进行转录
- 🎤 **自动区分发言人**：识别主持人与嘉宾
- 💻 **跨平台支持**：Windows、macOS、Linux
- 📱 **移动端扩展准备**：保留iOS和Android适配可能性

## 技术栈

- **主框架**：Electron
- **前端**：HTML5 + CSS3 + JavaScript
- **后端服务**：Node.js
- **语音识别**：预留国内可用API接口（百度AI、阿里AI、腾讯AI等）
- **网络请求**：Axios

## 项目结构

```
podcast-transcriber/
├── index.html          # 主界面
├── main.js             # Electron主进程
├── preload.js          # 渲染进程与主进程通信
├── package.json        # 项目配置
├── .gitignore          # Git忽略文件
└── README.md           # 项目说明
```

## 安装与运行

### 环境要求

- Node.js 18.x 或更高版本
- npm 或 yarn

### 安装步骤

1. 克隆或下载项目到本地

2. 安装依赖
   ```bash
   npm install
   ```
   
   如果遇到依赖冲突，可以尝试：
   ```bash
   npm install --legacy-peer-deps
   ```

3. 运行应用
   ```bash
   npm start
   ```

### 构建应用

```bash
npm run build
```

## 使用说明

1. **选择本地文件**：点击"选择本地文件"按钮，选择您的Podcast文件
2. **或输入在线链接**：在输入框中粘贴Podcast的在线URL
3. **开始转录**：点击"开始转录"按钮
4. **查看结果**：转录完成后，会显示带有发言人标记的文字稿

## 核心功能说明

### 1. 文件处理流程

```
本地文件/在线URL → 下载（如果是URL）→ 格式转换为WAV → 语音识别 → 区分发言人 → 显示结果
```

### 2. 发言人区分

应用使用语音识别API的说话人分离功能，自动区分主持人与嘉宾。当前版本使用模拟数据，实际部署时需要配置Google Speech-to-Text API或其他语音识别服务。

### 3. 移动端扩展准备

- 代码结构设计考虑了跨平台兼容性
- 核心业务逻辑与界面分离
- 预留了API接口，方便后续集成移动端框架（如React Native）

## 配置说明

### 语音识别API配置

在`main.js`文件中，需要配置语音识别API：

```javascript
// 当前为模拟数据，实际使用时需要替换为真实API调用
ipcMain.handle('transcribe', async (event, audioPath) => {
  // 集成Google Speech-to-Text或其他语音识别服务
  // ...
});
```

### FFmpeg配置

需要在系统中安装FFmpeg：

- **Windows**：下载FFmpeg并添加到环境变量
- **macOS**：`brew install ffmpeg`
- **Linux**：`sudo apt install ffmpeg`

## 注意事项

1. 首次运行时，Electron会自动下载，可能需要较长时间
2. 语音识别需要网络连接（如果使用在线API）
3. 大文件转录可能需要较长时间
4. 确保系统已安装FFmpeg

## 未来规划

- [ ] 支持更多语音识别服务
- [ ] 增加文本编辑功能
- [ ] 支持导出为TXT、PDF、SRT格式
- [ ] 开发React Native版本（iOS/Android）
- [ ] 增加批量处理功能
- [ ] 支持实时转录

## 许可证

MIT License
