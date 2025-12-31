from django.contrib import admin
from .models import Board, Post, PostReply


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'board_type', 'is_active', 'created_at']
    list_filter = ['board_type', 'is_active']
    search_fields = ['name', 'description']


class PostReplyInline(admin.TabularInline):
    model = PostReply
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'board', 'author', 'status', 'is_pinned', 'view_count', 'created_at']
    list_filter = ['board', 'status', 'is_pinned', 'is_deleted', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    inlines = [PostReplyInline]


@admin.register(PostReply)
class PostReplyAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['post__title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '내용 미리보기'
