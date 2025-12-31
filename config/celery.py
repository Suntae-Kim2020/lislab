"""
Celery 설정
"""
import os
from celery import Celery
from celery.schedules import crontab

# Django 설정 모듈 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Celery 인스턴스 생성
app = Celery('lis')

# Django settings.py에서 설정 로드 (CELERY_ 접두사가 있는 설정만)
app.config_from_object('django.conf:settings', namespace='CELERY')

# 등록된 Django 앱에서 tasks.py 자동 검색
app.autodiscover_tasks()

# 주기적 태스크 스케줄 설정
app.conf.beat_schedule = {
    # 주간 다이제스트 - 매주 월요일 오전 9시
    'send-weekly-digest': {
        'task': 'apps.accounts.tasks.send_weekly_digest_emails',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),  # 월요일 오전 9시
    },
    # 월간 다이제스트 - 매월 1일 오전 9시
    'send-monthly-digest': {
        'task': 'apps.accounts.tasks.send_monthly_digest_emails',
        'schedule': crontab(hour=9, minute=0, day_of_month=1),  # 매월 1일 오전 9시
    },
}

# 타임존 설정
app.conf.timezone = 'Asia/Seoul'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """디버그용 태스크"""
    print(f'Request: {self.request!r}')
