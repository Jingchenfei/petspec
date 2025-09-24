print("Testing basic Python functionality")
print("Hello from Python")

import socket
import time

try:
    # 尝试创建一个简单的套接字服务器
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 8000))
    s.listen(1)
    print("Server started on port 8000")
    print("Listening for connections...")
    
    # 运行5秒后退出
    time.sleep(5)
    s.close()
    print("Server stopped")
except Exception as e:
    print(f"Error: {e}")

print("Test completed")