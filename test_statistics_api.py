import requests
import json

# 로그인
login_response = requests.post(
    'http://localhost:8000/api/token/',
    json={'username': 'admin', 'password': 'admin1234'}
)

if login_response.status_code == 200:
    token = login_response.json()['access']
    print(f"Token obtained: {token[:20]}...")

    # 통계 API 호출
    stats_response = requests.get(
        'http://localhost:8000/api/accounts/statistics/',
        headers={'Authorization': f'Bearer {token}'}
    )

    print(f"\nStatus Code: {stats_response.status_code}")

    if stats_response.status_code == 200:
        print("\nStatistics data:")
        print(json.dumps(stats_response.json(), indent=2, ensure_ascii=False)[:1000])
    else:
        print(f"\nError: {stats_response.text}")
else:
    print(f"Login failed: {login_response.text}")
