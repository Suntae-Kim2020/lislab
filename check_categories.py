#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Category, Content

print('=== 최상위 카테고리들 ===')
top_categories = Category.objects.filter(parent__isnull=True).order_by('id')
for c in top_categories:
    print(f'{c.id}: {c.name} ({c.slug})')
    # 하위 카테고리 표시
    children = Category.objects.filter(parent=c).order_by('id')
    for child in children:
        content_count = Content.objects.filter(category=child).count()
        print(f'  └─ {child.name} ({child.slug}) - {content_count}개 콘텐츠')

print('\n=== 온톨로지 카테고리 상세 ===')
ontology = Category.objects.filter(slug='ontology').first()
if ontology:
    print(f'✓ 존재함')
    print(f'  ID: {ontology.id}')
    print(f'  이름: {ontology.name}')
    print(f'  슬러그: {ontology.slug}')
    print(f'  부모: {ontology.parent}')
    print(f'  하위 카테고리: {Category.objects.filter(parent=ontology).count()}개')
    print(f'  직접 콘텐츠: {Content.objects.filter(category=ontology).count()}개')
else:
    print('✗ 존재하지 않음')
