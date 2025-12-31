from django.db import models
from django.conf import settings


class Board(models.Model):
    """게시판 타입"""

    class BoardType(models.TextChoices):
        NOTICE = 'NOTICE', '공지사항'
        REQUEST = 'REQUEST', '콘텐츠 개발 요청'
        QNA = 'QNA', '질의응답'

    name = models.CharField(
        max_length=100,
        verbose_name='게시판명'
    )

    board_type = models.CharField(
        max_length=20,
        choices=BoardType.choices,
        unique=True,
        verbose_name='게시판 타입'
    )

    description = models.TextField(
        blank=True,
        verbose_name='설명'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='활성화 여부'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일'
    )

    class Meta:
        db_table = 'boards'
        verbose_name = '게시판'
        verbose_name_plural = '게시판 목록'

    def __str__(self):
        return self.name


class Post(models.Model):
    """게시글"""

    class Status(models.TextChoices):
        PENDING = 'PENDING', '대기'
        IN_PROGRESS = 'IN_PROGRESS', '진행중'
        COMPLETED = 'COMPLETED', '완료'
        REJECTED = 'REJECTED', '반려'
        PUBLISHED = 'PUBLISHED', '공개'

    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='게시판'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='작성자'
    )

    title = models.CharField(
        max_length=200,
        verbose_name='제목'
    )

    content = models.TextField(
        verbose_name='내용'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PUBLISHED,
        verbose_name='상태'
    )

    is_pinned = models.BooleanField(
        default=False,
        verbose_name='상단 고정'
    )

    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name='조회수'
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name='삭제 여부'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성일'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )

    class Meta:
        db_table = 'posts'
        verbose_name = '게시글'
        verbose_name_plural = '게시글 목록'
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['board', '-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return self.title


class PostReply(models.Model):
    """게시글 답글 (관리자 전용)"""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='admin_replies',
        verbose_name='게시글'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_replies',
        verbose_name='작성자'
    )

    content = models.TextField(
        verbose_name='답글 내용'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='작성일'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )

    class Meta:
        db_table = 'post_replies'
        verbose_name = '게시글 답글'
        verbose_name_plural = '게시글 답글 목록'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.post.title} - 답글"
