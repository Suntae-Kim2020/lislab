"""
디지털도서관 카테고리 생성 및 하위 카테고리 parent 설정
카테고리 순서를 메뉴 순서와 동일하게 설정
"""
from django.core.management.base import BaseCommand
from apps.contents.models import Category


class Command(BaseCommand):
    help = '디지털도서관 카테고리 구조 및 순서 수정'

    def handle(self, *args, **options):
        # 1. 디지털도서관 카테고리 찾기 또는 생성
        # 먼저 이름으로 검색
        digital_lib = Category.objects.filter(name='디지털도서관').first()
        if digital_lib:
            self.stdout.write(self.style.SUCCESS(
                f"디지털도서관 카테고리 이미 존재 (id: {digital_lib.id}, slug: {digital_lib.slug})"
            ))
        else:
            # slug로 검색
            digital_lib = Category.objects.filter(slug='digital-library').first()
            if digital_lib:
                self.stdout.write(self.style.SUCCESS(
                    f"디지털도서관 카테고리 이미 존재 (id: {digital_lib.id}, slug: {digital_lib.slug})"
                ))
            else:
                # 새로 생성
                digital_lib = Category.objects.create(
                    name='디지털도서관',
                    slug='digital-library',
                    description='디지털도서관 관련 교육 콘텐츠',
                    order=1,
                    show_in_menu=True,
                    menu_order=1,
                )
                self.stdout.write(self.style.SUCCESS(
                    f"디지털도서관 카테고리 생성됨 (id: {digital_lib.id})"
                ))

        # 디지털도서관 카테고리 설정 업데이트
        digital_lib.order = 1
        digital_lib.parent = None
        digital_lib.show_in_menu = True
        digital_lib.menu_order = 1
        digital_lib.url = ''  # 네비게이션 전용이 아닌 일반 카테고리로 설정
        digital_lib.is_active = True
        digital_lib.save()
        self.stdout.write(self.style.SUCCESS(
            f"디지털도서관 설정 업데이트 완료 (url: '{digital_lib.url}', is_active: {digital_lib.is_active})"
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
            # 디지털도서관은 위에서 order=1로 설정됨
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

        # 5. 불필요한 최상위 카테고리 처리 (경영관리 기능 영역 등)
        # 도서관경영론의 하위로 이동하거나 비활성화
        try:
            misc_cat = Category.objects.filter(name='경영관리 기능 영역').first()
            if misc_cat:
                # 도서관경영론의 하위 카테고리로 설정
                lib_mgmt = Category.objects.filter(slug='special-lecture-b').first()
                if lib_mgmt:
                    misc_cat.parent = lib_mgmt
                    misc_cat.order = 0
                    misc_cat.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"경영관리 기능 영역 → 도서관경영론 하위로 이동"
                    ))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"경영관리 기능 영역 처리 중 오류: {e}"))

        # 5. 결과 출력
        self.stdout.write("\n=== 카테고리 구조 ===")
        for cat in Category.objects.filter(parent__isnull=True).order_by('order'):
            self.stdout.write(f"  [{cat.order}] {cat.name} (id: {cat.id})")
            for child in cat.children.order_by('order'):
                self.stdout.write(f"      [{child.order}] {child.name} (id: {child.id})")

        self.stdout.write(self.style.SUCCESS("\n완료!"))
