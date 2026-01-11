# 🌐 Bcraping API 외부 공개 가이드

이 문서는 Bcraping API를 다른 사람들이 사용할 수 있도록 공개하는 방법을 설명합니다.

## 📋 목차

1. [ngrok을 사용한 즉시 공개](#1-ngrok을-사용한-즉시-공개-추천)
2. [로컬 네트워크 공유](#2-로컬-네트워크-공유)
3. [클라우드 배포](#3-클라우드-배포)

---

## 1. ngrok을 사용한 즉시 공개 (추천) ⭐

**장점**: 무료, 즉시 사용 가능, HTTPS 자동 제공
**단점**: 무료 버전은 URL이 매번 변경됨

### 설치 및 실행

#### Windows (이미 설치됨)
```bash
# 새 PowerShell 창 열기
ngrok http 8000
```

#### Mac/Linux
```bash
# Homebrew로 설치
brew install ngrok

# 실행
ngrok http 8000
```

### 사용 방법

1. API 서버 실행 (기존 터미널):
   ```bash
   cd E:\test\test\bcraping-api
   .\venv\Scripts\Activate.ps1
   python main.py
   ```

2. **새 터미널 창**에서 ngrok 실행:
   ```bash
   ngrok http 8000
   ```

3. 출력된 URL을 공유:
   ```
   Forwarding  https://abcd-1234-5678.ngrok-free.app -> http://localhost:8000
   ```

4. 다른 사람들은 이 URL로 접속:
   - API 문서: `https://abcd-1234-5678.ngrok-free.app/docs`
   - API 호출: `https://abcd-1234-5678.ngrok-free.app/monitor/pyh3646/290639636`

### ngrok 무료 계정 등록 (선택사항)

무료 계정을 만들면 더 많은 기능을 사용할 수 있습니다:

1. https://ngrok.com 에서 가입
2. 인증 토큰 받기
3. 토큰 설정:
   ```bash
   ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

---

## 2. 로컬 네트워크 공유

**장점**: 무료, 설정 불필요
**단점**: 같은 WiFi/네트워크에 있는 사람만 접속 가능

### 현재 설정

서버가 이미 `0.0.0.0:8000`으로 실행 중이므로 네트워크 공유가 활성화되어 있습니다.

### 접속 방법

1. **내 IP 주소 확인**:
   ```bash
   ipconfig  # Windows
   ifconfig  # Mac/Linux
   ```
   
   현재 IP: `118.45.196.89`

2. **방화벽 설정** (Windows):
   ```powershell
   # 8000 포트 허용
   New-NetFirewallRule -DisplayName "Bcraping API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   ```

3. **다른 사람들에게 공유**:
   - 같은 WiFi에 연결된 사람들은 다음 주소로 접속:
   - `http://118.45.196.89:8000/docs`

---

## 3. 클라우드 배포

### 3-1. Render (무료, 추천)

1. https://render.com 가입
2. "New Web Service" 클릭
3. GitHub 저장소 연결 또는 직접 업로드
4. 설정:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 배포 완료!

### 3-2. Railway (무료)

1. https://railway.app 가입
2. "New Project" → "Deploy from GitHub"
3. 저장소 선택
4. 자동 배포 완료

### 3-3. Fly.io (무료)

```bash
# Fly CLI 설치
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# 로그인
fly auth login

# 앱 생성
fly launch

# 배포
fly deploy
```

### 3-4. Heroku

```bash
# Heroku CLI 설치
# https://devcenter.heroku.com/articles/heroku-cli

# 로그인
heroku login

# Procfile 생성
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile

# 배포
heroku create bcraping-api
git push heroku main
```

---

## 4. Docker로 배포 (고급)

### Dockerfile 생성

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 빌드 및 실행

```bash
# 이미지 빌드
docker build -t bcraping-api .

# 컨테이너 실행
docker run -p 8000:8000 bcraping-api
```

---

## 📊 각 방법 비교

| 방법 | 난이도 | 비용 | 속도 | 안정성 | 추천도 |
|------|--------|------|------|--------|--------|
| ngrok | ⭐ 쉬움 | 무료 | 빠름 | 중간 | ⭐⭐⭐⭐⭐ |
| 로컬 네트워크 | ⭐ 쉬움 | 무료 | 매우 빠름 | 낮음 | ⭐⭐⭐ |
| Render | ⭐⭐ 보통 | 무료 | 보통 | 높음 | ⭐⭐⭐⭐ |
| Railway | ⭐⭐ 보통 | 무료 | 빠름 | 높음 | ⭐⭐⭐⭐ |
| Fly.io | ⭐⭐⭐ 어려움 | 무료 | 빠름 | 높음 | ⭐⭐⭐ |
| Docker | ⭐⭐⭐⭐ 어려움 | 무료 | 빠름 | 높음 | ⭐⭐ |

---

## 🔒 보안 고려사항

### API 키 인증 추가 (선택사항)

`main.py`에 간단한 API 키 인증을 추가할 수 있습니다:

```python
from fastapi import Header, HTTPException

API_KEY = "your-secret-api-key-here"

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# 엔드포인트에 적용
@app.get("/monitor/{bj_id}/{station_id}", dependencies=[Depends(verify_api_key)])
async def get_monitor_data(...):
    ...
```

### Rate Limiting 추가

```bash
pip install slowapi

# main.py에 추가
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.get("/monitor/{bj_id}/{station_id}")
@limiter.limit("10/minute")
async def get_monitor_data(...):
    ...
```

---

## 📞 문제 해결

### ngrok이 작동하지 않을 때
- PowerShell을 **관리자 권한**으로 다시 시작
- 또는 시스템 재시작 후 다시 시도

### 방화벽 문제
```powershell
# Windows 방화벽 규칙 추가
New-NetFirewallRule -DisplayName "Bcraping API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### 포트가 이미 사용 중일 때
```bash
# 다른 포트로 실행
uvicorn main:app --host 0.0.0.0 --port 8001

# ngrok도 포트 변경
ngrok http 8001
```

---

## 🎯 빠른 시작 (ngrok)

```bash
# 터미널 1: API 서버 실행
cd E:\test\test\bcraping-api
.\venv\Scripts\Activate.ps1
python main.py

# 터미널 2: ngrok 실행 (새 PowerShell 창)
ngrok http 8000

# 출력된 URL을 친구들에게 공유!
```

---

## 📚 추가 자료

- [ngrok 공식 문서](https://ngrok.com/docs)
- [FastAPI 배포 가이드](https://fastapi.tiangolo.com/deployment/)
- [Render 배포 가이드](https://render.com/docs)
- [Railway 배포 가이드](https://docs.railway.app/)
