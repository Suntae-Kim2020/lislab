"""
콘텐츠 관련 시그널
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Content


@receiver(post_save, sender=Content)
def send_immediate_notifications(sender, instance, created, **kwargs):
    """
    새 콘텐츠가 발행되면 즉시 알림 설정한 사용자들에게 이메일 발송
    """
    # 상태가 PUBLISHED로 변경되었는지 확인
    # 이미 발행된 콘텐츠를 수정하는 경우에는 이메일을 보내지 않음
    should_notify = False

    if created and instance.status == 'PUBLISHED':
        # 새로 생성되고 발행 상태인 경우
        should_notify = True
    elif not created and instance.status == 'PUBLISHED':
        # 기존 콘텐츠가 수정된 경우, published_at이 방금 설정되었는지 확인
        # (즉, DRAFT -> PUBLISHED로 변경된 경우)
        from django.utils import timezone
        from datetime import timedelta

        # published_at이 최근 10초 이내에 설정되었다면 새로 발행된 것으로 간주
        if instance.published_at:
            time_diff = timezone.now() - instance.published_at
            if time_diff < timedelta(seconds=10):
                should_notify = True

    if not should_notify:
        return

    print(f"[Signal] 콘텐츠 발행 감지: {instance.title}")

    from apps.accounts.models import User
    from apps.accounts.email_utils import send_immediate_content_notification
    from apps.accounts.kakao_message_utils import send_kakao_message_notification

    # 즉시 알림을 받도록 설정한 모든 활성 사용자
    users = User.objects.filter(
        is_active=True,
        mailing_preference__enabled=True,
        mailing_preference__frequency='IMMEDIATE'
    ).select_related('mailing_preference')

    for user in users:
        try:
            # 카테고리 확인
            pref = user.mailing_preference

            # 전체 카테고리 구독 또는 해당 카테고리 구독 확인
            if pref.all_categories:
                should_send = True
            else:
                selected_category_ids = list(pref.selected_categories.values_list('id', flat=True))
                should_send = instance.category_id in selected_category_ids

            if should_send:
                # 로컬 개발 환경에서는 동기적으로 발송 (Celery/Redis 불필요)
                # 이메일 발송
                send_immediate_content_notification(user, instance)
                print(f"[Signal] 이메일 발송 완료: {user.username} <- {instance.title}")

                # 카카오 메시지 발송 (카카오 로그인 사용자 + 알림 활성화된 경우)
                print(f"[Signal] 카카오 체크 - User: {user.username}, Provider: {user.social_provider}, Kakao enabled: {pref.kakao_notification_enabled}")
                if user.social_provider == User.SocialProvider.KAKAO and pref.kakao_notification_enabled:
                    print(f"[Signal] 카카오 메시지 발송 시도: {user.username}")
                    kakao_sent = send_kakao_message_notification(user, instance)
                    if kakao_sent:
                        print(f"[Signal] 카카오 메시지 발송 완료: {user.username} <- {instance.title}")
                    else:
                        print(f"[Signal] 카카오 메시지 발송 실패: {user.username}")

        except Exception as e:
            print(f"[Signal] 알림 발송 실패 ({user.username}): {e}")
            continue
