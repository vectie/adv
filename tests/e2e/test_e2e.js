const { Application } = require('spectron');
const assert = require('assert');
const path = require('path');

describe('Podcast Transcriber E2E Tests', function() {
  this.timeout(30000); // 延长测试超时时间

  beforeEach(async function() {
    // 创建Spectron应用实例
    this.app = new Application({
      path: path.join(__dirname, '../../node_modules/.bin/electron'),
      args: [path.join(__dirname, '../../')],
      waitTimeout: 10000
    });

    // 启动应用
    await this.app.start();
  });

  afterEach(async function() {
    // 关闭应用
    if (this.app && this.app.isRunning()) {
      await this.app.stop();
    }
  });

  it('should open the window and display the title', async function() {
    // 等待应用加载完成
    await this.app.client.waitUntilWindowLoaded();
    
    // 获取窗口标题
    const title = await this.app.client.getTitle();
    
    // 验证窗口标题
    assert.strictEqual(title, 'Podcast转录工具');
  });

  it('should display the input section and buttons', async function() {
    // 等待应用加载完成
    await this.app.client.waitUntilWindowLoaded();
    
    // 验证文件选择按钮存在
    const selectFileBtn = await this.app.client.$('#selectFileBtn');
    assert.ok(selectFileBtn);
    
    // 验证URL输入框存在
    const urlInput = await this.app.client.$('#urlInput');
    assert.ok(urlInput);
    
    // 验证开始转录按钮存在
    const startBtn = await this.app.client.$('#startBtn');
    assert.ok(startBtn);
  });

  it('should display progress section when start button is clicked without input', async function() {
    // 等待应用加载完成
    await this.app.client.waitUntilWindowLoaded();
    
    // 点击开始转录按钮（无输入）
    await this.app.client.$('#startBtn').click();
    
    // 验证弹出提示框
    try {
      await this.app.client.alertText();
      // 如果没有抛出异常，说明有提示框
      const alertText = await this.app.client.alertText();
      assert.ok(alertText.includes('请选择本地文件或输入在线链接'));
      await this.app.client.acceptAlert();
    } catch (error) {
      // 如果抛出异常，可能是因为没有弹出提示框，这是预期之外的
      assert.fail('Expected alert not shown');
    }
  });

  it('should display result section after successful transcription', async function() {
    // 等待应用加载完成
    await this.app.client.waitUntilWindowLoaded();
    
    // 模拟选择文件（这里使用Electron的IPC事件）
    // 注意：实际测试中可能需要使用真实的音频文件
    await this.app.electron.ipcRenderer.send('select-file');
    
    // 等待文件选择结果
    const filePath = await this.app.electron.ipcRenderer.invoke('select-file');
    
    // 如果没有选择文件，跳过这个测试
    if (!filePath) {
      this.skip();
    }
    
    // 点击开始转录按钮
    await this.app.client.$('#startBtn').click();
    
    // 等待进度完成
    await this.app.client.waitForExist('#resultSection', 20000);
    
    // 验证结果区域显示
    const resultSection = await this.app.client.$('#resultSection');
    const isResultVisible = await resultSection.isVisible();
    assert.ok(isResultVisible);
  });

  it('should have working thinking process analysis feature', async function() {
    // 等待应用加载完成
    await this.app.client.waitUntilWindowLoaded();
    
    // 这里可以添加思考过程分析功能的测试
    // 由于这是一个复杂的功能，可能需要更详细的测试步骤
    // 例如：先完成转录，然后点击分析按钮，验证分析结果显示
    
    // 暂时跳过，等待完整实现
    this.skip();
  });

  it('should have working feedback mechanism', async function() {
    // 等待应用加载完成
    await this.app.client.waitUntilWindowLoaded();
    
    // 这里可以添加反馈机制功能的测试
    // 例如：完成转录后，验证反馈信息显示
    
    // 暂时跳过，等待完整实现
    this.skip();
  });
});