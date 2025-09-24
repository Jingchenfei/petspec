#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
电商产品描述API验证脚本
此脚本用于快速验证API服务是否正常工作，包括健康检查和描述生成功能。
"""

import requests
import time
import json

# API基础URL
BASE_URL = "http://localhost:8000"

# 打印分隔线的函数
def print_separator(title):
    print("=" * 70)
    print(f"{title.center(70)}")
    print("=" * 70)

# 测试健康检查端点
def test_health_check():
    print_separator("测试健康检查端点")
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url)
        print(f"请求URL: {url}")
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.json()}")
        if response.status_code == 200:
            print("✅ 健康检查测试通过！")
            return True
        else:
            print("❌ 健康检查测试失败！")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务，请确认服务是否已启动。")
        return False
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")
        return False

# 测试产品描述生成端点
def test_generate_description():
    print_separator("测试产品描述生成端点")
    url = f"{BASE_URL}/generate-description"
    
    # 测试数据
    test_data = {
        "product_name": "智能手表Pro",
        "product_category": "电子产品",
        "key_features": ["心率监测", "睡眠分析", "防水50米", "7天续航", "GPS定位"],
        "target_audience": "健身爱好者，商务人士",
        "tone": "专业",
        "version_count": 2,
        "seo_keywords": ["智能手表", "健康监测", "长续航"]
    }
    
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    try:
        start_time = time.time()
        response = requests.post(url, json=test_data)
        end_time = time.time()
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"请求ID: {result.get('request_id', 'N/A')}")
            print(f"生成耗时: {result.get('generation_time', 'N/A')}秒")
            print(f"请求总耗时: {round(end_time - start_time, 2)}秒")
            
            # 打印生成的描述
            descriptions = result.get('descriptions', [])
            for i, desc in enumerate(descriptions, 1):
                print(f"\n描述版本 {i}:\n{desc[:200]}...")
            
            print("✅ 产品描述生成测试通过！")
            return True
        else:
            print(f"❌ 产品描述生成测试失败！")
            print(f"错误信息: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务，请确认服务是否已启动。")
        return False
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")
        return False

# 测试不同风格的描述生成
def test_different_tones():
    print_separator("测试不同风格的描述生成")
    url = f"{BASE_URL}/generate-description"
    
    # 测试的不同风格
    tones_to_test = ["亲切", "活泼", "高端"]
    
    # 基础测试数据
    base_data = {
        "product_name": "智能保温杯",
        "product_category": "家居用品",
        "key_features": ["24小时保温", "智能温度显示", "食品级材质", "便携设计"],
        "target_audience": "上班族，学生",
        "version_count": 1,
        "seo_keywords": ["智能保温杯", "持久保温"]
    }
    
    all_passed = True
    
    for tone in tones_to_test:
        print(f"\n测试风格: {tone}")
        test_data = base_data.copy()
        test_data["tone"] = tone
        
        try:
            response = requests.post(url, json=test_data)
            
            if response.status_code == 200:
                result = response.json()
                desc = result.get('descriptions', [''])[0]
                print(f"风格描述预览: {desc[:150]}...")
                print(f"✅ 风格 '{tone}' 测试通过！")
            else:
                print(f"❌ 风格 '{tone}' 测试失败！状态码: {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ 风格 '{tone}' 测试过程中发生错误: {str(e)}")
            all_passed = False
    
    return all_passed

# 主函数
def main():
    print_separator("电商产品描述API验证工具")
    print("此工具将帮助您验证API服务是否正常工作。\n")
    
    # 检查服务状态
    health_ok = test_health_check()
    
    if health_ok:
        print("\n服务状态良好，继续测试其他功能...\n")
        
        # 测试描述生成
        generate_ok = test_generate_description()
        
        # 测试不同风格（如果基本测试通过）
        if generate_ok:
            print("\n基本功能测试通过，继续测试高级功能...\n")
            different_tones_ok = test_different_tones()
        else:
            different_tones_ok = False
            print("\n⚠️  基本功能测试未通过，跳过高级功能测试。\n")
        
        # 总结测试结果
        print_separator("测试总结")
        
        if health_ok and generate_ok and different_tones_ok:
            print("✅ API服务所有功能测试通过！")
            print("您的API已经准备好投入生产使用。")
            print("建议：继续监控服务性能，并根据用户反馈进行优化。")
        elif health_ok and generate_ok:
            print("⚠️  API服务基本功能测试通过，但部分高级功能测试未通过。")
            print("建议：检查模型配置和参数设置。")
        elif health_ok:
            print("⚠️  API服务已启动，但核心功能测试未通过。")
            print("建议：检查模型加载和端点实现。")
        else:
            print("❌ API服务无法正常启动。")
            print("建议：检查服务配置和环境设置。")
    
    print_separator("测试完成")

if __name__ == "__main__":
    main()