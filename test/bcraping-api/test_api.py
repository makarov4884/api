"""
API 테스트 스크립트
"""

import httpx
import asyncio
import json


async def test_api():
    """API 엔드포인트 테스트"""
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("Bcraping.kr API 테스트")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. 루트 엔드포인트 테스트
        print("\n[1] 루트 엔드포인트 테스트...")
        try:
            response = await client.get(f"{base_url}/")
            print(f"✓ 상태 코드: {response.status_code}")
            print(f"✓ 응답: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"✗ 에러: {e}")
        
        # 2. 헬스 체크 테스트
        print("\n[2] 헬스 체크 테스트...")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"✓ 상태 코드: {response.status_code}")
            print(f"✓ 응답: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"✗ 에러: {e}")
        
        # 3. 모니터링 데이터 조회 테스트
        print("\n[3] 모니터링 데이터 조회 테스트...")
        try:
            response = await client.get(
                f"{base_url}/monitor/pyh3646/290639636",
                params={"page": 1, "per_page": 5}
            )
            print(f"✓ 상태 코드: {response.status_code}")
            data = response.json()
            
            if "data" in data and "contents" in data["data"]:
                print(f"✓ 데이터 개수: {len(data['data']['contents'])}개")
                if data['data']['contents']:
                    print(f"✓ 첫 번째 항목:")
                    first_item = data['data']['contents'][0]
                    print(f"  - 메시지 ID: {first_item.get('MESSAGE_ID')}")
                    print(f"  - 닉네임: {first_item.get('BALLON_USER_NAME')}")
                    print(f"  - 별풍선: {first_item.get('BALLON_COUNT')}")
                    print(f"  - 시간: {first_item.get('CREATE_DATE')}")
            else:
                print(f"✓ 응답 구조: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
        except Exception as e:
            print(f"✗ 에러: {e}")
        
        # 4. 통계 데이터 조회 테스트
        print("\n[4] 통계 데이터 조회 테스트...")
        try:
            response = await client.get(
                f"{base_url}/monitor/pyh3646/290639636/stats"
            )
            print(f"✓ 상태 코드: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ 응답 구조: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
            else:
                print(f"  (통계 엔드포인트가 원본 API에 없을 수 있습니다)")
        except Exception as e:
            print(f"  (예상된 에러 - 통계 엔드포인트가 원본 API에 없을 수 있습니다)")
        
        # 5. 이전 기록 조회 테스트
        print("\n[5] 이전 기록 조회 테스트...")
        try:
            response = await client.get(
                f"{base_url}/monitor/pyh3646/290639636/history"
            )
            print(f"✓ 상태 코드: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ 응답 구조: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
            else:
                print(f"  (이전 기록 엔드포인트가 원본 API에 없을 수 있습니다)")
        except Exception as e:
            print(f"  (예상된 에러 - 이전 기록 엔드포인트가 원본 API에 없을 수 있습니다)")
    
    print("\n" + "=" * 60)
    print("테스트 완료!")
    print("=" * 60)


if __name__ == "__main__":
    print("서버가 http://localhost:8000 에서 실행 중인지 확인하세요.")
    print("실행 명령: uvicorn main:app --reload\n")
    
    try:
        asyncio.run(test_api())
    except KeyboardInterrupt:
        print("\n\n테스트가 중단되었습니다.")
