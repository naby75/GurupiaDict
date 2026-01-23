# Win32 API Top 100 - 사용 빈도 높은 핵심 API

## Window Management (윈도우 관리)
- CreateWindowEx - 윈도우 생성
- DestroyWindow - 윈도우 제거
- ShowWindow - 윈도우 표시/숨김
- UpdateWindow - 윈도우 업데이트
- SetWindowText - 윈도우 제목 설정
- GetWindowText - 윈도우 제목 가져오기
- MoveWindow - 윈도우 이동/크기 변경
- SetWindowPos - 윈도우 위치 설정
- GetClientRect - 클라이언트 영역 크기
- GetWindowRect - 윈도우 전체 크기

## Message Handling (메시지 처리)
- GetMessage - 메시지 가져오기
- PeekMessage - 메시지 확인
- SendMessage - 메시지 전송 (동기)
- PostMessage - 메시지 전송 (비동기)
- DispatchMessage - 메시지 디스패치
- TranslateMessage - 메시지 변환
- DefWindowProc - 기본 메시지 처리

## GDI (Graphics Device Interface)
- BeginPaint - 그리기 시작
- EndPaint - 그리기 종료
- GetDC - 디바이스 컨텍스트 가져오기
- ReleaseDC - 디바이스 컨텍스트 해제
- TextOut - 텍스트 출력
- DrawText - 텍스트 그리기
- Rectangle - 사각형 그리기
- Ellipse - 타원 그리기
- LineTo - 선 그리기
- BitBlt - 비트맵 복사

## File I/O (파일 입출력)
- CreateFile - 파일 생성/열기
- ReadFile - 파일 읽기
- WriteFile - 파일 쓰기
- CloseHandle - 핸들 닫기
- GetFileSize - 파일 크기
- SetFilePointer - 파일 포인터 이동
- DeleteFile - 파일 삭제
- CopyFile - 파일 복사
- MoveFile - 파일 이동

## Memory Management (메모리 관리)
- VirtualAlloc - 가상 메모리 할당
- VirtualFree - 가상 메모리 해제
- HeapAlloc - 힙 메모리 할당
- HeapFree - 힙 메모리 해제
- GlobalAlloc - 전역 메모리 할당
- GlobalFree - 전역 메모리 해제

## Process/Thread (프로세스/스레드)
- CreateProcess - 프로세스 생성
- CreateThread - 스레드 생성
- ExitProcess - 프로세스 종료
- ExitThread - 스레드 종료
- WaitForSingleObject - 객체 대기
- Sleep - 대기
- GetCurrentProcess - 현재 프로세스
- GetCurrentThread - 현재 스레드

## Registry (레지스트리)
- RegOpenKeyEx - 레지스트리 키 열기
- RegCloseKey - 레지스트리 키 닫기
- RegQueryValueEx - 레지스트리 값 읽기
- RegSetValueEx - 레지스트리 값 쓰기
- RegCreateKeyEx - 레지스트리 키 생성
- RegDeleteKey - 레지스트리 키 삭제

## Common Controls (공통 컨트롤)
- CreateStatusWindow - 상태바 생성
- CreateToolbarEx - 툴바 생성
- ListView_InsertItem - 리스트뷰 항목 추가
- TreeView_InsertItem - 트리뷰 항목 추가

## Dialog (대화상자)
- DialogBox - 대화상자 표시
- CreateDialog - 대화상자 생성
- EndDialog - 대화상자 종료
- GetDlgItem - 대화상자 항목 가져오기
- SetDlgItemText - 대화상자 항목 텍스트 설정

## System Info (시스템 정보)
- GetSystemInfo - 시스템 정보
- GetVersionEx - 버전 정보
- GetComputerName - 컴퓨터 이름
- GetUserName - 사용자 이름

## Error Handling (에러 처리)
- GetLastError - 마지막 에러 코드
- FormatMessage - 에러 메시지 포맷
- SetLastError - 에러 코드 설정

## Keyboard/Mouse (키보드/마우스)
- GetKeyState - 키 상태
- GetAsyncKeyState - 비동기 키 상태
- SetCursor - 커서 설정
- GetCursorPos - 커서 위치
- SetCursorPos - 커서 위치 설정

## Timer (타이머)
- SetTimer - 타이머 설정
- KillTimer - 타이머 제거
- GetTickCount - 틱 카운트

## String (문자열)
- lstrlen - 문자열 길이
- lstrcpy - 문자열 복사
- lstrcat - 문자열 연결
- lstrcmp - 문자열 비교

## Clipboard (클립보드)
- OpenClipboard - 클립보드 열기
- CloseClipboard - 클립보드 닫기
- SetClipboardData - 클립보드 데이터 설정
- GetClipboardData - 클립보드 데이터 가져오기

---

**총 100개 핵심 API**

이 목록은 실제 Win32 프로그래밍에서 가장 자주 사용되는 API들입니다.
