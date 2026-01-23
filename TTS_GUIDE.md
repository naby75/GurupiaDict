# GurupiaDict TTS Generator

## 🎙️ Google Cloud TTS 통합

### 사전 준비

1. **Google Cloud 계정 설정**
   ```bash
   # 1. Google Cloud Console에서 프로젝트 생성
   # 2. Text-to-Speech API 활성화
   # 3. 서비스 계정 생성 및 JSON 키 다운로드
   ```

2. **환경 변수 설정**
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account-key.json"
   ```

### 사용 방법

#### 1. 인기 문서 100개 TTS 생성

```bash
python tts_generator.py GurupiaDict_Complete.db 100
```

**결과:**
- `gurupia-viewer/audio/` 폴더에 MP3 파일 생성
- 약 200,000자 처리 (무료 범위 내)
- 파일 크기: 약 300MB

#### 2. 특정 개수 생성

```bash
# Top 50개만
python tts_generator.py GurupiaDict_Complete.db 50

# Top 500개
python tts_generator.py GurupiaDict_Complete.db 500
```

### 비용 계산

| 문서 수 | 예상 문자 수 | 비용 (WaveNet) |
|---------|--------------|----------------|
| 100 | 200,000 | 무료 |
| 500 | 1,000,000 | 무료 |
| 1,000 | 2,000,000 | $16 |

**무료 쿼터:** 월 100만 자 (WaveNet)

### 생성된 파일 사용

웹 뷰어가 자동으로 `audio/` 폴더의 MP3 파일을 감지하고 사용합니다.

```
MP3 있음 → 즉시 재생 (오프라인)
MP3 없음 → 브라우저 TTS 사용 (온라인)
```

### 주의사항

- ✅ 한 번 생성한 MP3는 영구 사용 가능
- ✅ 같은 파일은 재생성하지 않음 (스킵)
- ⚠️ Google Cloud 인증 필요
- ⚠️ 무료 쿼터 초과 시 과금

### AI Studio 사용

Google AI Studio에서 직접 생성하는 것도 가능합니다:
1. AI Studio에서 TTS 생성
2. MP3 다운로드
3. `gurupia-viewer/audio/` 폴더에 복사

---

**완성!** 🎉
