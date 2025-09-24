@echo off

REM 最简化的API启动脚本 - 确保使用完整路径
color 0A
cls

echo ====================================================
echo              电商产品描述API启动器
echo ====================================================
echo.

REM 步骤1: 检查Python是否可用
echo [步骤1/4] 检查Python环境...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到Python! 请确保Python已安装并添加到系统PATH中。
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

REM 显示Python版本信息
echo 已找到Python环境，正在显示版本信息...
python --version
echo.

REM 步骤2: 安装依赖
echo [步骤2/4] 安装项目依赖...
echo 正在安装所需的Python包...
python -m pip install uvicorn openai python-dotenv requests
if %errorlevel% neq 0 (
    echo 错误: 依赖安装失败! 请检查网络连接或使用管理员权限运行此脚本。
    echo 按任意键退出...
    pause >nul
    exit /b 1
)
echo 依赖安装成功!
echo.

REM 步骤3: 提示配置OpenAI API密钥
echo [步骤3/4] 配置OpenAI API密钥...
echo 请确认你已经在.env文件中配置了有效的OpenAI API密钥
echo 如果尚未配置，现在可以打开.env文件进行编辑
echo.
echo 按任意键继续启动服务...
pause >nul

REM 步骤4: 启动API服务
echo [步骤4/4] 启动API服务...
echo 正在使用uvicorn启动FastAPI服务...
echo 服务启动后，可以访问 http://localhost:8000/docs 进行测试
echo 按Ctrl+C可以停止服务
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

REM 如果服务启动失败，显示错误信息
if %errorlevel% neq 0 (
    echo.
echo 错误: 服务启动失败! 请检查上面的错误信息。
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

REM 这个命令通常不会执行到，因为uvicorn会一直运行
echo 按任意键退出...
pause >nul