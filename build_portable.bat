@echo off
setlocal EnableDelayedExpansion

:: ================================================================
::   GurupiaDict - Portable Build Script
::   출력: dist\GurupiaDict-v0.2.0-portable\
::          dist\GurupiaDict-v0.2.0-portable.zip
:: ================================================================

set VERSION=v0.2.0
set DIST_DIR=dist\GurupiaDict-%VERSION%-portable
set ZIP_OUT=dist\GurupiaDict-%VERSION%-portable.zip

echo.
echo ================================================================
echo   GurupiaDict %VERSION% - Portable Build
echo ================================================================
echo.

:: 1. Rust 빌드
echo [1/5] Building Rust parser...
cd gurupia-parser
cargo build --release 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: cargo build failed
    cd ..
    pause & exit /b 1
)
cd ..
echo     OK

:: 2. 포터블 폴더 초기화
echo [2/5] Creating portable folder structure...
if exist "%DIST_DIR%" rmdir /s /q "%DIST_DIR%"
mkdir "%DIST_DIR%"
mkdir "%DIST_DIR%\gurupia-viewer\static\vendor"
mkdir "%DIST_DIR%\gurupia-synthesizer"
mkdir "%DIST_DIR%\bin"
echo     OK

:: 3. 파일 복사
echo [3/5] Copying files...

:: Parser exe
copy "gurupia-parser\target\release\gurupia-parser.exe" "%DIST_DIR%\bin\" >nul

:: Viewer
copy "gurupia-viewer\app.py"                        "%DIST_DIR%\gurupia-viewer\" >nul
copy "gurupia-viewer\static\index.html"             "%DIST_DIR%\gurupia-viewer\static\" >nul
copy "gurupia-viewer\static\app.js"                 "%DIST_DIR%\gurupia-viewer\static\" >nul
copy "gurupia-viewer\static\style.css"              "%DIST_DIR%\gurupia-viewer\static\" >nul
copy "gurupia-viewer\static\vendor\highlight.min.js"    "%DIST_DIR%\gurupia-viewer\static\vendor\" >nul
copy "gurupia-viewer\static\vendor\github-dark.min.css" "%DIST_DIR%\gurupia-viewer\static\vendor\" >nul
copy "gurupia-viewer\static\vendor\purify.min.js"       "%DIST_DIR%\gurupia-viewer\static\vendor\" >nul

:: Synthesizer
copy "gurupia-synthesizer\synthesizer.py"           "%DIST_DIR%\gurupia-synthesizer\" >nul
copy "gurupia-synthesizer\query.py"                 "%DIST_DIR%\gurupia-synthesizer\" >nul

:: Sample DB
copy "SampleDict.db"    "%DIST_DIR%\" >nul

:: Batch scripts
copy "viewer.bat"       "%DIST_DIR%\" >nul
copy "parse.bat"        "%DIST_DIR%\" >nul
copy "synthesize.bat"   "%DIST_DIR%\" >nul
copy "query.bat"        "%DIST_DIR%\" >nul
copy "demo.bat"         "%DIST_DIR%\" >nul

:: Docs
copy "README.md"        "%DIST_DIR%\" >nul
copy "QUICKSTART.md"    "%DIST_DIR%\" >nul
copy "CHANGELOG.md"     "%DIST_DIR%\" >nul

echo     OK

:: 4. requirements.txt 생성
echo [4/5] Generating requirements.txt...
(
    echo flask^>=2.0
    echo lxml^>=4.9
) > "%DIST_DIR%\requirements.txt"
echo     OK

:: 5. ZIP 압축
echo [5/5] Creating ZIP archive...
if exist "%ZIP_OUT%" del "%ZIP_OUT%"
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command "Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('%CD%\%DIST_DIR%', '%CD%\%ZIP_OUT%')"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: ZIP creation failed
    pause & exit /b 1
)
echo     OK

echo.
echo ================================================================
echo   BUILD COMPLETE!
echo.

for %%F in ("%ZIP_OUT%") do (
    set /a SIZE_KB=%%~zF / 1024
    echo   Portable ZIP : %ZIP_OUT% (!SIZE_KB! KB^)
)
echo   Portable DIR : %DIST_DIR%
echo.
echo   Quick Start:
echo     cd %DIST_DIR%
echo     pip install -r requirements.txt
echo     viewer.bat SampleDict.db
echo ================================================================
echo.
pause
