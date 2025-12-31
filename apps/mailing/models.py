from django.db import models
from django.conf import settings
import uuid


class MailingList(models.Model):
    """메일링 리스트 구독자"""

    email = models.EmailField(
        unique=True,
        verbose_name='이메일'
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mailing_subscription',
        verbose_name='연결된 사용자'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='구독 활성화'
    )

    unsubscribe_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='구독 해지 토큰'
    )

    subscribed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='구독일'
    )

    unsubscribed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='구독 해지일'
    )

    class Meta:
        db_table = 'mailing_list'
        verbose_name = '메일링 구독자'
        verbose_name_plural = '메일링 구독자 목록'
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class EmailCampaign(models.Model):
    """이메일 캠페인"""

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', '임시저장'
        SCHEDULED = 'SCHEDULED', '발송 예정'
        SENDING = 'SENDING', '발송 중'
        SENT = 'SENT', '발송 완료'
        FAILED = 'FAILED', '발송 실패'

    title = models.CharField(
        max_length=200,
        verbose_name='캠페인명'
    )

    subject = models.CharField(
        max_length=200,
        verbose_name='메일 제목'
    )

    content_html = models.TextField(
        verbose_name='메일 내용 (HTML)'
    )

    content_text = models.TextField(
        blank=True,
        verbose_name='메일 내용 (텍스트)'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='email_campaigns',
        verbose_name='생성자'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='상태'
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='발송 예정일'
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='발송 완료일'
    )

    total_recipients = models.PositiveIntegerField(
        default=0,
        verbose_name='총 수신자 수'
    )

    sent_count = models.PositiveIntegerField(
        default=0,
        verbose_name='발송 성공 수'
    )

    failed_count = models.PositiveIntegerField(
        default=0,
        verbose_name='발송 실패 수'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )

    class Meta:
        db_table = 'email_campaigns'
        verbose_name = '이메일 캠페인'
        verbose_name_plural = '이메일 캠페인 목록'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class EmailLog(models.Model):
    """이메일 발송 로그"""

    class Status(models.TextChoices):
        PENDING = 'PENDING', '대기'
        SENT = 'SENT', '발송 완료'
        FAILED = 'FAILED', '발송 실패'
        BOUNCED = 'BOUNCED', '반송됨'

    campaign = models.ForeignKey(
        EmailCampaign,
        on_delete=models.CASCADE,
        related_name='logs',
        verbose_name='캠페인'
    )

    recipient = models.EmailField(
        verbose_name='수신자'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='상태'
    )

    error_message = models.TextField(
        blank=True,
        verbose_name='오류 메시지'
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='발송일'
    )

    opened_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='열람일'
    )

    clicked_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='클릭일'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일'
    )

    class Meta:
        db_table = 'email_logs'
        verbose_name = '이메일 발송 로그'
        verbose_name_plural = '이메일 발송 로그 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['campaign', 'status']),
            models.Index(fields=['recipient']),
        ]

    def __str__(self):
        return f"{self.campaign.title} - {self.recipient}"
