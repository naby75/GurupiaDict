# 🏛️ GurupiaDict — Dynamic Intelligence Connective Taxonomy

**"연결된 지식, 깨어있는 지혜"** 🕸️ | **v0.2.0**

GurupiaDict는 위키백과 XML 덤프에서 지식을 추출하여 **오프라인에서 완전히 동작하는** 고성능 지식 그래프 사전 시스템입니다.

---

## 🚀 주요 기능

| 구성 요소 | 언어 | 역할 |
|-----------|------|------|
| **Gurupia-Parser** | 🦀 Rust | 위키백과 XML 스트리밍 파싱 |
| **Gurupia-Synthesizer** | 🐍 Python | JSONL → SQLite 지식 그래프 구축 |
| **Gurupia-Viewer** | 🌐 Flask | 웹 뷰어 (오프라인 완전 동작) |

### Gurupia-Parser (Rust v0.2.0)
- ✅ `quick-xml` 고속 스트리밍 파싱 — 690만 페이지 처리 가능
- ✅ `LazyLock` 기반 Regex 캐싱 — 재컴파일 없음 (v0.2.0 성능 개선)
- ✅ UTF-8 안전 절단 (`char_indices()` 기반)
- ✅ `#REDIRECT` / `#redirect` / `#넘겨주기` 자동 필터
- ✅ 동음이의어 페이지 필터, 첫 문단 지능형 추출
- ✅ JSONL 포맷 출력

### Gurupia-Synthesizer (Python v0.2.0)
- ✅ `[[위키링크]]` 패턴 추출 → 노드/엣지 지식 그래프 구축
- ✅ Bi-directional Backlink 쿼리 지원
- ✅ WAL 모드 + 배치 커밋(1,000건) — 대용량 안정성 강화
- ✅ SQLite FTS5 전체 텍스트 검색 인덱스
- ✅ `GurupiaSynthesizer → GurupiaQuery` 상속 구조

### Gurupia-Viewer (Flask + Vanilla JS)
- ✅ **완전 오프라인 동작** — highlight.js, DOMPurify 로컬 번들
- ✅ 다크 / 라이트 모드 토글 (localStorage 저장)
- ✅ DOMPurify XSS 방어
- ✅ 언어별 아이콘 (🐍🪟📜🎨🌐🦀🎯💬)
- ✅ 코드 블록 클릭 복사, TTS 읽기 기능

---

## 📦 설치 및 실행

### 방법 1: 포터블 버전 (설치 불필요)
`dist/GurupiaDict-v0.2.0-portable.zip`을 압축 해제하고:
```batch
viewer.bat SampleDict.db
```
브라우저에서 http://localhost:5000 접속

### 방법 2: 설치 스크립트 사용
```batch
installer\install.bat
```
`%LOCALAPPDATA%\GurupiaDict`에 설치 + 바탕화면 아이콘 생성

### 방법 3: 소스에서 직접 실행
전제 조건: [Rust](https://rustup.rs), [Python 3.8+](https://www.python.org)
```batch
pip install flask
viewer.bat SampleDict.db
```

---

## 🗺️ 프로젝트 구조

```
GurupiaDict/
├── gurupia-parser/          🦀 Rust — XML 파서
│   └── src/main.rs
├── gurupia-synthesizer/     🐍 Python — DB 구축
│   ├── synthesizer.py
│   └── query.py
├── gurupia-viewer/          🌐 Flask — 웹 뷰어
│   ├── app.py
│   └── static/
│       ├── vendor/          📦 오프라인 번들 (highlight.js, DOMPurify)
│       ├── app.js
│       ├── style.css
│       └── index.html
├── SampleDict.db            💾 샘플 사전 (50개 문서)
├── viewer.bat               ▶️  뷰어 실행
├── demo.bat                 🧪  데모 파이프라인
└── build_portable.bat       📦  포터블 버전 빌드
```

---

## 📖 파이프라인 사용법

### Step 1: 한국어 위키백과 파싱
```batch
cd gurupia-parser
cargo build --release
target\release\gurupia-parser.exe kowiki.xml output.jsonl
```

### Step 2: SQLite 데이터베이스 구축
```batch
python gurupia-synthesizer\synthesizer.py output.jsonl GurupiaDict.db --stats
```

### Step 3: Web Viewer 실행
```batch
viewer.bat GurupiaDict.db
```

---

## 📊 성능 수치 (GurupiaDict_Complete.db 기준)

| 항목 | 수치 |
|------|------|
| 총 문서 | 690,422 개 |
| 총 링크 (지식 그래프 엣지) | 26,710,233 개 |
| FTS5 검색 응답 | < 50ms |
| XML 파싱 속도 | ~5만 문서/초 |

---

## 🗄️ 데이터베이스 스키마

```sql
-- 문서 저장
CREATE TABLE Nodes (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE NOT NULL,
    raw_content TEXT NOT NULL,
    html_content TEXT NOT NULL,
    created_at TIMESTAMP
);

-- 지식 그래프 엣지
CREATE TABLE Edges (
    id INTEGER PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES Nodes(id),
    target_title TEXT NOT NULL,
    edge_type TEXT DEFAULT 'reference'
);

-- FTS5 전체 텍스트 검색
CREATE VIRTUAL TABLE NodesFTS USING fts5(title, content, tokenize='unicode61');
```

---

## 📜 라이선스

교육 및 개인 용도 자유 사용 가능.

---

**GurupiaDict** — *연결된 지식, 깨어있는 지혜* 🕸️
Created with 🦀 Rust · 🐍 Python · 💾 SQLite · 🌐 Flask
