#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content, Category, Tag
from apps.accounts.models import User
from django.utils.text import slugify
from django.utils import timezone

def create_rss_content():
    """RSS 교육 콘텐츠 생성"""

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

    # 웹기술 카테고리 가져오기
    try:
        web_tech_category = Category.objects.get(slug='web-technology')
        print(f"카테고리 찾음: {web_tech_category.name}")
    except Category.DoesNotExist:
        print("ERROR: '웹기술' 카테고리를 찾을 수 없습니다.")
        return

    # HTML 콘텐츠 파일 읽기
    html_file_path = 'rss_content.html'

    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"HTML 파일 읽기 완료: {len(html_content)} 글자")
    except FileNotFoundError:
        print(f"ERROR: {html_file_path} 파일을 찾을 수 없습니다.")
        return

    # 콘텐츠 생성
    content_data = {
        'title': 'RSS: 정보를 효율적으로 구독하는 방법',
        'slug': 'rss-really-simple-syndication',
        'category': web_tech_category,
        'author': admin_user,
        'summary': 'RSS(Really Simple Syndication)와 Atom 피드의 개념, 작동 원리, 차이점을 학습합니다. Feedly를 활용한 실전 RSS 리더 사용법과 학생들을 위한 다양한 활용 사례를 소개합니다.',
        'content_html': html_content,
        'difficulty': 'ADVANCED',
        'estimated_time': 20,
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
        'RSS',
        'Atom',
        'Feedly',
        'Feed',
        '웹 피드',
        '구독',
        'Syndication',
        'RSS 리더',
        'XML',
        '정보 구독',
        '뉴스 피드',
        '블로그',
        'YouTube',
        '콘텐츠 관리',
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
    print(f"RSS 콘텐츠 생성 완료!")
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
    create_rss_content()
