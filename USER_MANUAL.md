# 📖 GurupiaDict 사용 설명서 (초보자용)

**버전**: 1.0  
**최종 수정일**: 2026-01-05  
**대상**: 코딩 경험이 없는 초보자부터 고급 사용자까지

---

## 📑 목차

1. [GurupiaDict란?](#1-gurupiadict란)
2. [설치하기](#2-설치하기)
3. [첫 실행 - 데모 모드](#3-첫-실행---데모-모드)
4. [실제 위키백과 처리하기](#4-실제-위키백과-처리하기)
5. [지식 그래프 탐색하기](#5-지식-그래프-탐색하기)
6. [고급 사용법](#6-고급-사용법)
7. [문제 해결](#7-문제-해결)
8. [FAQ](#8-faq)

---

## 1. GurupiaDict란?

### 🎯 한 줄 요약
**위키백과를 내 컴퓨터에 검색 가능한 지식 그래프로 만들어주는 프로그램**

### 💡 무엇을 할 수 있나요?

- ✅ 위키백과 전체를 오프라인에서 검색
- ✅ 단어 간 연결 관계 탐색 (A를 참조하는 모든 문서 찾기)
- ✅ 초고속 검색 (밀리초 단위)
- ✅ 개인 메모와 통합 가능

### 🏗️ 어떻게 작동하나요?

```
Wikipedia XML 파일 
    ↓ [1단계: 파싱]
JSONL 파일 (정리된 데이터)
    ↓ [2단계: 데이터베이스 생성]
SQLite 파일 (검색 가능한 DB)
    ↓ [3단계: 검색/탐색]
나만의 지식 그래프!
```

---

## 2. 설치하기

### ✅ 사전 준비 (이미 설치됨)

프로젝트를 받으셨다면 이미 다음이 설치되어 있습니다:
- ✅ Rust 1.92.0
- ✅ Python 3.12.10
- ✅ GurupiaDict 프로그램

### 📁 폴더 구조 확인

프로젝트 폴더(`C:\repos\GurupiaDict`)를 열면 다음과 같은 구조여야 합니다:

```
GurupiaDict/
├── demo.bat                  ← 데모 실행 파일
├── parse.bat                 ← XML 파싱 실행 파일
├── synthesize.bat            ← DB 생성 실행 파일
├── query.bat                 ← 검색 실행 파일
├── gurupiaparser/           ← Rust 파서 폴더
└── gurupia-synthesizer/     ← Python 도구 폴더
```

**모든 파일이 있나요?** ✅  
→ 다음 단계로 진행하세요!

**파일이 없나요?** ❌  
→ [문제 해결](#7-문제-해결) 섹션을 확인하세요.

---

## 3. 첫 실행 - 데모 모드

### 🎬 데모 실행하기 (가장 쉬운 방법!)

#### Step 1: 파일 탐색기에서 프로젝트 폴더 열기

1. `C:\repos\GurupiaDict` 폴더를 엽니다
2. `demo.bat` 파일을 찾습니다

#### Step 2: demo.bat 더블클릭

`demo.bat` 파일을 **더블클릭**하면 검은 창(명령 프롬프트)이 열립니다.

#### Step 3: 자동 실행 관찰

다음 과정이 **자동으로** 진행됩니다:

```
[Step 1/4] Building Rust Parser...
   Compiling gurupia-parser v0.1.0
   ✅ Parser built successfully!

[Step 2/4] Parsing Test Wikipedia XML...
   🦀 GurupiaDict Parser v0.1.0
   📊 Processed: 3 articles
   ✅ Parsing completed!

[Step 3/4] Building Knowledge Graph Database...
   🐍 GurupiaDict Synthesizer v0.1.0
   📊 Processed: 3 nodes, 21 edges
   ✅ Database built successfully!

[Step 4/4] Running Query Demo...
   📊 Database Statistics:
      Total Articles: 3
      Total Links: 21
   
   🎉 Complete Workflow Test Finished Successfully!
```

#### Step 4: 결과 확인

데모가 끝나면 프로젝트 폴더에 다음 파일이 생성됩니다:

- `test_output.jsonl` - 파싱된 데이터
- `GurupiaDict_demo.db` - 지식 그래프 데이터베이스

**축하합니다! 첫 실행에 성공했습니다!** 🎉

---

## 4. 실제 위키백과 처리하기

이제 실제 위키백과 데이터를 처리해봅시다!

### 📥 Step 1: 위키백과 덤프 다운로드

#### 한국어 위키백과 다운로드

1. 웹브라우저를 열고 다음 주소로 이동:
   ```
   https://dumps.wikimedia.org/kowiki/latest/
   ```

2. 다음 파일을 찾아서 다운로드:
   ```
   kowiki-latest-pages-articles.xml.bz2
   ```
   - 파일 크기: 약 1~2GB (압축됨)
   - 다운로드 시간: 인터넷 속도에 따라 10분~1시간

3. 다운로드한 파일을 `C:\repos\GurupiaDict` 폴더에 저장

#### 💡 다른 언어 위키백과도 가능합니다!

- 영어: `https://dumps.wikimedia.org/enwiki/latest/`
- 일본어: `https://dumps.wikimedia.org/jawiki/latest/`
- 중국어: `https://dumps.wikimedia.org/zhwiki/latest/`

### 📦 Step 2: 압축 해제

#### 방법 1: 7-Zip 사용 (추천)

1. [7-Zip](https://www.7-zip.org/) 다운로드 및 설치
2. `kowiki-latest-pages-articles.xml.bz2` 파일 우클릭
3. `7-Zip` → `압축 풀기` 선택
4. 완료되면 `kowiki-latest-pages-articles.xml` 파일 생성
   - 파일 크기: 약 5~10GB (압축 해제됨)

#### 방법 2: WinRAR 사용

1. WinRAR이 설치되어 있다면 파일을 더블클릭
2. `압축 풀기` 버튼 클릭

### 🦀 Step 3: XML 파싱 (1단계)

#### 명령어 실행

1. `C:\repos\GurupiaDict` 폴더를 엽니다
2. 주소창에 `cmd` 입력 후 Enter (명령 프롬프트 실행)
3. 다음 명령어 입력:

```bash
parse.bat kowiki-latest-pages-articles.xml kowiki_output.jsonl
```

#### 실행 화면

```
========================================
  GurupiaDict Parser (Rust)
========================================

Input:  kowiki-latest-pages-articles.xml
Output: kowiki_output.jsonl

Building Rust parser...
Starting parser...

🦀 GurupiaDict Parser v0.1.0
📖 Reading: kowiki-latest-pages-articles.xml
📝 Writing: kowiki_output.jsonl

📊 Processed: 100000 articles (Total pages: 250000)
📊 Processed: 200000 articles (Total pages: 500000)
📊 Processed: 300000 articles (Total pages: 750000)
...

✅ Parsing completed successfully!
Output saved to: kowiki_output.jsonl
```

#### ⏱️ 예상 소요 시간

- **한국어 위키백과** (~50만 문서): 30분 ~ 2시간
- **영어 위키백과** (~600만 문서): 3시간 ~ 10시간

> 💡 **팁**: 파싱하는 동안 컴퓨터를 다른 용도로 사용해도 괜찮습니다!

### 🐍 Step 4: 데이터베이스 생성 (2단계)

#### 명령어 실행

```bash
synthesize.bat kowiki_output.jsonl GurupiaDict_KO.db --reset --stats
```

#### 실행 화면

```
========================================
  GurupiaDict Synthesizer (Python)
========================================

Input:  kowiki_output.jsonl
Output: GurupiaDict_KO.db

🐍 GurupiaDict Synthesizer v0.1.0
📐 Creating database schema...
✅ Schema created successfully

📖 Reading JSONL from: kowiki_output.jsonl
📊 Processed: 10000 nodes, 50000 edges
📊 Processed: 20000 nodes, 100000 edges
📊 Processed: 50000 nodes, 250000 edges
...

✅ Imported 500000 nodes and 2500000 edges

📊 Database Statistics:
   Total Nodes: 500,000
   Total Edges: 2,500,000

🔗 Most Referenced Articles:
   대한민국                          (15234 references)
   서울특별시                        (8932 references)
   미국                              (7654 references)
   일본                              (6543 references)
   ...

✅ Synthesis completed successfully!
Database ready at: GurupiaDict_KO.db
```

#### ⏱️ 예상 소요 시간

- **한국어 위키백과**: 10분 ~ 30분
- **영어 위키백과**: 1시간 ~ 3시간

### ✅ 완료!

이제 `GurupiaDict_KO.db` 파일이 생성되었습니다!
- 파일 크기: 약 2~5GB
- 이 파일 하나에 모든 위키백과 지식이 담겨 있습니다!

---

## 5. 지식 그래프 탐색하기

### 🔍 검색 도구 실행하기

#### 대화형 모드로 시작

```bash
query.bat GurupiaDict_KO.db --interactive
```

또는 파일 탐색기에서:
1. `query.bat` 파일 우클릭
2. `편집` 선택
3. 마지막 줄을 다음과 같이 수정:
   ```batch
   python gurupia-synthesizer\query.py GurupiaDict_KO.db --interactive
   ```
4. 저장 후 `query.bat` 더블클릭

### 💬 대화형 모드 사용법

#### 화면 예시

```
🔍 GurupiaDict Interactive Mode
Commands:
  search <query>  - Search for articles
  view <title>    - View article details
  stats           - Show database statistics
  quit/exit       - Exit

gurupia> _
```

#### 명령어 1: `search` - 검색하기

**사용법:**
```
gurupia> search 검색어
```

**예제:**
```
gurupia> search 컴퓨터

🔎 Found 10 results:
  1. 컴퓨터
  2. 컴퓨터 과학
  3. 컴퓨터 공학
  4. 컴퓨터 그래픽스
  5. 컴퓨터 네트워크
  6. 컴퓨터 프로그래밍
  7. 컴퓨터 바이러스
  8. 양자 컴퓨터
  9. 슈퍼컴퓨터
  10. 개인용 컴퓨터
```

**팁:**
- 일부만 입력해도 됩니다: `search 인공` → "인공지능", "인공신경망" 등
- 띄어쓰기 없이: `search AI` → "AI", "AI 윤리" 등

#### 명령어 2: `view` - 문서 보기

**사용법:**
```
gurupia> view 문서제목
```

**예제:**
```
gurupia> view 컴퓨터

================================================================================
📖 컴퓨터
================================================================================

【 Content 】
<p><strong>컴퓨터</strong>(computer)는 
<a href="dict://프로그램" class="dict-link">프로그램</a>을 
이용해 자료를 처리하는 전자기계이다. 
<a href="dict://하드웨어" class="dict-link">하드웨어</a>와 
<a href="dict://소프트웨어" class="dict-link">소프트웨어</a>로 
구성되며, 현대 사회에서 정보의 처리와 저장을 담당하는 핵심 장치로 사용된다.</p>

【 References (15) 】  ← 이 문서가 참조하는 다른 문서들
  → 프로그램
  → 하드웨어
  → 소프트웨어
  → 중앙처리장치
  → 메모리
  ...

【 Referenced By (234) 】  ← 이 문서를 참조하는 다른 문서들 (Backlink!)
  ← 인공지능
  ← 프로그래밍 언어
  ← 데이터베이스
  ← 운영 체제
  ← 알고리즘
  ...
================================================================================
```

**핵심 기능: Backlink (역참조)**
- `Referenced By` 섹션이 바로 GurupiaDict의 핵심 기능!
- "컴퓨터"를 언급하는 모든 문서를 찾을 수 있습니다
- 개념 간 연결 관계를 한눈에 파악!

#### 명령어 3: `stats` - 통계 보기

**사용법:**
```
gurupia> stats
```

**예제:**
```
📊 Database Statistics:
   Total Articles: 500,000
   Total Links: 2,500,000

🔗 Most Referenced Articles:
   대한민국                          (15234 references)
   서울특별시                        (8932 references)
   미국                              (7654 references)
   일본                              (6543 references)
   영어                              (5432 references)
   한국어                            (4321 references)
   중국                              (4123 references)
   프랑스                            (3987 references)
   독일                              (3654 references)
   러시아                            (3456 references)

📝 Articles with Most Links:
   한국의 역사                       (345 links)
   세계사                            (298 links)
   물리학                            (276 links)
   ...
```

#### 명령어 4: `quit` - 종료

```
gurupia> quit
👋 Goodbye!
```

### 🎯 실전 사용 예시

#### 예시 1: 연구 주제 탐색

```
gurupia> search 양자역학

🔎 Found 5 results:
  1. 양자역학
  2. 양자컴퓨터
  3. 양자얽힘
  4. 양자장론
  5. 양자암호

gurupia> view 양자역학

【 Content 】
양자역학은 원자와 아원자 입자의 행동을 설명하는 물리학의 한 분야...

【 References (25) 】
  → 물리학
  → 원자
  → 전자
  → 파동함수
  ...

【 Referenced By (156) 】
  ← 양자컴퓨터
  ← 양자얽힘
  ← 슈뢰딩거의 고양이
  ← 하이젠베르크의 불확정성 원리
  ...
```

**활용:**
- "양자역학"과 관련된 모든 개념을 한 번에 탐색
- 참고문헌을 찾지 않아도 관련 문서 자동 발견!

#### 예시 2: 인물 연구

```
gurupia> search 세종대왕

gurupia> view 세종대왕

【 Referenced By (89) 】
  ← 한글
  ← 훈민정음
  ← 조선의 역사
  ← 과학 기술사
  ← 장영실
  ...
```

**활용:**
- 세종대왕과 연관된 모든 주제 발견
- 역사 연구에 필수적인 상호참조 기능!

---

## 6. 고급 사용법

### 🔧 커맨드라인 옵션

#### 빠른 검색 (대화형 모드 없이)

```bash
# 검색만 하고 종료
query.bat GurupiaDict_KO.db --search "인공지능"

# 특정 문서만 보고 종료
query.bat GurupiaDict_KO.db --view "컴퓨터"

# 통계만 보고 종료
query.bat GurupiaDict_KO.db --stats
```

### 💾 데이터베이스 재생성

기존 DB를 삭제하고 새로 만들려면:

```bash
synthesize.bat kowiki_output.jsonl GurupiaDict_KO.db --reset --stats
```

`--reset` 옵션이 기존 DB를 삭제합니다.

### 🗄️ SQL 직접 사용하기

고급 사용자는 SQL로 직접 쿼리할 수 있습니다:

#### SQLite 설치

```bash
winget install SQLite.SQLite
```

#### 데이터베이스 열기

```bash
sqlite3 GurupiaDict_KO.db
```

#### 예제 쿼리

**1. 전체 텍스트 검색**
```sql
SELECT title 
FROM NodesFTS 
WHERE NodesFTS MATCH 'AI*' 
LIMIT 10;
```

**2. 가장 많이 참조된 문서 Top 20**
```sql
SELECT target_title, COUNT(*) as refs
FROM Edges
GROUP BY target_title
ORDER BY refs DESC
LIMIT 20;
```

**3. 특정 문서의 Backlinks**
```sql
SELECT DISTINCT n.title
FROM Edges e
JOIN Nodes n ON e.source_id = n.id
WHERE e.target_title = '인공지능'
ORDER BY n.title;
```

**4. 두 문서 간 최단 경로 (연결 관계)**
```sql
-- 복잡한 그래프 쿼리 예시
WITH RECURSIVE path(source, target, depth) AS (
  SELECT source_id, target_title, 1
  FROM Edges
  WHERE source_id = (SELECT id FROM Nodes WHERE title = '컴퓨터')
  UNION ALL
  SELECT e.source_id, e.target_title, p.depth + 1
  FROM Edges e
  JOIN path p ON e.source_id = (SELECT id FROM Nodes WHERE title = p.target)
  WHERE p.depth < 3
)
SELECT * FROM path WHERE target = '인공지능';
```

### 🐍 Python 스크립트에서 사용

직접 Python 코드를 작성하여 사용할 수도 있습니다:

```python
import sys
sys.path.append('gurupia-synthesizer')
from query import GurupiaQuery

# DB 연결
with GurupiaQuery('GurupiaDict_KO.db') as query:
    # 검색
    results = query.search_titles('컴퓨터')
    for result in results:
        print(f"- {result['title']}")
    
    # 문서 조회
    article = query.get_article('컴퓨터')
    if article:
        print(f"\n제목: {article['title']}")
        print(f"내용: {article['html_content'][:200]}...")
    
    # Backlinks 조회
    backlinks = query.get_backlinks('컴퓨터')
    print(f"\n컴퓨터를 참조하는 문서: {len(backlinks)}개")
    for link in backlinks[:10]:
        print(f"  ← {link}")
```

---

## 7. 문제 해결

### ❌ 문제: "Python이 인식되지 않습니다"

**증상:**
```
'python'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는 배치 파일이 아닙니다.
```

**해결 방법:**

1. Python 설치 확인:
   ```bash
   where python
   ```

2. 경로가 없다면 Python 재설치:
   ```bash
   winget install Python.Python.3.12
   ```

3. PowerShell을 관리자 권한으로 실행 후:
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Users\[사용자명]\AppData\Local\Programs\Python\Python312", "User")
   ```

4. 명령 프롬프트 재시작

### ❌ 문제: "cargo: command not found"

**증상:**
```
'cargo'은(는) 내부 또는 외부 명령이 아닙니다.
```

**해결 방법:**

1. https://rustup.rs 접속
2. `rustup-init.exe` 다운로드
3. 실행 후 기본 설정으로 설치
4. 명령 프롬프트 재시작

### ❌ 문제: "database is locked"

**증상:**
```
sqlite3.OperationalError: database is locked
```

**해결 방법:**

1. 다른 query.bat 창이 열려있는지 확인
2. 모든 query 창 닫기
3. 재시도

### ❌ 문제: 파싱이 너무 느려요

**증상:**
- 몇 시간이 지나도 끝나지 않음

**해결 방법:**

1. **SSD 사용 확인**: HDD는 10배 이상 느립니다
2. **CPU 확인**: 최소 4코어 권장
3. **메모리 확인**: 최소 8GB RAM 권장
4. **작은 덤프로 테스트**:
   ```bash
   # 영어 위키백과의 작은 버전
   https://dumps.wikimedia.org/simplewiki/latest/
   ```

### ❌ 문제: 메모리 부족 오류

**증상:**
```
MemoryError: Unable to allocate...
```

**해결 방법:**

1. 다른 프로그램 모두 종료
2. 가상 메모리 증가:
   - 시스템 → 고급 시스템 설정 → 성능 설정 → 고급 → 가상 메모리
   - 초기 크기: 4096MB, 최대 크기: 16384MB

### ❌ 문제: XML 파일이 손상됐어요

**증상:**
```
Error at position xxx: unexpected end of file
```

**해결 방법:**

1. XML 파일을 다시 다운로드
2. 다운로드 중 인터넷이 끊기지 않았는지 확인
3. 체크섬 확인:
   - 위키백과 덤프 페이지에서 MD5/SHA1 확인

---

## 8. FAQ

### Q1: 얼마나 많은 저장 공간이 필요한가요?

**A:** 
- XML 파일: ~10GB (압축 해제)
- JSONL 파일: ~5GB
- SQLite DB: ~3GB
- **총 필요 공간: 약 20GB** (여유 있게 30GB 권장)

### Q2: 인터넷 없이도 사용할 수 있나요?

**A:** 
네! 한 번 DB를 만들면 완전히 오프라인에서 사용 가능합니다.

### Q3: 여러 언어를 하나의 DB에 넣을 수 있나요?

**A:**
가능합니다! 다음과 같이:

```bash
# 한국어 파싱
parse.bat kowiki.xml ko.jsonl
# 영어 파싱
parse.bat enwiki.xml en.jsonl

# 두 파일을 합쳐서 DB 생성
copy /b ko.jsonl+en.jsonl combined.jsonl
synthesize.bat combined.jsonl MultiLang.db --stats
```

### Q4: DB를 업데이트하려면?

**A:**
위키백과는 매월 새 덤프를 제공합니다:
1. 새 XML 다운로드
2. 파싱
3. `--reset` 옵션으로 DB 재생성

### Q5: 모바일에서 사용할 수 있나요?

**A:**
SQLite DB는 Android/iOS 앱에서 직접 읽을 수 있습니다:
- Android: SQLite 라이브러리 내장
- iOS: Core Data로 SQLite 접근 가능

### Q6: 성능을 더 높이려면?

**A:**
1. **SQLite 최적화**:
   ```sql
   PRAGMA journal_mode = WAL;
   PRAGMA synchronous = NORMAL;
   PRAGMA cache_size = 1000000;
   ```

2. **인덱스 재구축**:
   ```sql
   REINDEX;
   VACUUM;
   ```

3. **FTS 최적화**:
   ```sql
   INSERT INTO NodesFTS(NodesFTS) VALUES('optimize');
   ```

### Q7: dict:// 프로토콜은 무엇인가요?

**A:**
GurupiaDict만의 내부 링크 형식입니다:
```html
<a href="dict://컴퓨터">컴퓨터</a>
```

이를 활용하면:
- 웹 앱에서 `dict://` 링크를 감지하여 해당 문서로 이동
- 데스크톱 앱에서 프로토콜 핸들러 등록 가능

### Q8: 상업적으로 사용해도 되나요?

**A:**
- **GurupiaDict 프로그램**: 자유롭게 사용 가능
- **위키백과 콘텐츠**: CC BY-SA 라이선스 준수 필요
  - 출처 표시
  - 동일 라이선스로 재배포

### Q9: 다른 데이터 소스도 추가할 수 있나요?

**A:**
네! synthesizer.py를 수정하여:
- 개인 블로그 (Markdown)
- 전자책 (EPUB)
- 연구 논문 (PDF → 텍스트)

등을 추가할 수 있습니다.

### Q10: 백업은 어떻게 하나요?

**A:**
DB 파일만 백업하면 됩니다:
```bash
copy GurupiaDict_KO.db E:\Backup\GurupiaDict_KO_2026-01-05.db
```

클라우드에 업로드해도 좋습니다 (OneDrive, Google Drive등).

---

## 📞 추가 도움말

### 📚 관련 문서

- **README.md** - 기술적 상세 설명
- **QUICKSTART.md** - 5분 빠른 시작
- **COMPLETION.md** - 프로젝트 완료 보고서

### 🌐 유용한 링크

- [위키미디어 덤프](https://dumps.wikimedia.org/)
- [SQLite 문서](https://www.sqlite.org/docs.html)
- [FTS5 가이드](https://www.sqlite.org/fts5.html)

### 💬 커뮤니티

질문이나 제안이 있으시면:
1. GitHub Issues에 등록
2. 이메일로 문의
3. 토론 게시판 참여

---

## 🎓 마무리

**GurupiaDict**로 다음을 할 수 있습니다:

✅ 위키백과 전체를 내 컴퓨터에서 검색  
✅ 개념 간 연결 관계 탐색 (Backlink)  
✅ 초고속 전체 텍스트 검색  
✅ 오프라인 지식 데이터베이스 구축  

**이제 여러분의 지식 탐험을 시작하세요!** 🚀

---

**즐거운 학습 되세요!** 🕸️✨

*GurupiaDict - "연결된 지식, 깨어있는 지혜"*
