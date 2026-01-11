# Bcraping.kr API 사용 가이드

## 🚨 현재 상태

Python과 Node.js가 시스템에 설치되어 있지 않아 API 서버를 실행할 수 없습니다.

## 📥 설치 옵션

### 옵션 1: Python 설치 (권장)

1. **Python 다운로드**
   - 링크: https://www.python.org/downloads/
   - Windows용 최신 버전 다운로드 (Python 3.11 이상 권장)

2. **설치 시 주의사항**
   - ✅ **반드시 "Add Python to PATH" 체크박스를 선택하세요!**
   - 이 옵션을 선택하지 않으면 명령 프롬프트에서 Python을 사용할 수 없습니다.

3. **설치 확인**
   ```bash
   python --version
   ```
   또는
   ```bash
   py --version
   ```

4. **의존성 설치 및 실행**
   ```bash
   cd C:\Users\Administrator\Desktop\test\bcraping-api
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

### 옵션 2: Node.js 설치

1. **Node.js 다운로드**
   - 링크: https://nodejs.org/
   - LTS 버전 다운로드

2. **설치 후 Node.js 버전 API 생성**
   - 설치 후 알려주시면 Node.js 버전의 API를 생성해드리겠습니다.

### 옵션 3: 브라우저에서 직접 테스트

Python이나 Node.js 없이도 브라우저에서 직접 bcraping.kr API를 호출할 수 있는 HTML 페이지를 만들 수 있습니다.

## 🎯 추천 방법

**Python 설치를 추천합니다:**
- 이미 FastAPI 코드가 완성되어 있음
- 설치가 간단함
- 자동 API 문서 생성 (Swagger UI)
- 비동기 처리로 빠른 성능

## 📞 다음 단계

어떤 방법을 선호하시나요?
1. Python 설치 후 FastAPI 사용
2. Node.js 설치 후 Express.js API 생성
3. 브라우저 테스트 페이지 생성

선택하시면 해당 방법으로 진행하겠습니다!
