# 电商产品描述API

一键生成高质量电商产品描述的极简API服务，基于FastAPI和OpenAI API开发。

## 功能特点

- 🏆 **AI驱动**：基于OpenAI GPT模型生成专业、吸引人的产品描述
- 🎨 **多风格支持**：支持专业、亲切、活泼、高端、实惠五种语言风格
- 🌐 **多语言生成**：支持中文和英文两种语言
- 📝 **多版本文案**：一次可生成多个不同版本的描述
- 🔍 **SEO优化**：支持融入指定的SEO关键词
- ⚡ **快速响应**：基于FastAPI框架，提供高性能的API服务
- 📱 **易于集成**：提供完整的API文档和测试脚本

## 技术栈

- **后端框架**：FastAPI
- **服务器**：Uvicorn
- **AI模型**：OpenAI GPT系列
- **依赖管理**：pip
- **环境配置**：python-dotenv

## 快速开始

### 1. 安装依赖

```bash
# 进入项目目录
cd ecommerce-product-description-api

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

复制`.env`文件并填写您的OpenAI API密钥：

```bash
# 复制示例文件（如果没有.env文件）
# cp .env.example .env

# 编辑.env文件，填写您的OpenAI API密钥
# OPENAI_API_KEY=sk-your-api-key-here
```

### 3. 启动API服务

```bash
# 使用Uvicorn启动服务
uvicorn main:app --reload

# 或使用Python直接运行
python main.py

# 或使用启动脚本（推荐）
python start_server.py
```

服务将在`http://localhost:8000`启动。

### 4. 访问API文档

启动服务后，可以访问以下URL查看自动生成的API文档：
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API使用指南

### 健康检查端点

```bash
# 检查API是否正常运行
curl http://localhost:8000/health
```

### 生成产品描述端点

```bash
# 生成产品描述示例
curl -X POST "http://localhost:8000/generate-description" \
  -H "Content-Type: application/json" \
  -d '{"product_name": "智能保温杯", "product_category": "厨房用品", "key_features": ["24小时保温", "智能温度显示", "304不锈钢材质"], "target_audience": "上班族", "tone": "亲切", "language": "中文", "version_count": 2}'
```

### 请求参数说明

| 参数名 | 类型 | 是否必填 | 描述 |
|-------|------|---------|------|
| product_name | string | 是 | 产品名称 |
| product_category | string | 是 | 产品类别 |
| key_features | array | 是 | 产品主要特点列表 |
| target_audience | string | 是 | 目标受众描述 |
| tone | string | 是 | 描述风格（专业/亲切/活泼/高端/实惠） |
| language | string | 否 | 生成语言（中文/英文），默认中文 |
| version_count | integer | 否 | 生成的描述版本数量（1-3），默认1 |
| seo_keywords | array | 否 | SEO关键词列表 |

### 响应格式

```json
{
  "request_id": "req_12345678_abcdefg",
  "descriptions": [
    "生成的产品描述文本...",
    "另一个版本的产品描述文本..."
  ],
  "generation_time": 1.23
}
```

## 测试API

项目包含两个测试脚本：

1. 基础测试脚本 - 验证API基本功能
```bash
python test_api.py
```

2. 演示使用脚本 - 提供详细的API调用示例和结果展示
```bash
python demo_api_usage.py
```

## 部署指南

### 本地开发部署

使用上述的快速开始指南即可在本地部署开发版本。

### 生产环境部署

1. 使用Gunicorn作为WSGI服务器：

```bash
pip install gunicorn

gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

2. 使用Docker部署：

```bash
# 创建Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 构建镜像
# docker build -t ecommerce-product-description-api .

# 运行容器
# docker run -d -p 8000:8000 --env-file .env ecommerce-product-description-api
```

## 注意事项

1. **API密钥安全**：请妥善保管您的OpenAI API密钥，不要将其直接硬编码在代码中或提交到版本控制系统
2. **费用控制**：使用OpenAI API会产生费用，请合理设置`MAX_TOKENS`参数以控制每次请求的token使用量
3. **错误处理**：API包含基本的错误处理机制，但在生产环境中建议添加更多的监控和日志记录
4. **性能优化**：对于高并发场景，可以考虑添加缓存机制和请求速率限制

## 常见问题

### Q: 如何获取OpenAI API密钥？
A: 您需要在OpenAI官网注册账号并创建API密钥：[https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

### Q: 可以使用其他LLM模型吗？
A: 可以，修改`.env`文件中的`DEFAULT_MODEL`参数，支持OpenAI兼容的模型名称

### Q: API响应时间较长怎么办？
A: 这可能是由于LLM模型生成文本需要一定时间。您可以调整`temperature`参数或使用更轻量级的模型来提高响应速度

## 开发说明

本项目采用极简开发方案，遵循"易开发、低成本、短周期"的原则。如需扩展功能，可以考虑以下方向：

- 添加更多文本生成模板
- 支持更多语言和风格
- 集成其他LLM服务提供商
- 添加用户认证和授权机制
- 实现更复杂的缓存策略
- 开发管理后台界面