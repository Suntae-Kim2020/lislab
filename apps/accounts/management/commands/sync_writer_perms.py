from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.accounts.models import User


class Command(BaseCommand):
    help = '작성자 그룹 멤버들의 user_permissions와 is_staff를 동기화합니다.'

    def handle(self, *args, **options):
        writer_group = Group.objects.filter(name='작성자').first()
        if not writer_group:
            self.stdout.write(self.style.ERROR('작성자 그룹이 없습니다.'))
            return

        group_perms = list(writer_group.permissions.all())
        self.stdout.write(f'작성자 그룹 권한 수: {len(group_perms)}')
        for p in group_perms:
            self.stdout.write(f'  - {p.content_type.app_label}.{p.codename} (pk={p.pk})')

        members = writer_group.user_set.all()
        self.stdout.write(f'\n작성자 그룹 멤버 수: {members.count()}')

        for user in members:
            current_perms = list(user.user_permissions.all())
            self.stdout.write(f'\n사용자: {user.username} (pk={user.pk})')
            self.stdout.write(f'  is_staff: {user.is_staff}')
            self.stdout.write(f'  is_superuser: {user.is_superuser}')
            self.stdout.write(f'  role: {user.role}')
            self.stdout.write(f'  현재 user_permissions 수: {len(current_perms)}')

            # is_staff 설정
            if not user.is_staff and not user.is_superuser:
                user.is_staff = True
                user.save(update_fields=['is_staff'])
                self.stdout.write(self.style.SUCCESS(f'  -> is_staff = True 설정'))

            # user_permissions에 그룹 권한 추가
            user.user_permissions.add(*group_perms)
            after_perms = user.user_permissions.count()
            self.stdout.write(self.style.SUCCESS(f'  -> user_permissions 설정 완료 (현재: {after_perms}개)'))
