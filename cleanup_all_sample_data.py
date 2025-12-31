"""
모든 샘플 데이터 삭제 및 교육 콘텐츠 재구성 스크립트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category, Tag, Content
from apps.accounts.models import User

print("🗑️  Cleaning up all data...")
print("=" * 50)

# 관리자 계정 확인
admin = User.objects.filter(username='admin').first()
if not admin:
    print("❌ Admin user not found")
    exit(1)

# 1. 모든 콘텐츠 삭제
print("\n📝 Deleting all contents...")
all_contents = Content.objects.all()
content_count = all_contents.count()
if content_count > 0:
    for content in all_contents:
        print(f"  ✓ Deleted content: {content.title}")
    all_contents.delete()
    print(f"\n  Total deleted contents: {content_count}")
else:
    print("  ○ No contents found")

# 2. 모든 태그 삭제
print("\n🏷️  Deleting all tags...")
all_tags = Tag.objects.all()
tag_count = all_tags.count()
if tag_count > 0:
    for tag in all_tags:
        print(f"  ✓ Deleted tag: {tag.name}")
    all_tags.delete()
    print(f"\n  Total deleted tags: {tag_count}")
else:
    print("  ○ No tags found")

# 3. 모든 카테고리 삭제 (하위부터)
print("\n📁 Deleting all categories...")
# 하위 카테고리 먼저 삭제
sub_categories = Category.objects.filter(parent__isnull=False)
sub_count = sub_categories.count()
if sub_count > 0:
    for cat in sub_categories:
        print(f"  ✓ Deleted sub-category: {cat.name}")
    sub_categories.delete()

# 상위 카테고리 삭제
parent_categories = Category.objects.filter(parent__isnull=True)
parent_count = parent_categories.count()
if parent_count > 0:
    for cat in parent_categories:
        print(f"  ✓ Deleted category: {cat.name}")
    parent_categories.delete()

total_categories = sub_count + parent_count
print(f"\n  Total deleted categories: {total_categories}")

print("\n" + "=" * 50)
print("✅ All sample data deleted!")
print(f"\nDeleted:")
print(f"  - Contents: {content_count}")
print(f"  - Tags: {tag_count}")
print(f"  - Categories: {total_categories}")

# 4. 최종 확인
print("\n📊 Current database state:")
print(f"  - Categories: {Category.objects.count()}")
print(f"  - Tags: {Tag.objects.count()}")
print(f"  - Contents: {Content.objects.count()}")

print("\n💡 Tip: Run 'python add_education_contents.py' to add education contents again.")
