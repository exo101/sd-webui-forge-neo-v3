@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

echo ========================================
echo   GitHub自动更新 - 快速配置向导
echo ========================================
echo.

REM 检查是否在Git仓库中
cd /d "%~dp0.."
git rev-parse --git-dir >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [步骤1/4] 初始化Git仓库...
    git init
    if %ERRORLEVEL% NEQ 0 (
        echo ✗ Git初始化失败，请确保已安装Git
        pause
        exit /b 1
    )
    echo ✓ Git仓库初始化成功
    echo.
) else (
    echo [步骤1/4] Git仓库已存在，跳过初始化
    echo.
)

REM 获取GitHub用户名和仓库名
echo [步骤2/4] 请配置GitHub仓库信息
echo.
set /p GITHUB_USER="请输入您的GitHub用户名: "
if "!GITHUB_USER!"=="" (
    echo ✗ 用户名不能为空
    pause
    exit /b 1
)

set /p REPO_NAME="请输入仓库名 (默认: sd-webui-forge-neo-v3): "
if "!REPO_NAME!"=="" set REPO_NAME=sd-webui-forge-neo-v3

echo.
echo 即将配置的仓库地址:
echo https://github.com/!GITHUB_USER!/!REPO_NAME!.git
echo.
set /p CONFIRM="确认配置？(y/n): "
if /i not "!CONFIRM!"=="y" (
    echo 已取消配置
    pause
    exit /b 0
)

echo.
echo [步骤3/4] 配置远程仓库...

REM 检查是否已配置remote
git remote get-url origin >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠ 检测到已存在的remote配置
    git remote get-url origin
    echo.
    set /p OVERWRITE="是否覆盖现有配置？(y/n): "
    if /i "!OVERWRITE!"=="y" (
        git remote remove origin
    ) else (
        echo 保留现有配置
        goto :skip_remote_config
    )
)

git remote add origin https://github.com/!GITHUB_USER!/!REPO_NAME!.git
if %ERRORLEVEL% NEQ 0 (
    echo ✗ 配置remote失败
    pause
    exit /b 1
)
echo ✓ Remote配置成功

:skip_remote_config
echo.

REM 更新version_manager.py中的仓库配置
echo [步骤4/4] 更新启动器配置文件...
set CONFIG_FILE="%~dp0core\version_manager.py"

if exist !CONFIG_FILE! (
    REM 使用PowerShell替换仓库地址
    powershell -Command "(Get-Content '!CONFIG_FILE!') -replace 'GITHUB_REPO = \"[^\"]+\"', 'GITHUB_REPO = \"!GITHUB_USER!/!REPO_NAME!\"' | Set-Content '!CONFIG_FILE!'"
    echo ✓ 配置文件已更新
) else (
    echo ✗ 配置文件不存在: !CONFIG_FILE!
)

echo.
echo ========================================
echo   配置完成！
echo ========================================
echo.
echo 下一步操作：
echo 1. 如果是首次上传，执行以下命令：
echo    git add .
echo    git commit -m "Initial commit"
echo    git branch -M main
echo    git push -u origin main
echo.
echo 2. 如果仓库已存在，直接推送即可：
echo    git push origin main
echo.
echo 3. 启动启动器，在"版本管理"标签页点击"检查GitHub更新"
echo.
echo 详细说明请查看: launcher\GITHUB_UPDATE_GUIDE.md
echo.

pause