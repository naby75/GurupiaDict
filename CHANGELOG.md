# Changelog

All notable changes to GurupiaDict are documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [v0.2.0] — 2026-02-20

### 🦀 Gurupia-Parser (Rust)

#### Changed

- **[성능]** `Regex` 7개를 `std::sync::LazyLock` static으로 캐싱 — 매 호출 재컴파일 제거
- **[안정성]** `smart_truncate()`: 바이트 인덱스 → `char_indices()` 기반 UTF-8 안전 절단 (한국어 패닉 수정)
- **[데이터]** `#넘겨주기` (한국어 리디렉트) 필터 추가 (`#REDIRECT` / `#redirect` 에 추가)
- **[빌드]** `Cargo.toml` edition `"2024"` → `"2021"` (stable 컴파일러 호환), `rust-version = "1.80"` MSRV 명시
- **[버전]** v0.1.0 → v0.2.0

### 🐍 Gurupia-Synthesizer & Query (Python)

#### Changed

- **[성능]** `PRAGMA journal_mode=WAL` + `PRAGMA synchronous=NORMAL` 적용 — 쓰기 성능 대폭 향상
- **[안정성]** 1,000건마다 중간 커밋 — 장애 시 데이터 손실 최소화
- **[아키텍처]** `GurupiaSynthesizer`가 `GurupiaQuery`를 상속 — 중복 메서드(`get_backlinks`, `get_statistics`, `search_titles`) 제거
- **[보안]** FTS5 쿼리에 Zero Trust 방어벽 구축 — 따옴표 등 특수기호 입력시 발생하는 `SQL OperationalError` (인젝션 공격) 원천 차단

#### Added

- `GurupiaQuery.get_random_title()` 메서드 추가

### 🌐 Gurupia-Viewer (Flask + Vanilla JS)

#### Changed

- **[보안]** `app.config['DB_PATH']` 전환 — 전역 변수 `db_path` 제거 및 Race Condition 차단
- **[보안]** Path Traversal (경로 탐색) 공격 방어 — 허용된 DB 확장자 화이트리스트 검사 추가
- **[보안]** 모든 라우트가 `GurupiaQuery` 컨텍스트 매니저 통일 사용 (`api_random()` 포함)
- **[보안]** `DOMPurify.sanitize()` 적용 — `innerHTML` XSS 방어
- **[UX]** 라이트 모드 구현 — CSS 변수 오버라이드 + 토글 버튼 + `localStorage` 저장
- **[오프라인]** CDN 의존성 → 로컬 vendor 번들 전환:
  - `highlight.js 11.9.0` (119 KB)
  - `DOMPurify 3.1.6` (21 KB)
  - `github-dark.css` (1 KB)
- **[오프라인]** Google Fonts `@import` 제거 → 시스템 폰트 스택 (`Inter` / `Segoe UI` / `system-ui`)

#### Removed

- 중복 `/static/<path>` 라우트 제거 (Flask auto-serving 활용)

### 🔧 설치 및 기타 (Installer/Scraper/Scripts)

- **[보안]** `install.bat` 및 `gurupia_inno.iss`: `flask==3.0.3` 버전 명시적 고정으로 공급망 보안(Supply Chain Security) 강화
- **[보안]** `fast_parser.py`: `XMLParser(resolve_entities=False)` 적용으로 XML Bomb (Billion Laughs) 공격 원천 방어
- **[안정성]** 언인스톨러 진행시 활성화된 `gurupia-parser.exe` 혹은 Python 뷰어 잔여 프로세스를 자동으로 강제 종료(`taskkill`)하여 깔끔한 파일 삭제 보장
- **[안정성]** `fast_parser.py`: 빈 예외 처리(Swallow Exception) 제거 및 `logging.exception()` 적용해 스택 트레이스 보존
- **[안정성]** `fast_parser.py`: 출력 경로 조작(Path Traversal) 검증 강화
- **[성능]** `fast_parser.py`: 루프 내 정규식 컴파일을 제거하고 모듈 레벨 전역 캐싱 적용 (GC 오버헤드 억제)
- **[성능]** `scrape_rust.js`: 대용량 리스트 힙(Heap) 누수 방지를 위한 스트리밍(WriteStream) 출력 방식으로 전환
- `enhanced_parser.py`: 미사용 `from multiprocessing import Pool` 제거
- `.gitignore`: `!SampleDict.db` 예외 추가 (샘플 DB 추적)
- `scrape_rust.js`: 더미 데이터 → `doc.rust-lang.org` 실제 크롤링 전환 (26개 Rust 표준 라이브러리 타입)

---

## [v0.1.0] — 2026-01-25

### Added

- 🦀 Gurupia-Parser: `quick-xml` 기반 스트리밍 XML 파서
- 🐍 Gurupia-Synthesizer: JSONL → SQLite 변환, FTS5 인덱스
- 🌐 Gurupia-Viewer: Flask 웹 뷰어, 다크 모드, TTS
- 💾 GurupiaDict_Complete.db: 한국어 위키백과 690,422개 문서
- 💾 DevDict.db: Win32 API 2,000개 + MDN + Python + Rust + .NET 통합
- 언어별 아이콘 (🐍🪟📜🎨🌐🦀🎯💬)
- 코드 블록 클릭 복사 버튼
- TTS (브라우저 음성 합성 + 파일 기반 폴백)
