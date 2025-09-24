import requests
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import requests

# API基础URL
base_url = "http://localhost:8000"


def test_health_check():
    """测试健康检查接口"""
    try:
        response = requests.get(f"{base_url}/health")
        print("健康检查结果:")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {str(e)}")
        return False


def generate_product_description():
    """生成产品描述"""
    # 产品信息示例
    product_info = {
        "product_name": "智能手表 Pro",
        "product_category": "电子产品",
        "key_features": ["心率监测", "GPS定位", "50米防水", "7天续航"],
        "target_audience": "运动爱好者",
        "style": "专业科技",
        "language": "zh",
        "version_count": 2
    }
    
    try:
        print("\n正在生成产品描述...")
        print(f"产品信息: {json.dumps(product_info, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            f"{base_url}/generate-description",
            json=product_info,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n生成成功!")
            print(f"生成的产品描述数量: {len(result.get('descriptions', []))}")
            
            for i, description in enumerate(result.get('descriptions', []), 1):
                print(f"\n版本 {i}:")
                print(description)
        else:
            print(f"生成失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"请求异常: {str(e)}")


if __name__ == "__main__":
    print("===== 电商产品描述API演示 =====")
    print("\n注意: 请确保API服务已启动！\n")
    
    # 测试健康检查
    if test_health_check():
        print("\nAPI服务正常运行，可以生成产品描述。\n")
        # 生成产品描述
        generate_product_description()
    else:
        print("\nAPI服务未启动，请先运行 start_server.py 启动服务。")
        print("\n启动命令示例：")
        print("python start_server.py")