#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
import time
import json
from urllib.parse import urlparse

"""
阿里云函数计算 API 自动测试工具
此工具用于自动测试部署到阿里云函数计算的产品描述API是否正常工作
支持命令行参数，无需交互式输入
"""

def validate_url(api_url):
    """验证URL格式是否正确"""
    try:
        result = urlparse(api_url)
        # 确保有协议和域名
        if not all([result.scheme, result.netloc]):
            # 尝试添加协议头
            if api_url.startswith('://'):
                api_url = 'https' + api_url
            elif not api_url.startswith(('http://', 'https://')):
                api_url = 'https://' + api_url
            result = urlparse(api_url)
        return result.geturl()
    except Exception as e:
        print(f"URL解析错误: {e}")
        return None

def test_health_check(api_url):
    """测试健康检查端点"""
    endpoint = f"{api_url.rstrip('/')}/health"
    print(f"\n[测试] 健康检查端点: {endpoint}")
    
    try:
        start_time = time.time()
        response = requests.get(endpoint, timeout=10)
        elapsed_time = time.time() - start_time
        
        print(f"[结果] 状态码: {response.status_code}")
        print(f"[结果] 响应时间: {elapsed_time:.2f} 秒")
        print(f"[结果] 响应内容: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('status') == 'healthy':
                    print("[状态] ✅ 健康检查通过")
                    return True, elapsed_time
                else:
                    print("[状态] ❌ 健康检查失败: 状态不是healthy")
                    return False, elapsed_time
            except json.JSONDecodeError:
                print("[状态] ❌ 健康检查失败: 响应不是有效的JSON格式")
                return False, elapsed_time
        else:
            print(f"[状态] ❌ 健康检查失败: 状态码为 {response.status_code}")
            return False, elapsed_time
    except requests.exceptions.RequestException as e:
        print(f"[状态] ❌ 健康检查失败: 请求异常 - {e}")
        return False, None

def test_generate_description(api_url):
    """测试产品描述生成端点"""
    endpoint = f"{api_url.rstrip('/')}/generate-description"
    print(f"\n[测试] 产品描述生成端点: {endpoint}")
    
    # 测试数据
    test_data = {
        "product_name": "智能手表",
        "product_features": ["心率监测", "睡眠追踪", "防水50米"],
        "target_audience": "健身爱好者"
    }
    print(f"[测试] 请求数据: {json.dumps(test_data, ensure_ascii=False)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            endpoint,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        elapsed_time = time.time() - start_time
        
        print(f"[结果] 状态码: {response.status_code}")
        print(f"[结果] 响应时间: {elapsed_time:.2f} 秒")
        print(f"[结果] 响应内容: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if "description" in data:
                    print("[状态] ✅ 产品描述生成成功")
                    print(f"[结果] 生成的描述: {data['description'][:100]}...")
                    return True, elapsed_time
                else:
                    print("[状态] ❌ 产品描述生成失败: 响应中缺少description字段")
                    return False, elapsed_time
            except json.JSONDecodeError:
                print("[状态] ❌ 产品描述生成失败: 响应不是有效的JSON格式")
                return False, elapsed_time
        else:
            print(f"[状态] ❌ 产品描述生成失败: 状态码为 {response.status_code}")
            return False, elapsed_time
    except requests.exceptions.RequestException as e:
        print(f"[状态] ❌ 产品描述生成失败: 请求异常 - {e}")
        return False, None

def main():
    """主函数"""
    print("===== 阿里云函数计算 API 自动验证工具 =====")
    print("此工具用于自动测试部署到阿里云函数计算的产品描述API是否正常工作")
    print("支持命令行参数，无需交互式输入")
    
    # 从命令行参数获取API URL
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        # 使用示例URL
        api_url = "https://xxxxxx.cn-shanghai.fcapp.run"
        print(f"\n未提供API URL，使用示例URL: {api_url}")
        print("提示: 可以通过命令行参数提供URL，例如: python test_aliyun_api_auto.py https://your-api-url")
    
    # 验证URL格式
    validated_url = validate_url(api_url)
    if not validated_url:
        print("错误: URL格式无效，请检查后重试")
        sys.exit(1)
    
    print(f"\n使用的API URL: {validated_url}")
    
    # 运行测试
    health_result, health_time = test_health_check(validated_url)
    desc_result, desc_time = test_generate_description(validated_url)
    
    # 生成测试报告
    print("\n===== 测试报告 =====")
    print(f"API URL: {validated_url}")
    print(f"健康检查: {'通过' if health_result else '失败'} {f'(响应时间: {health_time:.2f}秒)' if health_time else ''}")
    print(f"产品描述生成: {'通过' if desc_result else '失败'} {f'(响应时间: {desc_time:.2f}秒)' if desc_time else ''}")
    
    # 总体状态
    if health_result and desc_result:
        print("\n[总体状态] ✅ 所有测试通过！API功能正常")
    else:
        print("\n[总体状态] ❌ 测试未全部通过，请检查API部署")
        print("\n排查建议:")
        print("1. 确认阿里云函数计算已成功部署")
        print("2. 检查API URL是否正确")
        print("3. 验证阿里云函数计算的配置(启动命令、环境变量等)")
        print("4. 查看函数计算的日志信息")
        print("5. 确保函数计算有足够的资源配额")

if __name__ == "__main__":
    main()