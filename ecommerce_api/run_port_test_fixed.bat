@echo off
setlocal

REM 运行测试脚本并将输出重定向到日志文件
python test_port_8001.py > port_test_output.log 2>&1

echo 测试脚本执行完毕，输出已保存到 port_test_output.log

echo 正在显示日志文件内容...
type port_test_output.log

REM 暂停以便查看结果
pause