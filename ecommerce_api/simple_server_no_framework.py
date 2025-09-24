# -*- coding: utf-8 -*-
import os
import json
import logging
import time

# 兼容Python 2和Python 3的HTTP服务器模块导入
try:
    # Python 3
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    # Python 2
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("simple_server")

# 简单的HTTP请求处理器
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 健康检查端点
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "version": "1.0",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            # 处理Python 2和Python 3的编码差异
            response_data = json.dumps(response)
            if hasattr(response_data, 'encode'):
                response_data = response_data.encode('utf-8')
            self.wfile.write(response_data)
        # 根端点
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "API is running"}
            # 处理Python 2和Python 3的编码差异
            not_found_response = json.dumps(response)
            if hasattr(not_found_response, 'encode'):
                not_found_response = not_found_response.encode('utf-8')
            self.wfile.write(not_found_response)
        else:
            self.send_response(404)
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_POST(self):
        # 产品描述生成端点
        if self.path == '/generate-description':
            # 读取请求体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                # 处理Python 2和Python 3的编码差异
                post_data_str = post_data
                if hasattr(post_data, 'decode'):
                    post_data_str = post_data.decode('utf-8')
                # 解析JSON请求体
                request_data = json.loads(post_data_str)
                
                # 提取请求参数
                product_name = request_data.get('product_name', 'Unknown product')
                product_features = request_data.get('product_features', [])
                target_audience = request_data.get('target_audience', 'general audience')
                
                logger.info("Received request for: %s" % product_name)
                
                # 简单的模拟响应
                descriptions = ["This is a sample description for %s. It has features: %s. Targeting: %s." % (product_name, ', '.join(product_features), target_audience)]
                
                # 返回响应
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                # 注意：测试脚本期望的是单个description字段，而非descriptions数组
                response = {
                    "request_id": "mock_req_123",
                    "description": descriptions[0] if descriptions else "",
                    "generation_time": 0.5
                }
                # 处理Python 2和Python 3的编码差异
                success_response = json.dumps(response)
                if hasattr(success_response, 'encode'):
                    success_response = success_response.encode('utf-8')
                self.wfile.write(success_response)
            except Exception as e:
                logger.error("Error processing request: %s" % str(e))
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": str(e)}
                self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

    # 禁用日志中的日期时间前缀，使用我们自定义的日志格式
    def log_message(self, format, *args):
        return

def run_server(host, port):
    """启动HTTP服务器"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    logger.info("Starting server on %s:%s" % (host, port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.info("Server stopped")

if __name__ == "__main__":
    try:
        # 获取环境变量，设置默认值
        host = os.getenv('APP_HOST', '0.0.0.0')
        port = int(os.getenv('APP_PORT', '9000'))
        
        # 启动服务器
        run_server(host, port)
    except Exception as e:
        logger.critical("Server failed to start: %s" % str(e))