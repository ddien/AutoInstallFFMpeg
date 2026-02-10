"""
FFmpeg Installer Core Logic
"""

import os
import sys
import subprocess
import zipfile
import shutil
import urllib.request
import winreg
import ctypes
from pathlib import Path
from typing import Callable, Optional

FFMPEG_INSTALL_DIR = r"C:\Tools\ffmpeg"
FFMPEG_DOWNLOAD_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"


class FFmpegInstaller:
    """Handles FFmpeg installation process"""

    def __init__(self, progress_callback: Optional[Callable[[str, int], None]] = None):
        """
        Args:
            progress_callback: Function(message, percent) called on progress updates
        """
        self.progress_callback = progress_callback or (lambda msg, pct: None)
        self.install_dir = FFMPEG_INSTALL_DIR
        self.bin_path: Optional[str] = None

    def _update(self, message: str, percent: int):
        """Update progress"""
        self.progress_callback(message, percent)

    def check_installed(self) -> tuple[bool, str]:
        """Check if FFmpeg is already installed and in PATH"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0] if result.stdout else "Unknown"
                return True, version_line
        except FileNotFoundError:
            pass
        return False, ""

    def find_local_zip(self) -> Optional[Path]:
        """Find ffmpeg zip in current directory or exe directory"""
        search_dirs = [Path.cwd()]

        # Also check exe directory if running as frozen
        if getattr(sys, 'frozen', False):
            search_dirs.append(Path(sys.executable).parent)
        else:
            search_dirs.append(Path(__file__).parent.parent.parent)

        for dir_path in search_dirs:
            zip_files = list(dir_path.glob("*ffmpeg*.zip"))
            if zip_files:
                return zip_files[0]
        return None

    def download(self, dest_path: Path) -> bool:
        """Download FFmpeg from internet"""
        self._update("Dang tai FFmpeg tu internet...", 15)

        def progress_hook(count, block_size, total_size):
            if total_size > 0:
                percent = int(count * block_size * 100 / total_size)
                percent = min(percent, 100)
                # Map 15-50% for download phase
                mapped = 15 + int(percent * 0.35)
                self._update(f"Dang tai... {percent}%", mapped)

        try:
            urllib.request.urlretrieve(FFMPEG_DOWNLOAD_URL, str(dest_path), reporthook=progress_hook)
            return True
        except Exception as e:
            self._update(f"Loi tai file: {e}", 15)
            return False

    def extract(self, zip_path: Path) -> bool:
        """Extract FFmpeg to install directory"""
        self._update("Dang giai nen...", 55)

        try:
            # Remove old installation
            if os.path.exists(self.install_dir):
                shutil.rmtree(self.install_dir)

            os.makedirs(self.install_dir, exist_ok=True)

            # Extract
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                total = len(zip_ref.namelist())
                for i, file in enumerate(zip_ref.namelist()):
                    zip_ref.extract(file, self.install_dir)
                    percent = 55 + int((i / total) * 25)
                    self._update(f"Giai nen... {i}/{total}", percent)

            # Find bin directory
            for root, dirs, files in os.walk(self.install_dir):
                if "ffmpeg.exe" in files:
                    self.bin_path = root
                    return True

            return False

        except Exception as e:
            self._update(f"Loi giai nen: {e}", 55)
            return False

    def add_to_path(self) -> bool:
        """Add FFmpeg bin to User PATH"""
        if not self.bin_path:
            return False

        self._update("Dang them vao PATH...", 85)

        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Environment",
                0,
                winreg.KEY_ALL_ACCESS
            )

            try:
                current_path, _ = winreg.QueryValueEx(key, "Path")
            except WindowsError:
                current_path = ""

            paths = current_path.split(";")
            if self.bin_path.lower() not in [p.lower() for p in paths]:
                new_path = current_path + ";" + self.bin_path if current_path else self.bin_path
                winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

            winreg.CloseKey(key)

            # Broadcast environment change
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x1A
            ctypes.windll.user32.SendMessageTimeoutW(
                HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 0, 1000, None
            )

            self._update("Da them vao PATH!", 95)
            return True

        except Exception as e:
            self._update(f"Loi them PATH: {e}", 85)
            return False

    def install(self) -> tuple[bool, str]:
        """
        Run full installation process

        Returns:
            (success, message)
        """
        # Step 1: Check if already installed
        self._update("Kiem tra FFmpeg...", 5)
        installed, version = self.check_installed()
        if installed:
            return True, f"FFmpeg da duoc cai dat!\n{version}"

        # Step 2: Find or download zip
        self._update("Tim nguon cai dat...", 10)
        zip_path = self.find_local_zip()

        if zip_path:
            self._update(f"Tim thay: {zip_path.name}", 15)
        else:
            self._update("Khong tim thay zip, dang tai...", 15)
            zip_path = Path(self.install_dir).parent / "ffmpeg_temp.zip"
            os.makedirs(zip_path.parent, exist_ok=True)
            if not self.download(zip_path):
                return False, "Khong the tai FFmpeg!"

        # Step 3: Extract
        if not self.extract(zip_path):
            return False, "Loi giai nen file!"

        # Step 4: Add to PATH
        if not self.add_to_path():
            return False, "Loi them vao PATH!"

        # Cleanup temp download
        if "ffmpeg_temp.zip" in str(zip_path):
            try:
                os.remove(zip_path)
            except:
                pass

        self._update("Cai dat hoan tat!", 100)
        return True, f"Cai dat thanh cong!\nThu muc: {self.bin_path}"
