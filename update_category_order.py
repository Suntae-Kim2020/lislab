#!/usr/bin/env python
"""카테고리 순서 업데이트 스크립트"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category

# 상단 메뉴와 동일한 순서
category_order = [
    ('web-docs', 1),           # 웹문서
    ('web-technology', 2),      # 웹기술
    ('search-protocol', 3),     # 프로토콜
    ('standard-specifications', 4),  # 표준규격지침
    ('conceptual-model', 5),    # 개념 모델
    ('data-model', 6),          # 데이터 모델
    ('metadata', 7),            # 메타데이터
    ('ontology', 8),            # 온톨로지
    ('identifier-reference', 9),  # 식별자와 참조체계
    ('overview', 10),           # 한눈에 보기
]

def update_category_orders():
    """카테고리 순서 업데이트"""
    updated_count = 0

    for slug, order in category_order:
        try:
            category = Category.objects.get(slug=slug, parent=None)
            if category.order != order:
                category.order = order
                category.save()
                print(f"✓ {category.name} ({slug}) - order: {order}")
                updated_count += 1
            else:
                print(f"- {category.name} ({slug}) - order 변경 없음: {order}")
        except Category.DoesNotExist:
            print(f"✗ 카테고리 없음: {slug}")

    print(f"\n총 {updated_count}개의 카테고리 순서가 업데이트되었습니다.")

    # 전체 카테고리 목록 확인
    print("\n=== 전체 최상위 카테고리 목록 (순서대로) ===")
    all_categories = Category.objects.filter(parent=None).order_by('order', 'name')
    for idx, cat in enumerate(all_categories, 1):
        print(f"{idx}. {cat.name} ({cat.slug}) - order: {cat.order}")

if __name__ == '__main__':
    update_category_orders()
