from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Check mailing preference users'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("=== 메일링 설정 확인 ===\n"))

        # 모든 활성 사용자
        active_users = User.objects.filter(is_active=True)
        self.stdout.write(f"활성 사용자 수: {active_users.count()}")

        # 메일링 설정이 있는 사용자
        users_with_pref = User.objects.filter(
            is_active=True,
            mailing_preference__isnull=False
        ).select_related('mailing_preference')
        self.stdout.write(f"메일링 설정이 있는 사용자: {users_with_pref.count()}\n")

        for user in users_with_pref:
            pref = user.mailing_preference
            self.stdout.write(f"\n사용자: {user.username} ({user.email})")
            self.stdout.write(f"  - 활성화: {pref.enabled}")
            self.stdout.write(f"  - 빈도: {pref.frequency}")
            self.stdout.write(f"  - 전체 카테고리: {pref.all_categories}")

            if not pref.all_categories:
                categories = pref.selected_categories.all()
                cat_names = [cat.name for cat in categories]
                self.stdout.write(f"  - 선택된 카테고리: {', '.join(cat_names) if cat_names else '없음'}")

        # 즉시 알림 설정 사용자
        immediate_users = User.objects.filter(
            is_active=True,
            mailing_preference__enabled=True,
            mailing_preference__frequency='IMMEDIATE'
        ).select_related('mailing_preference')

        self.stdout.write(f"\n\n즉시 알림 설정 사용자: {immediate_users.count()}")

        if immediate_users.count() > 0:
            self.stdout.write("\n=== 데이터 모델 카테고리 확인 ===")
            from apps.contents.models import Category
            data_model = Category.objects.filter(name="데이터 모델").first()

            if data_model:
                self.stdout.write(f"데이터 모델 카테고리 ID: {data_model.id}")

                for user in immediate_users:
                    pref = user.mailing_preference

                    if pref.all_categories:
                        self.stdout.write(f"✓ {user.username}: 전체 카테고리 구독")
                    else:
                        selected_ids = list(pref.selected_categories.values_list('id', flat=True))
                        if data_model.id in selected_ids:
                            self.stdout.write(f"✓ {user.username}: 데이터 모델 구독 중")
                        else:
                            self.stdout.write(f"✗ {user.username}: 데이터 모델 미구독 (구독 중: {selected_ids})")
