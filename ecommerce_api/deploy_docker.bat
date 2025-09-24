@echo off
REM 电商产品描述API - Docker部署脚本
REM 此脚本将帮助您在Windows环境下一键部署API服务

SETLOCAL ENABLEDELAYEDEXPANSION

REM 检查Docker是否已安装
where docker >nul 2>nul
if %errorlevel% neq 0 (
echo 错误：未找到Docker。请先安装Docker Desktop并确保它正在运行。
echo 可以从以下链接下载：https://www.docker.com/products/docker-desktop
echo 按任意键退出...
pause >nul
exit /b 1
)

REM 检查Docker服务是否正在运行
docker info >nul 2>nul
if %errorlevel% neq 0 (
echo 错误：Docker服务未运行。请启动Docker Desktop并等待服务就绪。
echo 按任意键退出...
pause >nul
exit /b 1
)

REM 检查.env文件是否存在
if not exist .env (
echo 警告：未找到.env文件，将使用默认配置
REM 创建默认.env文件
(echo DEFAULT_MODEL=uer/gpt2-chinese-cluecorpussmall
echo MAX_TOKENS=300
echo TEMPERATURE=0.7
echo TOP_P=0.95
echo APP_HOST=0.0.0.0
echo APP_PORT=8000) > .env
echo 已创建默认.env文件
)

REM 创建logs目录（用于持久化日志）
if not exist logs mkdir logs

REM 构建Docker镜像
echo 正在构建Docker镜像...
docker build -t ecommerce-product-description-api:latest .
if %errorlevel% neq 0 (
echo 错误：Docker镜像构建失败，请检查Dockerfile是否正确。
echo 按任意键退出...
pause >nul
exit /b 1
)

REM 停止并删除旧容器（如果存在）
echo 正在清理旧容器...
docker stop ecommerce-api >nul 2>nul
docker rm ecommerce-api >nul 2>nul

REM 运行新容器
echo 正在启动API服务容器...
docker run -d ^
--name ecommerce-api ^
-p 8000:8000 ^
--env-file .env ^
-v %cd%\logs:/app/logs ^
--restart unless-stopped ^
ecommerce-product-description-api:latest

if %errorlevel% neq 0 (
echo 错误：容器启动失败。
echo 按任意键查看详细错误日志...
pause >nul
docker logs ecommerce-api
pause >nul
exit /b 1
)

REM 显示部署状态
echo. 
echo ==================================================
echo 电商产品描述API部署成功！
echo ==================================================
echo 服务状态：正在运行
echo 访问地址：http://localhost:8000
echo 容器名称：ecommerce-api
echo 日志目录：%cd%\logs
echo. 
echo 您可以使用以下命令查看服务状态和日志：
echo - 查看容器状态：docker ps -a ^| findstr ecommerce-api
echo - 查看服务日志：docker logs ecommerce-api
echo - 停止服务：docker stop ecommerce-api
echo - 启动服务：docker start ecommerce-api
echo. 
echo API端点：
echo - 健康检查：http://localhost:8000/health
echo - 根路由：http://localhost:8000/
echo - 描述生成：http://localhost:8000/generate-description [POST]
echo. 
echo 按任意键查看API服务初始化日志...
pause >nul
docker logs ecommerce-api

REM 提示用户测试API
echo. 
echo 建议：您可以使用demo_api_usage.py脚本测试API功能
echo 命令：python demo_api_usage.py
echo 按任意键退出...
pause >nul

ENDLOCAL