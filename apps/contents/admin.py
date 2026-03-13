from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from dal import autocomplete
from django import forms
from .models import Category, Tag, Content, ContentVersion, Favorite


# Content Form with CKEditor
class ContentAdminForm(forms.ModelForm):
    content_html = forms.CharField(widget=CKEditorWidget(config_name='content'))

    class Meta:
        model = Content
        fields = '__all__'
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='tag-autocomplete',
                attrs={
                    'data-placeholder': '태그를 입력하세요...',
                    'data-minimum-input-length': 1,
                },
            ),
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'order', 'is_active', 'show_in_menu', 'menu_order', 'created_at']
    list_filter = ['is_active', 'show_in_menu', 'parent']
    list_editable = ['order', 'is_active', 'show_in_menu', 'menu_order']
    search_fields = ['name', 'description']
    exclude = ['slug']
    filter_horizontal = ['assigned_writers']
    ordering = ['order', 'name']

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'parent', 'order', 'is_active')
        }),
        ('메뉴 설정', {
            'fields': ('show_in_menu', 'menu_order', 'menu_name', 'url', 'open_in_new_tab'),
            'description': '메뉴에 노출을 체크하면 메인 화면 상단 메뉴에 표시됩니다. 커스텀 URL을 설정하면 네비게이션 전용 항목이 됩니다.'
        }),
        ('담당 작성자', {
            'fields': ('assigned_writers',),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_admin:
            return qs
        if request.user.is_writer:
            assigned = request.user.assigned_categories.all()
            assigned_ids = set(assigned.values_list('id', flat=True))
            descendant_ids = set()
            for cat in assigned:
                for desc in cat.get_descendants():
                    descendant_ids.add(desc.id)
            return qs.filter(id__in=assigned_ids | descendant_ids)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            if not (request.user.is_superuser or request.user.is_admin):
                if request.user.is_writer:
                    # 작성자는 담당 카테고리와 그 하위 카테고리만 선택 가능
                    assigned = request.user.assigned_categories.all()
                    allowed_ids = set(assigned.values_list('id', flat=True))
                    for cat in assigned:
                        for desc in cat.get_descendants():
                            allowed_ids.add(desc.id)
                    kwargs['queryset'] = Category.objects.filter(id__in=allowed_ids)
                    kwargs['required'] = True  # 작성자는 상위 카테고리 필수
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """작성자가 카테고리 생성 시 상위 카테고리 검증"""
        if not (request.user.is_superuser or request.user.is_admin):
            if request.user.is_writer and not change:  # 새로 생성하는 경우
                if not obj.parent:
                    from django.contrib import messages
                    messages.error(request, '상위 카테고리를 선택해야 합니다.')
                    return
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_admin:
            return True
        if obj and request.user.is_writer:
            # 작성자는 담당 카테고리와 그 하위 카테고리 수정 가능
            assigned = request.user.assigned_categories.all()
            allowed_ids = set(assigned.values_list('id', flat=True))
            for cat in assigned:
                for desc in cat.get_descendants():
                    allowed_ids.add(desc.id)
            return obj.id in allowed_ids
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.is_admin:
            return True
        # 그룹 권한 체크 (Django 기본 권한 시스템 사용)
        return super().has_delete_permission(request, obj)

    def get_fieldsets(self, request, obj=None):
        if not (request.user.is_superuser or request.user.is_admin):
            return (
                (None, {
                    'fields': ('name', 'description', 'parent', 'order', 'is_active')
                }),
            )
        return super().get_fieldsets(request, obj)

    def get_exclude(self, request, obj=None):
        if not (request.user.is_superuser or request.user.is_admin):
            return ['assigned_writers']
        return super().get_exclude(request, obj) or []


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    exclude = ['slug']


class ContentVersionInline(admin.TabularInline):
    model = ContentVersion
    extra = 0
    readonly_fields = ['created_at', 'created_by']
    can_delete = False


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    form = ContentAdminForm
    list_display = ['title', 'category_name', 'order', 'author', 'status_badge', 'difficulty_badge', 'version', 'view_count', 'created_at']
    list_editable = ['order']
    list_filter = ['status', 'category', 'difficulty', 'created_at']
    search_fields = ['title', 'summary', 'author__username']
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'published_at']
    inlines = [ContentVersionInline]
    actions = ['make_published', 'make_draft']

    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'summary', 'content_html')
        }),
        ('분류', {
            'fields': ('category', 'tags', 'difficulty', 'order')
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

    @admin.display(description='카테고리', ordering='category__parent__name')
    def category_name(self, obj):
        """카테고리 이름 표시 (상위 카테고리 포함, 상위 카테고리 기준 정렬)"""
        if not obj.category:
            return '-'
        if obj.category.parent:
            return f"{obj.category.parent.name} > {obj.category.name}"
        return obj.category.name

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
            # HTML 태그를 제거하고 텍스트만 표시 (태그가 잘려서 페이지가 깨지는 것을 방지)
            import re
            text_only = re.sub(r'<[^>]+>', '', obj.content_html)
            preview_text = text_only[:500]
            return format_html('<div style="border: 1px solid #ddd; padding: 15px; max-height: 200px; overflow-y: auto; white-space: pre-wrap;">{}</div>', preview_text + '...' if len(text_only) > 500 else preview_text)
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

    def get_queryset(self, request):
        """작성자는 본인 콘텐츠만 목록에 표시"""
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_admin:
            return qs
        if request.user.is_writer:
            return qs.filter(author=request.user)
        return qs

    def get_fieldsets(self, request, obj=None):
        """작성자에게는 author 필드를 숨김 (자동 설정됨)"""
        fieldsets = super().get_fieldsets(request, obj)
        if not (request.user.is_superuser or request.user.is_admin):
            fieldsets = [
                (name, {**opts, 'fields': tuple(f for f in opts['fields'] if f != 'author')})
                for name, opts in fieldsets
            ]
        return fieldsets

    def get_actions(self, request):
        """작성자는 발행/초안 변경 액션 사용 불가"""
        actions = super().get_actions(request)
        if not (request.user.is_superuser or request.user.is_admin):
            actions.pop('make_published', None)
            actions.pop('make_draft', None)
        return actions

    def has_delete_permission(self, request, obj=None):
        """Django 그룹 권한 시스템 사용"""
        if request.user.is_superuser or request.user.is_admin:
            return True
        # 그룹 권한 체크 (Django 기본 권한 시스템 사용)
        return super().has_delete_permission(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            # 네비게이션 전용 카테고리(url 설정됨)는 콘텐츠 카테고리 선택에서 제외
            base_qs = Category.objects.filter(url='')
            if not (request.user.is_superuser or request.user.is_admin):
                if request.user.is_writer:
                    assigned = request.user.assigned_categories.all()
                    allowed_ids = set(assigned.values_list('id', flat=True))
                    for cat in assigned:
                        for desc in cat.get_descendants():
                            allowed_ids.add(desc.id)
                    base_qs = base_qs.filter(id__in=allowed_ids)
            kwargs['queryset'] = base_qs
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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
