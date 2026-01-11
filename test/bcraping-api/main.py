"""
Bcraping.kr API 래퍼
아프리카TV 방송 모니터링 데이터를 제공하는 FastAPI 애플리케이션
"""

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
from typing import Optional
import logging
import os
import asyncio
import json
import websockets
from websockets.client import WebSocketClientProtocol

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Bcraping.kr API",
    description="아프리카TV 방송 모니터링 데이터 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 헤더 (브라우저처럼 보이도록)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://bcraping.kr/",
}

BASE_URL = "https://bcraping.kr/api"




@app.get("/")
async def root():
    """대시보드 페이지"""
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {
        "message": "Bcraping.kr API 래퍼",
        "version": "1.0.0",
        "endpoints": {
            "monitor": "/monitor/{bj_id}/{station_id}",
            "stats": "/monitor/{bj_id}/{station_id}/stats",
            "docs": "/docs"
        }
    }


@app.get("/api/find-station/{bj_id}")
async def find_station_id(bj_id: str):
    """
    BJ ID로 현재 방송 중인 station_id 찾기
    
    - **bj_id**: BJ ID (예: pyh3646)
    """
    # 아프리카TV API를 통해 현재 방송 정보 조회
    url = f"https://bjapi.afreecatv.com/api/{bj_id}/station"
    
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            # 방송 중인 경우 station_id 반환
            if data.get("broad") and data["broad"].get("broad_no"):
                station_id = data["broad"]["broad_no"]
                return {
                    "success": True,
                    "bj_id": bj_id,
                    "station_id": station_id,
                    "is_live": True,
                    "title": data["broad"].get("broad_title", ""),
                    "category": data["broad"].get("broad_cate_no", "")
                }
            else:
                return {
                    "success": False,
                    "bj_id": bj_id,
                    "is_live": False,
                    "message": "현재 방송 중이 아닙니다"
                }
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP 에러: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"방송 정보 조회 실패: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"요청 에러: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"아프리카TV API 연결 실패: {str(e)}"
        )



@app.get("/monitor/{bj_id}/{station_id}")
async def get_monitor_data(
    bj_id: str,
    station_id: str,
    page: int = Query(1, ge=1, description="페이지 번호"),
    per_page: int = Query(20, ge=1, le=100, description="페이지당 항목 수")
):
    """
    방송 모니터링 데이터 조회
    
    - **bj_id**: BJ ID (예: pyh3646)
    - **station_id**: 방송국 ID (예: 290639636)
    - **page**: 페이지 번호 (기본값: 1)
    - **per_page**: 페이지당 항목 수 (기본값: 20, 최대: 100)
    """
    url = f"{BASE_URL}/monitor/{bj_id}/{station_id}"
    params = {
        "page": page,
        "perPage": per_page
    }
    
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP 에러: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"원본 API 요청 실패: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"요청 에러: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"원본 API 연결 실패: {str(e)}"
        )


@app.get("/monitor/{bj_id}/{station_id}/stats")
async def get_stats_data(
    bj_id: str,
    station_id: str,
    stat_type: Optional[str] = Query(None, description="통계 타입 (donation_rank, chat_share, keywords, hourly)")
):
    """
    방송 통계 데이터 조회
    
    - **bj_id**: BJ ID
    - **station_id**: 방송국 ID
    - **stat_type**: 통계 타입 (선택사항)
      - donation_rank: 후원 순위
      - chat_share: 채팅 지분
      - keywords: 주요 키워드
      - hourly: 시간대별 통계
    """
    url = f"{BASE_URL}/monitor/{bj_id}/{station_id}/stats"
    params = {}
    if stat_type:
        params["type"] = stat_type
    
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP 에러: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"통계 데이터 조회 실패: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"요청 에러: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"원본 API 연결 실패: {str(e)}"
        )


@app.get("/monitor/{bj_id}/{station_id}/history")
async def get_history_data(
    bj_id: str,
    station_id: str
):
    """
    이전 방송 세션 목록 조회
    
    - **bj_id**: BJ ID
    - **station_id**: 방송국 ID
    """
    url = f"{BASE_URL}/monitor/{bj_id}/{station_id}/history"
    
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP 에러: {e.response.status_code}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"이전 기록 조회 실패: {e.response.text}"
        )
    except httpx.RequestError as e:
        logger.error(f"요청 에러: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"원본 API 연결 실패: {str(e)}"
        )



@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy", "service": "bcraping-api"}




@app.websocket("/ws/monitor/{bj_id}/{station_id}")
async def websocket_monitor(websocket: WebSocket, bj_id: str, station_id: str):
    """
    실시간 모니터링 WebSocket (아프리카TV WebSocket 직접 연결)
    
    - **bj_id**: BJ ID
    - **station_id**: 방송국 ID
    """
    await websocket.accept()
    logger.info(f"✅ 클라이언트 WebSocket 연결: {bj_id}/{station_id}")
    
    broadcast_start_time = None
    
    # 방송 시작 시간 추출
    try:
        page_url = f"https://bcraping.kr/monitor/{bj_id}/{station_id}"
        async with httpx.AsyncClient(headers=HEADERS, timeout=10.0) as client:
            page_response = await client.get(page_url)
            if page_response.status_code == 200:
                html_content = page_response.text
                import re
                match = re.search(r'(\d{2}\.\d{2}\.\d{2}\s+\d{2}:\d{2}:\d{2})', html_content)
                if match:
                    time_str = match.group(1)
                    parts = time_str.split()
                    date_parts = parts[0].split('.')
                    time_part = parts[1]
                    broadcast_start_time = f"20{date_parts[0]}-{date_parts[1]}-{date_parts[2]} {time_part}"
                    logger.info(f"📅 방송 시작 시간: {broadcast_start_time}")
    except Exception as e:
        logger.error(f"❌ 방송 시작 시간 추출 실패: {str(e)}")
    
    # 아프리카TV WebSocket 연결 시도
    afreeca_ws_urls = [
        f"wss://chat.afreecatv.com:9443/Websocket/{bj_id}",
        f"wss://live.afreecatv.com:9443/Websocket/{bj_id}",
        f"wss://chat-ws.afreecatv.com/Websocket/{bj_id}",
    ]
    
    connected = False
    
    for ws_url in afreeca_ws_urls:
        try:
            logger.info(f"🔌 아프리카TV WebSocket 연결 시도: {ws_url}")
            
            async with websockets.connect(
                ws_url,
                extra_headers={
                    "User-Agent": HEADERS["User-Agent"],
                    "Origin": "https://play.afreecatv.com"
                },
                ping_interval=20,
                ping_timeout=10
            ) as afreeca_ws:
                logger.info(f"✅ 아프리카TV WebSocket 연결 성공!")
                connected = True
                
                # 초기 데이터 전송 (방송 시작 시간)
                if broadcast_start_time:
                    await websocket.send_json({
                        "type": "broadcast_start",
                        "broadcast_start": broadcast_start_time
                    })
                
                # 아프리카TV WebSocket에서 데이터 수신
                async for message in afreeca_ws:
                    try:
                        # 메시지 파싱
                        data = json.loads(message) if isinstance(message, str) else message
                        
                        # 방송 시작 시간 추가
                        if broadcast_start_time and isinstance(data, dict):
                            data["broadcast_start"] = broadcast_start_time
                        
                        # 클라이언트에 전달
                        await websocket.send_json(data)
                        logger.info(f"📨 데이터 전달: {type(data)}")
                        
                    except json.JSONDecodeError:
                        logger.warning(f"⚠️ JSON 파싱 불가: {message}")
                    except Exception as e:
                        logger.error(f"❌ 메시지 처리 에러: {str(e)}")
                
                break  # 연결 성공하면 루프 종료
                
        except websockets.exceptions.WebSocketException as e:
            logger.warning(f"⚠️ WebSocket 연결 실패 ({ws_url}): {str(e)}")
            continue
        except Exception as e:
            logger.warning(f"⚠️ 연결 에러 ({ws_url}): {str(e)}")
            continue
    
    # 모든 WebSocket 연결 실패 시 폴링 폴백
    if not connected:
        logger.warning(f"⚠️ 모든 WebSocket 연결 실패, 폴링 방식으로 폴백")
        
        try:
            last_message_id = None
            
            # 초기 데이터 로드
            url = f"{BASE_URL}/monitor/{bj_id}/{station_id}"
            params = {"page": 1, "perPage": 100}
            
            async with httpx.AsyncClient(headers=HEADERS, timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data.get("data") and data["data"].get("contents"):
                    contents = data["data"]["contents"]
                    
                    if contents:
                        broadcast_start = broadcast_start_time
                        if not broadcast_start and contents:
                            oldest = contents[-1]
                            if oldest.get("CREATE_DATE"):
                                broadcast_start = oldest["CREATE_DATE"]
                        
                        await websocket.send_json({
                            "type": "initial",
                            "data": contents,
                            "broadcast_start": broadcast_start
                        })
                        
                        last_message_id = contents[0].get("MESSAGE_ID")
                        logger.info(f"✅ 초기 데이터 {len(contents)}개 전송")
            
            # 실시간 업데이트 루프 (0.3초 간격으로 더 빠르게)
            while True:
                await asyncio.sleep(0.3)
                
                try:
                    async with httpx.AsyncClient(headers=HEADERS, timeout=5.0) as client:
                        response = await client.get(url, params={"page": 1, "perPage": 20})
                        response.raise_for_status()
                        data = response.json()
                        
                        if data.get("data") and data["data"].get("contents"):
                            contents = data["data"]["contents"]
                            
                            if contents:
                                current_message_id = contents[0].get("MESSAGE_ID")
                                
                                if current_message_id != last_message_id:
                                    new_items = []
                                    for item in contents:
                                        if item.get("MESSAGE_ID") == last_message_id:
                                            break
                                        new_items.append(item)
                                    
                                    if new_items:
                                        await websocket.send_json({
                                            "type": "update",
                                            "data": new_items
                                        })
                                        last_message_id = current_message_id
                                        logger.info(f"✅ 새 데이터 {len(new_items)}개 전송")
                                        
                except httpx.RequestError as e:
                    logger.error(f"❌ 데이터 조회 실패: {str(e)}")
                    await websocket.send_json({
                        "type": "error",
                        "message": f"데이터 조회 실패: {str(e)}"
                    })
                        
        except WebSocketDisconnect:
            logger.info(f"🔌 클라이언트 WebSocket 연결 종료: {bj_id}/{station_id}")
        except Exception as e:
            logger.error(f"❌ WebSocket 에러: {str(e)}")
            try:
                await websocket.send_json({
                    "type": "error",
                    "message": f"에러 발생: {str(e)}"
                })
            except:
                pass
            finally:
                try:
                    await websocket.close()
                except:
                    pass





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
