import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category, Content, Tag
from apps.accounts.models import User

# 1. 카테고리 생성
category, created = Category.objects.get_or_create(
    slug='web-technology',
    defaults={
        'name': '웹기술',
        'description': '웹 서비스와 API 개발을 위한 핵심 기술'
    }
)

if created:
    print(f"✅ 카테고리 '{category.name}' 생성 완료!")
else:
    print(f"ℹ️  카테고리 '{category.name}' 이미 존재함")

# 2. 태그 생성 (이미 존재하는 태그만 사용)
tag_names = [
    'REST',
    'REST API',
    'API',
    'HTTP',
    'JSON',
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'PATCH',
    'SUSHI',
    '웹서비스',
    'RESTful',
    'API 설계',
    '상태 코드',
    'OAuth',
    'JWT',
    'HTTPS'
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
with open('rest_api_content.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 5. 콘텐츠 생성 또는 업데이트
content, created = Content.objects.get_or_create(
    slug='rest-api-complete-guide',
    defaults={
        'title': 'REST API 완벽 가이드: 웹 서비스의 핵심 이해하기',
        'summary': 'REST API의 개념, 원칙, HTTP 메서드, 상태 코드부터 실제 구현 사례까지. 도서관 시스템(SUSHI)의 REST API 활용을 포함한 완벽한 가이드입니다. 실전 예시와 함께 웹 API 개발의 모든 것을 학습합니다.',
        'content_html': html_content,
        'category': category,
        'author': admin_user,
        'difficulty': 'INTERMEDIATE',
        'estimated_time': 30,
        'status': 'PUBLISHED'
    }
)

if created:
    valid_tags = [t for t in tags if t is not None]
    content.tags.set(valid_tags)
    print(f"\n✅ REST API 콘텐츠 생성 완료!")
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
    print(f"\n✅ REST API 콘텐츠 업데이트 완료!")
    print(f"   제목: {content.title}")
    print(f"   카테고리: {content.category.name}")
    print(f"   난이도: {content.get_difficulty_display()}")
    print(f"   예상 시간: {content.estimated_time}분")
    print(f"   태그 수: {content.tags.count()}개")
    print(f"   공개 상태: {content.get_status_display()}")
    print(f"\n🔗 접속 URL: /contents/{content.slug}")
