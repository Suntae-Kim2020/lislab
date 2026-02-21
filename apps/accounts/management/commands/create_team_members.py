from django.core.management.base import BaseCommand
from apps.accounts.models import TeamMember


class Command(BaseCommand):
    help = '초기 팀 멤버 데이터를 생성합니다.'

    def handle(self, *args, **options):
        member, created = TeamMember.objects.get_or_create(
            name='김선태',
            defaults={
                'title': '교수',
                'bio': '전북대학교 문헌정보학과 교수. 문헌정보학을 순수하게 공부하는 학생들에게 더 나은 교육 환경을 제공하고자 LIS Lab을 설립하였습니다.',
                'order': 1,
                'is_active': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('김선태 교수 팀 멤버를 생성했습니다.'))
        else:
            self.stdout.write('김선태 교수 팀 멤버가 이미 존재합니다.')
