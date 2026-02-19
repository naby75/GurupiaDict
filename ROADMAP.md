# 🗺️ GurupiaDict & DevDict Project Roadmap

## ✅ 완료된 Phase

### Phase 1: 지식의 바다 — `GurupiaDict_Complete.db`
- ✅ 한국어 위키백과 690,422개 문서 구축
- ✅ 26,710,233개 문서 간 링크 연결 (Knowledge Graph)
- ✅ FTS5 기반 초고속 검색 엔진
- ✅ 온라인/오프라인 하이브리드 TTS

### Phase 2: Web & UI 고도화
- ✅ MDN Web Docs (JS, HTML, CSS) 통합
- ✅ 언어별 아이콘 표시, Outfit 폰트 및 다크 테마
- ✅ 코드 스니펫 Highlight.js + 복사 버튼

### Phase 3: 지식 확장 — `DevDict.db`
- ✅ Win32 API 2,000개 통합
- ✅ Python 표준 라이브러리 핵심 모듈
- ✅ Stack Overflow 인기 Q&A 20개
- ✅ C# & .NET Core 9개 핵심 클래스
- ✅ Rust 표준 라이브러리 26개 타입 (실문서 크롤링)
- ✅ **총 3,134개+ 개발자 문서**

### Phase 4: 코드 품질 & 안정성 (v0.2.0)
- ✅ `LazyLock` Regex 캐싱 — 파싱 성능 대폭 향상
- ✅ UTF-8 안전 절단 (한국어 패닉 수정)
- ✅ WAL 모드 + 배치 커밋 — DB 쓰기 안정성
- ✅ DOMPurify XSS 방어
- ✅ 라이트 모드 완전 구현
- ✅ 완전 오프라인 동작 (CDN → 로컬 vendor)
- ✅ 릴리즈 배포 (포터블 ZIP + 설치 스크립트)

---

## 🔹 향후 로드맵 (Future Phases)

### Phase 5: 모바일 & 고성능화 (Next Target)
- [ ] **Android App 포팅**: SQLite DB 탑재 네이티브 앱 (Tauri2 / Kotlin)
- [ ] **오프라인 오디오 패키지**: 인기 문서 1,000개 TTS 오디오 미리 생성
- [ ] **AI 의미 검색**: 문서 임베딩 + 벡터 유사도 검색

### Phase 6: 데이터 확장
- [ ] **영어 위키백과 서브셋**: 핵심 STEM 문서 10만건
- [ ] **Go / Java / TypeScript** 표준 라이브러리 추가
- [ ] **한자어 사전** 연동

---

## 💡 다음 세션 재개 가이드
- **"Phase 5 진행해줘"**: 모바일 앱 및 고성능화 시작
- **"DevDict 데이터 추가해줘"**: 새 언어/프레임워크 문서 추가
- **"통합 뷰어 실행해줘"**: 5000/5001 서버 재가동
