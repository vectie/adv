class DOMController {
  constructor() {
    this.selectFileBtn = document.getElementById('selectFileBtn');
    this.fileInfo = document.getElementById('fileInfo');
    this.urlInput = document.getElementById('urlInput');
    this.startBtn = document.getElementById('startBtn');
    this.progressSection = document.getElementById('progressSection');
    this.statusText = document.getElementById('statusText');
    this.progressFill = document.getElementById('progressFill');
    this.resultSection = document.getElementById('resultSection');
    this.transcriptionResult = document.getElementById('transcriptionResult');
    this.modulesSection = document.getElementById('modulesSection');
    this.modulesGrid = document.getElementById('modulesGrid');
    this.analyzeBtn = document.getElementById('analyzeBtn');
    this.clearSelectionBtn = document.getElementById('clearSelectionBtn');
    this.resultsTabs = document.getElementById('resultsTabs');
    this.moduleResults = document.getElementById('moduleResults');
  }

  getSelectedFile() {
    return this._selectedFile;
  }

  setSelectedFile(filePath) {
    this._selectedFile = filePath;
    this.fileInfo.textContent = filePath ? filePath.split('\\').pop() : '未选择文件';
  }

  getUrlInput() {
    return this.urlInput.value.trim();
  }

  clearUrlInput() {
    this.urlInput.value = '';
  }

  showProgress() {
    this.progressSection.style.display = 'block';
    this.resultSection.style.display = 'none';
    this.transcriptionResult.innerHTML = '';
  }

  hideProgress() {
    this.progressSection.style.display = 'none';
  }

  showResult() {
    this.resultSection.style.display = 'block';
  }

  updateProgress(status, percentage) {
    this.statusText.textContent = status;
    this.progressFill.style.width = `${percentage}%`;
  }

  clearResult() {
    this.transcriptionResult.innerHTML = '';
  }

  // 模块选择相关方法
  showModulesSection() {
    this.modulesSection.style.display = 'block';
  }

  hideModulesSection() {
    this.modulesSection.style.display = 'none';
  }

  renderModules(modules) {
    this.modulesGrid.innerHTML = '';
    
    modules.forEach(module => {
      const moduleCard = document.createElement('div');
      moduleCard.className = 'module-card';
      moduleCard.dataset.moduleId = module.id;
      moduleCard.innerHTML = `
        <div class="module-title">${module.name}</div>
        <div class="module-description">${module.description}</div>
      `;
      
      moduleCard.addEventListener('click', () => {
        moduleCard.classList.toggle('selected');
      });
      
      this.modulesGrid.appendChild(moduleCard);
    });
  }

  getSelectedModules() {
    const selectedCards = this.modulesGrid.querySelectorAll('.module-card.selected');
    return Array.from(selectedCards).map(card => card.dataset.moduleId);
  }

  clearModuleSelection() {
    const selectedCards = this.modulesGrid.querySelectorAll('.module-card.selected');
    selectedCards.forEach(card => card.classList.remove('selected'));
  }

  // 结果展示相关方法
  renderResultsTabs(tabs) {
    this.resultsTabs.innerHTML = '';
    
    tabs.forEach((tab, index) => {
      const tabElement = document.createElement('div');
      tabElement.className = `tab ${index === 0 ? 'active' : ''}`;
      tabElement.textContent = tab.title;
      tabElement.dataset.tabId = tab.id;
      
      tabElement.addEventListener('click', () => {
        // 移除所有tab的active类
        this.resultsTabs.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        // 添加当前tab的active类
        tabElement.classList.add('active');
        // 显示对应的内容
        this.showTabContent(tab.id);
      });
      
      this.resultsTabs.appendChild(tabElement);
    });
  }

  showTabContent(tabId) {
    // 显示或隐藏不同的内容区域
    if (tabId === 'transcription') {
      this.transcriptionResult.style.display = 'block';
      this.moduleResults.style.display = 'none';
    } else {
      this.transcriptionResult.style.display = 'none';
      this.moduleResults.style.display = 'block';
    }
  }

  showModuleResults() {
    this.moduleResults.style.display = 'block';
  }

  hideModuleResults() {
    this.moduleResults.style.display = 'none';
  }

  renderModuleResults(results) {
    this.moduleResults.innerHTML = '';
    
    results.forEach(result => {
      const resultDiv = document.createElement('div');
      resultDiv.className = 'analysis-item';
      resultDiv.innerHTML = `
        <div class="analysis-title">${result.moduleName}分析结果</div>
        <div class="analysis-content">${result.content}</div>
      `;
      
      this.moduleResults.appendChild(resultDiv);
    });
  }
}

module.exports = DOMController;