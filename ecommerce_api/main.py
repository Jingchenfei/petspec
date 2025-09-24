from fastapi import FastAPI
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import uuid
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from dotenv import load_dotenv
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from fastapi import FastAPI
import logging

# 加载.env文件中的环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("product_description_api")

# 初始化FastAPI应用
app = FastAPI(
    title="E-commerce Product Description API",
    description="API for generating product descriptions",
    version="1.0.0"
)

# 加载模型和分词器
try:
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "uer/gpt2-chinese-cluecorpussmall")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "300"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P = float(os.getenv("TOP_P", "0.95"))
    
    logger.info(f"Loading model: {DEFAULT_MODEL}")
    
    # 使用AutoTokenizer和AutoModelForCausalLM加载模型
    tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL)
    model = AutoModelForCausalLM.from_pretrained(DEFAULT_MODEL)
    
    # 创建文本生成管道
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        do_sample=True,
        num_return_sequences=1
    )
    
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    generator = None

# 产品描述请求模型
class ProductDescriptionRequest(BaseModel):
    product_name: str = Field(..., description="产品名称")
    product_category: str = Field(..., description="产品类别")
    key_features: List[str] = Field(..., description="产品主要特点列表")
    target_audience: str = Field(..., description="目标受众描述")
    tone: str = Field("亲切", description="描述风格", pattern="^(专业|亲切|活泼|高端|实惠)$")
    language: str = Field("中文", description="生成语言", pattern="^(中文|英文)$")
    version_count: int = Field(1, description="生成的描述版本数量", ge=1, le=3)
    seo_keywords: Optional[List[str]] = Field([], description="SEO关键词列表")
    
    @validator('key_features')
    def validate_key_features(cls, v):
        if len(v) < 1:
            raise ValueError('产品特点至少需要提供一个')
        return v

# 健康检查端点
@app.get("/health")
def health_check():
    model_status = "loaded" if generator else "not loaded"
    return {
        "status": "ok",
        "version": "1.0.0",
        "model_status": model_status,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# 简单的测试端点
@app.get("/")
def root():
    return {"message": "API is running"}

# 生成产品描述端点
@app.post("/generate-description")
def generate_description(request: ProductDescriptionRequest):
    start_time = time.time()
    request_id = f"req_{uuid.uuid4().hex[:8]}"
    
    logger.info(f"Received description request: {request_id}, product: {request.product_name}")
    
    if not generator:
        raise Exception("Model not loaded properly")
    
    # 构建提示模板
    features_text = ",".join(request.key_features)
    keywords_text = ",".join(request.seo_keywords) if request.seo_keywords else ""
    
    # 根据风格调整提示
    style_prompts = {
        "专业": "请生成一段专业、详细的产品描述，突出产品的技术优势和品质保证。",
        "亲切": "请生成一段亲切、温暖的产品描述，让消费者感受到产品的贴心和实用。",
        "活泼": "请生成一段活泼、生动的产品描述，充满活力和趣味性，吸引年轻消费者。",
        "高端": "请生成一段高端、奢华的产品描述，彰显产品的品质和尊贵感。",
        "实惠": "请生成一段强调性价比和实用性的产品描述，突出产品的经济实惠。"
    }
    
    # 创建完整的提示
    prompt = f"""
    产品名称：{request.product_name}
    产品类别：{request.product_category}
    主要特点：{features_text}
    目标受众：{request.target_audience}
    SEO关键词：{keywords_text}
    要求：{style_prompts[request.tone]}使用中文撰写，语言流畅自然，有吸引力。
    产品描述：
    """
    
    descriptions = []
    try:
        # 生成描述
        for _ in range(request.version_count):
            result = generator(prompt, max_new_tokens=MAX_TOKENS)
            description = result[0]['generated_text'].split("产品描述：")[-1].strip()
            descriptions.append(description)
        
        generation_time = round(time.time() - start_time, 2)
        
        logger.info(f"Completed request: {request_id}, time: {generation_time}s")
        
        return {
            "request_id": request_id,
            "descriptions": descriptions,
            "generation_time": generation_time
        }
    except Exception as e:
        logger.error(f"Error generating description: {str(e)}")
        raise Exception(f"Failed to generate product description: {str(e)}")

# 注意：此文件现在只作为ASGI应用模块使用，启动逻辑已移至start_server.py
# 请通过运行 start_server.py 来启动服务