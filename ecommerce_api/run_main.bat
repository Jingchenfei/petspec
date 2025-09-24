@echo off
REM 运行主应用程序并将输出重定向到日志文件
python main.py > main_output.log 2>&1

echo 程序执行完毕，输出已保存到 main_output.log

echo 正在显示日志文件内容...
type main_output.log