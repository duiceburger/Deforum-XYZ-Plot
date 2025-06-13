@echo off
setlocal enabledelayedexpansion

:: Deforum Video Grid Generator Launcher
:: Place this file in the root directory containing batch output folders

echo =====================================================
echo         Deforum Video Grid Generator
echo =====================================================
echo.

:: Check for Python availability
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    echo Please install Python 3.6+ and ensure it's accessible
    pause
    exit /b 1
)

:: Check for deforum_video_grid.py in same directory
if not exist "%~dp0deforum_video_grid.py" (
    echo ERROR: deforum_video_grid.py not found in current directory
    echo Please ensure the Python script is in the same folder as this batch file
    pause
    exit /b 1
)

:: Display current directory and scan for batch folders
echo Current directory: %CD%
echo.
echo Scanning for batch output folders...
set folder_count=0
for /d %%i in (*) do (
    set /a folder_count+=1
)
echo Found %folder_count% subdirectories

echo.
echo =====================================================
echo Configuration Options
echo =====================================================

:: Get thumbnail size
set /p thumbnail_size="Enter thumbnail size in pixels (default: 150): "
if "%thumbnail_size%"=="" set thumbnail_size=150

:: Validate thumbnail size is numeric
echo %thumbnail_size%| findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo Invalid thumbnail size. Using default: 150
    set thumbnail_size=150
)

:: Get FPS
set /p fps="Enter output video FPS (default: 24): "
if "%fps%"=="" set fps=24

:: Validate FPS is numeric
echo %fps%| findstr /r "^[0-9][0-9]*$" >nul
if errorlevel 1 (
    echo Invalid FPS value. Using default: 24
    set fps=24
)

:: Get output filename
set /p output_name="Enter output filename (without extension, default: auto-generated): "

:: Get batch directory processing
echo.
echo Found %folder_count% batch output directories
echo Each directory will contribute one video to the grid
echo.

set /p confirm="Process all directories into single grid? (Y/n): "
if /i "%confirm%"=="n" (
    echo Operation cancelled.
    pause
    exit /b 0
)

set selected_dir=%CD%

:process
echo.
echo =====================================================
echo Processing Configuration
echo =====================================================
echo Directory: %selected_dir%
echo Thumbnail size: %thumbnail_size%px
echo FPS: %fps%
if not "%output_name%"=="" (
    echo Output filename: %output_name%.mp4
) else (
    echo Output filename: Auto-generated
)
echo.

:: Build command
set cmd_args="%selected_dir%" --size %thumbnail_size% --fps %fps%
if not "%output_name%"=="" (
    set cmd_args=%cmd_args% --output "%output_name%.mp4"
)

echo Executing: python deforum_video_grid.py %cmd_args%
echo.

:: Execute the Python script
python "%~dp0deforum_video_grid.py" %cmd_args%

if errorlevel 1 (
    echo.
    echo ERROR: Video grid generation failed
    echo Check the output above for error details
) else (
    echo.
    echo SUCCESS: Video grid generated successfully
    echo Grid contains %folder_count% videos arranged by parameter values
    echo Parameters detected: strength_schedule and cfg_scale_schedule
)

echo.
pause
exit /b 0

:invalid_selection
:: This section is now unused but kept for compatibility
echo Invalid selection. Please try again.
pause
exit /b 1