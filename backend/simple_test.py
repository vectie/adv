#!/usr/bin/env python3
"""
FunASR模型简单测试脚本
使用更简单的配置和模型
"""
import sys

# 先尝试导入torch，确保PyTorch已安装
try:
    import torch
    print(f"✅ PyTorch已安装: {torch.__version__}")
except ImportError:
    print("❌ PyTorch未安装")
    sys.exit(1)

# 尝试导入funasr
try:
    from funasr import AutoModel
    print(f"✅ FunASR已安装")
except ImportError as e:
    print(f"❌ FunASR导入失败: {e}")
    sys.exit(1)

def simple_test():
    """简单测试FunASR模型"""
    print("\n正在进行简单测试...")
    
    try:
        # 使用更简单的模型配置，避免远程代码问题
        print("正在加载模型...")
        
        # 使用本地模型或更简单的模型
        model = AutoModel(
            model="FunAudioLLM/Fun-ASR-Nano-2512",
            trust_remote_code=True,
            remote_code=None,  # 不使用远程代码
            device="cpu",
            disable_update=True,  # 禁用更新检查
        )
        
        print("✅ 模型加载成功!")
        print("✅ FunASR简单测试通过!")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print("\n详细错误信息:")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    simple_test()