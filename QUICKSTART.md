# GurupiaDict 빠른 시작 가이드

## 🚀 5분 안에 시작하기

### 전제 조건

1. **Rust 설치** (이미 설치됨 ✅)
   ```bash
   cargo --version  # 확인
   ```

2. **Python 설치** (이미 설치됨 ✅)
   ```bash
   python --version  # 확인
   ```

### 데모 실행하기

프로젝트 루트에서 다음 명령어를 실행하세요:

```bash
demo.bat
```

이 스크립트는 자동으로:
1. Rust 파서 빌드
2. 테스트 위키피디아 XML 파싱
3. SQLite 데이터베이스 생성
4. 쿼리 데모 실행

### 개별 단계 실행

#### 1. XML 파싱
```bash
parse.bat test_wiki.xml output.jsonl
```

#### 2. 데이터베이스 생성
```bash
synthesize.bat output.jsonl GurupiaDict.db --stats
```

#### 3. 지식 그래프 쿼리
```bash
# 대화형 모드
query.bat GurupiaDict.db --interactive

# 검색
query.bat GurupiaDict.db --search "컴퓨터"

# 문서 조회
query.bat GurupiaDict.db --view "컴퓨터"

# 통계
query.bat GurupiaDict.db --stats
```

## 📥 실제 위키백과 데이터 사용하기

### 1. 위키백과 덤프 다운로드

한국어 위키백과:
```
https://dumps.wikimedia.org/kowiki/latest/kowiki-latest-pages-articles.xml.bz2
```

영어 위키백과 (대용량):
```
https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
```

### 2. 압축 해제

```bash
# Windows에서 7-Zip 사용
7z x kowiki-latest-pages-articles.xml.bz2
```

### 3. 파싱 및 DB 생성

```bash
# 1단계: 파싱 (시간이 걸립니다 - 수백만 개 문서의 경우 수십 분~수 시간)
parse.bat kowiki-latest-pages-articles.xml wiki_full.jsonl

# 2단계: DB 생성
synthesize.bat wiki_full.jsonl GurupiaDict.db --reset --stats
```

### 4. 지식 그래프 탐색

```bash
query.bat GurupiaDict.db --interactive
```

## 🔍 쿼리 예시

### 대화형 모드에서

```
gurupia> search 인공지능
🔎 Found 10 results:
  1. 인공지능
  2. 인공지능 윤리
  3. 인공신경망
  ...

gurupia> view 인공지능
================================================================================
📖 인공지능
================================================================================
【 Content 】
...

【 References (15) 】
  → 기계학습
  → 딥러닝
  ...

【 Referenced By (234) 】
  ← 챗봇
  ← 자율주행자동차
  ...

gurupia> stats
📊 Database Statistics:
   Total Articles: 500,000
   Total Links: 2,500,000
   ...
```

## 💡 고급 사용법

### Python 스크립트에서 직접 사용

```python
from gurupia_synthesizer.query import GurupiaQuery

with GurupiaQuery('GurupiaDict.db') as query:
    # 검색
    results = query.search_titles('컴퓨')
    for result in results:
        print(result['title'])
    
    # 문서 조회
    article = query.get_article('컴퓨터')
    print(article['html_content'])
    
    # Backlinks 조회
    backlinks = query.get_backlinks('컴퓨터')
    print(f"Referenced by {len(backlinks)} articles")
```

### SQL 쿼리 직접 실행

```bash
sqlite3 GurupiaDict.db
```

```sql
-- 전체 텍스트 검색
SELECT title FROM NodesFTS WHERE NodesFTS MATCH 'AI*' LIMIT 10;

-- 가장 많이 참조된 문서
SELECT target_title, COUNT(*) as refs
FROM Edges
GROUP BY target_title
ORDER BY refs DESC
LIMIT 20;

-- 특정 문서의 Backlinks
SELECT n.title
FROM Edges e
JOIN Nodes n ON e.source_id = n.id
WHERE e.target_title = '컴퓨터';
```

## 🎯 성능 팁

### 대용량 데이터 처리

1. **SSD 사용**: SQLite는 I/O 집약적이므로 SSD 권장
2. **충분한 메모리**: 수백만 문서의 경우 8GB+ RAM 권장
3. **병렬 처리**: 여러 XML 파일이 있다면 각각 JSONL로 변환 후 병합

### 검색 최적화

```sql
-- FTS5 인덱스 최적화
INSERT INTO NodesFTS(NodesFTS) VALUES('optimize');

-- VACUUM으로 데이터베이스 최적화
VACUUM;
```

## 🐛 문제 해결

### "Python이 인식되지 않습니다"
```bash
# Python 경로 확인
where python

# 환경변수 PATH에 Python 경로 추가 필요
```

### "cargo: command not found"
```bash
# Rust 재설치 필요
# https://rustup.rs
```

### SQLite "database is locked" 오류
- 다른 프로세스에서 DB를 열고 있는지 확인
- 쿼리 도구를 여러 개 동시에 실행하지 마세요

## 📚 추가 자료

- [전체 README](README.md)
- [프로젝트 마스터 플랜](GurupiaDict.md)
- [위키백과 덤프 페이지](https://dumps.wikimedia.org/)

---

**즐거운 지식 탐험 되세요!** 🕸️
