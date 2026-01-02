"""
프로덕션 데이터베이스 카테고리 정리
불필요한 카테고리 삭제 및 올바른 구조로 재구성
"""
from django.core.management.base import BaseCommand
from apps.contents.models import Category, Content

class Command(BaseCommand):
    help = '프로덕션 카테고리를 정리합니다'

    def handle(self, *args, **options):
        self.stdout.write("=" * 80)
        self.stdout.write(self.style.SUCCESS("카테고리 정리 시작"))
        self.stdout.write("=" * 80)

        # 유지할 카테고리 목록 (slug와 올바른 order)
        keep_categories = {
            'web-docs': {'name': '웹문서', 'order': 1},
            'web-technology': {'name': '웹기술', 'order': 2},
            'search-protocol': {'name': '검색 프로토콜', 'order': 3},
            'standard-specifications': {'name': '표준규격지침', 'order': 4},
            'conceptual-model': {'name': '개념 모델', 'order': 5},
            'data-model': {'name': '데이터 모델', 'order': 6},
            'metadata': {'name': '메타데이터', 'order': 7},
            'ontology': {'name': '온톨로지', 'order': 8},
            'identifier-reference': {'name': '식별자와 참조체계', 'order': 9},
            'overview': {'name': '한눈에 보기', 'order': 10},
            'practice': {'name': '실습', 'order': 11},
        }

        # 현재 상태
        all_cats = Category.objects.all()
        self.stdout.write(f"\n현재 카테고리: {all_cats.count()}개")

        # 삭제할 카테고리 찾기
        to_delete = []
        to_update = []
        
        for cat in all_cats:
            if cat.slug in keep_categories:
                to_update.append(cat)
            else:
                to_delete.append(cat)

        self.stdout.write(f"유지: {len(to_update)}개")
        self.stdout.write(f"삭제: {len(to_delete)}개\n")

        # 삭제할 카테고리의 콘텐츠 처리
        # 콘텐츠를 적절한 카테고리로 이동하는 매핑
        category_mapping = {
            'format-comparison': 'metadata',
            'bibliographic-models-comparison': 'conceptual-model',
            'frbr': 'conceptual-model',
            'serialization': 'data-model',
            'dublin-core': 'metadata',
            'xml': 'data-model',
            'rdf': 'data-model',
            'oai-pmh': 'search-protocol',
            'html': 'web-technology',
            'srw': 'search-protocol',
            'sru': 'search-protocol',
            'sparql': 'search-protocol',
            'rdfs': 'ontology',
            'owl': 'ontology',
            'mods': 'metadata',
            'mets': 'metadata',
            'marc21': 'metadata',
            'lrm': 'conceptual-model',
            'json': 'data-model',
        }

        if to_delete:
            self.stdout.write("\n삭제할 카테고리 및 콘텐츠 이동:")
            for cat in to_delete:
                contents = Content.objects.filter(category=cat)
                content_count = contents.count()

                if content_count > 0:
                    # 이동할 카테고리 결정
                    target_slug = category_mapping.get(cat.slug, 'overview')
                    target_cat = Category.objects.get(slug=target_slug)

                    # 콘텐츠 이동
                    contents.update(category=target_cat)
                    self.stdout.write(
                        f"  ✓ {cat.slug} ({cat.name}): {content_count}개 콘텐츠 → {target_cat.name}"
                    )
                else:
                    self.stdout.write(f"  - {cat.slug} ({cat.name}): 콘텐츠 없음")

            # 자동 삭제 (콘텐츠는 이미 이동됨)
            deleted_count = 0
            for cat in to_delete:
                cat.delete()
                deleted_count += 1
            self.stdout.write(self.style.SUCCESS(f"\n✓ {deleted_count}개 카테고리 삭제 완료"))

        # 남은 카테고리 업데이트
        self.stdout.write("\n카테고리 정보 업데이트:")
        for cat in to_update:
            if cat.slug in keep_categories:
                info = keep_categories[cat.slug]
                cat.name = info['name']
                cat.order = info['order']
                cat.save()
                self.stdout.write(f"  ✓ {cat.slug}: order={cat.order}, name={cat.name}")

        # 최종 상태
        final_count = Category.objects.count()
        self.stdout.write(f"\n최종 카테고리 수: {final_count}개")

        self.stdout.write("\n" + "=" * 80)
        self.stdout.write(self.style.SUCCESS("✅ 카테고리 정리 완료"))
        self.stdout.write("=" * 80)
