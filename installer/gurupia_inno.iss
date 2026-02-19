; GurupiaDict v0.2.0 - Inno Setup 6 Script
; Build: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\gurupia_inno.iss

[Setup]
AppId={{A7B3C2D1-E4F5-6789-ABCD-EF0123456789}
AppName=GurupiaDict
AppVersion=0.2.0
AppVerName=GurupiaDict 0.2.0
AppPublisher=Gurupia
AppPublisherURL=https://github.com/naby75/GurupiaDict
AppSupportURL=https://github.com/naby75/GurupiaDict
AppUpdatesURL=https://github.com/naby75/GurupiaDict/releases
DefaultDirName={localappdata}\GurupiaDict
DefaultGroupName=GurupiaDict
PrivilegesRequired=lowest
OutputDir=..\dist
OutputBaseFilename=GurupiaDict-v0.2.0-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ShowLanguageDialog=no
VersionInfoVersion=0.2.0
VersionInfoCompany=Gurupia
VersionInfoDescription=GurupiaDict Installer
VersionInfoProductName=GurupiaDict
VersionInfoProductVersion=0.2.0

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"

[Tasks]
Name: "desktopicon"; Description: "바탕화면에 아이콘 만들기"; GroupDescription: "추가 작업:"
Name: "startmenuicon"; Description: "시작 메뉴에 등록"; GroupDescription: "추가 작업:"

[Files]
Source: "..\SampleDict.db"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\viewer.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\parse.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\synthesize.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\query.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\QUICKSTART.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\gurupia-parser\target\release\gurupia-parser.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "..\gurupia-viewer\app.py"; DestDir: "{app}\gurupia-viewer"; Flags: ignoreversion
Source: "..\gurupia-viewer\static\index.html"; DestDir: "{app}\gurupia-viewer\static"; Flags: ignoreversion
Source: "..\gurupia-viewer\static\app.js"; DestDir: "{app}\gurupia-viewer\static"; Flags: ignoreversion
Source: "..\gurupia-viewer\static\style.css"; DestDir: "{app}\gurupia-viewer\static"; Flags: ignoreversion
Source: "..\gurupia-viewer\static\vendor\highlight.min.js"; DestDir: "{app}\gurupia-viewer\static\vendor"; Flags: ignoreversion
Source: "..\gurupia-viewer\static\vendor\github-dark.min.css"; DestDir: "{app}\gurupia-viewer\static\vendor"; Flags: ignoreversion
Source: "..\gurupia-viewer\static\vendor\purify.min.js"; DestDir: "{app}\gurupia-viewer\static\vendor"; Flags: ignoreversion
Source: "..\gurupia-synthesizer\synthesizer.py"; DestDir: "{app}\gurupia-synthesizer"; Flags: ignoreversion
Source: "..\gurupia-synthesizer\query.py"; DestDir: "{app}\gurupia-synthesizer"; Flags: ignoreversion

[Icons]
Name: "{autodesktop}\GurupiaDict"; Filename: "{app}\viewer_sample.bat"; WorkingDir: "{app}"; Comment: "GurupiaDict - 연결된 지식, 깨어있는 지혜"; Tasks: desktopicon
Name: "{group}\GurupiaDict"; Filename: "{app}\viewer_sample.bat"; WorkingDir: "{app}"; Tasks: startmenuicon
Name: "{group}\GurupiaDict 제거"; Filename: "{uninstallexe}"; Tasks: startmenuicon

[Run]
Filename: "py"; Parameters: "-3 -m pip install flask --quiet"; StatusMsg: "Flask 설치 중..."; Flags: runhidden waituntilterminated; Check: PythonExists
Filename: "{app}\viewer_sample.bat"; Description: "지금 GurupiaDict 실행하기"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
function PythonExists(): Boolean;
var
  ResultCode: Integer;
begin
  Result := Exec('py', '-3 --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode)
         and (ResultCode = 0);
  if not Result then
    Result := Exec('python', '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode)
           and (ResultCode = 0);
end;

function InitializeSetup(): Boolean;
var
  ErrorCode: Integer;
begin
  Result := True;
  if not PythonExists() then begin
    if MsgBox(
      'Python 3.8 이상이 필요합니다.' + #13#10 +
      '지금 Python 다운로드 페이지를 열겠습니까?',
      mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://www.python.org/downloads/', '', '', SW_SHOW, ewNoWait, ErrorCode);
    end;
  end;
end;

procedure CreateSampleBat();
var
  Lines: TStringList;
begin
  Lines := TStringList.Create;
  try
    Lines.Add('@echo off');
    Lines.Add('pushd "' + ExpandConstant('{app}') + '"');
    Lines.Add('call viewer.bat SampleDict.db');
    Lines.Add('popd');
    Lines.SaveToFile(ExpandConstant('{app}\viewer_sample.bat'));
  finally
    Lines.Free;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    CreateSampleBat();
end;
