from django.db import models
from django.db.models.functions import Collate
from django.conf import settings
from django.utils.text import slugify
import uuid


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
        blank=True,
        allow_unicode=True,
        verbose_name='URL Slug',
        help_text='비워두면 카테고리명에서 자동 생성됩니다.'
    )

    description = models.TextField(
        blank=True,
        verbose_name='설명'
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='children',
        verbose_name='상위 카테고리'
    )

    assigned_writers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='assigned_categories',
        verbose_name='담당 작성자'
    )

    order = models.IntegerField(
        default=0,
        verbose_name='정렬 순서'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='활성화 여부'
    )

    # 메뉴 관련 필드
    show_in_menu = models.BooleanField(
        default=False,
        verbose_name='메뉴에 노출',
        help_text='체크하면 메인 화면 상단 메뉴에 표시됩니다.'
    )

    menu_order = models.IntegerField(
        default=0,
        verbose_name='메뉴 정렬 순서',
        help_text='메뉴에 노출 시 정렬 순서 (낮을수록 왼쪽)'
    )

    menu_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='메뉴 표시명',
        help_text='비워두면 카테고리명을 메뉴명으로 사용합니다.'
    )

    url = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='커스텀 URL',
        help_text='설정하면 콘텐츠 카테고리가 아닌 네비게이션 전용 링크가 됩니다.'
    )

    open_in_new_tab = models.BooleanField(
        default=False,
        verbose_name='새 탭에서 열기'
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

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True) or uuid.uuid4().hex[:8]
            slug = base
            n = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    def get_menu_name(self):
        """메뉴 표시명 반환"""
        return self.menu_name or self.name

    def get_menu_url(self):
        """메뉴 URL 반환: 커스텀 URL이 있으면 사용, 없으면 카테고리 URL 자동 생성"""
        if self.url:
            return self.url
        return f'/contents?category={self.slug}'

    def get_descendants(self):
        """모든 하위 카테고리를 재귀적으로 반환"""
        descendants = list(self.children.all())
        for child in list(descendants):
            descendants.extend(child.get_descendants())
        return descendants


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
        blank=True,
        allow_unicode=True,
        verbose_name='URL Slug',
        help_text='비워두면 태그명에서 자동 생성됩니다.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='생성일'
    )

    class Meta:
        db_table = 'tags'
        verbose_name = '태그'
        verbose_name_plural = '태그 목록'
        ordering = [Collate('name', 'C')]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True) or uuid.uuid4().hex[:8]
            slug = base
            n = 1
            while Tag.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

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
        blank=True,
        allow_unicode=True,
        verbose_name='URL Slug',
        help_text='비워두면 제목에서 자동 생성됩니다.'
    )

    summary = models.TextField(
        max_length=500,
        blank=True,
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

    order = models.IntegerField(
        default=0,
        verbose_name='정렬 순서',
        help_text='낮을수록 먼저 표시됩니다'
    )

    is_deleted = models.BooleanField(
        default=False,
        verbose_name='삭제 여부'
    )

    class Meta:
        db_table = 'contents'
        verbose_name = '콘텐츠'
        verbose_name_plural = '콘텐츠 목록'
        ordering = ['category', 'order', '-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title, allow_unicode=True) or uuid.uuid4().hex[:8]
            slug = base
            n = 1
            while Content.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
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
