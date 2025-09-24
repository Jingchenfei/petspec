#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uvicorn
import os

# 确保中文显示正常
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 获取环境变量配置
host = os.getenv('APP_HOST', '0.0.0.0')
port = int(os.getenv('APP_PORT', '8000'))
app_module = os.getenv('APP_MODULE', 'main:app')  # 默认使用main:app，但可以通过环境变量覆盖

if __name__ == "__main__":
    print(f"启动配置: host={host}, port={port}, app_module={app_module}")
    # 启动FastAPI应用
    uvicorn.run(
        app_module,
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )