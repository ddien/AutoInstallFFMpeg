"""
FFmpeg Auto Setup - Main Window UI
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QTextEdit, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

import sys
import os
import shutil
import webbrowser

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.installer import FFmpegInstaller
from version import __version__


def get_resource_path(relative_path):
    """Get path for bundled resources (works with PyInstaller)"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base_path, relative_path)


class InstallerThread(QThread):
    """Background thread for installation"""
    progress = pyqtSignal(str, int)  # message, percent
    finished = pyqtSignal(bool, str)  # success, message

    def run(self):
        installer = FFmpegInstaller(progress_callback=self._on_progress)
        success, message = installer.install()
        self.finished.emit(success, message)

    def _on_progress(self, message: str, percent: int):
        self.progress.emit(message, percent)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.installer_thread = None
        self.init_ui()
        self.check_status()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"FFmpeg Auto Setup v{__version__}")
        self.setFixedSize(520, 620)

        # Set window icon
        icon_path = get_resource_path("assets/icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton#installBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #11998e, stop:1 #38ef7d);
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 14px 28px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#installBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #38ef7d, stop:1 #11998e);
            }
            QPushButton#installBtn:disabled {
                background: #a0a0a0;
                color: #666666;
            }
            QPushButton#fbBtn {
                background: #1877f2;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton#fbBtn:hover {
                background: #166fe5;
            }
            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: rgba(255, 255, 255, 0.3);
                height: 10px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #11998e, stop:1 #38ef7d);
                border-radius: 6px;
            }
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.95);
                color: #333333;
                border: 2px solid rgba(255, 255, 255, 0.5);
                border-radius: 10px;
                padding: 10px;
                font-family: Consolas, monospace;
                font-size: 12px;
            }
        """)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel(f"FFmpeg Auto Setup v{__version__}")
        header.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);")
        layout.addWidget(header)

        subtitle = QLabel("Cài đặt FFmpeg tự động cho Windows")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.85);")
        layout.addWidget(subtitle)

        # Description - explain what FFmpeg is
        desc = QLabel("FFmpeg là công cụ xử lý video/audio cần thiết cho nhiều ứng dụng.\n"
                      "Chương trình sẽ tự động tải, giải nén và thêm vào PATH hệ thống.")
        desc.setFont(QFont("Segoe UI", 9))
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: rgba(255, 255, 255, 0.75);")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addSpacing(8)

        # Status log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(220)
        layout.addWidget(self.log_text)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Sẵn sàng cài đặt")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.status_label)

        layout.addStretch()

        # Install button
        self.install_btn = QPushButton("Cài đặt FFmpeg")
        self.install_btn.setObjectName("installBtn")
        self.install_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.install_btn.clicked.connect(self.start_install)
        layout.addWidget(self.install_btn)

        # Path info
        self.path_label = QLabel("Thư mục cài đặt: C:\\Tools\\ffmpeg")
        self.path_label.setFont(QFont("Segoe UI", 9))
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.path_label.setStyleSheet("color: rgba(255, 255, 255, 0.7);")
        layout.addWidget(self.path_label)

        # Warning label
        warning = QLabel("⚠️ KHÔNG đổi tên hoặc xóa thư mục trên, FFmpeg sẽ ngừng hoạt động!")
        warning.setFont(QFont("Segoe UI", 8))
        warning.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warning.setStyleSheet("color: #ffd93d; font-weight: bold;")
        warning.setWordWrap(True)
        layout.addWidget(warning)

        layout.addSpacing(10)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.3);")
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        # Footer - Credit
        credit = QLabel("Tool được tạo bởi Diện Tech - 0973323090")
        credit.setFont(QFont("Segoe UI", 9))
        credit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        layout.addWidget(credit)

        # Facebook button
        fb_btn = QPushButton("Facebook: Nguyễn Duy Diện")
        fb_btn.setObjectName("fbBtn")
        fb_btn.setFont(QFont("Segoe UI", 10))
        fb_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        fb_btn.clicked.connect(self.open_facebook)
        layout.addWidget(fb_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def open_facebook(self):
        """Open Facebook profile"""
        webbrowser.open("https://www.facebook.com/nguyenduydien")

    def log(self, message: str, icon: str = ""):
        """Add message to log"""
        prefix = f"{icon} " if icon else ""
        self.log_text.append(f"{prefix}{message}")
        # Scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def check_status(self):
        """Check if FFmpeg is already installed"""
        installer = FFmpegInstaller()
        installed, version = installer.check_installed()

        if installed:
            self.log("FFmpeg đã được cài đặt!", "[OK]")
            self.log(version, "")
            # Find and show installation path
            ffmpeg_path = shutil.which("ffmpeg")
            if ffmpeg_path:
                ffmpeg_dir = os.path.dirname(ffmpeg_path)
                self.log(f"Thư mục: {ffmpeg_dir}", "")
            self.status_label.setText("FFmpeg đã sẵn sàng sử dụng!")
            self.status_label.setStyleSheet("color: #38ef7d; font-weight: bold;")
            self.progress_bar.setValue(100)
            self.install_btn.setText("Cài đặt lại")
        else:
            self.log("FFmpeg chưa được cài đặt", "[!]")
            self.status_label.setText("Nhấn nút để bắt đầu cài đặt")

    def start_install(self):
        """Start installation process"""
        self.install_btn.setEnabled(False)
        self.install_btn.setText("Đang xử lý...")
        self.log_text.clear()
        self.progress_bar.setValue(0)

        self.installer_thread = InstallerThread()
        self.installer_thread.progress.connect(self.on_progress)
        self.installer_thread.finished.connect(self.on_finished)
        self.installer_thread.start()

    def on_progress(self, message: str, percent: int):
        """Handle progress updates"""
        self.progress_bar.setValue(percent)
        self.status_label.setText(message)

        # Add to log with appropriate icon
        if percent < 100:
            self.log(message, "[...]")

    def on_finished(self, success: bool, message: str):
        """Handle installation complete"""
        self.install_btn.setEnabled(True)

        if success:
            self.progress_bar.setValue(100)
            self.status_label.setText("Cài đặt hoàn tất!")
            self.status_label.setStyleSheet("color: #38ef7d; font-weight: bold;")
            self.install_btn.setText("Hoàn tất")
            self.log("=" * 40, "")
            self.log("CÀI ĐẶT THÀNH CÔNG!", "[OK]")
            self.log("", "")
            self.log("Hướng dẫn sử dụng:", "")
            self.log("• Mở CMD/Terminal MỚI để dùng ffmpeg", "")
            self.log("• KHÔNG cần khởi động lại máy", "")
            self.log("• KHÔNG cần Log out", "")
            self.log("", "")
            self.log("LƯU Ý QUAN TRỌNG:", "[!]")
            self.log("• KHÔNG đổi tên thư mục C:\\Tools\\ffmpeg", "")
            self.log("• KHÔNG xóa thư mục này", "")
            self.log("• Nếu vi phạm, FFmpeg sẽ ngừng hoạt động!", "")
        else:
            self.progress_bar.setValue(0)
            self.status_label.setText("Cài đặt thất bại!")
            self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
            self.install_btn.setText("Thử lại")
            self.log(message, "[X]")
