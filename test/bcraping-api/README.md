# Bcraping.kr API 래퍼

아프리카TV 방송 모니터링 데이터를 제공하는 FastAPI 기반 API 래퍼입니다.

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 서버 실행

```bash
uvicorn main:app --reload
```

또는

```bash
python main.py
```

서버가 `http://localhost:8000`에서 실행됩니다.

### 3. API 문서 확인

브라우저에서 다음 주소로 접속하면 자동 생성된 API 문서를 확인할 수 있습니다:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API 엔드포인트

### 1. 모니터링 데이터 조회

```
GET /monitor/{bj_id}/{station_id}
```

**파라미터:**
- `bj_id` (필수): BJ ID (예: pyh3646)
- `station_id` (필수): 방송국 ID (예: 290639636)
- `page` (선택): 페이지 번호 (기본값: 1)
- `per_page` (선택): 페이지당 항목 수 (기본값: 20, 최대: 100)

**예시:**
```bash
curl "http://localhost:8000/monitor/pyh3646/290639636?page=1&per_page=20"
```

**응답 예시:**
```json
{
  "data": {
    "contents": [
      {
        "MESSAGE_ID": "176805985970580",
        "BALLON_COUNT": 300,
        "BALLON_USER_NAME": "JINU혀니",
        "BALLON_USER_ID": "user123",
        "CREATE_DATE": "2026-01-11 00:44:24",
        "MESSAGE": "응원합니다!",
        "BJ_ID": "pyh3646",
        "STATION_ID": "290639636"
      }
    ],
    "total": 1500,
    "page": 1,
    "perPage": 20
  }
}
```

### 2. 통계 데이터 조회

```
GET /monitor/{bj_id}/{station_id}/stats
```

**파라미터:**
- `bj_id` (필수): BJ ID
- `station_id` (필수): 방송국 ID
- `stat_type` (선택): 통계 타입
  - `donation_rank`: 후원 순위
  - `chat_share`: 채팅 지분
  - `keywords`: 주요 키워드
  - `hourly`: 시간대별 통계

**예시:**
```bash
curl "http://localhost:8000/monitor/pyh3646/290639636/stats?stat_type=donation_rank"
```

### 3. 이전 방송 기록 조회

```
GET /monitor/{bj_id}/{station_id}/history
```

**예시:**
```bash
curl "http://localhost:8000/monitor/pyh3646/290639636/history"
```

### 4. 헬스 체크

```
GET /health
```

**예시:**
```bash
curl "http://localhost:8000/health"
```

## 🔧 개발 모드

개발 모드로 실행 (자동 재시작):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 주의사항

- 이 API는 `bcraping.kr`의 내부 API를 래핑한 것입니다.
- 원본 사이트의 API가 변경되거나 접근 제한이 생기면 작동하지 않을 수 있습니다.
- 과도한 요청은 원본 서버에 부담을 줄 수 있으니 적절한 간격으로 요청하세요.

## 🛠️ 기술 스택

- **FastAPI**: 현대적이고 빠른 Python 웹 프레임워크
- **httpx**: 비동기 HTTP 클라이언트
- **uvicorn**: ASGI 서버

## 🌐 외부 공개하기

다른 사람들도 이 API를 사용할 수 있도록 공개하는 방법:

### 방법 1: ngrok 사용 (가장 쉬움) ⭐

```bash
# 새 PowerShell 창에서 실행
ngrok http 8000
```

출력된 URL (예: `https://xxxx.ngrok-free.app`)을 친구들에게 공유하세요!

자세한 내용은 [DEPLOYMENT.md](DEPLOYMENT.md) 참고

### 방법 2: 로컬 네트워크 공유

같은 WiFi에 연결된 사람들은 다음 주소로 접속 가능:
- `http://118.45.196.89:8000/docs`

## 📄 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 제공됩니다.
