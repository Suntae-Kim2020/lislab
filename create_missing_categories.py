#!/usr/bin/env python
"""누락된 카테고리 생성 스크립트"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category

# 생성할 카테고리 목록
categories_to_create = [
    {
        'name': '웹문서',
        'slug': 'web-docs',
        'description': '웹 기반 문서 형식과 표준',
        'order': 1
    },
    {
        'name': '프로토콜',
        'slug': 'search-protocol',
        'description': '검색 및 통신 프로토콜',
        'order': 3
    },
    {
        'name': '데이터 모델',
        'slug': 'data-model',
        'description': '데이터 구조화 및 모델링',
        'order': 6
    },
]

def create_categories():
    """카테고리 생성"""
    created_count = 0

    for cat_data in categories_to_create:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description'],
                'order': cat_data['order'],
                'parent': None,
                'is_active': True
            }
        )

        if created:
            print(f"✓ 카테고리 생성됨: {category.name} ({category.slug})")
            created_count += 1
        else:
            print(f"- 이미 존재함: {category.name} ({category.slug})")

    print(f"\n총 {created_count}개의 카테고리가 생성되었습니다.")

    # 전체 카테고리 목록 확인
    print("\n=== 전체 최상위 카테고리 목록 ===")
    all_categories = Category.objects.filter(parent=None).order_by('order', 'name')
    for idx, cat in enumerate(all_categories, 1):
        print(f"{idx}. {cat.name} ({cat.slug}) - order: {cat.order}")

if __name__ == '__main__':
    create_categories()
