"""
카테고리 평면화 Management Command

하위 카테고리의 콘텐츠를 상위 카테고리로 이동하고,
하위 카테고리를 삭제합니다.
"""
from django.core.management.base import BaseCommand
from apps.contents.models import Category, Content


class Command(BaseCommand):
    help = '카테고리를 평면 구조로 변환 (하위 카테고리의 콘텐츠를 상위로 이동 후 삭제)'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("카테고리 평면화 마이그레이션 시작"))
        self.stdout.write("=" * 60)

        # 0. 자기참조 카테고리 수정 (parent가 자기 자신인 경우)
        self_referencing = Category.objects.filter(parent__isnull=False).extra(
            where=["id = parent_id"]
        )
        self_ref_count = self_referencing.count()

        if self_ref_count > 0:
            self.stdout.write(f"\n🔧 자기참조 카테고리 수정 중...")
            for cat in self_referencing:
                self.stdout.write(f"  - '{cat.name}' (parent를 NULL로 변경)")
                cat.parent = None
                cat.save()
            self.stdout.write(self.style.SUCCESS(f"✓ {self_ref_count}개 카테고리의 parent를 NULL로 변경했습니다."))

        # 1. 현재 상태 확인
        total_categories = Category.objects.count()
        parent_categories = Category.objects.filter(parent__isnull=True).count()
        child_categories = Category.objects.filter(parent__isnull=False).count()

        self.stdout.write(f"\n📊 현재 상태:")
        self.stdout.write(f"  - 전체 카테고리: {total_categories}개")
        self.stdout.write(f"  - 상위 카테고리: {parent_categories}개")
        self.stdout.write(f"  - 하위 카테고리: {child_categories}개")

        if child_categories == 0:
            self.stdout.write(self.style.WARNING("\n✅ 하위 카테고리가 없습니다. 마이그레이션이 필요하지 않습니다."))
            return

        # 2. 하위 카테고리의 콘텐츠를 상위 카테고리로 이동
        self.stdout.write(f"\n🔄 하위 카테고리의 콘텐츠를 상위 카테고리로 이동 중...")

        moved_contents = 0
        child_cats = Category.objects.filter(parent__isnull=False).select_related('parent')

        for child_cat in child_cats:
            parent_cat = child_cat.parent
            contents = Content.objects.filter(category=child_cat)
            content_count = contents.count()

            if content_count > 0:
                self.stdout.write(f"  - '{child_cat.name}' → '{parent_cat.name}': {content_count}개 콘텐츠")
                contents.update(category=parent_cat)
                moved_contents += content_count

        self.stdout.write(self.style.SUCCESS(f"\n✓ 총 {moved_contents}개의 콘텐츠를 이동했습니다."))

        # 3. 하위 카테고리 삭제
        self.stdout.write(f"\n🗑️  하위 카테고리 삭제 중...")

        deleted_categories = []
        # 다시 쿼리해서 최신 상태 가져오기
        child_cats_to_delete = Category.objects.filter(parent__isnull=False)

        for child_cat in child_cats_to_delete:
            # 삭제 전 해당 카테고리의 콘텐츠 수 확인
            remaining_contents = Content.objects.filter(category=child_cat).count()
            if remaining_contents > 0:
                self.stdout.write(self.style.WARNING(f"  ⚠️ '{child_cat.name}' 카테고리에 {remaining_contents}개 콘텐츠가 남아있습니다. 강제 이동 중..."))
                # 강제로 상위 카테고리로 이동
                Content.objects.filter(category=child_cat).update(category=child_cat.parent)

            deleted_categories.append(child_cat.name)
            child_cat.delete()

        self.stdout.write(self.style.SUCCESS(f"\n✓ 삭제된 카테고리 ({len(deleted_categories)}개):"))
        for cat_name in deleted_categories:
            self.stdout.write(f"  - {cat_name}")

        # 4. 최종 상태 확인
        final_categories = Category.objects.count()

        self.stdout.write(f"\n📊 최종 상태:")
        self.stdout.write(f"  - 전체 카테고리: {final_categories}개 (평면 구조)")

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("✅ 카테고리 평면화 마이그레이션 완료!"))
        self.stdout.write("=" * 60)
