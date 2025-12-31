# 메일링 시스템 설정 가이드

LIS Lab의 주간 다이제스트 및 메일링 기능을 사용하기 위한 설정 가이드입니다.

## 목차
1. [필수 패키지 설치](#필수-패키지-설치)
2. [Redis 설치 및 실행](#redis-설치-및-실행)
3. [환경 변수 설정](#환경-변수-설정)
4. [Celery 실행](#celery-실행)
5. [이메일 설정](#이메일-설정)
6. [테스트](#테스트)

---

## 1. 필수 패키지 설치

```bash
# 가상환경 활성화
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

설치되는 주요 패키지:
- `celery==5.3.6` - 비동기 작업 큐
- `redis==5.0.1` - 메시지 브로커

---

## 2. Redis 설치 및 실행

### macOS (Homebrew)
```bash
# Redis 설치
brew install redis

# Redis 서버 시작
brew services start redis

# 또는 수동 실행
redis-server
```

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### Redis 연결 확인
```bash
redis-cli ping
# PONG이 출력되면 정상
```

---

## 3. 환경 변수 설정

`.env` 파일에 다음 설정 추가:

```env
# Celery & Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Site URL (이메일 링크에 사용)
SITE_URL=http://localhost:3000

# Email 설정 (Gmail 예시)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@lis.com

# 개발 환경에서는 콘솔로 출력
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Gmail 앱 비밀번호 생성 (2FA 필수)
1. Google 계정 → 보안 → 2단계 인증 활성화
2. 보안 → 앱 비밀번호 생성
3. 생성된 16자리 비밀번호를 `EMAIL_HOST_PASSWORD`에 설정

---

## 4. Celery 실행

### 터미널 1: Celery Worker 실행
```bash
cd /Users/kimsuntae/LIS
source venv/bin/activate
celery -A config worker --loglevel=info
```

### 터미널 2: Celery Beat 실행 (주기적 작업 스케줄러)
```bash
cd /Users/kimsuntae/LIS
source venv/bin/activate
celery -A config beat --loglevel=info
```

### 개발 환경에서 함께 실행 (권장하지 않음, 테스트용)
```bash
celery -A config worker --beat --loglevel=info
```

---

## 5. 이메일 설정

### 주간 다이제스트 스케줄
- **실행 시간**: 매주 월요일 오전 9시
- **대상**: 메일링 설정에서 "주간 다이제스트"를 선택한 사용자
- **내용**: 지난 주(월~일)에 발행된 새 콘텐츠

### 월간 다이제스트 스케줄
- **실행 시간**: 매월 1일 오전 9시
- **대상**: 메일링 설정에서 "월간 다이제스트"를 선택한 사용자
- **내용**: 지난 달에 발행된 새 콘텐츠

### 즉시 알림
- **실행 시간**: 새 콘텐츠 발행 시 즉시
- **대상**: 메일링 설정에서 "즉시"를 선택한 사용자
- **내용**: 방금 발행된 콘텐츠 정보

---

## 6. 테스트

### Django Shell에서 수동 실행

```bash
python manage.py shell
```

```python
from apps.accounts.tasks import send_weekly_digest_emails
from django.utils import timezone
from datetime import timedelta

# 주간 다이제스트 수동 실행
result = send_weekly_digest_emails()
print(result)
```

### 특정 사용자에게 테스트 이메일 발송

```python
from apps.accounts.models import User
from apps.accounts.email_utils import get_weekly_contents_for_user, send_weekly_digest
from django.utils import timezone
from datetime import timedelta

# 사용자 가져오기
user = User.objects.get(username='admin')

# 지난 주 날짜 계산
today = timezone.now().date()
week_start = today - timedelta(days=7)
week_end = today

week_start_dt = timezone.datetime.combine(week_start, timezone.datetime.min.time())
week_end_dt = timezone.datetime.combine(week_end, timezone.datetime.min.time())
week_start_dt = timezone.make_aware(week_start_dt)
week_end_dt = timezone.make_aware(week_end_dt)

# 콘텐츠 가져오기
contents_by_category = get_weekly_contents_for_user(user, week_start_dt, week_end_dt)
print(f"카테고리 수: {len(contents_by_category)}")

# 이메일 발송
send_weekly_digest(user, week_start_dt, week_end_dt, contents_by_category)
print("이메일 발송 완료!")
```

### Celery 작업 상태 확인

```bash
# Celery Flower (모니터링 도구) 설치 및 실행
pip install flower
celery -A config flower

# 웹 브라우저에서 http://localhost:5555 접속
```

---

## 주요 파일 구조

```
/Users/kimsuntae/LIS/
├── apps/
│   └── accounts/
│       ├── models.py              # MailingPreference 모델
│       ├── serializers.py         # MailingPreferenceSerializer
│       ├── views.py               # MailingPreferenceViewSet
│       ├── email_utils.py         # 이메일 발송 유틸리티
│       ├── tasks.py               # Celery 작업 정의
│       └── templates/
│           └── emails/
│               ├── weekly_digest.html  # HTML 이메일 템플릿
│               └── weekly_digest.txt   # 텍스트 이메일 템플릿
├── config/
│   ├── celery.py                  # Celery 설정 및 스케줄
│   ├── settings.py                # Django 설정 (Celery 포함)
│   └── __init__.py                # Celery 앱 로드
└── frontend/
    └── src/
        └── app/
            └── (main)/
                └── my/
                    └── mailing-settings/
                        └── page.tsx    # 메일링 설정 페이지
```

---

## 문제 해결

### Redis 연결 실패
```
ConnectionError: Error connecting to Redis
```
**해결**: Redis 서버가 실행 중인지 확인
```bash
redis-cli ping
```

### Celery Worker가 작업을 받지 못함
**해결**: Celery Beat가 실행 중인지 확인하고, 로그를 확인

### 이메일이 발송되지 않음
1. `.env` 파일의 이메일 설정 확인
2. Gmail 앱 비밀번호 확인 (2FA 활성화 필요)
3. 개발 환경에서는 `EMAIL_BACKEND=console`로 설정하여 콘솔에 출력

### 콘텐츠가 없는데 이메일이 발송됨
- `get_weekly_contents_for_user()` 함수는 콘텐츠가 없으면 빈 딕셔너리 반환
- `send_weekly_digest_emails()` 작업은 콘텐츠가 있을 때만 이메일 발송

---

## 운영 환경 배포 시 주의사항

1. **Redis 보안**: Redis에 비밀번호 설정 및 방화벽 설정
2. **Celery Worker**: Supervisor, systemd 등으로 데몬화
3. **로그 관리**: 로그 파일 로테이션 설정
4. **모니터링**: Flower, Sentry 등으로 작업 모니터링
5. **이메일 제한**: 대량 발송 시 이메일 제공자의 제한 고려

---

## API 엔드포인트

### 메일링 설정 조회
```http
GET /api/accounts/mailing-preferences/
Authorization: Bearer {token}
```

### 메일링 설정 업데이트
```http
PATCH /api/accounts/mailing-preferences/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
  "enabled": true,
  "frequency": "WEEKLY",
  "all_categories": false,
  "selected_category_ids": [1, 2, 3]
}
```

---

## 참고 자료

- [Celery Documentation](https://docs.celeryq.dev/)
- [Redis Documentation](https://redis.io/docs/)
- [Django Email Documentation](https://docs.djangoproject.com/en/4.2/topics/email/)
