"""
Celery 태스크
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User
from .email_utils import send_weekly_digest, get_weekly_contents_for_user


@shared_task
def send_weekly_digest_emails():
    """
    모든 활성 사용자에게 주간 다이제스트 이메일 발송
    매주 월요일 오전 9시에 실행되도록 스케줄링
    """
    # 지난 주의 시작과 끝 계산
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday() + 7)  # 지난주 월요일
    week_end = week_start + timedelta(days=7)  # 이번주 월요일 (미포함)

    # 주간 다이제스트 전환
    week_start_dt = timezone.datetime.combine(week_start, timezone.datetime.min.time())
    week_end_dt = timezone.datetime.combine(week_end, timezone.datetime.min.time())
    week_start_dt = timezone.make_aware(week_start_dt)
    week_end_dt = timezone.make_aware(week_end_dt)

    # 활성 사용자 중 메일링 설정이 있는 사용자들
    users = User.objects.filter(
        is_active=True,
        mailing_preference__enabled=True,
        mailing_preference__frequency='WEEKLY'
    ).select_related('mailing_preference')

    sent_count = 0
    for user in users:
        try:
            # 사용자별 콘텐츠 가져오기
            contents_by_category = get_weekly_contents_for_user(user, week_start_dt, week_end_dt)

            # 콘텐츠가 있을 때만 이메일 발송
            if contents_by_category:
                send_weekly_digest(user, week_start_dt, week_end_dt, contents_by_category)
                sent_count += 1
        except Exception as e:
            # 개별 사용자 발송 실패 시 로그만 남기고 계속 진행
            print(f"Failed to send weekly digest to {user.email}: {str(e)}")
            continue

    return f"Weekly digest sent to {sent_count} users"


@shared_task
def send_monthly_digest_emails():
    """
    모든 활성 사용자에게 월간 다이제스트 이메일 발송
    매월 1일 오전 9시에 실행되도록 스케줄링
    """
    # 지난 달의 시작과 끝 계산
    today = timezone.now().date()
    # 이번 달 1일
    month_start = today.replace(day=1)
    # 지난 달 1일
    if month_start.month == 1:
        last_month_start = month_start.replace(year=month_start.year - 1, month=12)
    else:
        last_month_start = month_start.replace(month=month_start.month - 1)

    # datetime으로 변환
    month_start_dt = timezone.datetime.combine(month_start, timezone.datetime.min.time())
    last_month_start_dt = timezone.datetime.combine(last_month_start, timezone.datetime.min.time())
    month_start_dt = timezone.make_aware(month_start_dt)
    last_month_start_dt = timezone.make_aware(last_month_start_dt)

    # 활성 사용자 중 메일링 설정이 있는 사용자들
    users = User.objects.filter(
        is_active=True,
        mailing_preference__enabled=True,
        mailing_preference__frequency='MONTHLY'
    ).select_related('mailing_preference')

    sent_count = 0
    for user in users:
        try:
            # 사용자별 콘텐츠 가져오기 (주간 다이제스트 함수 재사용)
            contents_by_category = get_weekly_contents_for_user(user, last_month_start_dt, month_start_dt)

            # 콘텐츠가 있을 때만 이메일 발송
            if contents_by_category:
                send_weekly_digest(user, last_month_start_dt, month_start_dt, contents_by_category)
                sent_count += 1
        except Exception as e:
            # 개별 사용자 발송 실패 시 로그만 남기고 계속 진행
            print(f"Failed to send monthly digest to {user.email}: {str(e)}")
            continue

    return f"Monthly digest sent to {sent_count} users"


@shared_task
def send_immediate_notification(user_id, content_id):
    """
    새 콘텐츠 발행 시 즉시 알림 발송

    Args:
        user_id: User ID
        content_id: Content ID
    """
    from apps.contents.models import Content
    from .email_utils import send_immediate_content_notification

    try:
        user = User.objects.get(id=user_id)
        content = Content.objects.get(id=content_id)
        send_immediate_content_notification(user, content)
        return f"Immediate notification sent to {user.email}"
    except (User.DoesNotExist, Content.DoesNotExist) as e:
        return f"Error: {str(e)}"
