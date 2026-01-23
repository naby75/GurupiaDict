# Win32Dict - 1000개 API 수집 전략

## 🎯 목표: 1000개 핵심 Win32 API

### 전략: 주요 헤더 파일별로 수집

## 주요 헤더 파일 (API 개수 추정)

### 1. User32.dll (윈도우/메시지) - 약 300개
- CreateWindow, ShowWindow, GetMessage, SendMessage...
- 윈도우 관리, 메시지 처리, 입력 처리

### 2. Kernel32.dll (시스템/파일) - 약 200개  
- CreateFile, ReadFile, CreateProcess, CreateThread...
- 파일 I/O, 프로세스/스레드, 메모리 관리

### 3. GDI32.dll (그래픽) - 약 150개
- BeginPaint, TextOut, Rectangle, BitBlt...
- 그래픽 출력, 폰트, 비트맵

### 4. Advapi32.dll (보안/레지스트리) - 약 100개
- RegOpenKey, RegQueryValue, CreateService...
- 레지스트리, 서비스, 보안

### 5. Shell32.dll (쉘) - 약 80개
- SHGetFolderPath, ShellExecute...
- 파일 탐색기, 쉘 통합

### 6. Comctl32.dll (공통 컨트롤) - 약 70개
- ListView, TreeView, ToolBar...
- 리스트뷰, 트리뷰, 툴바

### 7. Ole32.dll (COM) - 약 50개
- CoInitialize, CoCreateInstance...
- COM 인터페이스

### 8. WinInet.dll (인터넷) - 약 50개
- InternetOpen, HttpSendRequest...
- HTTP, FTP

---

## 📊 총합: 약 1000개

이 방식으로 주요 헤더별로 크롤링하면 실용적인 1000개를 확보할 수 있습니다.

## 🚀 구현 방법

1. Microsoft Learn에서 각 헤더 파일 페이지 크롤링
2. 각 헤더의 함수 목록 추출
3. 각 함수의 상세 페이지 크롤링
4. JSONL로 저장

**예상 시간: 약 30분~1시간**
