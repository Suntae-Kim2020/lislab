#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content, Category, Tag
from apps.accounts.models import User
from django.utils.text import slugify
from django.utils import timezone

def create_open_access_content():
    """오픈 액세스 교육 콘텐츠 생성"""

    # 관리자 사용자 가져오기
    try:
        admin_user = User.objects.filter(role='ADMIN').first()
        if not admin_user:
            admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.first()
        print(f"작성자: {admin_user.username}")
    except Exception as e:
        print(f"ERROR: 사용자를 찾을 수 없습니다: {e}")
        return

    # 한눈에 보기 카테고리 가져오기
    try:
        overview_category = Category.objects.get(slug='overview')
        print(f"카테고리 찾음: {overview_category.name}")
    except Category.DoesNotExist:
        print("ERROR: '한눈에 보기' 카테고리를 찾을 수 없습니다.")
        return

    # HTML 콘텐츠 파일 읽기
    html_file_path = 'open_access_content.html'

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"HTML 파일 읽기 완료: {len(html_content)} 글자")
    except FileNotFoundError:
        print(f"ERROR: {html_file_path} 파일을 찾을 수 없습니다.")
        return

    # 콘텐츠 생성
    content_data = {
        'title': '오픈 액세스: 모두를 위한 학술 정보',
        'slug': 'open-access-for-everyone',
        'category': overview_category,
        'author': admin_user,
        'summary': '오픈 액세스의 개념부터 오픈 사이언스 운동, 발전 과정, 구현 전략, 다양한 종류(골드/그린/하이브리드/다이아몬드 OA)까지 종합적으로 학습합니다. 학술 정보의 민주화와 지식 공유의 중요성을 이해합니다.',
        'content_html': html_content,
        'difficulty': 'BEGINNER',
        'estimated_time': 10,
        'status': 'PUBLISHED',
        'published_at': timezone.now(),
    }

    # 기존 콘텐츠 확인
    existing_content = Content.objects.filter(slug=content_data['slug']).first()

    if existing_content:
        print(f"기존 콘텐츠 업데이트: {existing_content.title}")
        for key, value in content_data.items():
            setattr(existing_content, key, value)
        existing_content.save()
        content = existing_content
    else:
        print("새 콘텐츠 생성 중...")
        content = Content.objects.create(**content_data)
        print(f"✓ 콘텐츠 생성 완료: {content.title}")

    # 태그 추가
    tags_to_add = [
        '오픈 액세스',
        'Open Access',
        'OA',
        '오픈 사이언스',
        'Open Science',
        '골드 OA',
        '그린 OA',
        '학술 출판',
        '학술지',
        '리포지토리',
        'DOAJ',
        'arXiv',
        'PubMed Central',
        '셀프 아카이빙',
        'Plan S',
        '저작권',
        'CC 라이선스',
        'APC',
        '약탈적 학술지',
        '연구 윤리',
    ]

    print("\n태그 추가 중...")
    for tag_name in tags_to_add:
        tag, created = Tag.objects.get_or_create(
            name=tag_name,
            defaults={'slug': slugify(tag_name, allow_unicode=True)}
        )
        content.tags.add(tag)
        status = "생성됨" if created else "기존"
        print(f"  - {tag_name} ({status})")

    print(f"\n" + "="*60)
    print(f"오픈 액세스 콘텐츠 생성 완료!")
    print(f"="*60)
    print(f"제목: {content.title}")
    print(f"슬러그: {content.slug}")
    print(f"카테고리: {content.category.name}")
    print(f"난이도: {content.get_difficulty_display()}")
    print(f"예상 시간: {content.estimated_time}분")
    print(f"상태: {content.get_status_display()}")
    print(f"태그 수: {content.tags.count()}개")
    print(f"발행일: {content.published_at}")
    print(f"\n접속 URL: http://localhost:3000/contents/{content.slug}")
    print(f"="*60)

if __name__ == '__main__':
    create_open_access_content()
