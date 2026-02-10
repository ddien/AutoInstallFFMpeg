@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
title Cài đặt FFmpeg Tự động

set "INSTALL_DIR=C:\Tools\ffmpeg"
set "DOWNLOAD_URL=https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
set "SCRIPT_DIR=%~dp0"

echo.
echo ══════════════════════════════════════════════════════════
echo       FFmpeg Auto Setup - Cài đặt FFmpeg Tự động
echo ══════════════════════════════════════════════════════════
echo.

:: 1. Kiểm tra FFmpeg đã cài chưa
echo [1] Kiểm tra FFmpeg...
where ffmpeg >nul 2>&1
if %errorlevel% equ 0 (
    echo     √ FFmpeg đã được cài đặt!
    ffmpeg -version 2>&1 | findstr /i "ffmpeg version"
    echo.
    pause
    exit /b 0
)
echo     X FFmpeg chưa được cài đặt hoặc không có trong PATH
echo.

:: 2. Tìm file zip local
echo [2] Tìm nguồn cài đặt...
set "ZIP_FILE="
for %%f in ("%SCRIPT_DIR%*ffmpeg*.zip") do (
    set "ZIP_FILE=%%f"
    goto :found_zip
)

:download_zip
echo     X Không tìm thấy file zip trong folder
echo     Đang tải FFmpeg từ internet...
echo     URL: %DOWNLOAD_URL%
echo.

set "ZIP_FILE=%SCRIPT_DIR%ffmpeg_temp.zip"

:: Dùng PowerShell để tải (có sẵn trên Windows)
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%ZIP_FILE%'}"

if not exist "%ZIP_FILE%" (
    echo     [!] Lỗi tải file! Vui lòng tải thủ công từ:
    echo         %DOWNLOAD_URL%
    pause
    exit /b 1
)
echo     √ Tải hoàn tất!
goto :extract

:found_zip
echo     √ Tìm thấy: %ZIP_FILE%
echo.

:extract
:: 3. Giải nén
echo [3] Giải nén FFmpeg...

:: Xóa folder cũ nếu có
if exist "%INSTALL_DIR%" (
    echo     Xóa cài đặt cũ...
    rmdir /s /q "%INSTALL_DIR%" 2>nul
)

:: Tạo thư mục
mkdir "%INSTALL_DIR%" 2>nul

:: Giải nén bằng PowerShell
echo     Đang giải nén vào %INSTALL_DIR%...
powershell -Command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%INSTALL_DIR%' -Force"

:: Tìm thư mục bin chứa ffmpeg.exe
set "BIN_PATH="
for /r "%INSTALL_DIR%" %%d in (.) do (
    if exist "%%d\ffmpeg.exe" (
        set "BIN_PATH=%%~dpd"
        goto :found_bin
    )
)

echo     [!] Không tìm thấy ffmpeg.exe!
pause
exit /b 1

:found_bin
:: Loại bỏ dấu \ cuối nếu có
if "%BIN_PATH:~-1%"=="\" set "BIN_PATH=%BIN_PATH:~0,-1%"
echo     √ Đã giải nén: %BIN_PATH%
echo.

:: 4. Thêm vào User PATH
echo [4] Thêm vào PATH...

:: Lấy PATH hiện tại của User
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%b"

:: Kiểm tra xem đã có trong PATH chưa
echo %USER_PATH% | findstr /i /c:"%BIN_PATH%" >nul
if %errorlevel% equ 0 (
    echo     Đường dẫn đã có trong PATH
    goto :done
)

:: Thêm vào PATH
if defined USER_PATH (
    set "NEW_PATH=%USER_PATH%;%BIN_PATH%"
) else (
    set "NEW_PATH=%BIN_PATH%"
)

:: Cập nhật registry
reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "%NEW_PATH%" /f >nul
echo     √ Đã thêm vào User PATH

:: Broadcast thay đổi environment (cần admin để hoạt động hoàn toàn)
powershell -Command "[System.Environment]::SetEnvironmentVariable('Path', [System.Environment]::GetEnvironmentVariable('Path', 'User'), 'User')" 2>nul

:done
echo.
echo ══════════════════════════════════════════════════════════
echo                   CÀI ĐẶT HOÀN TẤT!
echo ══════════════════════════════════════════════════════════
echo.
echo  Thư mục cài đặt: %BIN_PATH%
echo.
echo  LƯU Ý QUAN TRỌNG:
echo  - Mở CMD/PowerShell MỚI để sử dụng lệnh ffmpeg
echo  - Hoặc khởi động lại ứng dụng đang chạy
echo.

:: Xóa file tải về tạm
if "%ZIP_FILE%"=="%SCRIPT_DIR%ffmpeg_temp.zip" (
    del "%ZIP_FILE%" 2>nul
    echo  ^(Đã xóa file tải về tạm thời^)
    echo.
)

pause
