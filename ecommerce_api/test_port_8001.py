import uvicorn
from fastapi import FastAPI
import os

# 创建FastAPI应用
app = FastAPI()

# 根路由
@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI on port 8001"}

# 健康检查路由
@app.get("/health")
async def health_check():
    return {"status": "healthy", "port": 8001}

if __name__ == "__main__":
    # 打印环境变量以确认配置
    print(f"当前APP_PORT环境变量: {os.getenv('APP_PORT')}")
    
    # 使用8001端口运行服务
    uvicorn.run(
        "test_port_8001:app",
        host="127.0.0.1",
        port=8001,
        reload=False,
        workers=1
    )