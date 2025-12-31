import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category

# 검색프로토콜 카테고리 찾기
try:
    category = Category.objects.get(slug='search-protocol')
    old_name = category.name

    # 이름 수정
    category.name = '프로토콜'
    category.save()

    print(f"✅ 카테고리 이름이 수정되었습니다!")
    print(f"   변경 전: {old_name}")
    print(f"   변경 후: {category.name}")
    print(f"   Slug: {category.slug}")

except Category.DoesNotExist:
    print("❌ '검색프로토콜' 카테고리를 찾을 수 없습니다.")
    print("\n현재 존재하는 카테고리:")
    for cat in Category.objects.all():
        print(f"   - {cat.name} (slug: {cat.slug})")
