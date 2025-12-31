import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category, Content, Tag
from apps.accounts.models import User

# 1. 카테고리 생성
category, created = Category.objects.get_or_create(
    slug='standard-specifications',
    defaults={
        'name': '표준규격지침',
        'description': '도서관 전자자원 관련 국제 표준 및 규격 지침'
    }
)

if created:
    print(f"✅ 카테고리 '{category.name}' 생성 완료!")
else:
    print(f"ℹ️  카테고리 '{category.name}' 이미 존재함")

# 2. 태그 생성
tag_names = [
    'COUNTER',
    'Project COUNTER',
    'Release 5',
    'R5',
    '이용통계',
    '전자저널',
    '전자책',
    'Title Report',
    'Platform Report',
    'Database Report',
    'Item Report',
    'Metric Type',
    'Total Item Requests',
    'Unique Item Requests',
    'SUSHI',
    '전자자원 평가',
    '컬렉션 평가',
    '구독 관리',
    'TSV',
    'JSON',
    'COUNTER Registry',
    'Big Deal',
    '예산 관리'
]

tags = []
for tag_name in tag_names:
    try:
        # 먼저 name으로 조회 시도
        tag = Tag.objects.filter(name=tag_name).first()
        if tag:
            tags.append(tag)
            print(f"  ℹ️  태그 '{tag_name}' 이미 존재함")
        else:
            # 없으면 새로 생성
            tag = Tag(name=tag_name)
            tag.save()
            tags.append(tag)
            print(f"  ✅ 태그 '{tag_name}' 생성")
    except Exception as e:
        print(f"  ⚠️  태그 '{tag_name}' 생성 실패: {e}")
        # 실패해도 계속 진행

# 3. 관리자 사용자 가져오기
admin_user = User.objects.filter(role='ADMIN').first()
if not admin_user:
    print("❌ 관리자 사용자를 찾을 수 없습니다.")
    exit(1)

# 4. HTML 콘텐츠 읽기
with open('counter_content.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 5. 콘텐츠 생성
content, created = Content.objects.get_or_create(
    slug='counter-code-of-practice-complete-guide',
    defaults={
        'title': 'COUNTER Code of Practice: 전자자원 이용통계 표준의 모든 것',
        'summary': 'COUNTER R5의 개념, 보고서 유형, 측정 항목, 실제 활용 사례까지 전자자원 이용통계 표준을 완벽하게 이해합니다. 실제 보고서 예시와 함께 도서관 실무에 바로 적용할 수 있는 상세한 가이드입니다.',
        'content_html': html_content,
        'category': category,
        'author': admin_user,
        'difficulty': 'INTERMEDIATE',
        'estimated_time': 35,
        'status': 'PUBLISHED'
    }
)

if created:
    # 태그 추가 (실패한 태그는 제외)
    valid_tags = [t for t in tags if t is not None]
    content.tags.set(valid_tags)
    print(f"\n✅ COUNTER 콘텐츠 생성 완료!")
    print(f"   제목: {content.title}")
    print(f"   카테고리: {content.category.name}")
    print(f"   난이도: {content.get_difficulty_display()}")
    print(f"   예상 시간: {content.estimated_time}분")
    print(f"   태그 수: {content.tags.count()}개")
    print(f"   공개 상태: {content.get_status_display()}")
    print(f"\n🔗 접속 URL: /contents/{content.slug}")
else:
    print(f"\n⚠️  콘텐츠가 이미 존재합니다: {content.slug}")
    print(f"   기존 콘텐츠를 업데이트하려면 먼저 삭제하거나 slug를 변경하세요.")
