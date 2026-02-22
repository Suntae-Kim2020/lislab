import logging
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, PasswordResetToken, TeamMember

logger = logging.getLogger(__name__)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'full_name', 'email', 'user_type', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'user_type', 'is_active', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'organization']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('개인정보', {'fields': ('first_name', 'last_name', 'email')}),
        ('추가 정보', {
            'fields': ('role', 'user_type', 'phone', 'organization', 'bio', 'profile_image', 'is_email_verified')
        }),
        ('작성자 권한', {
            'fields': ('groups', 'assigned_categories_display'),
            'description': '"작성자" 그룹을 추가하면 스태프 권한과 사용자 권한이 자동 설정됩니다. 담당 카테고리는 카테고리 관리에서 배정합니다.'
        }),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('중요한 일정', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ['assigned_categories_display']

    def save_model(self, request, obj, form, change):
        """그룹 지정 시 is_staff 자동 설정 (save_related 전에 처리)"""
        if not obj.is_superuser and obj.role != 'ADMIN':
            writer_group = Group.objects.filter(name='작성자').first()
            if writer_group:
                # form.cleaned_data['groups']에서 저장 전 그룹 확인
                new_groups = form.cleaned_data.get('groups', [])
                is_writer = writer_group in new_groups
                obj.is_staff = is_writer
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """그룹 저장 후 user_permissions 자동 설정"""
        user = form.instance
        logger.warning(f'[save_related] 시작: user={user.username}, superuser={user.is_superuser}, role={user.role}')

        # 먼저 super로 m2m 저장 (groups, user_permissions 등)
        super().save_related(request, form, formsets, change)

        if user.is_superuser or user.role == 'ADMIN':
            logger.warning(f'[save_related] 관리자/슈퍼유저 → 스킵')
            return

        writer_group = Group.objects.filter(name='작성자').first()
        if not writer_group:
            logger.warning(f'[save_related] 작성자 그룹 없음 → 스킵')
            return

        is_writer = user.groups.filter(pk=writer_group.pk).exists()
        group_perms = list(writer_group.permissions.all())
        logger.warning(f'[save_related] is_writer={is_writer}, group_perms count={len(group_perms)}')

        if is_writer:
            user.user_permissions.add(*group_perms)
            final_count = user.user_permissions.count()
            logger.warning(f'[save_related] 권한 추가 완료: {final_count}개')
        else:
            user.user_permissions.remove(*group_perms)
            final_count = user.user_permissions.count()
            logger.warning(f'[save_related] 권한 제거 완료: {final_count}개')

    @admin.display(description='담당 카테고리')
    def assigned_categories_display(self, obj):
        cats = obj.assigned_categories.all()
        if not cats:
            return '-'
        return ', '.join(cat.name for cat in cats)

    @admin.display(description='이름')
    def full_name(self, obj):
        name = f'{obj.last_name}{obj.first_name}'.strip()
        return name or '-'

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': ('role', 'user_type', 'email', 'phone', 'organization')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'title']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__username', 'user__email', 'token']
    readonly_fields = ['created_at']
