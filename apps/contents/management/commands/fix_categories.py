"""
디지털도서관 카테고리 생성 및 하위 카테고리 parent 설정
카테고리 순서를 메뉴 순서와 동일하게 설정
"""
from django.core.management.base import BaseCommand
from apps.contents.models import Category


class Command(BaseCommand):
    help = '디지털도서관 카테고리 구조 및 순서 수정'

    def handle(self, *args, **options):
        # 1. 디지털도서관 카테고리 생성 (없으면)
        digital_lib, created = Category.objects.get_or_create(
            slug='digital-library',
            defaults={
                'name': '디지털도서관',
                'description': '디지털도서관 관련 교육 콘텐츠',
                'order': 1,
                'show_in_menu': True,
                'menu_order': 1,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(
                f"디지털도서관 카테고리 생성됨 (id: {digital_lib.id})"
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"디지털도서관 카테고리 이미 존재 (id: {digital_lib.id})"
            ))

        # 2. 하위 카테고리 목록 (메뉴 순서대로)
        child_categories = [
            ('web-docs', '웹문서', 0),
            ('web-technology', '웹기술', 1),
            ('search-protocol', '검색 프로토콜', 2),
            ('standard-specifications', '표준규격지침', 3),
            ('conceptual-model', '개념 모델', 4),
            ('data-model', '데이터 모델', 5),
            ('metadata', '메타데이터', 6),
            ('ontology', '온톨로지', 7),
            ('identifier-reference', '식별자와 참조체계', 8),
            ('overview', '한눈에 보기', 9),
        ]

        # 3. 하위 카테고리 업데이트
        for slug, name, order in child_categories:
            try:
                cat = Category.objects.get(slug=slug)
                cat.parent = digital_lib
                cat.order = order
                cat.save()
                self.stdout.write(self.style.SUCCESS(
                    f"{name} (slug: {slug}) - parent: 디지털도서관, order: {order}"
                ))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"{name} (slug: {slug}) - 카테고리를 찾을 수 없음"
                ))

        # 4. 다른 최상위 카테고리 순서 설정 (메뉴 순서대로)
        top_level_categories = [
            ('바이브코딩', 0),
            ('digital-library', 1),  # 디지털도서관
            ('statistics', 2),  # 알기쉬운 통계
            ('special-lecture-a', 3),  # 데이터베이스설계론
            ('special-lecture-b', 4),  # 도서관경영론
            ('practice', 5),  # 실습공간
        ]

        for slug_or_name, order in top_level_categories:
            try:
                cat = Category.objects.filter(slug=slug_or_name).first() or \
                      Category.objects.filter(name=slug_or_name).first()
                if cat:
                    cat.order = order
                    cat.parent = None  # 최상위로 설정
                    cat.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"{cat.name} (최상위) - order: {order}"
                    ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"{slug_or_name} 업데이트 실패: {e}"
                ))

        # 5. 결과 출력
        self.stdout.write("\n=== 카테고리 구조 ===")
        for cat in Category.objects.filter(parent__isnull=True).order_by('order'):
            self.stdout.write(f"  [{cat.order}] {cat.name} (id: {cat.id})")
            for child in cat.children.order_by('order'):
                self.stdout.write(f"      [{child.order}] {child.name} (id: {child.id})")

        self.stdout.write(self.style.SUCCESS("\n완료!"))
