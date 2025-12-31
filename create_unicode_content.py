import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category, Content, Tag
from apps.accounts.models import User

# 1. 카테고리 가져오기
try:
    category = Category.objects.get(slug='standard-specifications')
    print(f"ℹ️  카테고리 '{category.name}' 사용")
except Category.DoesNotExist:
    print("❌ '표준규격지침' 카테고리를 찾을 수 없습니다.")
    exit(1)

# 2. 태그 생성
tag_names = [
    'UNICODE',
    'UTF-8',
    'UTF-16',
    'UTF-32',
    'Character Encoding',
    '문자 인코딩',
    'ASCII',
    'Code Point',
    'BMP',
    'Plane',
    '다국어',
    'Multilingual',
    '이모지',
    'Emoji',
    'Normalization',
    '정규화',
    'MARC',
    '디지털 아카이브',
    '장기 보존',
    '웹 표준',
    'ISO 10646',
    '한글 인코딩',
    'EUC-KR',
    'CP949',
    '글자 깨짐',
    'Mojibake',
    'NFC',
    'NFD',
    '국제 표준',
    'AI',
    '자연어 처리'
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
with open('unicode_content.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 5. 콘텐츠 생성 또는 업데이트
content, created = Content.objects.get_or_create(
    slug='unicode-complete-guide',
    defaults={
        'title': 'UNICODE 완벽 가이드: 전 세계 문자를 하나로',
        'summary': 'ASCII부터 UNICODE까지, 문자 인코딩의 역사와 원리를 문과생도 이해할 수 있게 설명합니다. UTF-8/UTF-16/UTF-32의 차이, 한글 깨짐 현상의 원인, 도서관 시스템에서의 다국어 처리, 이모지의 비밀, 그리고 AI 시대 UNICODE의 중요성까지 완벽하게 학습합니다.',
        'content_html': html_content,
        'category': category,
        'author': admin_user,
        'difficulty': 'ADVANCED',
        'estimated_time': 30,
        'status': 'PUBLISHED'
    }
)

if created:
    valid_tags = [t for t in tags if t is not None]
    content.tags.set(valid_tags)
    print(f"\n✅ UNICODE 콘텐츠 생성 완료!")
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
    print(f"\n✅ UNICODE 콘텐츠 업데이트 완료!")
    print(f"   제목: {content.title}")
    print(f"   카테고리: {content.category.name}")
    print(f"   난이도: {content.get_difficulty_display()}")
    print(f"   예상 시간: {content.estimated_time}분")
    print(f"   태그 수: {content.tags.count()}개")
    print(f"   공개 상태: {content.get_status_display()}")
    print(f"\n🔗 접속 URL: /contents/{content.slug}")
