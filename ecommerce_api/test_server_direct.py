import uvicorn
from fastapi import FastAPI
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import time

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'server_test.log',
            maxBytes=5*1024*1024,
            backupCount=3
        ),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("test_server")

# 创建FastAPI应用
app = FastAPI()

# 根路由
@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Hello World from FastAPI on port 8001", "timestamp": time.time()}

# 健康检查路由
@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "port": 8001, "timestamp": time.time()}

if __name__ == "__main__":
    try:
        # 打印环境变量以确认配置
        logger.info(f"当前APP_PORT环境变量: {os.getenv('APP_PORT')}")
        logger.info(f"Python版本: {sys.version}")
        logger.info("尝试在端口8001启动服务...")
        
        # 使用8001端口运行服务
        uvicorn.run(
            "test_server_direct:app",
            host="127.0.0.1",
            port=8001,
            reload=False,
            workers=1,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}")
        print(f"服务启动失败: {str(e)}")
        # 将错误信息写入文件以便查看
        with open("server_error.log", "w") as f:
            f.write(f"服务启动失败: {str(e)}")