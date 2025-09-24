@echo off
REM 简单的API服务启动脚本
cd /d "%~dp0"
echo 正在启动API服务...
python start_server.py
if %errorlevel% neq 0 (
    echo 服务启动失败！
    echo 请按任意键退出...
    pause >nul
)
