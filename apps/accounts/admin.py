from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'user_type', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'organization']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': ('role', 'user_type', 'phone', 'organization', 'bio', 'profile_image', 'is_email_verified')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': ('role', 'user_type', 'email', 'phone', 'organization')
        }),
    )


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['created_at']
