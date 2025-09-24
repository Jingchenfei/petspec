import requests
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import requests

# 配置API端点
base_url = "http://localhost:8000"

def test_health_check():
    """测试健康检查端点"""
    url = f"{base_url}/health"
    try:
        response = requests.get(url)
        print("健康检查结果:")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {str(e)}")
        return False

def test_generate_description():
    """测试产品描述生成端点"""
    url = f"{base_url}/generate-description"
    
    # 测试数据
    payload = {
        "product_name": "智能保温杯",
        "product_category": "厨房用品",
        "key_features": ["24小时保温", "智能温度显示", "304不锈钢材质", "防漏设计"],
        "target_audience": "上班族、学生、户外活动爱好者",
        "tone": "亲切",
        "language": "中文",
        "version_count": 2,
        "seo_keywords": ["智能保温杯", "24小时保温", "304不锈钢"]
    }
    
    try:
        response = requests.post(url, json=payload)
        print("\n产品描述生成结果:")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"请求ID: {data['request_id']}")
            print(f"生成耗时: {data['generation_time']}秒")
            print("生成的描述:")
            for i, desc in enumerate(data['descriptions'], 1):
                print(f"\n版本{i}:")
                print(desc)
        else:
            print(f"错误信息: {response.text}")
            
        return response.status_code == 200
    except Exception as e:
        print(f"产品描述生成失败: {str(e)}")
        return False

def main():
    print("=== 电商产品描述API测试脚本 ===")
    
    # 提示用户在运行测试前启动API服务
    print("\n请确保已启动API服务。如果尚未启动，请在另一个终端中运行：")
    print("uvicorn main:app --reload")
    input("\n按Enter键继续测试...")
    
    # 运行测试
    health_ok = test_health_check()
    
    if health_ok:
        print("\n健康检查通过，开始测试产品描述生成功能...")
        test_generate_description()
    else:
        print("\n健康检查失败，请检查API服务是否正常运行。")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()