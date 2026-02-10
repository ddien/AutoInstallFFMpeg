"""
FFmpeg Auto Setup - Tự động cài đặt FFmpeg cho Windows
Chạy với quyền Administrator để thêm vào System PATH (tùy chọn)
"""

import os
import sys
import subprocess
import zipfile
import shutil
import urllib.request
import winreg
from pathlib import Path

# Cấu hình
FFMPEG_INSTALL_DIR = r"C:\Tools\ffmpeg"
FFMPEG_DOWNLOAD_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"


def print_banner():
    print("=" * 50)
    print("   FFmpeg Auto Setup - Cài đặt tự động FFmpeg")
    print("=" * 50)
    print()


def is_ffmpeg_installed():
    """Kiểm tra ffmpeg đã có trong PATH chưa"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def find_local_zip():
    """Tìm file ffmpeg.zip trong folder hiện tại"""
    script_dir = Path(__file__).parent
    zip_files = list(script_dir.glob("*ffmpeg*.zip"))
    if zip_files:
        return zip_files[0]
    return None


def download_ffmpeg(dest_path):
    """Tải FFmpeg từ internet"""
    print(f"[*] Đang tải FFmpeg từ internet...")
    print(f"    URL: {FFMPEG_DOWNLOAD_URL}")
    try:
        urllib.request.urlretrieve(FFMPEG_DOWNLOAD_URL, dest_path, reporthook=download_progress)
        print()
        return True
    except Exception as e:
        print(f"\n[!] Lỗi tải file: {e}")
        return False


def download_progress(count, block_size, total_size):
    """Hiển thị tiến trình tải"""
    percent = int(count * block_size * 100 / total_size)
    percent = min(percent, 100)
    print(f"\r    Tiến trình: {percent}%", end="", flush=True)


def extract_ffmpeg(zip_path, dest_dir):
    """Giải nén ffmpeg"""
    print(f"[*] Đang giải nén vào {dest_dir}...")

    # Tạo thư mục đích nếu chưa có
    os.makedirs(dest_dir, exist_ok=True)

    # Giải nén
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)

    # Tìm folder bin chứa ffmpeg.exe
    for root, dirs, files in os.walk(dest_dir):
        if "ffmpeg.exe" in files:
            return root

    return None


def add_to_user_path(new_path):
    """Thêm đường dẫn vào User PATH"""
    print(f"[*] Đang thêm vào User PATH...")

    try:
        # Mở registry key cho User Environment
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_ALL_ACCESS
        )

        # Lấy PATH hiện tại
        try:
            current_path, _ = winreg.QueryValueEx(key, "Path")
        except WindowsError:
            current_path = ""

        # Kiểm tra xem đường dẫn đã tồn tại chưa
        paths = current_path.split(";")
        if new_path.lower() not in [p.lower() for p in paths]:
            # Thêm đường dẫn mới
            new_path_value = current_path + ";" + new_path if current_path else new_path
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path_value)
            print(f"    Đã thêm: {new_path}")
        else:
            print(f"    Đường dẫn đã tồn tại trong PATH")

        winreg.CloseKey(key)

        # Thông báo cho Windows cập nhật environment
        import ctypes
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x1A
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 0, 1000, None
        )

        return True

    except Exception as e:
        print(f"[!] Lỗi thêm vào PATH: {e}")
        return False


def main():
    print_banner()

    # 1. Kiểm tra ffmpeg đã cài đặt chưa
    print("[1] Kiểm tra FFmpeg...")
    if is_ffmpeg_installed():
        print("    ✓ FFmpeg đã được cài đặt và có trong PATH!")
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        version_line = result.stdout.split('\n')[0] if result.stdout else "Unknown"
        print(f"    Version: {version_line}")
        input("\nNhấn Enter để thoát...")
        return

    print("    ✗ FFmpeg chưa được cài đặt hoặc không có trong PATH")

    # 2. Tìm file zip local hoặc tải về
    print("\n[2] Tìm nguồn cài đặt...")
    zip_path = find_local_zip()

    if zip_path:
        print(f"    ✓ Tìm thấy file local: {zip_path.name}")
    else:
        print("    ✗ Không tìm thấy file zip trong folder")
        zip_path = Path(__file__).parent / "ffmpeg_download.zip"
        if not download_ffmpeg(str(zip_path)):
            print("\n[!] Không thể tải FFmpeg. Vui lòng tải thủ công từ:")
            print(f"    {FFMPEG_DOWNLOAD_URL}")
            input("\nNhấn Enter để thoát...")
            return

    # 3. Giải nén
    print(f"\n[3] Giải nén FFmpeg...")

    # Xóa folder cũ nếu có
    if os.path.exists(FFMPEG_INSTALL_DIR):
        print(f"    Xóa cài đặt cũ...")
        shutil.rmtree(FFMPEG_INSTALL_DIR)

    bin_path = extract_ffmpeg(zip_path, FFMPEG_INSTALL_DIR)

    if not bin_path:
        print("    ✗ Không tìm thấy ffmpeg.exe trong file zip!")
        input("\nNhấn Enter để thoát...")
        return

    print(f"    ✓ Đã giải nén thành công")
    print(f"    Thư mục bin: {bin_path}")

    # 4. Thêm vào PATH
    print(f"\n[4] Cập nhật PATH...")
    if add_to_user_path(bin_path):
        print("    ✓ Đã thêm vào User PATH")

    # 5. Xác nhận
    print("\n" + "=" * 50)
    print("   CÀI ĐẶT HOÀN TẤT!")
    print("=" * 50)
    print()
    print("Lưu ý:")
    print("  - Mở CMD/PowerShell MỚI để sử dụng ffmpeg")
    print("  - Hoặc khởi động lại các ứng dụng đang mở")
    print()
    print(f"Thư mục cài đặt: {bin_path}")
    print()

    # Xóa file tải về nếu là file tạm
    if "ffmpeg_download.zip" in str(zip_path):
        try:
            os.remove(zip_path)
            print("(Đã xóa file tải về tạm thời)")
        except:
            pass

    input("Nhấn Enter để thoát...")


if __name__ == "__main__":
    main()
