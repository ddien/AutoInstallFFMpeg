"""
Test all required imports for PyInstaller build.
These tests ensure all modules used in the app can be imported.
"""

import pytest


class TestCoreImports:
    """Test imports used in core/installer.py"""

    def test_import_os(self):
        import os
        assert os is not None

    def test_import_sys(self):
        import sys
        assert sys is not None

    def test_import_subprocess(self):
        import subprocess
        assert subprocess is not None

    def test_import_zipfile(self):
        import zipfile
        assert zipfile is not None

    def test_import_shutil(self):
        import shutil
        assert shutil is not None

    def test_import_urllib_request(self):
        import urllib.request
        assert urllib.request is not None

    def test_import_winreg(self):
        import winreg
        assert winreg is not None

    def test_import_ctypes(self):
        import ctypes
        assert ctypes is not None

    def test_import_ctypes_windll(self):
        import ctypes
        assert hasattr(ctypes, 'windll')

    def test_import_pathlib(self):
        from pathlib import Path
        assert Path is not None


class TestUIImports:
    """Test imports used in ui/main_window.py"""

    def test_import_webbrowser(self):
        import webbrowser
        assert webbrowser is not None

    def test_import_pyqt6_widgets(self):
        from PyQt6.QtWidgets import QMainWindow, QWidget
        assert QMainWindow is not None
        assert QWidget is not None

    def test_import_pyqt6_core(self):
        from PyQt6.QtCore import Qt, QThread
        assert Qt is not None
        assert QThread is not None

    def test_import_pyqt6_gui(self):
        from PyQt6.QtGui import QFont, QIcon
        assert QFont is not None
        assert QIcon is not None


class TestModuleIntegration:
    """Test that modules can be used together"""

    def test_urllib_can_create_request(self):
        import urllib.request
        req = urllib.request.Request("https://example.com")
        assert req is not None

    def test_ctypes_can_access_windll(self):
        import ctypes
        # This should work on Windows
        assert ctypes.windll is not None

    def test_zipfile_can_be_used(self):
        import zipfile
        import io
        # Create in-memory zip
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as zf:
            zf.writestr('test.txt', 'hello')
        assert buffer.getvalue() is not None

    def test_pathlib_operations(self):
        from pathlib import Path
        p = Path(".")
        assert p.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
