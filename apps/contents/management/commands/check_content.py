"""
특정 콘텐츠 정보 확인
"""
from django.core.management.base import BaseCommand
from apps.contents.models import Content, Category
import sys


class Command(BaseCommand):
    help = '특정 콘텐츠의 정보를 확인합니다'

    def add_arguments(self, parser):
        parser.add_argument('content_id', type=int, help='확인할 콘텐츠 ID')

    def handle(self, *args, **options):
        content_id = options['content_id']

        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS(f"콘텐츠 ID {content_id} 정보 확인"))
        self.stdout.write("=" * 80)

        try:
            content = Content.objects.get(id=content_id)

            self.stdout.write(f"\n제목: {content.title}")
            self.stdout.write(f"Slug: {content.slug}")
            self.stdout.write(f"상태: {content.status} ({content.get_status_display()})")
            self.stdout.write(f"작성자: {content.author}")

            # Category 정보
            if hasattr(content, 'category') and content.category:
                self.stdout.write(f"\n카테고리: {content.category.name} (slug: {content.category.slug})")
            else:
                self.stdout.write(self.style.WARNING(f"\n⚠️  카테고리: 없음 또는 NULL"))

            # Category field 존재 여부 확인
            self.stdout.write(f"\n카테고리 필드 존재: {hasattr(content, 'category')}")
            if hasattr(content, 'category_id'):
                self.stdout.write(f"카테고리 ID: {content.category_id}")

            # Tags
            tags = content.tags.all()
            if tags.exists():
                tag_names = ', '.join([tag.name for tag in tags])
                self.stdout.write(f"태그: {tag_names}")
            else:
                self.stdout.write(f"태그: 없음")

            self.stdout.write(f"\n생성일: {content.created_at}")
            self.stdout.write(f"수정일: {content.updated_at}")

        except Content.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"\n❌ ID {content_id} 콘텐츠를 찾을 수 없습니다."))
            return

        self.stdout.write("\n" + "=" * 80)
