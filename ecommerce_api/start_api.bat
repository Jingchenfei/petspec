@echo off

REM 电商产品描述API启动脚本

REM 步骤1: 安装依赖
pip install -r requirements.txt

REM 步骤2: 提示用户配置API密钥
cls
echo ========================================================
echo             电商产品描述API启动脚本
========================================================
echo 
echo 请确保你已经在.env文件中配置了你的OpenAI API密钥！
echo 
echo 要编辑.env文件，请按任意键继续...
pause >nul
notepad .env

REM 步骤3: 启动API服务
cls
echo ========================================================
echo 正在启动API服务...
echo 服务启动后，可访问 http://localhost:8000/docs 查看API文档
echo 按Ctrl+C可以停止服务
echo ========================================================

echo 1. 使用启动脚本 (推荐)
echo 2. 直接运行主文件

echo 请选择启动方式 (输入1或2):
set /p choice=

if %choice%==1 (
python start_server.py
) else if %choice%==2 (
python main.py
) else (
echo 无效的选择，使用默认方式启动...
python start_server.py
)

pause