from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    """콘텐츠 카테고리"""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='카테고리명'
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL Slug'
    )

    description = models.TextField(
        blank=True,
        verbose_name='설명'
    )

    order = models.IntegerField(
        default=0,
        verbose_name='정렬 순서'
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
        db_table = 'categories'
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리 목록'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """콘텐츠 태그"""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='태그명'
    )

    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='URL Slug'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일'
    )

    class Meta:
        db_table = 'tags'
        verbose_name = '태그'
        verbose_name_plural = '태그 목록'
        ordering = ['name']

    def __str__(self):
        return self.name


class Content(models.Model):
    """교육 콘텐츠 (교육 웹페이지)"""

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', '임시저장'
        PUBLISHED = 'PUBLISHED', '공개'
        PRIVATE = 'PRIVATE', '비공개'
        ARCHIVED = 'ARCHIVED', '보관'

    title = models.CharField(
        max_length=200,
        verbose_name='제목'
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL Slug'
    )

    summary = models.TextField(
        max_length=500,
        verbose_name='요약'
    )

    content_html = models.TextField(
        verbose_name='콘텐츠 HTML'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='contents',
        verbose_name='카테고리'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='contents',
        verbose_name='태그'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='contents',
        verbose_name='작성자'
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='공개 상태'
    )

    version = models.CharField(
        max_length=20,
        default='1.0',
        verbose_name='버전'
    )

    thumbnail = models.ImageField(
        upload_to='contents/thumbnails/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='썸네일'
    )

    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name='조회수'
    )

    estimated_time = models.PositiveIntegerField(
        default=0,
        help_text='예상 학습 시간 (분)',
        verbose_name='예상 소요 시간'
    )

    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('BEGINNER', '초급'),
            ('INTERMEDIATE', '중급'),
            ('ADVANCED', '고급'),
        ],
        default='BEGINNER',
        verbose_name='난이도'
    )

    prerequisites = models.TextField(
        blank=True,
        verbose_name='선수 학습'
    )

    learning_objectives = models.TextField(
        blank=True,
        verbose_name='학습 목표'
    )

    # SEO
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name='메타 설명'
    )

    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='메타 키워드'
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='수정일'
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='최초 공개일'
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name='삭제 여부'
    )

    class Meta:
        db_table = 'contents'
        verbose_name = '콘텐츠'
        verbose_name_plural = '콘텐츠 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class ContentVersion(models.Model):
    """콘텐츠 버전 관리"""

    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='versions',
        verbose_name='콘텐츠'
    )

    version = models.CharField(
        max_length=20,
        verbose_name='버전'
    )

    content_html = models.TextField(
        verbose_name='콘텐츠 HTML'
    )

    change_log = models.TextField(
        verbose_name='변경 내역'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='content_versions',
        verbose_name='수정자'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일'
    )

    class Meta:
        db_table = 'content_versions'
        verbose_name = '콘텐츠 버전'
        verbose_name_plural = '콘텐츠 버전 목록'
        ordering = ['-created_at']
        unique_together = ['content', 'version']

    def __str__(self):
        return f"{self.content.title} v{self.version}"


class Favorite(models.Model):
    """즐겨찾기"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='사용자'
    )

    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='콘텐츠'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='등록일'
    )

    class Meta:
        db_table = 'favorites'
        verbose_name = '즐겨찾기'
        verbose_name_plural = '즐겨찾기 목록'
        ordering = ['-created_at']
        unique_together = ['user', 'content']

    def __str__(self):
        return f"{self.user.username} - {self.content.title}"
