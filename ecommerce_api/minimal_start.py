#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
极简版启动脚本 - 专为Anaconda环境设计
"""

import os
import sys
import subprocess
import time

def main():
    try:
        # 显示基本信息
        print("=" * 50)
        print("  电商产品描述API - 极简启动器  ")
        print("=" * 50)
        print(f"Python路径: {sys.executable}")
        print(f"当前目录: {os.getcwd()}")
        print("=" * 50)
        
        # 步骤1: 安装依赖
        print("\n[1/3] 正在安装必要的依赖包...")
        # 注意：我们现在使用HuggingFace Transformers替代OpenAI
        required_packages = ['fastapi', 'uvicorn', 'transformers', 'torch', 'python-dotenv', 'pydantic', 'accelerate']
        
        # 使用--no-cache-dir参数确保获取最新版本
        install_cmd = [
            sys.executable, '-m', 'pip', 'install', '--no-cache-dir', '--upgrade'
        ] + required_packages
        
        # 直接打印安装过程的输出
        print(f"执行命令: {' '.join(install_cmd)}")
        subprocess.run(install_cmd, check=True)
        print("✓ 依赖安装成功!")
        
        # 步骤2: 检查.env文件
        print("\n[2/3] 检查.env文件配置...")
        env_path = '.env'
        
        if not os.path.exists(env_path):
            print("创建默认.env文件...")
            with open(env_path, 'w') as f:
                # HuggingFace模型配置
                f.write("# HuggingFace配置\n")
                f.write("# 默认使用中文电商产品描述模型\n")
                f.write("DEFAULT_MODEL=uer/gpt2-chinese-cluecorpussmall\n")
                f.write("# 生成参数配置\n")
                f.write("MAX_TOKENS=300\n")
                f.write("TEMPERATURE=0.7\n")
                f.write("TOP_P=0.95\n")
                f.write("\n# 应用配置\n")
                f.write("APP_HOST=0.0.0.0\n")
                f.write("APP_PORT=8000\n")
            print("✓ 创建.env文件成功! 已配置HuggingFace相关参数。")
        else:
            print("✓ 找到.env文件。")
        
        # 步骤3: 启动服务
        print("\n[3/3] 启动API服务...")
        print("服务将在 http://localhost:8000 启动")
        print("访问 http://localhost:8000/docs 查看API文档")
        print("按Ctrl+C可以停止服务")
        print("\n服务输出:\n")
        
        # 启动uvicorn服务
        uvicorn_cmd = [
            sys.executable, '-m', 'uvicorn', 'main:app', 
            '--host', '0.0.0.0', '--port', '8000', '--reload'
        ]
        
        subprocess.run(uvicorn_cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 错误: 命令执行失败，退出代码: {e.returncode}")
        input("按Enter键退出...")
    except KeyboardInterrupt:
        print("\n✓ 服务已停止")
    except Exception as e:
        print(f"\n✗ 发生错误: {str(e)}")
        input("按Enter键退出...")

if __name__ == "__main__":
    main()