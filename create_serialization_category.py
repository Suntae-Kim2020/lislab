import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category

# 1. 부모 카테고리 가져오기
try:
    parent_category = Category.objects.get(slug='data-model')
    print(f"✅ 부모 카테고리 '{parent_category.name}' 찾음")
except Category.DoesNotExist:
    print("❌ '데이터 모델' 카테고리를 찾을 수 없습니다.")
    exit(1)

# 2. 직렬화 카테고리 생성
category, created = Category.objects.get_or_create(
    slug='serialization',
    defaults={
        'name': '직렬화',
        'description': 'RDF 데이터를 다양한 형식으로 표현하는 직렬화 방법 (Turtle, JSON-LD, N-Triples, N3)',
        'parent': parent_category,
        'is_active': True
    }
)

if created:
    print(f"\n✅ 카테고리 '{category.name}' 생성 완료!")
    print(f"   Slug: {category.slug}")
    print(f"   부모: {category.parent.name}")
    print(f"   설명: {category.description}")
else:
    print(f"\nℹ️  카테고리 '{category.name}' 이미 존재함")
