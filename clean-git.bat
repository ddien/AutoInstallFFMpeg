@echo off
:: Clean desktop.ini files from .git folder (Google Drive sync issue)
:: Run this if you get "fatal: bad object refs/desktop.ini" error

echo Cleaning desktop.ini from .git folder...

for /r ".git" %%f in (desktop.ini) do (
    if exist "%%f" (
        del /f /q "%%f"
        echo Deleted: %%f
    )
)

echo Done!
pause
