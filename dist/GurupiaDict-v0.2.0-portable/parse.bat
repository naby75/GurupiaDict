@echo off
REM GurupiaDict Parser Runner
REM Parses Wikipedia XML dump to JSONL format

echo.
echo ========================================
echo   GurupiaDict Parser (Rust)
echo ========================================
echo.

if "%~1"=="" (
    echo Usage: parse.bat input.xml output.jsonl
    echo.
    echo Example:
    echo   parse.bat kowiki-latest-pages-articles.xml wiki_nodes.jsonl
    echo.
    exit /b 1
)

if "%~2"=="" (
    echo Usage: parse.bat input.xml output.jsonl
    echo.
    exit /b 1
)

set INPUT_XML=%~1
set OUTPUT_JSONL=%~2

if not exist "%INPUT_XML%" (
    echo ERROR: Input file not found: %INPUT_XML%
    exit /b 1
)

echo Input:  %INPUT_XML%
echo Output: %OUTPUT_JSONL%
echo.

REM Build parser if needed
if not exist "gurupia-parser\target\release\gurupia-parser.exe" (
    echo Building Rust parser...
    cd gurupia-parser
    cargo build --release
    cd ..
    echo.
)

REM Run parser
echo Starting parser...
gurupia-parser\target\release\gurupia-parser.exe "%INPUT_XML%" "%OUTPUT_JSONL%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Parsing completed successfully!
    echo Output saved to: %OUTPUT_JSONL%
) else (
    echo.
    echo ❌ Parsing failed with error code: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

echo.
pause
