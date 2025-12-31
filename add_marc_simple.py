#!/usr/bin/env python
"""
MARC21 학습 콘텐츠 추가 스크립트 (간단 버전)
"""
import os
import sys
import django

# Django 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.contents.models import Content, Category, Tag

User = get_user_model()

def create_marc_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 생성 또는 가져오기: 메타데이터
    metadata_category, created = Category.objects.get_or_create(
        slug='metadata',
        defaults={
            'name': '메타데이터',
            'description': '도서관 메타데이터 표준과 포맷',
            'parent': None
        }
    )
    if created:
        print("✓ 상위 카테고리 생성: 메타데이터")
    else:
        print("✓ 상위 카테고리 확인: 메타데이터")

    # 하위 카테고리 생성 또는 가져오기: MARC21
    marc_category, created = Category.objects.get_or_create(
        slug='marc21',
        defaults={
            'name': 'MARC21',
            'description': 'MARC21 메타데이터 포맷',
            'parent': metadata_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: MARC21")
    else:
        print("✓ 하위 카테고리 확인: MARC21")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': '메타데이터 포맷', 'slug': 'metadata-format'},
        {'name': '인코딩포맷', 'slug': 'encoding-format'},
        {'name': '교환포맷', 'slug': 'exchange-format'}
    ]
    tags = []
    for tag_info in tag_data:
        tag, created = Tag.objects.get_or_create(
            name=tag_info['name'],
            defaults={'slug': tag_info['slug']}
        )
        tags.append(tag)
        print(f"  ✓ 태그 확인: {tag_info['name']}")

    # 학습 콘텐츠 생성 - 간단한 테스트 버전
    content_html = """
<div class="content-section">
  <h2>MARC21이란?</h2>
  <p><strong>MARC (MAchine-Readable Cataloging)</strong>은 1960년대 미국 의회도서관에서 개발한 기계가 읽을 수 있는 목록 형식입니다.</p>

  <h3>MARC21의 구조</h3>
  <p>MARC21 레코드는 3개의 주요 부분으로 구성됩니다:</p>
  <ul>
    <li>Leader: 24바이트 고정길이</li>
    <li>Directory: 가변길이 색인</li>
    <li>Variable Fields: 실제 데이터</li>
  </ul>

  <h3>주요 필드</h3>
  <p>자주 사용하는 필드들:</p>
  <ul>
    <li>020: ISBN</li>
    <li>100: 개인저자</li>
    <li>245: 표제</li>
    <li>260/264: 발행사항</li>
    <li>300: 형태사항</li>
  </ul>
</div>
"""

    content = Content.objects.create(
        title="MARC21 완벽 가이드: 도서관 메타데이터의 표준",
        slug="marc21-complete-guide",
        summary="도서관 서지데이터의 국제 표준 MARC21의 구조와 활용법을 실전 예제와 함께 배웁니다.",
        content_html=content_html,
        category=marc_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=305,
        prerequisites="",
        learning_objectives="MARC21의 구조와 목적 이해하기, 주요 필드와 서브필드 활용법 익히기, 실전 MARC21 레코드 읽고 작성하기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {marc_category.name} (상위: {metadata_category.name})")
    print(f"  - 난이도: 중급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=metadata")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_marc_content()
