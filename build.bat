@echo off
chcp 65001 >nul
echo.
echo ══════════════════════════════════════════════════
echo    Build FFmpeg Auto Setup - EXE
echo ══════════════════════════════════════════════════
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python chua duoc cai dat!
    pause
    exit /b 1
)

:: Install dependencies
echo [1] Cai dat dependencies...
pip install -r requirements.txt -q

:: Build exe
echo.
echo [2] Build EXE voi PyInstaller...
echo     (Co the mat vai phut)
echo.

pyinstaller --onefile --windowed --name=FFmpegSetup --clean ^
    --icon=assets/icon.ico ^
    --add-data "src/core;core" ^
    --add-data "src/ui;ui" ^
    --add-data "src;." ^
    --add-data "assets;assets" ^
    src/main.py

if exist "dist\FFmpegSetup.exe" (
    echo.
    echo ══════════════════════════════════════════════════
    echo    BUILD THANH CONG!
    echo ══════════════════════════════════════════════════
    echo.
    echo    File: dist\FFmpegSetup.exe
    echo.
    echo    Ban co the copy file nay va ffmpeg.zip
    echo    den bat ky may nao de su dung.
    echo.
) else (
    echo.
    echo [!] Build that bai! Kiem tra log phia tren.
)

pause
