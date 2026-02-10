"""
FFmpeg Auto Setup - Entry Point
"""

import sys
import os

# Ensure we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.main_window import MainWindow


def get_resource_path(relative_path):
    """Get path for bundled resources (works with PyInstaller)"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set app icon
    icon_path = get_resource_path("assets/icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
