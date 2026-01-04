import React, { useState, useEffect } from 'react';

const App = () => {
  // 状态管理
  const [audioWorkset, setAudioWorkset] = useState([]);
  const [urlInput, setUrlInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState('');
  const [selectedModules, setSelectedModules] = useState([]);
  const [chatMessages, setChatMessages] = useState([
    { id: 1, type: 'system', content: '欢迎使用智能播客分析平台！您可以添加音频文件到工作集，然后向我提问或选择分析功能。' }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [activeAudio, setActiveAudio] = useState(null);
  const [planetJourney, setPlanetJourney] = useState([
    { id: 1, name: '数据采集', status: 'completed', color: 'green' },
    { id: 2, name: '音频转录', status: 'pending', color: 'blue' },
    { id: 3, name: '内容分析', status: 'pending', color: 'purple' },
    { id: 4, name: '洞察生成', status: 'pending', color: 'orange' },
    { id: 5, name: '结果呈现', status: 'pending', color: 'red' }
  ]);

  // 定义分析模块
  const modules = [
    {
      id: 'role-play',
      name: '角色扮演分析',
      description: '分析当前系统中的生态位，理解各参与者角色和关系，评估自身定位'
    },
    {
      id: 'future-prediction',
      name: '未来预测',
      description: '基于转录内容预测未来趋势和潜在后果，提供前瞻性洞察'
    },
    {
      id: 'non-consensus',
      name: '非共识观点识别',
      description: '发现隐藏的非共识观点，识别打破常规的思考角度'
    },
    {
      id: 'advantage-increment',
      name: '优势与增量分析',
      description: '识别超越平均水平的核心竞争力，发现个人成长和进步的关键点'
    },
    {
      id: 'visualization',
      name: '可视化展示',
      description: '通过交互式画布展示复杂关系，使用多种图表类型呈现结构化数据'
    },
    {
      id: 'actionable-advice',
      name: '可行动建议',
      description: '生成具体、可执行的行动方案，包含时间线和优先级'
    }
  ];

  // 文件选择处理
  const handleFileSelect = async () => {
    // 触发隐藏的文件输入元素
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.mp3,.mp4,.m4a,.wav,.aac';
    fileInput.multiple = true;
    
    fileInput.onchange = (e) => {
      const files = Array.from(e.target.files);
      if (files.length > 0) {
        const newAudios = files.map(file => ({
          id: Date.now() + Math.random(),
          name: file.name,
          path: file.path || file.name,
          file,
          status: 'added',
          transcription: null,
          analysis: null
        }));
        setAudioWorkset(prev => [...prev, ...newAudios]);
        setUrlInput('');
      }
    };
    
    fileInput.click();
  };

  // 添加URL音频
  const handleAddUrlAudio = () => {
    if (!urlInput.trim()) {
      alert('请输入有效的播客URL');
      return;
    }
    
    const newAudio = {
      id: Date.now() + Math.random(),
      name: '在线播客',
      path: urlInput.trim(),
      status: 'added',
      transcription: null,
      analysis: null
    };
    
    setAudioWorkset(prev => [...prev, newAudio]);
    setUrlInput('');
  };

  // 开始处理音频
  const handleProcessAudio = async (audio) => {
    setActiveAudio(audio);
    setIsProcessing(true);
    setProgress(0);
    setStatusText('正在准备处理...');

    try {
      // 更新音频状态
      setAudioWorkset(prev => prev.map(item => 
        item.id === audio.id ? { ...item, status: 'processing' } : item
      ));

      // 模拟处理过程 - 数据采集
      await updatePlanetJourney(1, 'completed');
      for (let i = 0; i <= 20; i += 5) {
        await new Promise(resolve => setTimeout(resolve, 200));
        setProgress(i);
        setStatusText('正在采集音频数据...');
      }

      // 模拟处理过程 - 音频转录
      await updatePlanetJourney(2, 'completed');
      for (let i = 20; i <= 50; i += 5) {
        await new Promise(resolve => setTimeout(resolve, 200));
        setProgress(i);
        setStatusText('正在转录音频...');
      }

      // 模拟处理过程 - 内容分析
      await updatePlanetJourney(3, 'completed');
      for (let i = 50; i <= 80; i += 5) {
        await new Promise(resolve => setTimeout(resolve, 200));
        setProgress(i);
        setStatusText('正在分析内容...');
      }

      // 模拟处理过程 - 洞察生成
      await updatePlanetJourney(4, 'completed');
      for (let i = 80; i <= 95; i += 5) {
        await new Promise(resolve => setTimeout(resolve, 200));
        setProgress(i);
        setStatusText('正在生成洞察...');
      }

      // 模拟处理过程 - 结果呈现
      await updatePlanetJourney(5, 'completed');
      await new Promise(resolve => setTimeout(resolve, 300));
      setProgress(100);
      setStatusText('处理完成！');

      // 更新音频状态
      setAudioWorkset(prev => prev.map(item => 
        item.id === audio.id ? { 
          ...item, 
          status: 'processed',
          transcription: {
            text: '欢迎收听今天的播客节目，今天我们邀请到了一位非常特别的嘉宾。大家好，很高兴能来到这里和大家交流。能否请您介绍一下您最近在做的项目？当然可以，我们最近在开发一个跨平台的语音识别应用，它能够自动区分不同的说话人，并生成准确的文字稿。',
            speakers: [
              { id: 'speaker_1', name: '主持人', type: 'host' },
              { id: 'speaker_2', name: '嘉宾', type: 'guest' }
            ]
          },
          analysis: {
            summary: '这是对播客内容的分析摘要，包含了主要观点和关键信息。',
            insights: [
              '洞察1: 跨平台语音识别是当前热点',
              '洞察2: 说话人区分是核心技术难点',
              '洞察3: 准确的文字稿生成是基础需求'
            ]
          }
        } : item
      ));

      setIsProcessing(false);
    } catch (error) {
      console.error('处理失败:', error);
      setIsProcessing(false);
      alert('处理失败: ' + error.message);
    }
  };

  // 更新星球旅程状态
  const updatePlanetJourney = async (stepId, status) => {
    setPlanetJourney(prev => prev.map(step => 
      step.id === stepId ? { ...step, status } : step
    ));
    await new Promise(resolve => setTimeout(resolve, 500));
  };

  // 模块选择处理
  const toggleModuleSelection = (moduleId) => {
    setSelectedModules(prev => {
      if (prev.includes(moduleId)) {
        return prev.filter(id => id !== moduleId);
      } else {
        return [...prev, moduleId];
      }
    });
  };

  // 发送聊天消息
  const handleSendChat = () => {
    if (!chatInput.trim()) return;

    // 添加用户消息
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: chatInput
    };
    
    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');

    // 模拟AI回复
    setTimeout(() => {
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: `感谢您的提问："${chatInput}"。我正在分析相关内容，请稍候...`
      };
      setChatMessages(prev => [...prev, aiMessage]);
    }, 1000);
  };

  // 开始分析模块
  const handleStartAnalysis = () => {
    if (selectedModules.length === 0) {
      alert('请至少选择一个分析模块');
      return;
    }

    // 添加系统消息
    const systemMessage = {
      id: Date.now(),
      type: 'system',
      content: `已开始执行分析功能：${selectedModules.map(id => modules.find(m => m.id === id).name).join(', ')}`
    };
    
    setChatMessages(prev => [...prev, systemMessage]);
    setSelectedModules([]);
  };

  // 渲染星球可视化
  const renderPlanet = () => {
    return (
      <div className="relative w-full h-full flex items-center justify-center bg-gradient-to-br from-blue-900 to-purple-900 rounded-xl overflow-hidden">
        {/* 星球主体 */}
        <div className="relative w-64 h-64 rounded-full bg-gradient-to-br from-blue-400 to-purple-600 shadow-lg">
          {/* 星球纹理 */}
          <div className="absolute inset-0 rounded-full bg-[radial-gradient(circle_at_30%_30%,rgba(255,255,255,0.3)_0%,rgba(255,255,255,0)_50%)]"></div>
          <div className="absolute inset-0 rounded-full bg-[radial-gradient(circle_at_70%_70%,rgba(0,0,0,0.2)_0%,rgba(0,0,0,0)_50%)]"></div>
          
          {/* 旅行路径 */}
          {planetJourney.map((step, index) => (
            <React.Fragment key={step.id}>
              {/* 路径点 */}
              <div 
                className={`absolute w-4 h-4 rounded-full transition-all duration-500 ${step.status === 'completed' ? 'bg-green-400 scale-125' : 'bg-gray-400'}`}
                style={{
                  left: `${20 + index * 15}%`,
                  top: '50%',
                  transform: 'translate(-50%, -50%)'
                }}
              ></div>
              {/* 路径线 */}
              {index < planetJourney.length - 1 && (
                <div 
                  className={`absolute h-1 transition-all duration-500 ${planetJourney[index + 1].status === 'completed' ? 'bg-green-400' : 'bg-gray-600'}`}
                  style={{
                    left: `${25 + index * 15}%`,
                    top: '50%',
                    width: '10%',
                    transform: 'translateY(-50%)'
                  }}
                ></div>
              )}
              {/* 步骤标签 */}
              <div 
                className="absolute text-xs font-medium transition-all duration-500"
                style={{
                  left: `${20 + index * 15}%`,
                  top: '60%',
                  transform: 'translateX(-50%)',
                  color: step.status === 'completed' ? '#4ade80' : '#94a3b8'
                }}
              >
                {step.name}
              </div>
            </React.Fragment>
          ))}
        </div>
        
        {/* 卫星 */}
        <div className="absolute w-8 h-8 rounded-full bg-gray-400 shadow-lg animate-orbit" style={{ animationDelay: '0s' }}></div>
        <div className="absolute w-6 h-6 rounded-full bg-gray-500 shadow-lg animate-orbit" style={{ animationDelay: '-1s' }}></div>
        <div className="absolute w-5 h-5 rounded-full bg-gray-600 shadow-lg animate-orbit" style={{ animationDelay: '-2s' }}></div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary to-purple-600 p-4">
      <div className="flex flex-col h-screen">
        {/* 顶部标题栏 */}
        <header className="mb-4 text-white">
          <h1 className="text-3xl font-bold">智能播客分析平台</h1>
          <p className="text-sm opacity-80">Great adventure starts here!</p>
        </header>

        {/* 主体工作区 */}
        <div className="flex-1 flex gap-4 overflow-hidden">
          {/* 左侧：音频工作集 */}
          <div className="w-72 bg-white rounded-xl shadow-lg overflow-hidden flex flex-col">
            <div className="p-4 bg-neutral-100 border-b">
              <h2 className="text-lg font-semibold text-neutral-800">音频工作集</h2>
              <p className="text-xs text-neutral-600">添加和管理音频文件</p>
            </div>
            
            {/* 音频输入区域 */}
            <div className="p-4 border-b space-y-3">
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="输入播客URL"
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                  className="flex-1 px-3 py-2 border border-neutral-300 rounded-lg text-sm focus:outline-none focus:border-primary"
                />
                <button
                  onClick={handleAddUrlAudio}
                  className="px-3 py-2 bg-primary text-white rounded-lg text-sm hover:bg-primary/90 transition-colors"
                >
                  添加
                </button>
              </div>
              <button
                onClick={handleFileSelect}
                className="w-full px-3 py-2 bg-neutral-200 text-neutral-800 rounded-lg text-sm hover:bg-neutral-300 transition-colors"
              >
                选择本地文件
              </button>
            </div>
            
            {/* 音频列表 */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {audioWorkset.length === 0 ? (
                <div className="text-center py-8 text-neutral-500">
                  <div className="text-xl mb-2">📁</div>
                  <p>工作集为空，请添加音频文件</p>
                </div>
              ) : (
                audioWorkset.map(audio => (
                  <div 
                    key={audio.id}
                    className={`p-3 border rounded-lg cursor-pointer transition-all ${activeAudio?.id === audio.id ? 'border-primary bg-blue-50 shadow-md' : 'border-neutral-300 hover:border-primary hover:shadow-sm'}`}
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div className="font-medium text-sm text-neutral-800 truncate">
                        {audio.name}
                      </div>
                      <div className={`text-xs px-2 py-1 rounded-full ${audio.status === 'processing' ? 'bg-yellow-100 text-yellow-800' : audio.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                        {audio.status === 'processing' ? '处理中' : audio.status === 'completed' ? '已完成' : '待处理'}
                      </div>
                    </div>
                    <div className="text-xs text-neutral-600 truncate mb-3">
                      {audio.path}
                    </div>
                    <button
                      onClick={() => handleProcessAudio(audio)}
                      disabled={audio.status === 'processing'}
                      className={`w-full px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${audio.status === 'processing' ? 'bg-gray-200 text-gray-500 cursor-not-allowed' : 'bg-primary text-white hover:bg-primary/90'}`}
                    >
                      {audio.status === 'processing' ? '处理中...' : '开始处理'}
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* 中间：星球可视化和对话框 */}
          <div className="flex-1 flex flex-col gap-4">
            {/* 中间上侧：星球可视化 */}
            <div className="h-1/2 bg-white rounded-xl shadow-lg overflow-hidden">
              <div className="p-4 bg-neutral-100 border-b">
                <h2 className="text-lg font-semibold text-neutral-800">推理过程可视化</h2>
                <p className="text-xs text-neutral-600">星球旅行：从数据到洞察</p>
              </div>
              <div className="flex-1 p-4">
                {renderPlanet()}
              </div>
            </div>

            {/* 中间下侧：对话框 */}
            <div className="h-1/2 bg-white rounded-xl shadow-lg overflow-hidden flex flex-col">
              <div className="p-4 bg-neutral-100 border-b">
                <h2 className="text-lg font-semibold text-neutral-800">智能对话</h2>
                <p className="text-xs text-neutral-600">向AI提问或提出需求</p>
              </div>
              
              {/* 聊天消息 */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {chatMessages.map(message => (
                  <div key={message.id} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] p-3 rounded-lg ${message.type === 'user' ? 'bg-primary text-white' : message.type === 'ai' ? 'bg-neutral-100 text-neutral-800' : 'bg-blue-100 text-blue-800'}`}>
                      <p className="text-sm">{message.content}</p>
                    </div>
                  </div>
                ))}
              </div>
              
              {/* 聊天输入 */}
              <div className="p-4 border-t flex gap-3">
                <input
                  type="text"
                  placeholder="输入您的问题或需求..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendChat()}
                  className="flex-1 px-4 py-2 border border-neutral-300 rounded-lg focus:outline-none focus:border-primary"
                />
                <button
                  onClick={handleSendChat}
                  className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
                >
                  发送
                </button>
              </div>
            </div>
          </div>

          {/* 右侧：功能框 */}
          <div className="w-80 bg-white rounded-xl shadow-lg overflow-hidden flex flex-col">
            <div className="p-4 bg-neutral-100 border-b">
              <h2 className="text-lg font-semibold text-neutral-800">功能中心</h2>
              <p className="text-xs text-neutral-600">选择要开启的功能</p>
            </div>
            
            {/* 分析模块选择 */}
            <div className="p-4 border-b">
              <h3 className="font-medium text-sm text-neutral-800 mb-3">分析模块</h3>
              <div className="space-y-2 max-h-60 overflow-y-auto">
                {modules.map((module) => (
                  <div
                    key={module.id}
                    onClick={() => toggleModuleSelection(module.id)}
                    className={`p-3 border rounded-lg cursor-pointer transition-all text-sm ${selectedModules.includes(module.id) ? 'border-primary bg-blue-50' : 'border-neutral-200 hover:border-primary hover:bg-neutral-50'}`}
                  >
                    <div className="font-medium text-neutral-800">{module.name}</div>
                    <div className="text-xs text-neutral-600 mt-1">{module.description}</div>
                  </div>
                ))}
              </div>
              <button
                onClick={handleStartAnalysis}
                className="w-full mt-3 px-3 py-2 bg-green-500 text-white rounded-lg text-sm hover:bg-green-600 transition-colors"
              >
                开始分析
              </button>
            </div>
            
            {/* 进度显示 */}
            {isProcessing && (
              <div className="p-4 border-b bg-blue-50">
                <h3 className="font-medium text-sm text-neutral-800 mb-2">处理进度</h3>
                <div className="text-xs text-neutral-600 mb-3">{statusText}</div>
                <div className="w-full bg-neutral-200 rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
                <div className="text-right text-xs text-neutral-600 mt-1">{progress}%</div>
              </div>
            )}
            
            {/* 活跃音频信息 */}
            {activeAudio && (
              <div className="p-4 border-b">
                <h3 className="font-medium text-sm text-neutral-800 mb-2">活跃音频</h3>
                <div className="text-sm font-medium text-neutral-800 mb-1">{activeAudio.name}</div>
                <div className="text-xs text-neutral-600 truncate">{activeAudio.path}</div>
              </div>
            )}
            
            {/* 快速操作 */}
            <div className="p-4">
              <h3 className="font-medium text-sm text-neutral-800 mb-3">快速操作</h3>
              <div className="space-y-2">
                <button className="w-full px-3 py-2 bg-neutral-200 text-neutral-800 rounded-lg text-sm hover:bg-neutral-300 transition-colors">
                  📊 生成报告
                </button>
                <button className="w-full px-3 py-2 bg-neutral-200 text-neutral-800 rounded-lg text-sm hover:bg-neutral-300 transition-colors">
                  📤 导出结果
                </button>
                <button className="w-full px-3 py-2 bg-neutral-200 text-neutral-800 rounded-lg text-sm hover:bg-neutral-300 transition-colors">
                  ⚙️ 设置
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
