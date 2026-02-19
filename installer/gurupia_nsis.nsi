; GurupiaDict v0.2.0 -- NSIS MUI2 Installer
; Build: "C:\Program Files (x86)\NSIS\makensis.exe" installer\gurupia_nsis.nsi

Unicode True

!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "FileFunc.nsh"

!define PRODUCT_NAME      "GurupiaDict"
!define PRODUCT_VERSION   "0.2.0"
!define PRODUCT_PUBLISHER "Gurupia"
!define PRODUCT_URL       "https://github.com/naby75/GurupiaDict"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_DIR_REG   "Software\${PRODUCT_NAME}"

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "..\dist\GurupiaDict-v${PRODUCT_VERSION}-setup-nsis.exe"
InstallDir "$LOCALAPPDATA\${PRODUCT_NAME}"
InstallDirRegKey HKCU "${PRODUCT_DIR_REG}" "InstallPath"
ShowInstDetails   show
ShowUninstDetails show
RequestExecutionLevel user

!define MUI_ABORTWARNING
!define MUI_WELCOMEPAGE_TITLE  "GurupiaDict ${PRODUCT_VERSION}"
!define MUI_WELCOMEPAGE_TEXT   "Knowledge graph dictionary installer.$\r$\n$\r$\nKorean Wikipedia 690,422 articles + DevDict (Win32/Python/MDN/Rust) offline viewer."
!define MUI_FINISHPAGE_RUN         "$INSTDIR\viewer_sample.bat"
!define MUI_FINISHPAGE_RUN_TEXT    "Launch GurupiaDict now"
!define MUI_FINISHPAGE_LINK        "${PRODUCT_URL}"
!define MUI_FINISHPAGE_LINK_TEXT   "GitHub Repository"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE    "..\README.md"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Korean"

; ---- Install Section ----
Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    File /oname=SampleDict.db       "..\SampleDict.db"
    File /oname=viewer.bat          "..\viewer.bat"
    File /oname=parse.bat           "..\parse.bat"
    File /oname=synthesize.bat      "..\synthesize.bat"
    File /oname=query.bat           "..\query.bat"
    File /oname=README.md           "..\README.md"
    File /oname=QUICKSTART.md       "..\QUICKSTART.md"
    File /oname=CHANGELOG.md        "..\CHANGELOG.md"

    SetOutPath "$INSTDIR\bin"
    File /oname=gurupia-parser.exe "..\gurupia-parser\target\release\gurupia-parser.exe"

    SetOutPath "$INSTDIR\gurupia-viewer"
    File "..\gurupia-viewer\app.py"

    SetOutPath "$INSTDIR\gurupia-viewer\static"
    File "..\gurupia-viewer\static\index.html"
    File "..\gurupia-viewer\static\app.js"
    File "..\gurupia-viewer\static\style.css"

    SetOutPath "$INSTDIR\gurupia-viewer\static\vendor"
    File "..\gurupia-viewer\static\vendor\highlight.min.js"
    File "..\gurupia-viewer\static\vendor\github-dark.min.css"
    File "..\gurupia-viewer\static\vendor\purify.min.js"

    SetOutPath "$INSTDIR\gurupia-synthesizer"
    File "..\gurupia-synthesizer\synthesizer.py"
    File "..\gurupia-synthesizer\query.py"

    ; Create launcher batch
    SetOutPath "$INSTDIR"
    FileOpen  $0 "$INSTDIR\viewer_sample.bat" w
    FileWrite $0 "@echo off$\r$\n"
    FileWrite $0 "pushd $\"$INSTDIR$\"$\r$\n"
    FileWrite $0 "call viewer.bat SampleDict.db$\r$\n"
    FileWrite $0 "popd$\r$\n"
    FileClose $0

    WriteUninstaller "$INSTDIR\uninstall.exe"

    WriteRegStr HKCU "${PRODUCT_DIR_REG}"    "InstallPath"     "$INSTDIR"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayName"     "${PRODUCT_NAME} ${PRODUCT_VERSION}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "DisplayVersion"  "${PRODUCT_VERSION}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "Publisher"       "${PRODUCT_PUBLISHER}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "URLInfoAbout"    "${PRODUCT_URL}"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKCU "${PRODUCT_UNINST_KEY}" "InstallLocation" "$INSTDIR"

    CreateShortcut "$DESKTOP\GurupiaDict.lnk" "$INSTDIR\viewer_sample.bat" "" "$INSTDIR\viewer_sample.bat" 0
    CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
    CreateShortcut "$SMPROGRAMS\${PRODUCT_NAME}\GurupiaDict.lnk" "$INSTDIR\viewer_sample.bat"
    CreateShortcut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk"   "$INSTDIR\uninstall.exe"
SectionEnd

; ---- Uninstall Section ----
Section "Uninstall"
    RMDir /r "$INSTDIR\gurupia-viewer"
    RMDir /r "$INSTDIR\gurupia-synthesizer"
    RMDir /r "$INSTDIR\bin"
    Delete   "$INSTDIR\SampleDict.db"
    Delete   "$INSTDIR\*.bat"
    Delete   "$INSTDIR\*.md"
    Delete   "$INSTDIR\uninstall.exe"
    RMDir    "$INSTDIR"

    Delete "$DESKTOP\GurupiaDict.lnk"
    RMDir /r "$SMPROGRAMS\${PRODUCT_NAME}"

    DeleteRegKey HKCU "${PRODUCT_UNINST_KEY}"
    DeleteRegKey HKCU "${PRODUCT_DIR_REG}"
SectionEnd
