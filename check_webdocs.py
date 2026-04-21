from apps.contents.models import Category, Content

print("=" * 80)
print("웹문서 카테고리 콘텐츠 확인")
print("=" * 80)

try:
    cat = Category.objects.get(slug='web-docs')
    print(f"\n카테고리: {cat.name} (slug: {cat.slug}, order: {cat.order})")

    contents = Content.objects.filter(category=cat).order_by('-created_at')
    print(f"\n총 {contents.count()}개의 콘텐츠가 있습니다.\n")

    if contents.exists():
        for content in contents[:10]:  # 처음 10개만 출력
            print(f"ID: {content.id:4d} | {content.title[:50]:50s} | 작성일: {content.created_at}")

        if contents.count() > 10:
            print(f"\n... 외 {contents.count() - 10}개 더 있음")
    else:
        print("콘텐츠가 없습니다.")

except Category.DoesNotExist:
    print("\n❌ web-docs 카테고리를 찾을 수 없습니다.")
    print("\n현재 존재하는 카테고리:")
    for cat in Category.objects.all().order_by('order'):
        print(f"  - {cat.slug} ({cat.name})")

print("\n" + "=" * 80)
