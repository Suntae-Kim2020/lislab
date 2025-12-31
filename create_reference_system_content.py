import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category, Content, Tag
from apps.accounts.models import User

# 1. 카테고리 가져오기 (이미 생성되어 있음)
try:
    category = Category.objects.get(slug='identifier-reference')
    print(f"ℹ️  카테고리 '{category.name}' 사용")
except Category.DoesNotExist:
    print("❌ '식별자와 참조체계' 카테고리를 찾을 수 없습니다.")
    print("   먼저 URI 콘텐츠 생성 스크립트를 실행하세요.")
    exit(1)

# 2. 태그 생성
tag_names = [
    '참조체계',
    'Reference System',
    '식별자',
    '전거 제어',
    'Authority Control',
    '링크드 데이터',
    'Linked Data',
    'RDF',
    'URI',
    'DOI',
    'ISBN',
    '온톨로지',
    'Ontology',
    '메타데이터',
    'Metadata',
    '도서관 시스템',
    'DNS',
    'SPARQL',
    'LOD',
    '데이터 통합'
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
with open('reference_system_content.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 5. 콘텐츠 생성 또는 업데이트
content, created = Content.objects.get_or_create(
    slug='reference-system-complete-guide',
    defaults={
        'title': '참조체계: 정보를 연결하는 보이지 않는 규칙',
        'summary': '참조체계(Reference System)의 개념과 역할을 문과생도 쉽게 이해할 수 있게 설명합니다. 식별자와의 차이, 도서관·웹·학술 세계의 다양한 사례, 그리고 왜 참조체계가 정보 시스템의 핵심인지 완벽하게 학습합니다.',
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
    print(f"\n✅ 참조체계 콘텐츠 생성 완료!")
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
    print(f"\n✅ 참조체계 콘텐츠 업데이트 완료!")
    print(f"   제목: {content.title}")
    print(f"   카테고리: {content.category.name}")
    print(f"   난이도: {content.get_difficulty_display()}")
    print(f"   예상 시간: {content.estimated_time}분")
    print(f"   태그 수: {content.tags.count()}개")
    print(f"   공개 상태: {content.get_status_display()}")
    print(f"\n🔗 접속 URL: /contents/{content.slug}")
