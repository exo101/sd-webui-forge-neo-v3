@echo off
call %~dp0system\environment.bat
rem 使用 start /B 命令在后台运行，不显示命令行窗口
start /B "" "%~dp0system\python\python.exe" "%~dp0launcher\main.py"
