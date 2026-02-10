# FFmpeg Auto Setup - Project Guidelines

## Project Overview
A Windows GUI application that automatically downloads, installs, and configures FFmpeg with PATH environment variable setup.

## Tech Stack
- **Language**: Python 3.11+
- **GUI Framework**: PyQt6
- **Bundler**: PyInstaller (creates standalone .exe)
- **Target OS**: Windows only

## Project Structure
```
AutoFixFFMpeg/
├── src/
│   ├── main.py              # Entry point
│   ├── version.py           # Version info
│   ├── core/
│   │   ├── __init__.py
│   │   └── installer.py     # FFmpeg installation logic
│   └── ui/
│       ├── __init__.py
│       └── main_window.py   # PyQt6 GUI
├── assets/
│   └── icon.ico             # App icon
├── tests/
│   └── test_imports.py      # Import verification tests
├── build.bat                # Build script
├── FFmpegSetup_v1.0.0.spec  # PyInstaller spec file
└── requirements.txt         # Dependencies
```

## Build Instructions

### Using .spec file (Recommended)
```batch
pyinstaller FFmpegSetup_v1.0.0.spec --clean
```

### Using build.bat
```batch
build.bat
```

## PyInstaller Hidden Imports
When building with PyInstaller, these standard library modules MUST be explicitly included as hidden imports:

```python
hidden_imports = [
    'webbrowser',        # For opening URLs
    'urllib',            # URL handling
    'urllib.request',    # HTTP downloads
    'urllib.error',
    'urllib.parse',
    'http',
    'http.client',
    'winreg',            # Windows registry access
    'ctypes',            # Windows API calls
    'ctypes.wintypes',
    'zipfile',           # ZIP extraction
    'shutil',            # File operations
    'subprocess',        # Running FFmpeg
    'pathlib',
    'ssl',               # HTTPS support
    'encodings',         # Text encoding
    'encodings.utf_8',
    'codecs',
]
```

## Common Issues

### ModuleNotFoundError in bundled exe
If the built .exe shows `ModuleNotFoundError`, add the missing module to:
1. `FFmpegSetup_v1.0.0.spec` -> `hiddenimports` list
2. `build.bat` -> `--hidden-import` flags

### Testing imports before build
Run the import test to verify all modules are available:
```batch
python -m pytest tests/test_imports.py -v
```

## Development Workflow
1. Make code changes
2. Run import tests
3. Build using .spec file
4. Test the .exe on a clean machine (no Python installed)

## Key Files to Edit
- `src/version.py` - Update version before release
- `FFmpegSetup_v1.0.0.spec` - Add hidden imports if needed
- `src/core/installer.py` - Core installation logic
- `src/ui/main_window.py` - GUI updates
