"""
웹문서 카테고리의 콘텐츠 확인
"""
from django.core.management.base import BaseCommand
from apps.contents.models import Category, Content


class Command(BaseCommand):
    help = '웹문서 카테고리의 콘텐츠를 확인합니다'

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("웹문서 카테고리 콘텐츠 확인"))
        self.stdout.write("=" * 80)

        try:
            cat = Category.objects.get(slug='web-docs')
            self.stdout.write(f"\n카테고리: {cat.name} (slug: {cat.slug}, order: {cat.order})")

            contents = Content.objects.filter(category=cat).order_by('-created_at')
            self.stdout.write(f"\n총 {contents.count()}개의 콘텐츠가 있습니다.\n")

            if contents.exists():
                for content in contents[:20]:  # 처음 20개 출력
                    self.stdout.write(
                        f"ID: {content.id:4d} | {content.title[:60]:60s} | {content.created_at.strftime('%Y-%m-%d %H:%M')}"
                    )

                if contents.count() > 20:
                    self.stdout.write(f"\n... 외 {contents.count() - 20}개 더 있음")
            else:
                self.stdout.write(self.style.WARNING("콘텐츠가 없습니다."))

        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR("\n❌ web-docs 카테고리를 찾을 수 없습니다."))
            self.stdout.write("\n현재 존재하는 카테고리:")
            for cat in Category.objects.all().order_by('order'):
                self.stdout.write(f"  - {cat.slug} ({cat.name})")

        self.stdout.write("\n" + "=" * 80)
