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

### Git error: fatal: bad object refs/desktop.ini
This happens because Google Drive creates `desktop.ini` files inside `.git/` folder.

**Fix:**
```batch
clean-git.bat
```

**Prevention:**
- A pre-commit hook auto-cleans these files before each commit
- Hook location: `.git/hooks/pre-commit`

## Planning Workflow

### ALWAYS Create Plan File First
Before starting any task, create a plan file in `docs/plans/`:

**Naming Convention:** `YYYY-MM-DD-[type]-[short-name].md`

**Types:**
- `feature` - New functionality
- `bugfix` - Bug fixes
- `refactor` - Code improvements
- `docs` - Documentation updates
- `chore` - Maintenance tasks

**Examples:**
```
docs/plans/
├── 2025-02-10-bugfix-pyinstaller-imports.md
├── 2025-02-10-bugfix-git-desktop-ini.md
├── 2025-02-11-feature-auto-update.md
└── 2025-02-12-refactor-installer-class.md
```

### Plan File Template
```markdown
# YYYY-MM-DD [Type] Short Name

## Goal
[Clear description of what needs to be done]

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Status
- Started: YYYY-MM-DD HH:MM
- Completed: [pending]

## Notes
[Any relevant notes, blockers, decisions]

## Related Files
- `path/to/file1.py`
- `path/to/file2.py`
```

### Update Plan When Done
After completing each step:
1. Mark step as done: `- [x] Step 1`
2. Add completion timestamp
3. Document any issues encountered
4. Move completed plans to `docs/plans/completed/` (optional)

---

## TDD Workflow (Test-Driven Development)

### Core Principles
1. **Tests BEFORE Code** - Always write tests first
2. **Coverage Target** - Minimum 80% coverage
3. **Test All Paths** - Happy path + error cases + edge cases

### TDD Cycle
```
1. Write Test (RED)    → Test fails (expected)
2. Write Code (GREEN)  → Minimal code to pass
3. Refactor (CLEAN)    → Improve while tests stay green
4. Repeat
```

### Test Types for This Project

#### Unit Tests (`tests/test_*.py`)
```python
# tests/test_installer.py
import pytest
from core.installer import FFmpegInstaller

class TestFFmpegInstaller:
    def test_check_installed_returns_tuple(self):
        installer = FFmpegInstaller()
        result = installer.check_installed()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_find_local_zip_returns_path_or_none(self):
        installer = FFmpegInstaller()
        result = installer.find_local_zip()
        assert result is None or result.exists()
```

#### Import Tests (`tests/test_imports.py`)
```python
# Verify all modules for PyInstaller
def test_import_ctypes():
    import ctypes
    assert ctypes.windll is not None
```

### Running Tests
```batch
# Install pytest first
pip install pytest pytest-cov

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Test File Organization
```
tests/
├── test_imports.py      # PyInstaller module verification
├── test_installer.py    # Core installer logic tests
├── test_main_window.py  # UI component tests (mock Qt)
└── conftest.py          # Shared fixtures
```

---

## Development Workflow
1. **Plan** - Create `docs/plans/YYYY-MM-DD-[type]-[name].md`
2. **Test First** - Write failing tests
3. **Implement** - Write minimal code to pass tests
4. **Refactor** - Clean up while keeping tests green
5. **Build** - Run `build.bat` or use .spec file
6. **Verify** - Test .exe on clean machine
7. **Update Plan** - Mark tasks complete, move to `completed/`

## Key Files to Edit
- `src/version.py` - Update version before release
- `FFmpegSetup_v1.0.0.spec` - Add hidden imports if needed
- `src/core/installer.py` - Core installation logic
- `src/ui/main_window.py` - GUI updates
- `docs/plans/` - Task plans (active and completed)
