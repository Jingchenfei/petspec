# 电商产品描述API - 入门指南

本指南将帮助你快速配置和开始使用电商产品描述API。

## 步骤1：配置环境变量

API需要OpenAI API密钥才能正常工作。请按照以下步骤配置环境变量：

1. 打开项目目录下的 `.env` 文件
2. 将你的OpenAI API密钥填入 `OPENAI_API_KEY` 字段中：

```env
# OpenAI API配置
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7

# API服务配置
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=True
```

> **提示：** 如果你还没有OpenAI API密钥，可以访问 [OpenAI官网](https://platform.openai.com/account/api-keys) 获取。

## 步骤2：安装依赖

确保你的Python版本为3.8或更高版本，然后安装项目所需的依赖：

```bash
# 在项目目录下执行以下命令
pip install -r requirements.txt
```

## 步骤3：启动API服务

你可以通过以下三种方式之一启动API服务：

### 方式1：使用启动脚本（推荐）

```bash
python start_server.py
```

### 方式2：使用Uvicorn命令

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 方式3：直接运行主文件

```bash
python main.py
```

服务启动后，你应该能看到类似以下的输出：

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 步骤4：使用API

API启动后，有三种主要方式可以使用它：

### 方式1：通过Swagger UI文档（推荐）

打开浏览器，访问 `http://localhost:8000/docs`，你将看到交互式API文档。在这里，你可以：

1. 查看API的所有端点
2. 了解请求和响应的格式
3. 直接在浏览器中测试API调用

### 方式2：使用演示脚本

项目中包含了一个演示脚本 `demo_api_usage.py`，它展示了如何调用API：

```bash
python demo_api_usage.py
```

运行后，你将看到API返回的智能手表产品描述示例。

### 方式3：使用基础测试脚本

项目中还包含了一个基础测试脚本 `test_api.py`，用于验证API的基本功能：

```bash
python test_api.py
```

## 步骤5：API调用示例

以下是使用Python `requests` 库调用API的基本示例：

```python
import requests
import json

# 健康检查API调用
def test_health_check():
    url = "http://localhost:8000/health"
    response = requests.get(url)
    print(f"健康检查响应: {response.json()}")

# 生成产品描述API调用
def generate_product_description():
    url = "http://localhost:8000/generate-description"
    headers = {"Content-Type": "application/json"}
    data = {
        "product_name": "智能手表Pro",
        "product_features": ["全天候心率监测", "血氧饱和度检测", "50米防水", "14天超长续航"],
        "product_type": "智能穿戴设备",
        "target_audience": "运动爱好者、健康关注者",
        "language": "zh",  # 或 "en" 英语
        "style": "professional",  # 可选: professional, friendly, lively, premium, affordable
        "seo_keywords": ["智能手表", "健康监测", "长续航"],
        "num_versions": 1  # 生成描述的版本数量
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(f"产品描述生成响应: {response.json()}")

# 运行测试
if __name__ == "__main__":
    test_health_check()
    generate_product_description()
```

## 步骤6：迁移项目到其他位置（可选）

如果你想将项目迁移到D盘或其他位置，可以按照以下步骤操作：

1. 复制整个 `ecommerce-product-description-api` 文件夹到目标位置
2. 更新 `.env` 文件中的配置（如果需要）
3. 在新位置重新安装依赖并启动服务

## 常见问题排查

### 问题：API服务无法启动

**可能原因：**
- 端口8000已被占用
- OpenAI API密钥配置错误
- 依赖包未正确安装

**解决方案：**
- 修改 `.env` 文件中的 `API_PORT` 为其他未被占用的端口
- 检查并确保OpenAI API密钥格式正确
- 重新安装依赖：`pip install -r requirements.txt`

### 问题：生成产品描述时返回错误

**可能原因：**
- OpenAI API密钥无效或余额不足
- 请求参数格式错误
- 网络连接问题

**解决方案：**
- 验证OpenAI API密钥的有效性
- 检查请求参数是否符合API文档中的要求
- 确认网络连接正常

### 问题：响应时间过长

**可能原因：**
- OpenAI API服务器响应缓慢
- 请求中设置了生成多个版本的描述
- 网络延迟

**解决方案：**
- 耐心等待，特别是在生成多个版本时
- 减少 `num_versions` 参数的值
- 检查网络连接质量

## 下一步做什么

成功配置并使用API后，你可以：

1. 探索不同的描述风格和语言选项
2. 根据实际需求调整产品信息和SEO关键词
3. 参考 `DEPLOYMENT.md` 文档将API部署到生产环境
4. 根据业务需求扩展API功能

如果你在使用过程中遇到任何问题，请随时查阅项目文档或联系技术支持。