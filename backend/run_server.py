#!/usr/bin/env python3
"""
FunASR语音识别后端服务器启动脚本
"""
import os
import sys
import subprocess
import time
import requests

# 检查Python版本
if sys.version_info < (3, 8):
    print("Error: Python 3.8 or higher is required!")
    sys.exit(1)

# 安装依赖
def install_dependencies():
    print("Installing dependencies...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "-r", "requirements.txt"
    ], check=True)

# 启动服务器
def start_server():
    print("Starting FunASR backend server...")
    
    # 设置环境变量，使用CPU运行（如需GPU，将USE_GPU设为true）
    env = os.environ.copy()
    env["USE_GPU"] = "false"
    
    # 启动服务器
    server_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "0.0.0.0",
        "--port", "8000",
        "--workers", "1"
    ], env=env)
    
    # 增加模型加载时间，FunASR模型较大，需要更多时间加载
    print("正在加载FunASR模型，这可能需要几分钟...")
    time.sleep(60)  # 增加到60秒，给模型足够的加载时间
    
    # 检查服务器是否启动成功
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)  # 增加超时时间到10秒
        if response.status_code == 200:
            print("✅ FunASR backend server started successfully!")
            print("   API地址: http://localhost:8000")
            print("   健康检查: http://localhost:8000/health")
            print("   Swagger文档: http://localhost:8000/docs")
            return server_process
        else:
            print(f"❌ Server started but health check failed with status: {response.status_code}!")
            print(f"   Response: {response.text}")
            server_process.terminate()
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect to server!")
        print("   可能的原因: 模型加载时间过长或服务器启动失败")
        print("   解决方法: 增加sleep时间或检查模型下载是否完整")
        # 不立即终止，让服务器继续运行，用户可以手动检查
        print("   服务器仍在后台运行，您可以手动访问 http://localhost:8000/health 检查状态")
        return server_process
    except requests.exceptions.Timeout:
        print("❌ Health check timed out!")
        print("   模型可能仍在加载中，请稍等几分钟后手动检查")
        # 不立即终止，让服务器继续运行
        return server_process

# 主函数
def main():
    try:
        # 安装依赖
        install_dependencies()
        
        # 启动服务器
        server_process = start_server()
        if not server_process:
            sys.exit(1)
        
        # 保持服务器运行
        print("\n服务器正在运行中...")
        print("按 Ctrl+C 停止服务器")
        server_process.wait()
        
    except KeyboardInterrupt:
        print("\nStopping server...")
        if 'server_process' in locals():
            server_process.terminate()
            server_process.wait()
        print("✅ Server stopped!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
