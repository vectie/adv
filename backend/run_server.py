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
    
    # 启动uvicorn服务器
    server_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "0.0.0.0",
        "--port", "8000",
        "--workers", "1"
    ], env=env)
    
    # 等待服务器启动
    time.sleep(5)
    
    # 检查服务器是否启动成功
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ FunASR backend server started successfully!")
            print("   API地址: http://localhost:8000")
            print("   健康检查: http://localhost:8000/health")
            print("   Swagger文档: http://localhost:8000/docs")
            return server_process
        else:
            print("❌ Server started but health check failed!")
            server_process.terminate()
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Failed to connect to server!")
        server_process.terminate()
        return None

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
