@echo off
call %~dp0system\environment.bat
echo 正在安装启动器依赖 (PyQt6, PyYAML, PyInstaller)...
"%~dp0system\python\python.exe" -m pip install PyQt6 PyYAML pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.
echo 安装完成！
pause
