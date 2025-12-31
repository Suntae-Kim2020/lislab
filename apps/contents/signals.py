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
    # 새로 생성되었고, 발행 상태인 경우에만
    if instance.status == 'PUBLISHED':
        from apps.accounts.models import User
        from apps.accounts.email_utils import send_immediate_content_notification

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
                    # Celery를 사용할 수 있으면 비동기로, 아니면 동기로 발송
                    try:
                        from apps.accounts.tasks import send_immediate_notification
                        send_immediate_notification.delay(user.id, instance.id)
                        print(f"[Signal] 비동기 알림 발송 예약: {user.username} <- {instance.title}")
                    except Exception as celery_error:
                        # Celery/Redis가 없으면 동기적으로 발송
                        print(f"[Signal] Celery 사용 불가, 동기 발송: {celery_error}")
                        send_immediate_content_notification(user, instance)
                        print(f"[Signal] 동기 알림 발송 완료: {user.username} <- {instance.title}")

            except Exception as e:
                print(f"[Signal] 알림 발송 실패 ({user.username}): {e}")
                continue
