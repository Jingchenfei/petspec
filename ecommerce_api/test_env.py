import os
import sys

print("Python版本:", sys.version)
print("当前工作目录:", os.getcwd())
print("文件列表:", os.listdir('.'))
print("环境变量:", os.environ)