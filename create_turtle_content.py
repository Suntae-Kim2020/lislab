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
    print("❌ '직렬화' 카테고리를 찾을 수 없습니다.")
    exit(1)

# 2. 태그 생성
tag_names = [
    'Turtle',
    'RDF',
    '직렬화',
    'Serialization',
    'Triple',
    'Prefix',
    'Semantic Web',
    '시맨틱 웹',
    'Linked Data',
    'W3C',
    'Terse RDF',
    'URI',
    'Blank Node',
    'Collection',
    'FOAF',
    'Dublin Core',
    'BIBFRAME',
    '온톨로지',
    '메타데이터',
    'DBpedia'
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
with open('turtle_content.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 5. 콘텐츠 생성 또는 업데이트
content, created = Content.objects.get_or_create(
    slug='turtle-rdf-serialization',
    defaults={
        'title': 'Turtle: 사람이 읽기 쉬운 RDF 직렬화',
        'summary': 'Turtle(Terse RDF Triple Language)은 RDF 데이터를 사람이 읽고 쓰기 쉽게 표현하는 텍스트 형식입니다. XML/RDF의 복잡함을 벗어나 간결한 문법으로 Triple, Prefix, 데이터 타입, 언어 태그 등을 표현하는 방법을 배웁니다.',
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
    print(f"\n✅ Turtle 콘텐츠 생성 완료!")
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
    print(f"\n✅ Turtle 콘텐츠 업데이트 완료!")
    print(f"   제목: {content.title}")
    print(f"   카테고리: {content.category.name}")
    print(f"   난이도: {content.get_difficulty_display()}")
    print(f"   예상 시간: {content.estimated_time}분")
    print(f"   태그 수: {content.tags.count()}개")
    print(f"   공개 상태: {content.get_status_display()}")
    print(f"\n🔗 접속 URL: /contents/{content.slug}")
