#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uvicorn
import time
import logging
import traceback
import sys
import os

# 配置日志
sys_logger = logging.getLogger('uvicorn.error')
sys_logger.setLevel(logging.DEBUG)

# 设置文件日志
log_file = "server.log"
with open(log_file, "w") as f:
    f.write(f"[START] 服务器启动日志 - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Python版本: {sys.version}\n")

# 定义日志函数
def log_to_file(message):
    with open(log_file, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
    print(message)

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 获取环境变量配置
host = os.getenv('APP_HOST', '0.0.0.0')
port = int(os.getenv('APP_PORT', '8000'))
model_name = os.getenv('DEFAULT_MODEL', 'facebook/bart-large-cnn')

log_to_file("[DEBUG] 启动服务器配置检查")
log_to_file(f"[DEBUG] 当前工作目录: {os.getcwd()}")
log_to_file(f"[DEBUG] Python路径: {os.environ.get('PYTHONPATH', '未设置')}")
log_to_file(f"[DEBUG] 主机: {host}")
log_to_file(f"[DEBUG] 端口: {port}")
log_to_file(f"[DEBUG] 默认模型: {model_name}")
log_to_file(f"[DEBUG] 文件列表: {os.listdir('.')}")

# 检查main.py文件是否存在
if os.path.exists('main.py'):
    log_to_file("[DEBUG] main.py文件存在")
    # 检查文件内容的前几行
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            first_lines = ''.join(f.readlines()[:5])
            log_to_file(f"[DEBUG] main.py前几行: {first_lines}")
    except Exception as e:
        log_to_file(f"[ERROR] 无法读取main.py: {e}")
else:
    log_to_file("[ERROR] main.py文件不存在")

if __name__ == "__main__":
    try:
        log_to_file(f"[INFO] 准备启动UVicorn服务器")
        # 导入main模块进行测试
        try:
            import main
            log_to_file("[INFO] 成功导入main模块")
            if hasattr(main, 'app'):
                log_to_file("[INFO] main模块中存在app对象")
        except Exception as e:
            log_to_file(f"[ERROR] 导入main模块失败: {e}")
            traceback.print_exc(file=open(log_file, "a"))
            
        # 启动FastAPI应用
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=False,
            log_level="debug"
        )
    except Exception as e:
        log_to_file(f"[CRITICAL] 服务器启动失败: {e}")
        traceback.print_exc(file=open(log_file, "a"))