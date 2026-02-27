@echo off
REM GurupiaDict Synthesizer Runner
REM Converts JSONL to SQLite database

echo.
echo ========================================
echo   GurupiaDict Synthesizer (Python)
echo ========================================
echo.

if "%~1"=="" (
    echo Usage: synthesize.bat input.jsonl output.db [--reset] [--stats]
    echo.
    echo Example:
    echo   synthesize.bat wiki_nodes.jsonl GurupiaDict.db --stats
    echo.
    exit /b 1
)

if "%~2"=="" (
    echo Usage: synthesize.bat input.jsonl output.db [--reset] [--stats]
    echo.
    exit /b 1
)

set INPUT_JSONL=%~1
set OUTPUT_DB=%~2
set EXTRA_ARGS=%3 %4 %5 %6

if not exist "%INPUT_JSONL%" (
    echo ERROR: Input file not found: %INPUT_JSONL%
    exit /b 1
)

echo Input:  %INPUT_JSONL%
echo Output: %OUTPUT_DB%
echo.

REM Run synthesizer
python gurupia-synthesizer\synthesizer.py "%INPUT_JSONL%" "%OUTPUT_DB%" %EXTRA_ARGS%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Synthesis completed successfully!
    echo Database ready at: %OUTPUT_DB%
) else (
    echo.
    echo ❌ Synthesis failed with error code: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

echo.
pause
