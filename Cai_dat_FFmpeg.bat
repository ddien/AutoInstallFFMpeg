@echo off
chcp 65001 >nul
title Cài đặt FFmpeg Tự động

echo.
echo ══════════════════════════════════════════════════
echo    Cài đặt FFmpeg Tự động - Auto Setup
echo ══════════════════════════════════════════════════
echo.

:: Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python chưa được cài đặt!
    echo     Vui lòng cài Python từ: https://python.org
    echo.
    pause
    exit /b 1
)

:: Chạy script Python
python "%~dp0setup_ffmpeg.py"
