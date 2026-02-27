@echo off
REM GurupiaDict Web Viewer Runner

echo.
echo ========================================
echo   GurupiaDict Web Viewer
echo ========================================
echo.

if "%~1"=="" (
    echo Usage: viewer.bat database.db [--port PORT]
    echo.
    echo Example:
    echo   viewer.bat SampleDict.db
    echo   viewer.bat GurupiaDict.db --port 8080
    echo.
    exit /b 1
)

set DATABASE=%~1
shift
set EXTRA_ARGS=%1 %2 %3 %4 %5 %6

if not exist "%DATABASE%" (
    echo ERROR: Database not found: %DATABASE%
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Flask is not installed. Installing...
    python -m pip install flask
)

echo Database: %DATABASE%
echo.
echo Starting web server...
echo.

REM Run viewer
python gurupia-viewer\app.py "%DATABASE%" %EXTRA_ARGS%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Viewer failed with error code: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)
