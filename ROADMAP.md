# 🗺️ GurupiaDict & DevDict Project Roadmap

## 📊 현재 진행 상황 (Status: Completed Phase 3)

### 1. GurupiaDict (지식의 바다) - `GurupiaDict_Complete.db`
- ✅ 한국어 위키백과 690,422개 문서 구축 완료
- ✅ 26,710,233개 문서 간 링크 연결 (Knowledge Graph)
- ✅ FTS5 기반 초고속 검색 엔진 탑재
- ✅ 온라인/오프라인 하이브리드 TTS 기능 구현

### 2. DevDict (개발자의 무기) - `DevDict.db`
- ✅ Win32 API 2,000개 핵심 레퍼런스 통합
- ✅ Python Standard Library 핵심 함수 및 모듈(os, sys, json 등) 통합
- ✅ 제목 접두사(`python:`, `win32:`)를 통한 언어별 구분 체계 수립
- ✅ MDN Web Docs (JS, HTML, CSS) 25개 핵심 레퍼런스
- ✅ Stack Overflow 인기 Q&A 20개
- ✅ C# & .NET Core 9개 핵심 클래스
- ✅ Rust 표준 라이브러리 14개 타입
- ✅ **총 3,134개 개발자 문서 구축 완료**

### 3. Viewer (통합 뷰어)
- ✅ 포트 5000: 위키백과 전용 뷰어
- ✅ 포트 5001: 개발자 사전 전용 뷰어
- ✅ Outfit/Fira Code 프리미엄 폰트
- ✅ Highlight.js 코드 하이라이팅
- ✅ 📋 클릭 복사 버튼
- ✅ 언어별 아이콘 (🐍🪟📜🎨🌐🦀🎯💬)

---

## 🚀 향후 로드맵 (Future Phases)

### 🔹 Phase 2: Web & UI 고도화 (Completed ✅)
- [x] **MDN Web Docs 통합**: JavaScript, HTML, CSS 레퍼런스 데이터 수집 및 이식
- [x] **UI/UX 개선**: 언어별 아이콘(🐍, 🪟, 📜 등) 표시, Outfit 폰트 및 테마 조정
- [x] **코드 스니펫 기능**: 문서 내 예제 코드 Syntax Highlighting 및 복사 버튼 추가

### 🔹 Phase 3: 지식 확장 (Completed ✅)
- [x] **Stack Overflow 인기 Q&A**: 실무 에러 해결을 위한 핵심 문답 데이터 이식
- [x] **C# & .NET**: Windows 개발을 위한 추가 레퍼런스 확보
- [x] **Rust**: 고성능 언어 탐구를 위한 표준 라이브러리 추가

### 🔹 Phase 4: 모바일 및 고성능화 (Next Target)
- [ ] **Android App 포팅**: 로컬 DB를 탑재한 네이티브/하이브리드 앱 개발
- [ ] **오프라인 오디오 패키지**: 인기 문서 1,000개에 대한 Google TTS 고품질 오디오 미리 생성
- [ ] **이미지 오프라인 캐싱**: 문서 내 핵심 이미지 데이터 패키징

---

## 💡 다음 세션 재개 가이드
다음 세션을 시작할 때 아래와 같이 요청하시면 즉시 이어서 작업이 가능합니다:
- **"Phase 4 진행해줘"**: 모바일 앱 및 고성능화 작업 시작
- **"로드맵 업데이트해줘"**: 새로운 아이디어 추가 및 진행 상황 갱신
- **"통합 뷰어 실행해줘"**: 기존에 구축된 5000/5001번 서버 재가동
