@echo off
REM 设置批处理文件的工作目录为当前目录
dir /b >nul 2>&1 || (echo 无法设置工作目录 & pause & exit /b 1)

REM 显示当前目录
echo 当前工作目录: %CD%

REM 显示环境变量信息
echo APP_PORT环境变量: %APP_PORT%

echo. & echo 正在启动API服务... & echo.

REM 运行主应用程序
python main.py

REM 如果上面的命令执行失败，显示错误信息并等待用户按键
if %errorlevel% neq 0 (
    echo. & echo 服务启动失败！ & echo.
    echo 请确保已安装所有依赖: pip install -r requirements.txt
    echo. & echo 按任意键退出...
    pause >nul
    exit /b %errorlevel%
)

REM 程序正常退出后的提示
if %errorlevel% equ 0 (
    echo. & echo 服务已停止 & echo.
    echo 按任意键退出...
    pause >nul
)