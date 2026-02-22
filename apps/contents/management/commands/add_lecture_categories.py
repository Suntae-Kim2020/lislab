from django.core.management.base import BaseCommand
from apps.contents.models import Category


class Command(BaseCommand):
    help = '특강A(베타), 특강B(베타) 카테고리 추가'

    def handle(self, *args, **options):
        cats = [
            {'name': '특강A(베타)', 'slug': 'special-lecture-a', 'order': 20},
            {'name': '특강B(베타)', 'slug': 'special-lecture-b', 'order': 21},
        ]
        for c in cats:
            obj, created = Category.objects.get_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'order': c['order'], 'is_active': True},
            )
            status = '생성됨' if created else '이미 존재'
            self.stdout.write(f"{obj.name} (slug={obj.slug}): {status}")
