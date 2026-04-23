@echo off
chcp 65001 >nul
call %~dp0system\environment.bat
echo.
echo  ================================
echo   SD WebUI Forge Launcher Build
echo  ================================
echo.
echo  [1] Quick build  (folder mode, fast, for testing)
echo  [2] Single file  (slow, for release)
echo.
set /p choice= Enter 1 or 2: 

if "%choice%"=="2" (
    echo Building single-file exe...
    "%~dp0system\python\python.exe" "%~dp0launcher\build.py" --onefile
) else (
    echo Building folder mode...
    "%~dp0system\python\python.exe" "%~dp0launcher\build.py"
)
echo.
pause