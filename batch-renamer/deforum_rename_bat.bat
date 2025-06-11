@echo off
echo =====================================================
echo         Deforum Video Renamer
echo =====================================================
echo.
echo This will rename video files in Deforum output folders
echo to match their folder names.
echo.
echo Current directory: %CD%
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python first.
    pause
    exit /b 1
)

echo Python found! Starting rename process...
echo.

REM First show what would be renamed (dry run)
echo --- DRY RUN (showing what would be renamed) ---
python deforum_video_renamer.py --dry-run "%CD%"
echo.

set /p choice="Do you want to proceed with renaming? (y/N): "
if /i "%choice%" NEQ "y" (
    echo Operation cancelled.
    pause
    exit /b 0
)

echo.
echo --- RENAMING FILES ---
python deforum_video_renamer.py "%CD%"

echo.
echo Done! Press any key to exit...
pause