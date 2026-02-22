from django.core.management.base import BaseCommand
from apps.contents.models import Category, Tag


class Command(BaseCommand):
    help = 'slug 자동 생성 테스트'

    def handle(self, *args, **options):
        # 카테고리 테스트
        cat = Category(name='슬러그테스트카테고리', order=99)
        cat.save()
        self.stdout.write(f'카테고리: name={cat.name}, slug={cat.slug}')

        # 태그 테스트
        tag = Tag(name='슬러그테스트태그')
        tag.save()
        self.stdout.write(f'태그: name={tag.name}, slug={tag.slug}')

        # 정리
        cat.delete()
        tag.delete()
        self.stdout.write('테스트 데이터 삭제 완료')
