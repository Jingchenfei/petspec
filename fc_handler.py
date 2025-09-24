import json
import os
from aliyun.oss2 import Auth

def generate_signed_url(object_key, expiry=3600):
    """Generate OSS signed URL"""
    auth = Auth(
        os.environ['OSS_ACCESS_KEY'],
        os.environ['OSS_SECRET_KEY']
    )
    return auth.sign_url(
        'GET',
        'petspec-static',
        object_key,
        expiry
    )

def build_prompt(text):
    """Build optimization prompt"""
    return f"""Optimization requirements:
1. Include [Usage] section
2. Mark important warnings
3. Add disclaimer
Original text: {text}"""

def error_response(code, message):
    """Error response template"""
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"error": message, "status": "error"})
    }

def success_response(result):
    """Success response template"""
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"result": result, "status": "success"})
    }

def handler(event, context):
    # Handle QR code request
    if event.get('path') == '/get-qrcode-url':
        try:
            return success_response({
                "url": generate_signed_url('images/wechat-pay.png')
            })
        except Exception as e:
            return error_response(500, f"QR code generation failed: {str(e)}")

    # Main processing logic
    try:
        data = json.loads(event['body'])
        if not data.get('text'):
            return error_response(400, "Input text cannot be empty")
            
        prompt = build_prompt(data['text'])
        # Add actual API call here
        optimized_text = f"Optimized: {prompt}"  # Replace with real API call
        
        return success_response(optimized_text)
        
    except json.JSONDecodeError:
        return error_response(400, "Invalid JSON format")
    except Exception as e:
        return error_response(500, f"Processing error: {str(e)}")
    
    # 获取环境变量
    wx_access_key = os.environ.get('WX_ACCESS_KEY')
    wx_secret_key = os.environ.get('WX_SECRET_KEY')
    
    if not all([wx_access_key, wx_secret_key]):
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "API密钥未配置"})
        }

    # 构造Prompt
    prompt = f"""你是一个专业的宠物健康顾问，请优化以下宠物用品说明书：
    {user_input}
    
    要求：
    1. 语言亲切易懂，使用表情符号标记重点
    2. 必须包含【用法用量】、【重要提醒】、【禁忌症】模块
    3. 转换专业术语为通俗表达
    4. 开头简短总结，结尾加免责声明"""
    
    # 调用文心API (示例代码，需替换实际API密钥)
    try:
        # 这里应替换为实际的文心API调用代码
        api_result = "这是模拟的API返回结果

【用法用量】每天2次
【重要提醒】⚠️不可与牛奶同服
*本内容由AI生成，仅供参考*"
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "result": api_result,
                "status": "success"
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "status": "error"
            })
        }