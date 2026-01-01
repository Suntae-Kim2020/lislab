from django.core.management.base import BaseCommand
from apps.accounts.models import User


class Command(BaseCommand):
    help = 'Delete all Kakao social login users'

    def handle(self, *args, **options):
        kakao_users = User.objects.filter(social_provider='KAKAO')
        count = kakao_users.count()
        usernames = list(kakao_users.values_list('username', flat=True))

        if count == 0:
            self.stdout.write(self.style.WARNING('No Kakao users found'))
            return

        kakao_users.delete()

        self.stdout.write(self.style.SUCCESS(f'✓ Deleted {count} Kakao users:'))
        for username in usernames:
            self.stdout.write(f'  - {username}')
