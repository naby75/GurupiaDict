# 📚 GurupiaDict 샘플 사전

**파일명**: `SampleDict.db`  
**생성일**: 2026-01-05  
**문서 수**: 17개  
**링크 수**: 193개  
**주제**: 현대 기술 (AI, 블록체인, 클라우드, 양자컴퓨터 등)

---

## 🎯 샘플 사전 개요

실제 위키백과의 축소판으로, **GurupiaDict의 모든 기능을 체험**할 수 있는 샘플 데이터입니다!

### 📖 수록 문서 (17개)

#### 🤖 인공지능 & 머신러닝
1. **인공지능** - AI의 정의, 역사, 응용 분야
2. **기계학습** - ML 알고리즘, 지도학습, 비지도학습
3. **딥러닝** - 심층신경망, CNN, RNN
4. **자연어 처리** - NLP, BERT, GPT
5. **컴퓨터 비전** - OpenCV, 객체 검출, 얼굴 인식

#### 💻 프로그래밍 & 프레임워크
6. **Python** - 파이썬 언어, 라이브러리
7. **TensorFlow** - 구글의 딥러닝 프레임워크
8. **PyTorch** - Meta의 딥러닝 프레임워크
9. **GPT** - OpenAI의 언어 모델
10. **트랜스포머** - Attention 메커니즘

#### 📊 데이터 & 클라우드
11. **데이터 과학** - 데이터 분석, 시각화
12. **빅데이터** - Hadoop, Spark, MapReduce
13. **클라우드 컴퓨팅** - AWS, Azure, GCP

#### 🔮 신기술
14. **블록체인** - 분산원장, 비트코인, 이더리움
15. **양자 컴퓨터** - 큐비트, 양자 우월성
16. **사이버 보안** - 해킹 방지, 암호화
17. **메타버스** - VR, AR, 가상세계

---

## 🔗 지식 그래프 통계

### 가장 많이 참조되는 문서 Top 10

| 순위 | 문서 | 참조 횟수 |
|------|------|-----------|
| 🥇 1 | 딥러닝 | 7회 |
| 🥈 2 | 기계학습 | 6회 |
| 🥉 3 | 인공지능 | 6회 |
| 4 | 데이터 | 5회 |
| 5 | Python | 5회 |
| 6 | 컴퓨터 | 4회 |
| 7 | 자연어 처리 | 3회 |
| 8 | 컴퓨터 비전 | 2회 |
| 9 | GPT | 2회 |
| 10 | 트랜스포머 | 2회 |

### 연결 관계 예시

```
인공지능 (6개 참조)
  ← 기계학습
  ← 딥러닝
  ← 자연어 처리
  ← 컴퓨터 비전
  ← 데이터 과학
  ← PyTorch

딥러닝 (7개 참조)
  ← 자연어 처리
  ← 컴퓨터 비전
  ← TensorFlow
  ← PyTorch
  ← GPT
  ← 트랜스포머
  ← 데이터 과학
```

---

## 🚀 샘플 사전 사용법

### 1️⃣ 통계 보기

```bash
query.bat SampleDict.db --stats
```

**출력:**
```
📊 Database Statistics:
   Total Articles: 17
   Total Links: 193

🔗 Most Referenced Articles:
   딥러닝                            (7 references)
   기계학습                          (6 references)
   인공지능                          (6 references)
   ...
```

### 2️⃣ 검색하기

```bash
query.bat SampleDict.db --search "인공"
```

**출력:**
```
🔎 Found 4 results:
  1. 인공지능
  2. 인공신경망
  ...
```

### 3️⃣ 문서 보기

```bash
query.bat SampleDict.db --view "인공지능"
```

**출력:**
```
================================================================================
📖 인공지능
================================================================================

【 Content 】
<p><strong>인공지능</strong>(人工知能, Artificial Intelligence, AI)은 
<a href="dict://기계" class="dict-link">기계</a>가 인간의 
<a href="dict://지능" class="dict-link">지능</a>을 모방하여 
<a href="dict://학습" class="dict-link">학습</a>, 
<a href="dict://추론" class="dict-link">추론</a>, 
<a href="dict://문제 해결" class="dict-link">문제 해결</a> 등을 
수행하는 기술이다...</p>

【 References (17) 】  ← 이 문서가 참조하는 문서들
  → 기계
  → 지능
  → 학습
  → 추론
  → 문제 해결
  → 다트머스 회의
  → 컴퓨터 과학
  → 기계학습
  → 딥러닝
  → 자연어 처리
  → 컴퓨터 비전
  → 심층신경망
  → 자율주행자동차
  → 의료 진단
  → 챗봇
  → 추천 시스템
  → OpenAI

【 Referenced By (6) 】  ← 이 문서를 참조하는 문서들 (Backlink!)
  ← 기계학습
  ← 딥러닝
  ← 자연어 처리
  ← 컴퓨터 비전
  ← 데이터 과학
  ← PyTorch
================================================================================
```

### 4️⃣ 대화형 모드

```bash
query.bat SampleDict.db --interactive
```

**사용 예:**
```
gurupia> search 딥러닝

🔎 Found 1 results:
  1. 딥러닝

gurupia> view 딥러닝

📖 딥러닝
...

gurupia> search 블록체인

🔎 Found 1 results:
  1. 블록체인

gurupia> view 블록체인
...

gurupia> stats

📊 Database Statistics:
   Total Articles: 17
   Total Links: 193
...

gurupia> quit
👋 Goodbye!
```

---

## 💡 샘플로 배울 수 있는 것

### 1. Backlink 기능 체험

**질문**: "딥러닝과 관련된 모든 문서는?"

```bash
query.bat SampleDict.db --view "딥러닝"
```

→ **Referenced By** 섹션에서 7개 문서 발견!

### 2. 지식 그래프 탐색

**질문**: "인공지능 → 기계학습 → 딥러닝" 연결 관계는?

```
인공지능
  ↓ 참조
기계학습
  ↓ 참조
딥러닝
  ↓ 참조
트랜스포머
  ↓ 참조
GPT
```

### 3. 도메인별 클러스터링

**AI/ML 클러스터:**
- 인공지능 ↔ 기계학습 ↔ 딥러닝 ↔ 자연어 처리 ↔ 컴퓨터 비전

**프레임워크 클러스터:**
- Python ↔ TensorFlow ↔ PyTorch

**신기술 클러스터:**
- 블록체인, 양자 컴퓨터, 메타버스

---

## 🎓 실습 예제

### 예제 1: 연구 주제 탐색

**목표**: "GPT와 관련된 모든 기술 찾기"

```bash
gurupia> view GPT

【 References 】
  → OpenAI
  → 언어 모델
  → 트랜스포머
  → ChatGPT
  → RLHF
  → 자연어 처리
  → Microsoft
  ...

【 Referenced By 】
  ← 딥러닝
  ← 자연어 처리
  ← 트랜스포머
```

**발견**: GPT는 트랜스포머 기반이며, ChatGPT로 발전했고, Microsoft가 활용 중!

### 예제 2: 기술 스택 조사

**목표**: "딥러닝 프로젝트에 필요한 도구는?"

```bash
gurupia> view 딥러닝

【 References 】
  → TensorFlow
  → PyTorch
  → Keras
  → GPU
  → CUDA
```

**발견**: TensorFlow나 PyTorch 중 하나 선택, GPU 필요, CUDA 설치 필요!

### 예제 3: 개념 이해

**목표**: "트랜스포머가 왜 중요한가?"

```bash
gurupia> view 트랜스포머

【 Referenced By 】
  ← BERT
  ← GPT
  ← T5
  ← 자연어 처리
  ← 딥러닝
```

**발견**: 거의 모든 최신 NLP 모델이 트랜스포머 기반!

---

## 📊 데이터 품질

### 문서당 평균 통계

- **평균 참조 수**: 11.4개
- **평균 역참조 수**: 11.4개
- **최대 참조 문서**: 인공지능 (17개 나가는 링크)
- **최대 역참조 문서**: 딥러닝 (7개 들어오는 링크)

### 네트워크 특성

- **연결도**: 매우 높음 (거의 모든 문서가 연결됨)
- **클러스터**: 3개 주요 클러스터 (AI/ML, 프로그래밍, 신기술)
- **중심 노드**: 인공지능, 딥러닝, 기계학습

---

## 🔍 SQL 쿼리 예제

샘플 사전으로 SQL도 연습할 수 있습니다:

```bash
sqlite3 SampleDict.db
```

### 1. 전체 텍스트 검색

```sql
SELECT title 
FROM NodesFTS 
WHERE NodesFTS MATCH 'AI*' 
LIMIT 10;
```

### 2. 가장 많이 참조된 문서

```sql
SELECT target_title, COUNT(*) as refs
FROM Edges
GROUP BY target_title
ORDER BY refs DESC
LIMIT 10;
```

### 3. 특정 문서의 Backlinks

```sql
SELECT DISTINCT n.title
FROM Edges e
JOIN Nodes n ON e.source_id = n.id
WHERE e.target_title = '딥러닝'
ORDER BY n.title;
```

---

## 🎯 다음 단계

샘플 사전으로 충분히 연습했다면:

### 1️⃣ 실제 위키백과 처리

```bash
# 한국어 위키백과 다운로드
# https://dumps.wikimedia.org/kowiki/latest/

parse.bat kowiki-latest-pages-articles.xml kowiki.jsonl
synthesize.bat kowiki.jsonl GurupiaDict_KO.db --stats
```

### 2️⃣ 개인 메모 추가

자신만의 Markdown 문서를 JSONL 형식으로 변환하여 추가 가능!

### 3️⃣ 웹 인터페이스 구축

Flask나 FastAPI로 웹 UI 만들기

---

## 📁 파일 정보

| 파일 | 크기 | 설명 |
|------|------|------|
| `sample_dictionary.xml` | 45KB | 원본 XML (17개 문서) |
| `sample_dict.jsonl` | 22KB | 파싱된 JSONL |
| `SampleDict.db` | 56KB | SQLite 지식 그래프 |

---

## 🙏 결론

**SampleDict.db**로 다음을 체험할 수 있습니다:

✅ **검색** - FTS5 전체 텍스트 검색  
✅ **Backlink** - 양방향 참조 시스템  
✅ **지식 그래프** - 개념 간 연결 탐색  
✅ **dict:// 프로토콜** - 내부 링크 시스템  
✅ **SQL 쿼리** - 고급 데이터 분석  

**이제 GurupiaDict의 모든 기능을 마스터했습니다!** 🎉

실제 위키백과로 확장하여 수십만 개 문서를 담은 나만의 지식 그래프를 만들어보세요!

---

**샘플 사전으로 즐거운 학습 되세요!** 🕸️✨

*GurupiaDict - "연결된 지식, 깨어있는 지혜"*
