import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category, Content, Tag
from apps.accounts.models import User

# 1. 카테고리 가져오기
try:
    category = Category.objects.get(slug='serialization')
    print(f"ℹ️  카테고리 '{category.name}' 사용")
except Category.DoesNotExist:
    print("❌ 'serialization' 카테고리를 찾을 수 없습니다.")
    exit(1)

# 2. 태그 생성
tag_names = [
    'JSON-LD',
    'RDF',
    '직렬화',
    'Serialization',
    'Semantic Web',
    '시맨틱 웹',
    'Linked Data',
    'W3C',
    'Schema.org',
    '@context',
    '@id',
    '@type',
    '@graph',
    'JSON',
    'JavaScript',
    'Web API',
    'SEO',
    'Structured Data',
    '구조화 데이터',
    'BIBFRAME',
    '메타데이터',
    'URI',
    'Ontology',
    '온톨로지',
    'Web Development',
    '웹 개발',
    'Google',
    'Rich Results',
    'Dublin Core'
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
with open('jsonld_content.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 5. 콘텐츠 생성 또는 업데이트
content, created = Content.objects.get_or_create(
    slug='jsonld-rdf-for-web-developers',
    defaults={
        'title': 'JSON-LD: 웹 개발자를 위한 RDF',
        'summary': 'JSON-LD는 JSON 형식으로 Linked Data를 표현하는 웹 개발자 친화적인 RDF 직렬화 형식입니다. @context, @id, @type, @graph 등 핵심 개념과 Schema.org 구조화 데이터, 도서관 메타데이터 활용 방법을 배웁니다.',
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
    print(f"\n✅ JSON-LD 콘텐츠 생성 완료!")
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
    print(f"\n✅ JSON-LD 콘텐츠 업데이트 완료!")
    print(f"   제목: {content.title}")
    print(f"   카테고리: {content.category.name}")
    print(f"   난이도: {content.get_difficulty_display()}")
    print(f"   예상 시간: {content.estimated_time}분")
    print(f"   태그 수: {content.tags.count()}개")
    print(f"   공개 상태: {content.get_status_display()}")
    print(f"\n🔗 접속 URL: /contents/{content.slug}")
