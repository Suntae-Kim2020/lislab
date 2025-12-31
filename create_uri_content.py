import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category, Content, Tag
from apps.accounts.models import User

# 1. 카테고리 생성
category, created = Category.objects.get_or_create(
    slug='identifier-reference',
    defaults={
        'name': '식별자와 참조체계',
        'description': '인터넷 자원 식별을 위한 URI, URL, URN과 DOI 등 영구 식별자 시스템'
    }
)

if created:
    print(f"✅ 카테고리 '{category.name}' 생성 완료!")
else:
    print(f"ℹ️  카테고리 '{category.name}' 이미 존재함")

# 2. 태그 생성
tag_names = [
    'URI',
    'URL',
    'URN',
    'DOI',
    '식별자',
    'Identifier',
    'ISBN',
    'ISSN',
    'Handle',
    'ARK',
    'CrossRef',
    '영구 식별자',
    'Persistent Identifier',
    '학술 자료',
    '참조체계',
    '인터넷 주소',
    '도서관 시스템',
    '디지털 아카이브'
]

tags = []
for tag_name in tag_names:
    try:
        tag = Tag.objects.filter(name=tag_name).first()
        if tag:
            tags.append(tag)
            print(f"  ℹ️  태그 '{tag_name}' 사용")
        else:
            tag = Tag(name=tag_name)
            tag.save()
            tags.append(tag)
            print(f"  ✅ 태그 '{tag_name}' 생성")
    except Exception as e:
        print(f"  ⚠️  태그 '{tag_name}' 처리 실패: {e}")

# 3. 관리자 사용자 가져오기
admin_user = User.objects.filter(role='ADMIN').first()
if not admin_user:
    print("❌ 관리자 사용자를 찾을 수 없습니다.")
    exit(1)

# 4. HTML 콘텐츠 읽기
with open('uri_content.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 5. 콘텐츠 생성 또는 업데이트
content, created = Content.objects.get_or_create(
    slug='uri-complete-guide',
    defaults={
        'title': 'URI 완벽 가이드: 인터넷 주소의 모든 것',
        'summary': 'URI, URL, URN의 개념과 차이점을 문과생도 이해할 수 있게 설명합니다. 식별자의 역할, DOI의 활용, 도서관 시스템에서의 실제 사례까지 포함한 완벽한 가이드입니다.',
        'content_html': html_content,
        'category': category,
        'author': admin_user,
        'difficulty': 'BEGINNER',
        'estimated_time': 20,
        'status': 'PUBLISHED'
    }
)

if created:
    valid_tags = [t for t in tags if t is not None]
    content.tags.set(valid_tags)
    print(f"\n✅ URI 콘텐츠 생성 완료!")
    print(f"   제목: {content.title}")
    print(f"   카테고리: {content.category.name}")
    print(f"   난이도: {content.get_difficulty_display()}")
    print(f"   예상 시간: {content.estimated_time}분")
    print(f"   태그 수: {content.tags.count()}개")
    print(f"   공개 상태: {content.get_status_display()}")
    print(f"\n🔗 접속 URL: /contents/{content.slug}")
else:
    # 기존 콘텐츠 업데이트
    content.content_html = html_content
    content.save()
    valid_tags = [t for t in tags if t is not None]
    content.tags.set(valid_tags)
    print(f"\n✅ URI 콘텐츠 업데이트 완료!")
    print(f"   제목: {content.title}")
    print(f"   카테고리: {content.category.name}")
    print(f"   난이도: {content.get_difficulty_display()}")
    print(f"   예상 시간: {content.estimated_time}분")
    print(f"   태그 수: {content.tags.count()}개")
    print(f"   공개 상태: {content.get_status_display()}")
    print(f"\n🔗 접속 URL: /contents/{content.slug}")
