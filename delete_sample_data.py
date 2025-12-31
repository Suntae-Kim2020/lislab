"""
샘플 데이터 삭제 스크립트
create_sample_data.py로 생성한 샘플 콘텐츠, 카테고리, 태그를 삭제합니다.
교육 콘텐츠(웹페이지, 검색프로토콜)는 유지됩니다.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category, Tag, Content

print("🗑️  Deleting sample data...")
print("=" * 50)

# 삭제할 카테고리 slug 목록 (샘플 데이터)
sample_category_slugs = [
    'programming',
    'data-science',
    'web-development',
    'database',
    'cloud'
]

# 삭제할 태그 slug 목록 (샘플 데이터)
sample_tag_slugs = [
    'python',
    'javascript',
    'react',
    'django',
    'postgresql',
    'machine-learning',
    'deep-learning',
    'aws',
    'docker',
    'git'
]

# 1. 샘플 카테고리의 콘텐츠 삭제
print("\n📝 Deleting contents from sample categories...")
sample_categories = Category.objects.filter(slug__in=sample_category_slugs)
deleted_contents = 0

for category in sample_categories:
    contents = Content.objects.filter(category=category)
    count = contents.count()
    if count > 0:
        contents.delete()
        deleted_contents += count
        print(f"  ✓ Deleted {count} content(s) from category: {category.name}")

print(f"\n  Total deleted contents: {deleted_contents}")

# 2. 샘플 태그 삭제
print("\n🏷️  Deleting sample tags...")
sample_tags = Tag.objects.filter(slug__in=sample_tag_slugs)
deleted_tags = sample_tags.count()

if deleted_tags > 0:
    tag_names = [tag.name for tag in sample_tags]
    sample_tags.delete()
    for name in tag_names:
        print(f"  ✓ Deleted tag: {name}")
    print(f"\n  Total deleted tags: {deleted_tags}")
else:
    print("  ○ No sample tags found")

# 3. 샘플 카테고리 삭제 (하위 카테고리부터)
print("\n📁 Deleting sample categories...")
deleted_categories = 0

# 하위 카테고리 먼저 삭제
for slug in sample_category_slugs:
    try:
        category = Category.objects.get(slug=slug)
        # 하위 카테고리가 있으면 먼저 삭제
        children = Category.objects.filter(parent=category)
        if children.exists():
            child_count = children.count()
            child_names = [c.name for c in children]
            children.delete()
            for name in child_names:
                print(f"  ✓ Deleted sub-category: {name}")
            deleted_categories += child_count

        # 부모 카테고리 삭제
        category.delete()
        print(f"  ✓ Deleted category: {category.name}")
        deleted_categories += 1
    except Category.DoesNotExist:
        pass

print(f"\n  Total deleted categories: {deleted_categories}")

# 4. 남아있는 콘텐츠 확인
print("\n📊 Remaining data:")
remaining_categories = Category.objects.all()
remaining_tags = Tag.objects.all()
remaining_contents = Content.objects.all()

print(f"  - Categories: {remaining_categories.count()}")
for cat in remaining_categories:
    parent_name = f" (under {cat.parent.name})" if cat.parent else ""
    print(f"    • {cat.name}{parent_name}")

print(f"\n  - Tags: {remaining_tags.count()}")
for tag in remaining_tags:
    print(f"    • {tag.name}")

print(f"\n  - Contents: {remaining_contents.count()}")
for content in remaining_contents:
    print(f"    • {content.title} ({content.category.name})")

print("\n" + "=" * 50)
print("✅ Sample data deletion completed!")
print(f"\nDeleted:")
print(f"  - Contents: {deleted_contents}")
print(f"  - Tags: {deleted_tags}")
print(f"  - Categories: {deleted_categories}")
