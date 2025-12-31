from django.contrib import admin
from .models import Category, Tag, Content, ContentVersion, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'parent']
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
    list_display = ['title', 'category', 'author', 'status', 'version', 'view_count', 'created_at']
    list_filter = ['status', 'category', 'difficulty', 'created_at']
    search_fields = ['title', 'summary', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['view_count', 'created_at', 'updated_at', 'published_at']
    inlines = [ContentVersionInline]

    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'slug', 'summary', 'content_html', 'thumbnail')
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
