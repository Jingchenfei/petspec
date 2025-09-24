#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Anaconda环境专用启动脚本
这个脚本绕过批处理文件，直接在Python中执行所有必要的启动步骤
"""

import os
import sys
import subprocess
import time
import webbrowser

# 打印带颜色的消息
def print_color(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def print_green(text):
    print_color(text, "32")

def print_red(text):
    print_color(text, "31")

def print_yellow(text):
    print_color(text, "33")

def print_blue(text):
    print_color(text, "34")

# 检查并安装依赖
def install_dependencies():
    print_blue("[步骤1/4] 检查并安装项目依赖...")
    
    # 需要安装的包列表
    required_packages = [
        'fastapi',
        'uvicorn',
        'openai',
        'python-dotenv',
        'pydantic'
    ]
    
    try:
        # 检查pip是否可用
        subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 安装或更新依赖
        print("正在安装所需的Python包...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade'] + required_packages,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print_green("✓ 依赖安装成功!")
        else:
            print_yellow("警告: 依赖安装过程中有警告，但可能仍可运行。错误信息:\n")
            print(result.stderr)
            print_yellow("请确保所有必要的包都已正确安装")
            
    except Exception as e:
        print_red(f"✗ 依赖安装失败: {str(e)}")
        print_red("请检查您的Python环境或使用管理员权限运行此脚本")
        input("按Enter键退出...")
        sys.exit(1)

# 检查.env文件配置
def check_env_file():
    print_blue("[步骤2/4] 检查.env文件配置...")
    
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    
    if not os.path.exists(env_path):
        print_red("✗ 错误: 未找到.env文件!")
        create_default_env = input("是否创建默认.env文件? (y/n): ").strip().lower()
        if create_default_env == 'y':
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write("""
# OpenAI API配置
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
DEFAULT_MODEL=gpt-3.5-turbo
MAX_TOKENS=1000
TEMPERATURE=0.7

# 服务器配置
APP_HOST=0.0.0.0
APP_PORT=8000
                """.strip())
            print_yellow("已创建默认.env文件。请务必在启动前编辑此文件并填入真实的OpenAI API密钥!")
            input("按Enter键继续...")
        else:
            print_red("无法继续，必须有.env文件配置。")
            input("按Enter键退出...")
            sys.exit(1)
    else:
        # 检查API密钥是否已配置
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if 'sk-your-api-key-here' in content:
                print_yellow("⚠️ 警告: 您的.env文件中使用的是默认的API密钥占位符!")
                print_yellow("请编辑.env文件并填入真实的OpenAI API密钥，否则API调用将失败。")
                edit_now = input("是否现在打开.env文件进行编辑? (y/n): ").strip().lower()
                if edit_now == 'y':
                    if os.name == 'nt':  # Windows
                        os.startfile(env_path)
                    else:  # macOS/Linux
                        subprocess.run(['open', env_path] if sys.platform == 'darwin' else ['xdg-open', env_path])
                    print_yellow("请编辑完文件后保存并返回此窗口。")
                    input("按Enter键继续...")
            else:
                print_green("✓ .env文件配置已检查，发现API密钥已设置")

# 启动API服务
def start_api_service():
    print_blue("[步骤3/4] 准备启动API服务...")
    print("正在准备FastAPI应用...")
    
    # 定义启动参数
    host = "0.0.0.0"
    port = 8000
    
    # 构建启动命令
    cmd = [
        sys.executable,
        '-m', 'uvicorn',
        'main:app',
        '--reload',
        f'--host={host}',
        f'--port={port}'
    ]
    
    print_blue(f"[步骤4/4] 启动API服务...")
    print_green(f"✓ 服务将在 http://localhost:{port} 启动")
    print(f"服务启动后，可以访问 http://localhost:{port}/docs 查看API文档和测试接口")
    print("按Ctrl+C可以停止服务")
    print("\n=== 服务输出开始 ===\n")
    
    # 自动打开浏览器
    def open_browser():
        time.sleep(3)  # 等待服务启动
        try:
            webbrowser.open(f"http://localhost:{port}/docs")
        except Exception as e:
            print_yellow(f"无法自动打开浏览器: {str(e)}")
    
    # 在新线程中启动浏览器，避免阻塞服务启动
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # 启动服务
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n=== 服务已停止 ===")
    except Exception as e:
        print_red(f"\n\n✗ 服务启动失败: {str(e)}")
        input("按Enter键退出...")
        sys.exit(1)

# 主函数
def main():
    try:
        # 清除屏幕
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # 显示欢迎信息
        print("=" * 60)
        print_green("        电商产品描述API - Anaconda环境专用启动器        ")
        print("=" * 60)
        print(f"正在使用Python解释器: {sys.executable}")
        print(f"当前工作目录: {os.getcwd()}")
        print("=" * 60)
        
        # 执行步骤
        install_dependencies()
        check_env_file()
        start_api_service()
        
    except Exception as e:
        print_red(f"发生未预期的错误: {str(e)}")
        input("按Enter键退出...")
        sys.exit(1)

if __name__ == "__main__":
    main()