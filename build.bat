@echo off
chcp 65001 >nul
echo.
echo ==================================================
echo    Build FFmpeg Auto Setup - EXE
echo ==================================================
echo.

:: Get version from version.py
for /f "tokens=2 delims==" %%a in ('findstr /c:"__version__" src\version.py') do set "RAW_VER=%%a"
set "VERSION=%RAW_VER: =%"
set "VERSION=%VERSION:"=%"
set "EXE_NAME=FFmpegSetup_v%VERSION%"

echo    Version: %VERSION%
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

:: Try to clean build folder (ignore errors)
echo.
echo [2] Xoa build cache cu...
rmdir /s /q build 2>nul
rmdir /s /q __pycache__ 2>nul

:: Build exe using .spec file (recommended for better control)
echo.
echo [3] Build EXE voi PyInstaller (spec file)...
echo     (Co the mat vai phut)
echo.

pyinstaller FFmpegSetup_v%VERSION%.spec --clean --noconfirm

if exist "dist\%EXE_NAME%.exe" (
    echo.
    echo ==================================================
    echo    BUILD THANH CONG!
    echo ==================================================
    echo.
    echo    File: dist\%EXE_NAME%.exe
    echo.
    echo    Ban co the copy file nay va ffmpeg.zip
    echo    den bat ky may nao de su dung.
    echo.
) else (
    echo.
    echo [!] Build that bai! Kiem tra log phia tren.
)

pause
