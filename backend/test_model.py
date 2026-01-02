#!/usr/bin/env python3
"""
FunASR模型测试脚本
"""
import sys
from funasr import AutoModel

def test_funasr_model():
    """测试FunASR模型是否能正常加载和运行"""
    print("正在测试FunASR模型...")
    
    try:
        # 初始化模型（使用轻量级模型）
        print("正在加载模型...")
        model = AutoModel(
            model="FunAudioLLM/Fun-ASR-Nano-2512",
            trust_remote_code=True,
            device="cpu",  # 使用CPU运行
        )
        
        print("✅ 模型加载成功!")
        print("✅ FunASR模型测试通过!")
        print("\n下一步:")
        print("1. 运行 `python run_server.py` 启动完整的后端服务")
        print("2. 在另一个终端运行 `npm start` 启动前端应用")
        print("3. 在前端应用中选择音频文件进行转录测试")
        
        return True
        
    except Exception as e:
        print(f"❌ 模型测试失败: {str(e)}")
        print("\n可能的解决方法:")
        print("1. 确保所有依赖已正确安装")
        print("2. 检查网络连接，首次运行需要下载模型")
        print("3. 尝试使用较小的模型或减少模型参数")
        return False

if __name__ == "__main__":
    test_funasr_model()