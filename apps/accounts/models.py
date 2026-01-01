from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    사용자 모델 (확장)

    역할:
    - GUEST: 비회원 (로그인 없이 열람만)
    - USER: 일반 회원 (학생/교수/취업준비생)
    - ADMIN: 관리자
    """

    class Role(models.TextChoices):
        GUEST = 'GUEST', '비회원'
        USER = 'USER', '일반회원'
        ADMIN = 'ADMIN', '관리자'

    class UserType(models.TextChoices):
        STUDENT = 'STUDENT', '학생'
        PROFESSOR = 'PROFESSOR', '교수/연구자'
        JOB_SEEKER = 'JOB_SEEKER', '취업준비생'
        OTHER = 'OTHER', '기타'

    class SocialProvider(models.TextChoices):
        NONE = 'NONE', '일반 회원가입'
        KAKAO = 'KAKAO', '카카오'
        GOOGLE = 'GOOGLE', '구글'
        NAVER = 'NAVER', '네이버'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='역할'
    )

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.STUDENT,
        verbose_name='사용자 구분'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='연락처'
    )

    organization = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='소속기관'
    )

    bio = models.TextField(
        blank=True,
        verbose_name='자기소개'
    )

    profile_image = models.ImageField(
        upload_to='profiles/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='프로필 이미지'
    )

    is_email_verified = models.BooleanField(
        default=False,
        verbose_name='이메일 인증 여부'
    )

    # 소셜 로그인 관련 필드
    social_provider = models.CharField(
        max_length=10,
        choices=SocialProvider.choices,
        default=SocialProvider.NONE,
        verbose_name='소셜 로그인 제공자'
    )

    social_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='소셜 로그인 ID'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='가입일'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['social_provider', 'social_id'],
                condition=~models.Q(social_provider='NONE'),
                name='unique_social_account'
            )
        ]

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_admin(self):
        """관리자 권한 체크"""
        return self.role == self.Role.ADMIN or self.is_staff or self.is_superuser

    @property
    def can_manage_content(self):
        """콘텐츠 관리 권한"""
        return self.is_admin

    @property
    def can_comment(self):
        """댓글 작성 권한"""
        return self.is_authenticated and self.role != self.Role.GUEST

    @property
    def is_social_user(self):
        """소셜 로그인 사용자 여부"""
        return self.social_provider != self.SocialProvider.NONE


class PasswordResetToken(models.Model):
    """비밀번호 재설정 토큰"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reset_tokens',
        verbose_name='사용자'
    )

    token = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='토큰'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일'
    )

    expires_at = models.DateTimeField(
        verbose_name='만료일'
    )

    is_used = models.BooleanField(
        default=False,
        verbose_name='사용 여부'
    )

    class Meta:
        db_table = 'password_reset_tokens'
        verbose_name = '비밀번호 재설정 토큰'
        verbose_name_plural = '비밀번호 재설정 토큰 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.token[:10]}..."


class MailingPreference(models.Model):
    """메일링 설정"""

    class Frequency(models.TextChoices):
        IMMEDIATE = 'IMMEDIATE', '즉시'
        WEEKLY = 'WEEKLY', '주간'
        MONTHLY = 'MONTHLY', '월간'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='mailing_preference',
        verbose_name='사용자'
    )

    enabled = models.BooleanField(
        default=False,
        verbose_name='메일링 활성화'
    )

    frequency = models.CharField(
        max_length=10,
        choices=Frequency.choices,
        default=Frequency.WEEKLY,
        verbose_name='발송 빈도'
    )

    all_categories = models.BooleanField(
        default=False,
        verbose_name='전체 카테고리 구독'
    )

    selected_categories = models.ManyToManyField(
        'contents.Category',
        blank=True,
        related_name='mailing_subscribers',
        verbose_name='구독 카테고리'
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
        db_table = 'mailing_preferences'
        verbose_name = '메일링 설정'
        verbose_name_plural = '메일링 설정 목록'
        ordering = ['-created_at']

    def __str__(self):
        status = '활성화' if self.enabled else '비활성화'
        return f"{self.user.username} - {status} ({self.get_frequency_display()})"
