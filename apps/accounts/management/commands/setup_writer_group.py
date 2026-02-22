from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = '"작성자" 그룹을 생성하고 콘텐츠 관련 권한을 부여합니다.'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='작성자')

        if created:
            self.stdout.write(self.style.SUCCESS('"작성자" 그룹을 생성했습니다.'))
        else:
            self.stdout.write('"작성자" 그룹이 이미 존재합니다. 권한을 업데이트합니다.')

        # 부여할 권한 목록: (app_label, model, codename)
        permission_specs = [
            # Content: 추가, 수정, 조회
            ('contents', 'content', 'add_content'),
            ('contents', 'content', 'change_content'),
            ('contents', 'content', 'view_content'),
            # Category: 조회, 추가 (하위 카테고리 생성 가능)
            ('contents', 'category', 'view_category'),
            ('contents', 'category', 'add_category'),
            ('contents', 'category', 'change_category'),
            # Tag: 조회, 추가
            ('contents', 'tag', 'view_tag'),
            ('contents', 'tag', 'add_tag'),
            # ContentVersion: 조회
            ('contents', 'contentversion', 'view_contentversion'),
        ]

        permissions = []
        for app_label, model, codename in permission_specs:
            try:
                ct = ContentType.objects.get(app_label=app_label, model=model)
                perm = Permission.objects.get(content_type=ct, codename=codename)
                permissions.append(perm)
            except (ContentType.DoesNotExist, Permission.DoesNotExist):
                self.stdout.write(self.style.WARNING(
                    f'  권한을 찾을 수 없음: {app_label}.{codename}'
                ))

        group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS(
            f'  {len(permissions)}개의 권한이 그룹에 부여되었습니다.'
        ))

        for perm in permissions:
            self.stdout.write(f'  - {perm.content_type.app_label}.{perm.codename}')

        # 기존 작성자 그룹 멤버들에게 user_permissions + is_staff 일괄 설정
        members = group.user_set.all()
        for user in members:
            user.user_permissions.add(*permissions)
            if not user.is_staff:
                user.is_staff = True
                user.save(update_fields=['is_staff'])
            self.stdout.write(f'  사용자 {user.username}: 권한 설정 완료')

        self.stdout.write(self.style.SUCCESS(
            f'  {members.count()}명의 기존 멤버에게 권한을 설정했습니다.'
        ))
