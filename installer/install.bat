@echo off
setlocal EnableDelayedExpansion

:: ================================================================
::   GurupiaDict v0.2.0 - Windows Installer
::   설치 경로: %LOCALAPPDATA%\GurupiaDict
::   - 바탕화면 아이콘 생성
::   - 시작 메뉴 그룹 생성
::   - 언인스톨러 등록
:: ================================================================

set VERSION=v0.2.0
set APP_NAME=GurupiaDict
set INSTALL_DIR=%LOCALAPPDATA%\%APP_NAME%
set MENU_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\%APP_NAME%
set SCRIPT_DIR=%~dp0

echo.
echo ================================================================
echo   %APP_NAME% %VERSION% Installer
echo   연결된 지식, 깨어있는 지혜
echo ================================================================
echo.
echo   설치 경로: %INSTALL_DIR%
echo.
set /p CONFIRM="계속하시겠습니까? [Y/N]: "
if /i not "%CONFIRM%"=="Y" (
    echo 설치를 취소했습니다.
    exit /b 0
)

:: ── Step 1: Python 확인 ──────────────────────────────────────
echo.
echo [1/6] Python 확인 중...
py -3 --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    python --version >nul 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo.
        echo ERROR: Python 3.8 이상이 필요합니다.
        echo   다운로드: https://www.python.org/downloads/
        pause & exit /b 1
    )
    set PYTHON=python
) else (
    set PYTHON=py -3
)
echo     OK (%PYTHON% 사용)

:: ── Step 2: Flask 설치 ───────────────────────────────────────
echo [2/6] Flask 의존성 설치 중...
%PYTHON% -m pip install flask --quiet
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pip install flask 실패
    pause & exit /b 1
)
echo     OK

:: ── Step 3: 설치 폴더 생성 ───────────────────────────────────
echo [3/6] 설치 폴더 생성 중...
if exist "%INSTALL_DIR%" (
    echo     기존 설치 발견 — 덮어씁니다.
    rmdir /s /q "%INSTALL_DIR%"
)
mkdir "%INSTALL_DIR%"
mkdir "%INSTALL_DIR%\gurupia-viewer\static\vendor"
mkdir "%INSTALL_DIR%\gurupia-synthesizer"
mkdir "%INSTALL_DIR%\bin"
echo     OK

:: ── Step 4: 파일 복사 ────────────────────────────────────────
echo [4/6] 파일 복사 중...

:: 소스 루트 결정 (installer\ 아래에서 실행 가능하도록 부모 기준)
set SRC=%SCRIPT_DIR%..

:: Parser exe
if exist "%SRC%bin\gurupia-parser.exe" (
    copy "%SRC%bin\gurupia-parser.exe" "%INSTALL_DIR%\bin\" >nul
) else if exist "%SRC%gurupia-parser\target\release\gurupia-parser.exe" (
    copy "%SRC%gurupia-parser\target\release\gurupia-parser.exe" "%INSTALL_DIR%\bin\" >nul
)

:: Viewer
copy "%SRC%gurupia-viewer\app.py"                        "%INSTALL_DIR%\gurupia-viewer\" >nul
copy "%SRC%gurupia-viewer\static\index.html"             "%INSTALL_DIR%\gurupia-viewer\static\" >nul
copy "%SRC%gurupia-viewer\static\app.js"                 "%INSTALL_DIR%\gurupia-viewer\static\" >nul
copy "%SRC%gurupia-viewer\static\style.css"              "%INSTALL_DIR%\gurupia-viewer\static\" >nul
for %%F in (highlight.min.js github-dark.min.css purify.min.js) do (
    copy "%SRC%gurupia-viewer\static\vendor\%%F" "%INSTALL_DIR%\gurupia-viewer\static\vendor\" >nul
)

:: Synthesizer
copy "%SRC%gurupia-synthesizer\synthesizer.py" "%INSTALL_DIR%\gurupia-synthesizer\" >nul
copy "%SRC%gurupia-synthesizer\query.py"       "%INSTALL_DIR%\gurupia-synthesizer\" >nul

:: Sample DB & scripts
copy "%SRC%SampleDict.db"    "%INSTALL_DIR%\" >nul
copy "%SRC%viewer.bat"       "%INSTALL_DIR%\" >nul
copy "%SRC%parse.bat"        "%INSTALL_DIR%\" >nul
copy "%SRC%synthesize.bat"   "%INSTALL_DIR%\" >nul
copy "%SRC%query.bat"        "%INSTALL_DIR%\" >nul
copy "%SRC%README.md"        "%INSTALL_DIR%\" >nul
copy "%SRC%QUICKSTART.md"    "%INSTALL_DIR%\" >nul
echo     OK

:: ── Step 5: 바탕화면 & 시작 메뉴 아이콘 ─────────────────────
echo [5/6] 바탕화면 및 시작 메뉴 아이콘 생성 중...

:: 아이콘용 VBS 런처 생성
(
    echo @echo off
    echo pushd "%INSTALL_DIR%"
    echo call viewer.bat SampleDict.db
    echo popd
) > "%INSTALL_DIR%\구루피아사전.bat"

:: PowerShell로 .lnk 바탕화면 아이콘 생성
powershell -NoProfile -Command ^
    "$s=(New-Object -COM WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Desktop')+'\\GurupiaDict.lnk');" ^
    "$s.TargetPath='%INSTALL_DIR%\\구루피아사전.bat';" ^
    "$s.WorkingDirectory='%INSTALL_DIR%';" ^
    "$s.Description='GurupiaDict - 연결된 지식, 깨어있는 지혜';" ^
    "$s.Save()"

:: 시작 메뉴
if not exist "%MENU_DIR%" mkdir "%MENU_DIR%"
powershell -NoProfile -Command ^
    "$s=(New-Object -COM WScript.Shell).CreateShortcut('%MENU_DIR%\\GurupiaDict.lnk');" ^
    "$s.TargetPath='%INSTALL_DIR%\\구루피아사전.bat';" ^
    "$s.WorkingDirectory='%INSTALL_DIR%';" ^
    "$s.Description='GurupiaDict - 연결된 지식, 깨어있는 지혜';" ^
    "$s.Save()"
echo     OK

:: ── Step 6: 언인스톨러 등록 (레지스트리) ────────────────────
echo [6/6] 언인스톨러 등록 중...

:: 언인스톨 배치 파일 생성
(
    echo @echo off
    echo echo GurupiaDict 제거 중...
    echo rmdir /s /q "%INSTALL_DIR%"
    echo del /f /q "%USERPROFILE%\Desktop\GurupiaDict.lnk" 2^>nul
    echo rmdir /s /q "%MENU_DIR%" 2^>nul
    echo reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\GurupiaDict" /f 2^>nul
    echo echo GurupiaDict 제거 완료!
    echo pause
) > "%INSTALL_DIR%\uninstall.bat"

:: 레지스트리에 언인스톨 항목 추가
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\GurupiaDict" ^
    /v "DisplayName" /t REG_SZ /d "GurupiaDict v0.2.0" /f >nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\GurupiaDict" ^
    /v "DisplayVersion" /t REG_SZ /d "0.2.0" /f >nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\GurupiaDict" ^
    /v "Publisher" /t REG_SZ /d "Gurupia" /f >nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\GurupiaDict" ^
    /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\uninstall.bat" /f >nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\GurupiaDict" ^
    /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f >nul
echo     OK

echo.
echo ================================================================
echo   설치 완료! GurupiaDict %VERSION%
echo.
echo   설치 경로  : %INSTALL_DIR%
echo   바탕화면   : GurupiaDict.lnk
echo   시작 메뉴  : %MENU_DIR%
echo.
echo   지금 실행하려면 바탕화면의 GurupiaDict 아이콘을 클릭하거나:
echo     cd "%INSTALL_DIR%"
echo     viewer.bat SampleDict.db
echo ================================================================
echo.
set /p LAUNCH="지금 바로 실행하시겠습니까? [Y/N]: "
if /i "%LAUNCH%"=="Y" (
    start "" "%INSTALL_DIR%\구루피아사전.bat"
)
pause
