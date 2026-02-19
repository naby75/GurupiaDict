@echo off
:: ================================================================
::   GurupiaDict — 통합 릴리즈 빌드 스크립트
::   생성 산출물:
::     dist\GurupiaDict-v0.2.0-portable\    (포터블 폴더)
::     dist\GurupiaDict-v0.2.0-portable.zip (포터블 ZIP)
::     dist\GurupiaDict-v0.2.0-setup.exe    (Inno Setup 설치파일)
::     dist\GurupiaDict-v0.2.0-setup-nsis.exe (NSIS 설치파일)
:: ================================================================
setlocal
set VERSION=v0.2.0
set NSIS="C:\Program Files (x86)\NSIS\makensis.exe"
set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

if not exist dist mkdir dist

echo.
echo ================================================================
echo   GurupiaDict %VERSION% - Full Release Build
echo ================================================================
echo.

:: ── 1. Rust 빌드 ────────────────────────────────────────────────
echo [1/4] Rust parser build (cargo release)...
cd gurupia-parser && cargo build --release 2>&1
if %ERRORLEVEL% NEQ 0 ( echo FAILED & cd .. & pause & exit /b 1 )
cd ..
echo     DONE

:: ── 2. 포터블 버전 ──────────────────────────────────────────────
echo [2/4] Building portable version...
call build_portable.bat >nul 2>&1
echo     DONE

:: ── 3. Inno Setup 설치파일 ──────────────────────────────────────
echo [3/4] Building Inno Setup installer...
%ISCC% /Q "installer\gurupia_inno.iss"
if %ERRORLEVEL% NEQ 0 ( echo FAILED (ISCC) & echo Inno Setup 경로: %ISCC% ) else ( echo     DONE )

:: ── 4. NSIS 설치파일 ────────────────────────────────────────────
echo [4/4] Building NSIS installer...
%NSIS% /V2 "installer\gurupia_nsis.nsi"
if %ERRORLEVEL% NEQ 0 ( echo FAILED (makensis) & echo NSIS 경로: %NSIS% ) else ( echo     DONE )

echo.
echo ================================================================
echo   OUTPUT FILES:
for %%F in (dist\*.zip dist\*.exe) do (
    for %%S in ("%%F") do echo   %%~nxF  ^(%%~zS bytes^)
)
echo ================================================================
echo.
pause
