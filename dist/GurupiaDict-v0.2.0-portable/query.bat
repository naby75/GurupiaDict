@echo off
REM GurupiaDict Query Tool Runner
REM Interactive knowledge graph explorer

echo.
echo ========================================
echo   GurupiaDict Query Tool
echo ========================================
echo.

if "%~1"=="" (
    echo Usage: query.bat database.db [--search query] [--view title] [--stats]
    echo.
    echo Examples:
    echo   query.bat GurupiaDict.db --interactive
    echo   query.bat GurupiaDict.db --search "컴퓨터"
    echo   query.bat GurupiaDict.db --view "프로그래밍 언어"
    echo   query.bat GurupiaDict.db --stats
    echo.
    exit /b 1
)

set DATABASE=%~1
set EXTRA_ARGS=%2 %3 %4 %5 %6 %7 %8 %9

if not exist "%DATABASE%" (
    echo ERROR: Database not found: %DATABASE%
    exit /b 1
)

echo Database: %DATABASE%
echo.

REM Run query tool
python gurupia-synthesizer\query.py "%DATABASE%" %EXTRA_ARGS%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Query failed with error code: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

echo.
