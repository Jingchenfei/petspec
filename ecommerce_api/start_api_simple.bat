@echo off

REM 使用绝对路径的简单批处理文件
echo 电商产品描述API启动器

echo.
REM 1. 检查Python是否安装
echo 正在检查Python环境...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到Python。请确保Python已安装并添加到系统PATH中。
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

echo 找到Python环境!

REM 2. 安装依赖
echo.
echo 步骤1: 安装项目依赖
echo 按任意键继续...
pause >nul
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo 错误: 依赖安装失败！
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

echo 依赖安装成功！

REM 3. 配置OpenAI API密钥提示
echo.
echo 步骤2: 配置OpenAI API密钥
echo 请确保你已经在.env文件中配置了有效的OpenAI API密钥
echo 按任意键继续...
pause >nul

REM 4. 启动API服务
echo.
echo 步骤3: 启动API服务
echo 正在启动服务...

REM 使用完整路径运行服务
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

REM 如果启动失败，显示错误信息
if %errorlevel% neq 0 (
    echo 错误: 服务启动失败！
    echo 按任意键退出...
    pause >nul
    exit /b 1
)

REM 这个命令通常不会执行到，因为uvicorn会一直运行
pause >nul