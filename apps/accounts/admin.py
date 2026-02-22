import json
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, PasswordResetToken, TeamMember


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

    class Media:
        js = ('accounts/js/sync_group_perms.js',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """그룹별 권한 데이터를 페이지에 임베드"""
        response = super().change_view(request, object_id, form_url, extra_context)
        if hasattr(response, 'render'):
            group_perms_map = {}
            for group in Group.objects.prefetch_related('permissions__content_type').all():
                group_perms_map[str(group.pk)] = [
                    {'id': p.pk, 'name': str(p)}
                    for p in group.permissions.all()
                ]
            script = '<script>window.GROUP_PERMS_MAP = %s;</script>' % json.dumps(group_perms_map, ensure_ascii=False)

            original_render = response.render
            def patched_render():
                result = original_render()
                content = result.content.decode('utf-8')
                content = content.replace('</body>', script + '</body>')
                result.content = content.encode('utf-8')
                return result
            response.render = patched_render
        return response

    def save_model(self, request, obj, form, change):
        """그룹 지정 시 is_staff 자동 설정"""
        if not obj.is_superuser and obj.role != 'ADMIN':
            writer_group = Group.objects.filter(name='작성자').first()
            if writer_group:
                new_groups = form.cleaned_data.get('groups', [])
                is_writer = writer_group in new_groups
                obj.is_staff = is_writer
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """그룹 저장 후 user_permissions 자동 설정"""
        super().save_related(request, form, formsets, change)

        user = form.instance
        if user.is_superuser or user.role == 'ADMIN':
            return

        writer_group = Group.objects.filter(name='작성자').first()
        if not writer_group:
            return

        is_writer = user.groups.filter(pk=writer_group.pk).exists()
        group_perms = list(writer_group.permissions.all())

        if is_writer:
            user.user_permissions.add(*group_perms)
        else:
            user.user_permissions.remove(*group_perms)

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
