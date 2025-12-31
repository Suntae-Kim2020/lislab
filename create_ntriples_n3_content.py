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
    'N-Triples',
    'N3',
    'Notation3',
    'RDF',
    '직렬화',
    'Serialization',
    'Semantic Web',
    '시맨틱 웹',
    'Linked Data',
    'W3C',
    'Triple',
    'Big Data',
    '대용량 데이터',
    'Streaming',
    'Inference',
    '추론',
    'Rules',
    '규칙',
    'N-Quads',
    'Turtle',
    'Tim Berners-Lee',
    'URI',
    'Parser',
    '파싱',
    'Data Processing',
    '데이터 처리',
    'cwm',
    'EYE',
    'rdflib',
    'Apache Jena',
    'BIBFRAME',
    '메타데이터'
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
with open('ntriples_n3_content.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 5. 콘텐츠 생성 또는 업데이트
content, created = Content.objects.get_or_create(
    slug='ntriples-n3-simplicity-and-power',
    defaults={
        'title': 'N-Triples와 N3: 단순함과 강력함',
        'summary': 'N-Triples는 가장 단순한 RDF 형식으로 대용량 데이터 처리에 최적화되어 있고, N3는 Turtle의 전신으로 변수와 추론 규칙을 지원합니다. 두 형식의 특징과 활용 사례를 비교하며 배웁니다.',
        'content_html': html_content,
        'category': category,
        'author': admin_user,
        'difficulty': 'BEGINNER',
        'estimated_time': 15,
        'status': 'PUBLISHED'
    }
)

if created:
    valid_tags = [t for t in tags if t is not None]
    content.tags.set(valid_tags)
    print(f"\n✅ N-Triples/N3 콘텐츠 생성 완료!")
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
    print(f"\n✅ N-Triples/N3 콘텐츠 업데이트 완료!")
    print(f"   제목: {content.title}")
    print(f"   카테고리: {content.category.name}")
    print(f"   난이도: {content.get_difficulty_display()}")
    print(f"   예상 시간: {content.estimated_time}분")
    print(f"   태그 수: {content.tags.count()}개")
    print(f"   공개 상태: {content.get_status_display()}")
    print(f"\n🔗 접속 URL: /contents/{content.slug}")
