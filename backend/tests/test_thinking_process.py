import pytest
from app.services.thinking_process import ThinkingProcessService

class TestThinkingProcessService:
    def setup_method(self):
        self.thinking_service = ThinkingProcessService()
    
    def test_analyze_thinking_process(self):
        """测试思考过程分析功能"""
        # 准备测试数据
        transcription = [
            {
                "speaker": "主持人",
                "text": "首先，我认为我们需要分析当前的市场状况。因为市场变化很快，所以我们必须及时调整策略。"
            },
            {
                "speaker": "嘉宾",
                "text": "我同意你的观点。如果我们不做出改变，可能会面临很大的挑战。核心问题是如何平衡短期利益和长期发展。"
            }
        ]
        
        # 调用思考过程分析服务
        result = self.thinking_service.analyze_thinking_process(transcription)
        
        # 验证结果格式
        assert result["status"] == "success"
        assert "thinking_steps" in result
        assert "thinking_models" in result
        assert "visualization" in result
        
        # 验证思考步骤被正确提取
        assert len(result["thinking_steps"]) > 0
        for step in result["thinking_steps"]:
            assert "id" in step
            assert "speaker" in step
            assert "text" in step
            assert "type" in step
            assert step["type"] in ["分析型", "决策型", "创新型", "批判性", "综合型"]
        
        # 验证可视化数据格式
        assert "nodes" in result["visualization"]
        assert "edges" in result["visualization"]
        assert len(result["visualization"]["nodes"]) > 0
    
    def test_classify_thinking_type(self):
        """测试思考类型分类功能"""
        # 测试分析型思考
        analytical_text = "因为市场需求增加，所以我们的销售额上升了。"
        assert ThinkingProcessService._classify_thinking_type(analytical_text) == "分析型"
        
        # 测试决策型思考
        decision_text = "我们应该增加研发投入，提升产品竞争力。"
        assert ThinkingProcessService._classify_thinking_type(decision_text) == "决策型"
        
        # 测试创新型思考
        creative_text = "如果我们尝试新的商业模式，可能会打开更大的市场。"
        assert ThinkingProcessService._classify_thinking_type(creative_text) == "创新型"
        
        # 测试批判性思考
        critical_text = "这个方案的核心问题在于成本控制，我们需要重新评估。"
        assert ThinkingProcessService._classify_thinking_type(critical_text) == "批判性"
        
        # 测试综合型思考
        comprehensive_text = "根据以上分析，我们可以得出以下结论。"
        assert ThinkingProcessService._classify_thinking_type(comprehensive_text) == "综合型"
    
    def test_identify_thinking_models(self):
        """测试思维模型识别功能"""
        # 准备测试数据
        thinking_steps = [
            {
                "id": 1,
                "speaker": "主持人",
                "text": "首先，我们需要分析优势和劣势，然后看机会和威胁。",
                "type": "分析型",
                "position": 0
            },
            {
                "id": 2,
                "speaker": "嘉宾",
                "text": "什么是问题的核心？为什么会出现这个问题？我们应该如何解决？",
                "type": "批判性",
                "position": 1
            }
        ]
        
        # 调用思维模型识别
        models = self.thinking_service._identify_thinking_models(thinking_steps)
        
        # 验证结果
        assert len(models) > 0
        model_names = [model["name"] for model in models]
        assert "SWOT分析" in model_names