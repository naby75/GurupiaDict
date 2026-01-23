# Win32Dict - Microsoft Win32 API 오프라인 레퍼런스

## 🎯 목표

Microsoft Learn의 Win32 API 문서를 오프라인에서 빠르게 검색할 수 있는 사전

```
현재: 인터넷 → learn.microsoft.com → 검색 → 로딩
Win32Dict: 오프라인 → 로컬 검색 → 즉시 결과
```

## 📚 프로젝트 구조

```
Win32Dict/
├── win32_crawler.py      # Microsoft Docs 크롤러
├── win32dict_data/        # 크롤링된 데이터
│   └── win32_api.jsonl
├── Win32Dict.db           # SQLite 데이터베이스
└── viewer/                # 웹 뷰어 (GurupiaDict 재사용)
```

## 🚀 사용 방법

### 1단계: 데이터 크롤링

```bash
# 테스트 (10개 페이지)
python win32_crawler.py --max-pages 10

# 전체 크롤링 (시간 소요)
python win32_crawler.py --max-pages 1000
```

### 2단계: 데이터베이스 생성

```bash
# GurupiaDict synthesizer 재사용
python gurupia-synthesizer\synthesizer.py win32dict_data\win32_api.jsonl Win32Dict.db --reset
```

### 3단계: 웹 뷰어 실행

```bash
# GurupiaDict viewer 재사용
python gurupia-viewer\app.py Win32Dict.db
```

## 📊 예상 규모

| 항목 | 수량 |
|------|------|
| Win32 API 함수 | 2,000~3,000 |
| 구조체/인터페이스 | 1,000~2,000 |
| 총 문서 | 3,000~5,000 |
| DB 크기 | 50~100 MB |

## 🎯 특징

- ✅ **완전 오프라인** - 인터넷 불필요
- ✅ **빠른 검색** - FTS5 전체 텍스트 검색
- ✅ **코드 예제** - 실제 사용 예제 포함
- ✅ **관련 API** - Backlink로 연결된 API 탐색
- ✅ **최신 문서** - Microsoft Learn 기준

## 🔧 개선 계획

### Phase 1: Win32 API (현재)
- Core API 크롤링
- 기본 검색 기능

### Phase 2: 확장
- .NET API Reference
- C# Language Reference
- PowerShell Cmdlets

### Phase 3: 고급 기능
- 코드 하이라이팅
- 예제 복사 버튼
- 버전별 차이점 표시

## 📝 주의사항

- Microsoft Docs를 크롤링하므로 **로봇 예절** 준수
- 크롤링 간격: 1초 (서버 부하 방지)
- 개인 사용 목적 권장

## 🎉 완성 예정

**Win32Dict - 개발자를 위한 빠른 Win32 API 레퍼런스!**

---

**GurupiaDict 프로젝트의 확장판입니다!** 🚀
