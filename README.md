# 🏛️ GurupiaDict - Dynamic Intelligence Connective Taxonomy

**"연결된 지식, 깨어있는 지혜"** 🕸️

GurupiaDict는 위키백과 XML 덤프에서 지식을 추출하여 고성능 검색 가능한 지식 그래프를 구축하는 시스템입니다.

## 🚀 프로젝트 구조

```
GurupiaDict/
├── gurupia-parser/         (🦀 Rust) - 위키백과 XML 스트리밍 파서
│   ├── src/main.rs
│   ├── Cargo.toml
│   └── target/release/gurupia-parser.exe
│
├── gurupia-synthesizer/    (🐍 Python) - 데이터 가공 및 DB 구축
│   ├── synthesizer.py      - JSONL → SQLite 변환기
│   └── query.py            - 지식 그래프 쿼리 도구
│
├── GurupiaDict.db          (💾 SQLite) - 최종 지식 그래프 데이터베이스
└── GurupiaDict.md          (📋) - 프로젝트 마스터 플랜
```

## 🎯 핵심 기능

### 1️⃣ Gurupia-Parser (Rust)
- ✅ `quick-xml`을 사용한 고속 스트리밍 XML 파싱
- ✅ 메인 네임스페이스(`<ns>0</ns>`) 문서만 추출
- ✅ 리다이렉트, 동음이의어 페이지 자동 필터링
- ✅ 위키 마크업 정리 (`[[File:...]]`, `<ref>`, HTML 태그 제거)
- ✅ 첫 문단 지능형 추출 (500-1500자, 문장 단위 절단)
- ✅ JSONL 포맷 출력

### 2️⃣ Gurupia-Synthesizer (Python)
- ✅ `[[위키링크]]` 패턴 추출 및 노드/엣지 생성
- ✅ **상호 연결(Bi-directional) 지원**: Backlink 쿼리 가능
- ✅ 위키 마크업 → HTML 변환 (`dict://` 프로토콜 링크)
- ✅ SQLite FTS5 전체 텍스트 검색 인덱스
- ✅ 지식 그래프 통계 및 분석

### 3️⃣ Gurupia-Vault (SQLite)
- ✅ `Nodes` 테이블: 문서 저장 (title, content, HTML)
- ✅ `Edges` 테이블: 참조 관계 (source → target)
- ✅ `NodesFTS` 가상 테이블: FTS5 검색
- ✅ 고성능 인덱스: 제목, 소스, 대상 인덱싱

## 📖 사용 방법

### Step 1: 위키백과 XML 파싱

```bash
# 한국어 위키백과 덤프 다운로드 (예시)
# https://dumps.wikimedia.org/kowiki/latest/

# Rust 파서 실행
cd gurupia-parser
cargo build --release
.\target\release\gurupia-parser.exe kowiki-latest-pages-articles.xml output.jsonl
```

**출력 예시:**
```
🦀 GurupiaDict Parser v0.1.0
📖 Reading: kowiki-latest-pages-articles.xml
📝 Writing: output.jsonl

📊 Processed: 500000 articles (Total pages: 1234567)
✅ Parsing completed successfully!
```

### Step 2: SQLite 데이터베이스 구축

```bash
cd ..
python gurupia-synthesizer\synthesizer.py gurupia-parser\output.jsonl GurupiaDict.db --stats
```

**출력 예시:**
```
🐍 GurupiaDict Synthesizer v0.1.0
📥 Input:  output.jsonl
💾 Output: GurupiaDict.db

📐 Creating database schema...
✅ Schema created successfully
📊 Processed: 500000 nodes, 2500000 edges

🔗 Most Referenced Articles:
   대한민국        (15234 references)
   서울특별시      (8932 references)
   ...
```

### Step 3: 지식 그래프 쿼리

```bash
# 대화형 모드
python gurupia-synthesizer\query.py GurupiaDict.db --interactive

# 특정 문서 조회
python gurupia-synthesizer\query.py GurupiaDict.db --view "컴퓨터"

# 검색
python gurupia-synthesizer\query.py GurupiaDict.db --search "프로그래밍"

# 통계
python gurupia-synthesizer\query.py GurupiaDict.db --stats
```

## 🔍 쿼리 예시

### 대화형 모드에서:

```
gurupia> search 컴퓨
🔎 Found 5 results:
  1. 컴퓨터
  2. 컴퓨터 과학
  3. 컴퓨터 공학
  4. 컴퓨터 그래픽스
  5. 컴퓨터 네트워크

gurupia> view 컴퓨터
================================================================================
📖 컴퓨터
================================================================================

【 Content 】
<p><strong>컴퓨터</strong>(computer)는 <a href="dict://프로그램" class="dict-link">프로그램</a>을 
이용해 자료를 처리하는 전자기계이다...</p>

【 References (2) 】
  → 프로그램
  → 하드웨어

【 Referenced By (15) 】
  ← 프로그래밍 언어
  ← 인공지능
  ← 소프트웨어 공학
  ...
```

## 💡 고급 쿼리 (SQL)

### Backlink 조회 (참조하는 문서 찾기)
```sql
SELECT DISTINCT n.title
FROM Edges e
JOIN Nodes n ON e.source_id = n.id
WHERE e.target_title = '컴퓨터'
ORDER BY n.title
LIMIT 10;
```

### 전체 텍스트 검색
```sql
SELECT n.title, snippet(NodesFTS, 1, '<mark>', '</mark>', '...', 50) as snippet
FROM NodesFTS
JOIN Nodes n ON NodesFTS.rowid = n.id
WHERE NodesFTS MATCH '인공지능*'
ORDER BY rank
LIMIT 10;
```

### 가장 많이 참조된 문서
```sql
SELECT target_title, COUNT(*) as ref_count
FROM Edges
GROUP BY target_title
ORDER BY ref_count DESC
LIMIT 20;
```

## 🛠️ 필요한 도구

### Rust 설치
```bash
# Windows
# https://rustup.rs에서 rustup-init.exe 다운로드 및 실행
```

### Python 설치
```bash
# Windows
winget install Python.Python.3.12
```

## 📊 성능 특징

- **메모리 효율성**: 스트리밍 파싱으로 대용량 XML도 안정적 처리
- **고속 검색**: SQLite FTS5 인덱스로 밀리초 단위 검색
- **확장성**: 수백만 개 문서도 처리 가능
- **크로스 플랫폼**: Windows, macOS, Linux 모두 지원

## 🎓 확장 가능성

1. **개인 메모 통합**: Markdown 파일을 같은 DB에 추가
2. **웹 인터페이스**: Flask/FastAPI로 웹 UI 구축
3. **API 서버**: RESTful API 제공
4. **모바일 앱**: SQLite DB를 직접 사용하는 네이티브 앱
5. **AI 통합**: 문서 임베딩 추가로 의미 기반 검색

## 📝 데이터베이스 스키마

### Nodes 테이블
```sql
CREATE TABLE Nodes (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE NOT NULL,
    raw_content TEXT NOT NULL,      -- 원본 위키 마크업
    html_content TEXT NOT NULL,     -- dict:// 링크가 포함된 HTML
    created_at TIMESTAMP
);
```

### Edges 테이블 (지식 그래프)
```sql
CREATE TABLE Edges (
    id INTEGER PRIMARY KEY,
    source_id INTEGER NOT NULL,     -- 참조하는 문서
    target_title TEXT NOT NULL,     -- 참조되는 문서 제목
    edge_type TEXT DEFAULT 'reference',
    FOREIGN KEY (source_id) REFERENCES Nodes(id)
);
```

### NodesFTS 가상 테이블
```sql
CREATE VIRTUAL TABLE NodesFTS USING fts5(
    title, 
    content,
    tokenize='unicode61'
);
```

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Wikipedia XML Dump                        │
│               (kowiki-latest-pages-articles.xml)             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Gurupia-Parser (Rust) │  🦀 고속 스트리밍 파싱
        │  - quick-xml           │
        │  - Regex 필터링         │
        │  - 첫 문단 추출         │
        └────────────┬───────────┘
                     │
                     ▼ JSONL
        ┌────────────────────────────┐
        │ Gurupia-Synthesizer (Python) │  🐍 지식 그래프 구축
        │  - 링크 추출                │
        │  - HTML 변환               │
        │  - SQLite 저장             │
        └────────────┬───────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │  Gurupia-Vault (SQLite)  │  🗄️ 지식 그래프 DB
        │  - FTS5 검색 인덱스       │
        │  - Nodes & Edges         │
        │  - Backlink 쿼리 지원     │
        └────────────┬─────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │    Query Tool (Python)  │  🔍 대화형 탐색
        │    - 검색               │
        │    - 조회               │
        │    - 통계               │
        └────────────────────────┘
```

## 📜 라이선스

이 프로젝트는 교육 및 개인 용도로 자유롭게 사용 가능합니다.

## 🤝 기여

버그 리포트, 기능 제안, Pull Request 환영합니다!

---

**GurupiaDict** - *연결된 지식, 깨어있는 지혜* 🕸️  
Created with 🦀 Rust, 🐍 Python, and 💾 SQLite
