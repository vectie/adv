const DOMController = require('./domController');
const UIRenderer = require('./uiRenderer');
// 直接使用electron模块，因为我们已经设置了nodeIntegration: true
const electron = require('electron');
const { dialog } = electron;

class AppController {
  constructor() {
    this.domController = new DOMController();
    this.uiRenderer = new UIRenderer(this.domController);
    this.transcriptionResult = null;
    
    this.initEventListeners();
    this.initModules();
  }

  initEventListeners() {
    // 文件选择按钮事件
    this.domController.selectFileBtn.addEventListener('click', async () => {
      await this.handleFileSelect();
    });

    // 开始转录按钮事件
    this.domController.startBtn.addEventListener('click', async () => {
      await this.handleStartTranscription();
    });

    // 分析按钮事件
    this.domController.analyzeBtn.addEventListener('click', async () => {
      await this.handleStartAnalysis();
    });

    // 清除选择按钮事件
    this.domController.clearSelectionBtn.addEventListener('click', () => {
      this.domController.clearModuleSelection();
    });
  }

  initModules() {
    // 定义所有16个模块
    this.modules = [
      {
        id: 'role-play',
        name: '角色扮演分析',
        description: '分析当前系统中的生态位，理解各参与者角色和关系，评估自身定位',
        endpoint: '/api/v1/role-play/analyze'
      },
      {
        id: 'future-prediction',
        name: '未来预测',
        description: '基于转录内容预测未来趋势和潜在后果，提供前瞻性洞察',
        endpoint: '/api/v1/future-prediction/predict'
      },
      {
        id: 'non-consensus',
        name: '非共识观点识别',
        description: '发现隐藏的非共识观点，识别打破常规的思考角度',
        endpoint: '/api/v1/non-consensus/identify'
      },
      {
        id: 'advantage-increment',
        name: '优势与增量分析',
        description: '识别超越平均水平的核心竞争力，发现个人成长和进步的关键点',
        endpoint: '/api/v1/advantage-increment/analyze'
      },
      {
        id: 'visualization',
        name: '可视化展示',
        description: '通过交互式画布展示复杂关系，使用多种图表类型呈现结构化数据',
        endpoint: '/api/v1/visualization/generate'
      },
      {
        id: 'actionable-advice',
        name: '可行动建议',
        description: '生成具体、可执行的行动方案，包含时间线和优先级',
        endpoint: '/api/v1/actionable-advice/generate'
      },
      {
        id: 'multi-perspective',
        name: '多角度提问',
        description: '从5个不同视角提出关键问题，拓展思考维度',
        endpoint: '/api/v1/multi-perspective-questions/generate'
      },
      {
        id: 'market-benchmark',
        name: '市场基准测试',
        description: '基于金融市场数据评估产品/服务效果，提供相对竞争力排名',
        endpoint: '/api/v1/market-benchmark/test'
      },
      {
        id: 'market-trend',
        name: '市场趋势捕捉',
        description: '识别市场风向和机会窗口，把握时机',
        endpoint: '/api/v1/market-trend/analyze'
      },
      {
        id: 'academic-paper',
        name: '学术论文扩展',
        description: '将分析扩展到学术层面，生成学术风格的分析报告',
        endpoint: '/api/v1/academic-paper/expand'
      },
      {
        id: 'regenerate-podcast',
        name: '再生Podcast',
        description: '基于原内容创建改进版本，形成内容迭代循环',
        endpoint: '/api/v1/regenerate-podcast/regenerate'
      },
      {
        id: 'cost-optimization',
        name: '计算成本优化',
        description: '优化计算成本，实现计算成本大于通信成本的高效学习',
        endpoint: '/api/v1/cost-optimization/optimize'
      },
      {
        id: 'failure-case',
        name: '失败案例分析',
        description: '分析失败案例，提供风险规避策略',
        endpoint: '/api/v1/failure-case/analyze'
      },
      {
        id: 'fact-opinion',
        name: '事实与观点区分',
        description: '区分转录内容中的事实陈述和主观观点，提供可信度评估',
        endpoint: '/api/v1/fact-opinion/distinguish'
      },
      {
        id: 'thinking-process',
        name: '思考过程拆解',
        description: '拆解成功人士的思考过程，生成可模仿的思考框架',
        endpoint: '/api/v1/thinking-process/analyze'
      },
      {
        id: 'feedback',
        name: '正反馈机制',
        description: '提供实时反馈、成就系统和个性化激励，可视化学习进步',
        endpoint: '/api/v1/feedback/generate'
      }
    ];
  }

  async handleFileSelect() {
    try {
      // 直接使用electron.dialog模块
      const result = await dialog.showOpenDialog({
        filters: [
          { name: 'Audio/Video Files', extensions: ['mp3', 'mp4', 'm4a', 'wav', 'aac'] },
          { name: 'All Files', extensions: ['*'] }
        ],
        properties: ['openFile']
      });
      
      const filePath = result.filePaths[0] || null;
      if (filePath) {
        this.domController.setSelectedFile(filePath);
        this.domController.clearUrlInput();
      }
    } catch (error) {
      console.error('选择文件出错:', error);
      this.uiRenderer.showError(error.message);
    }
  }

  async handleStartTranscription() {
    const selectedFile = this.domController.getSelectedFile();
    const url = this.domController.getUrlInput();
    
    if (!selectedFile && !url) {
      this.uiRenderer.showAlert('请选择本地文件或输入在线链接');
      return;
    }
    
    this.domController.showProgress();
    
    try {
      let audioPath;
      
      if (selectedFile) {
        this.domController.updateProgress('正在准备转录...', 50);
        audioPath = selectedFile;
      } else {
        this.domController.updateProgress('正在下载Podcast...', 30);
        audioPath = await window.electronAPI.downloadPodcast(url);
      }
      
      this.domController.updateProgress('正在转录并区分发言人...', 70);
      
      const result = await window.electronAPI.transcribe(audioPath);
      
      if (result.status === 'success') {
        this.transcriptionResult = result.transcription;
        this.uiRenderer.renderTranscription(result.transcription);
        this.domController.updateProgress('转录完成', 100);
        
        setTimeout(() => {
          this.domController.hideProgress();
          this.domController.showResult();
          this.domController.showModulesSection();
          // 渲染模块列表
          this.domController.renderModules(this.modules);
          // 渲染结果标签
          this.domController.renderResultsTabs([
            { id: 'transcription', title: '转录结果' },
            { id: 'analysis', title: '分析结果' }
          ]);
        }, 1000);
      }
    } catch (error) {
      console.error('Error:', error);
      this.uiRenderer.showError(error.message);
      this.domController.hideProgress();
    }
  }

  async handleStartAnalysis() {
    const selectedModules = this.domController.getSelectedModules();
    
    if (selectedModules.length === 0) {
      this.uiRenderer.showAlert('请至少选择一个分析模块');
      return;
    }
    
    this.domController.showProgress();
    this.domController.updateProgress('正在分析中...', 0);
    
    try {
      const analysisResults = [];
      
      // 依次调用每个选中模块的API
      for (let i = 0; i < selectedModules.length; i++) {
        const moduleId = selectedModules[i];
        const module = this.modules.find(m => m.id === moduleId);
        
        if (!module) continue;
        
        this.domController.updateProgress(`正在分析 ${module.name}...`, (i / selectedModules.length) * 80);
        
        // 调用后端API
        const result = await this.callBackendAPI(module.endpoint, this.transcriptionResult);
        
        analysisResults.push({
          moduleId: module.id,
          moduleName: module.name,
          result: result
        });
      }
      
      this.domController.updateProgress('分析完成', 100);
      
      setTimeout(() => {
        this.domController.hideProgress();
        this.domController.showResult();
        // 渲染分析结果
        this.renderAnalysisResults(analysisResults);
        // 切换到分析结果标签
        this.domController.resultsTabs.querySelector('[data-tab-id="analysis"]').click();
      }, 1000);
    } catch (error) {
      console.error('分析出错:', error);
      this.uiRenderer.showError(error.message);
      this.domController.hideProgress();
    }
  }

  async callBackendAPI(endpoint, data) {
    // 这里需要实现与后端API的通信
    // 由于我们在Electron环境中，需要通过主进程或直接调用后端API
    // 这里使用fetch API作为示例
    try {
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        throw new Error(`API请求失败: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API调用出错:', error);
      throw error;
    }
  }

  renderAnalysisResults(results) {
    // 渲染分析结果
    const resultsHTML = results.map(result => {
      return `
        <div class="analysis-item">
          <div class="analysis-title">${result.moduleName}</div>
          <div class="analysis-content">
            <pre style="background: #f1f5f9; padding: 15px; border-radius: 6px; overflow-x: auto;">${JSON.stringify(result.result, null, 2)}</pre>
          </div>
        </div>
      `;
    }).join('');
    
    this.domController.moduleResults.innerHTML = resultsHTML;
    this.domController.showModuleResults();
  }
}

module.exports = AppController;