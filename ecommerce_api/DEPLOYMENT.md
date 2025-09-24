# 电商产品描述API部署指南

本文档详细说明如何在不同环境中部署电商产品描述API服务。

## 目录

- [本地开发环境](#本地开发环境)
- [生产环境部署](#生产环境部署)
  - [使用Gunicorn](#使用gunicorn)
  - [使用Docker容器](#使用docker容器)
  - [Serverless部署（推荐）](#serverless部署（推荐）)
- [环境变量配置](#环境变量配置)
- [安全注意事项](#安全注意事项)
- [监控与维护](#监控与维护)

## 本地开发环境

### 前提条件
- Python 3.8+ 已安装
- 已获取OpenAI API密钥

### 部署步骤

1. **安装依赖**
   ```bash
   cd ecommerce-product-description-api
   pip install -r requirements.txt
   ```

2. **配置环境变量**
   编辑`.env`文件，填入您的OpenAI API密钥：
   ```bash
   OPENAI_API_KEY=sk-your-api-key-here
   ```

3. **启动服务**
   ```bash
   python start_server.py
   # 或
   uvicorn main:app --reload
   ```

4. **验证服务**
   打开浏览器访问：
   - API文档：[http://localhost:8000/docs](http://localhost:8000/docs)
   - 健康检查：[http://localhost:8000/health](http://localhost:8000/health)

## 生产环境部署

### 使用Gunicorn

1. **安装Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **启动服务**
   ```bash
   # 使用4个工作进程
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   
   # 或指定主机和端口
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
   ```

### 使用Docker容器

1. **前提条件**
   - Docker已安装并运行

2. **构建Docker镜像**
   ```bash
   docker build -t ecommerce-product-description-api .
   ```

3. **运行Docker容器**
   ```bash
   # 基础运行
   docker run -d -p 8000:8000 --env-file .env ecommerce-product-description-api
   
   # 持久化日志（可选）
   docker run -d -p 8000:8000 --env-file .env -v $(pwd)/logs:/app/logs ecommerce-product-description-api
   ```

### Serverless部署（推荐）

对于低成本、易扩展的部署方式，推荐使用Serverless平台。以下是使用Vercel或Netlify的简单步骤：

**使用Vercel部署**

1. 安装Vercel CLI
   ```bash
   npm install -g vercel
   ```

2. 创建`vercel.json`配置文件
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "main.py"
       }
     ]
   }
   ```

3. 部署到Vercel
   ```bash
   vercel
   ```

4. 在Vercel控制台设置环境变量
   - OPENAI_API_KEY
   - 其他必要的环境变量

## 环境变量配置

以下是API支持的所有环境变量及其默认值：

| 环境变量 | 默认值 | 描述 |
|---------|-------|------|
| OPENAI_API_KEY | - | **必填** OpenAI API密钥 |
| OPENAI_API_BASE | https://api.openai.com/v1 | OpenAI API基础URL |
| APP_HOST | 0.0.0.0 | 应用主机地址 |
| APP_PORT | 8000 | 应用端口号 |
| DEFAULT_MODEL | gpt-3.5-turbo | 默认使用的AI模型 |
| MAX_TOKENS | 1000 | 最大token数量限制 |
| TEMPERATURE | 0.7 | 生成文本的随机性（0-2） |

## 安全注意事项

1. **API密钥保护**
   - 永远不要将API密钥直接硬编码在代码中
   - 不要将`.env`文件提交到版本控制系统
   - 使用环境变量或密钥管理服务来存储API密钥

2. **请求限制**
   - 在生产环境中考虑添加请求速率限制
   - 可以使用FastAPI的`slowapi`等第三方库实现

3. **输入验证**
   - API已包含基本的输入验证，但在生产环境中建议增加更多的验证逻辑
   - 防止恶意输入和注入攻击

## 监控与维护

1. **日志记录**
   - API会输出基本的日志信息
   - 在生产环境中可以集成更完善的日志系统，如ELK Stack

2. **错误处理**
   - API包含基本的错误处理机制
   - 建议在生产环境中添加告警系统，及时发现和处理异常

3. **性能优化**
   - 对于高并发场景，可以考虑添加缓存机制
   - 监控API响应时间，必要时进行优化

## 常见问题排查

1. **服务启动失败**
   - 检查端口是否被占用
   - 确认Python依赖是否正确安装
   - 查看日志输出以获取具体错误信息

2. **OpenAI API调用失败**
   - 验证API密钥是否有效
   - 检查网络连接是否正常
   - 确认账户余额是否充足

3. **生成的描述质量不满足要求**
   - 尝试调整`TEMPERATURE`参数
   - 更换为更高级的模型（如`gpt-4`）
   - 优化输入的产品信息和特点描述