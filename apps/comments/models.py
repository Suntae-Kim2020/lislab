from django.db import models
from django.conf import settings


class Comment(models.Model):
    """콘텐츠 댓글"""

    content = models.ForeignKey(
        'contents.Content',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='콘텐츠'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='작성자'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='상위 댓글'
    )

    text = models.TextField(
        verbose_name='내용'
    )

    url_link = models.URLField(
        blank=True,
        verbose_name='URL 링크'
    )

    is_admin_reply = models.BooleanField(
        default=False,
        verbose_name='관리자 답글 여부'
    )

    is_hidden = models.BooleanField(
        default=False,
        verbose_name='숨김 여부'
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
        db_table = 'comments'
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ['-created_at']  # 최신 댓글 상단
        indexes = [
            models.Index(fields=['content', '-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return f"{self.author.username} - {self.text[:50]}"

    @property
    def replies_count(self):
        """답글 개수"""
        return self.replies.filter(is_deleted=False, is_hidden=False).count()
