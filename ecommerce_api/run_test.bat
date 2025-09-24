@echo off
python test_basic.py > output.log 2>&1
type output.log
pause