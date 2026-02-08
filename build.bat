@echo off
chcp 65001 >nul
echo ========================================
echo    ZGIRC时间同步 - EXE打包工具
echo ========================================
echo.

REM 检查pyinstaller是否安装
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [1/3] 正在安装 pyinstaller...
    pip install pyinstaller
    echo.
)

echo [2/3] 正在清理旧文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
del /q *.spec 2>nul
echo.

echo [3/3] 正在打包 EXE...
echo.
REM 打包命令
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "ZGIRC_TimeSync" ^
    --icon NONE ^
    --clean ^
    --log-level WARN ^
    --add-data "wget.exe;." ^
    --hidden-import requests ^
    --hidden-import urllib3 ^
    --hidden-import certifi ^
    --hidden-import charset_normalizer ^
    --hidden-import idna ^
    --hidden-import pywin32 ^
    time.py

echo.
if exist dist\ZGIRC_TimeSync.exe (
    echo ========================================
    echo    打包完成！
    echo ========================================
    echo.
    echo EXE文件位置: dist\ZGIRC_TimeSync.exe
    echo 文件大小: %~za
    echo.
    echo 下一步操作:
    echo 1. 上传到GitHub Releases
    echo 2. 测试EXE功能
    echo.
    if exist dist\ZGIRC_TimeSync.exe (
        echo 按任意键打开目录...
        pause >nul
        explorer dist
    )
) else (
    echo [错误] 打包失败，请检查错误信息
    pause
)
