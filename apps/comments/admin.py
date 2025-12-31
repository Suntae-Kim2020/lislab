from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'author', 'text_preview', 'is_admin_reply', 'is_hidden', 'is_deleted', 'created_at']
    list_filter = ['is_admin_reply', 'is_hidden', 'is_deleted', 'created_at']
    search_fields = ['text', 'author__username', 'content__title']
    readonly_fields = ['created_at', 'updated_at']

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = '내용 미리보기'
