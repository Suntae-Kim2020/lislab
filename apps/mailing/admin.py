from django.contrib import admin
from .models import MailingList, EmailCampaign, EmailLog


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ['email', 'user', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'user__username']
    readonly_fields = ['unsubscribe_token', 'subscribed_at', 'unsubscribed_at']


class EmailLogInline(admin.TabularInline):
    model = EmailLog
    extra = 0
    readonly_fields = ['recipient', 'status', 'sent_at', 'created_at']
    can_delete = False


@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'total_recipients', 'sent_count', 'failed_count', 'scheduled_at', 'sent_at']
    list_filter = ['status', 'created_at', 'scheduled_at']
    search_fields = ['title', 'subject']
    readonly_fields = ['total_recipients', 'sent_count', 'failed_count', 'created_at', 'updated_at', 'sent_at']
    inlines = [EmailLogInline]


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['campaign', 'recipient', 'status', 'sent_at', 'opened_at']
    list_filter = ['status', 'created_at', 'sent_at']
    search_fields = ['recipient', 'campaign__title']
    readonly_fields = ['created_at', 'sent_at', 'opened_at', 'clicked_at']
