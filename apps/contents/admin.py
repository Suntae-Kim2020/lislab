from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Category, Tag, Content, ContentVersion, Favorite


# Content Form with CKEditor
class ContentAdminForm(forms.ModelForm):
    content_html = forms.CharField(widget=CKEditorWidget(config_name='content'))

    class Meta:
        model = Content
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class ContentVersionInline(admin.TabularInline):
    model = ContentVersion
    extra = 0
    readonly_fields = ['created_at', 'created_by']
    can_delete = False


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    form = ContentAdminForm
    list_display = ['title', 'category', 'author', 'status_badge', 'difficulty_badge', 'version', 'view_count', 'created_at']
    list_filter = ['status', 'category', 'difficulty', 'created_at']
    search_fields = ['title', 'summary', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'published_at', 'content_preview']
    inlines = [ContentVersionInline]
    actions = ['make_published', 'make_draft']

    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'slug', 'summary', 'content_html', 'thumbnail', 'content_preview')
        }),
        ('분류', {
            'fields': ('category', 'tags', 'difficulty')
        }),
        ('메타 정보', {
            'fields': ('author', 'status', 'version', 'estimated_time')
        }),
        ('학습 정보', {
            'fields': ('prerequisites', 'learning_objectives')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('통계', {
            'fields': ('view_count', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        """상태를 색상 배지로 표시"""
        colors = {
            'DRAFT': '#ffc107',
            'PUBLISHED': '#28a745',
            'ARCHIVED': '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = '상태'

    def difficulty_badge(self, obj):
        """난이도를 색상 배지로 표시"""
        colors = {
            'BEGINNER': '#28a745',
            'INTERMEDIATE': '#ffc107',
            'ADVANCED': '#dc3545',
        }
        color = colors.get(obj.difficulty, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_difficulty_display()
        )
    difficulty_badge.short_description = '난이도'

    def content_preview(self, obj):
        """콘텐츠 HTML 미리보기"""
        if obj.content_html:
            return mark_safe(f'<div style="border: 1px solid #ddd; padding: 15px; max-height: 400px; overflow-y: auto;">{obj.content_html[:1000]}...</div>')
        return '-'
    content_preview.short_description = '콘텐츠 미리보기'

    def make_published(self, request, queryset):
        """선택된 콘텐츠를 발행 상태로 변경"""
        from django.utils import timezone
        updated = 0
        for content in queryset:
            if content.status != 'PUBLISHED':
                content.status = 'PUBLISHED'
                if not content.published_at:
                    content.published_at = timezone.now()
                content.save()
                updated += 1
        self.message_user(request, f'{updated}개의 콘텐츠가 발행되었습니다.')
    make_published.short_description = '선택된 콘텐츠 발행'

    def make_draft(self, request, queryset):
        """선택된 콘텐츠를 초안 상태로 변경"""
        updated = queryset.update(status='DRAFT')
        self.message_user(request, f'{updated}개의 콘텐츠가 초안으로 변경되었습니다.')
    make_draft.short_description = '선택된 콘텐츠를 초안으로 변경'

    def save_model(self, request, obj, form, change):
        """콘텐츠 저장 시 작성자 및 발행일 자동 설정"""
        from django.utils import timezone

        if not change:  # 새로 생성하는 경우
            obj.author = request.user

        # PUBLISHED 상태인데 published_at이 없으면 현재 시간으로 설정
        if obj.status == 'PUBLISHED' and not obj.published_at:
            obj.published_at = timezone.now()

        super().save_model(request, obj, form, change)


@admin.register(ContentVersion)
class ContentVersionAdmin(admin.ModelAdmin):
    list_display = ['content', 'version', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content__title', 'change_log']
    readonly_fields = ['created_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'content__title']
    readonly_fields = ['created_at']
