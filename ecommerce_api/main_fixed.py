#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI
import os
import time
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from transformers import pipeline

# 确保中文显示正常
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 初始化FastAPI应用
app = FastAPI(
    title="E-commerce Product Description API",
    description="API for generating product descriptions",
    version="1.0.0"
)

# 产品信息模型
class ProductInfo(BaseModel):
    product_name: str = Field(..., description="产品名称")
    product_category: str = Field(..., description="产品类别")
    key_features: List[str] = Field(..., description="产品主要特性")
    target_audience: str = Field(..., description="目标受众")
    style: Optional[str] = Field("专业科技", description="描述风格")
    language: Optional[str] = Field("zh", description="语言")
    version_count: Optional[int] = Field(1, ge=1, le=5, description="生成的描述版本数")

# 加载模型（使用简单的模型进行测试）
# 注意：在实际部署时可能需要修改为适合的模型
model_name = os.getenv('DEFAULT_MODEL', 'sshleifer/distilbart-cnn-12-6')
try:
    nlp = pipeline("summarization", model=model_name)
except Exception as e:
    # 如果无法加载模型，创建一个简单的回退函数
    def simple_generate(text, max_length=150, min_length=30):
        return {
            "summary_text": f"这是{text[:20]}...的产品描述。该产品具有多项优势，适合目标用户使用。"
        }
    nlp = simple_generate

# 健康检查端点
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "model": model_name
    }

# 生成产品描述端点
@app.post("/generate-description")
async def generate_description(product_info: ProductInfo):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    try:
        # 构建用于生成描述的文本
        features_text = ", ".join(product_info.key_features)
        input_text = (
            f"产品名称：{product_info.product_name}\n" +
            f"产品类别：{product_info.product_category}\n" +
            f"主要特性：{features_text}\n" +
            f"目标受众：{product_info.target_audience}\n" +
            f"描述风格：{product_info.style}\n"
        )
        
        # 生成描述
        descriptions = []
        for _ in range(product_info.version_count):
            if callable(nlp):
                result = nlp(input_text)
            else:
                result = nlp(input_text, max_length=150, min_length=50, do_sample=True)
            
            if isinstance(result, dict) and "summary_text" in result:
                descriptions.append(result["summary_text"])
            elif isinstance(result, list) and len(result) > 0 and "summary_text" in result[0]:
                descriptions.append(result[0]["summary_text"])
            else:
                descriptions.append(f"这是{product_info.product_name}的产品描述。")
        
        generation_time = round(time.time() - start_time, 2)
        
        return {
            "request_id": request_id,
            "generation_time": generation_time,
            "descriptions": descriptions
        }
    except Exception as e:
        return {
            "request_id": request_id,
            "error": str(e),
            "status": "error"
        }