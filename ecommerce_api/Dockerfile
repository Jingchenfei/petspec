# 使用Python 3.10官方镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（可能需要的编译工具）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制所有源代码文件
COPY . .

# 设置环境变量（默认值，实际部署时可通过--env-file覆盖）
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000
ENV DEFAULT_MODEL=gpt-3.5-turbo
ENV MAX_TOKENS=1000
ENV TEMPERATURE=0.7

# 暴露端口
EXPOSE 8000

# 设置启动命令
CMD ["python", "start_server.py"]