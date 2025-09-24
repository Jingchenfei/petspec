@echo off

REM 开启命令回显，让你能看到每个命令的执行情况
echo 正在启动电商产品描述API服务...
echo 此窗口将在执行结束后保持打开状态，以便查看错误信息

echo.
echo 步骤1: 安装项目依赖
echo.----------------------------------------
pip install -r requirements.txt

REM 检查pip命令是否执行成功
if %errorlevel% neq 0 (
    echo 错误: 依赖安装失败！请按任意键退出...
    pause >nul
    exit /b 1
)

echo.
echo 步骤2: 配置OpenAI API密钥
echo.----------------------------------------
echo 请确保你已经在.env文件中配置了有效的OpenAI API密钥
echo 按任意键继续...
pause >nul

echo.
echo 步骤3: 启动API服务
echo.----------------------------------------
echo 请选择启动方式:
echo 1. 使用启动脚本 (start_server.py)
echo 2. 直接运行主程序 (main.py)

echo.
set /p choice="请输入选项 (1 或 2): "

echo.
if %choice% equ 1 (
    echo 正在使用启动脚本启动服务...
    python start_server.py
) else if %choice% equ 2 (
    echo 正在直接运行主程序...
    python main.py
) else (
    echo 无效的选项，默认使用启动脚本
    python start_server.py
)

REM 检查服务启动是否成功
if %errorlevel% neq 0 (
    echo 错误: 服务启动失败！请查看上面的错误信息
) else (
    echo 服务启动成功！
)

echo.
echo 按任意键退出...
pause >nul