@echo off
REM One-click AutoIt Support Installer for claude-code-indexer
REM Windows Batch File

echo ===================================================
echo  AutoIt Support Installer for claude-code-indexer
echo ===================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+ first.
    echo Download from: https://python.org
    pause
    exit /b 1
)

echo [INFO] Python found - proceeding with installation...
echo.

REM Run the simple installer
python simple-autoit-installer.py

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo  Installation completed successfully!
echo ===================================================
echo.
echo You can now use AutoIt support with:
echo   claude-code-indexer index /path/to/autoit/project
echo   claude-code-indexer query --important
echo.
echo Supported file types: .au3, .aut, .a3x
echo.
pause