@echo off
chcp 65001 >nul
set "BIN_PATH=C:\Tools\ffmpeg\bin"

if not exist "%BIN_PATH%\ffmpeg.exe" (
    echo [X] Không tìm thấy %BIN_PATH%\ffmpeg.exe
    pause & exit /b 1
)

for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%b"
echo %USER_PATH% | findstr /i /c:"%BIN_PATH%" >nul && (
    echo [OK] Đã có trong PATH
    pause & exit /b 0
)

if defined USER_PATH (set "NEW_PATH=%USER_PATH%;%BIN_PATH%") else (set "NEW_PATH=%BIN_PATH%")
reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "%NEW_PATH%" /f >nul

echo [OK] Đã thêm: %BIN_PATH%
echo Mở CMD mới để dùng ffmpeg
pause
