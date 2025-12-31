#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.contents.models import Content, Category, Tag

User = get_user_model()

# 관리자 사용자 가져오기
admin = User.objects.filter(is_superuser=True).first()
if not admin:
    print("관리자 사용자를 찾을 수 없습니다.")
    sys.exit(1)

# 온톨로지 카테고리 찾기
ontology_category = Category.objects.filter(slug='ontology').first()
if not ontology_category:
    print("온톨로지 카테고리를 찾을 수 없습니다.")
    sys.exit(1)

# OWL 하위 카테고리 생성 또는 가져오기
owl_category, created = Category.objects.get_or_create(
    slug='owl',
    defaults={
        'name': 'OWL',
        'description': 'Web Ontology Language',
        'parent': ontology_category
    }
)

if created:
    print(f"✓ OWL 카테고리 생성됨: {owl_category.name}")
else:
    print(f"✓ 기존 OWL 카테고리 사용: {owl_category.name}")

# 태그 데이터
tag_data = [
    {'name': 'OWL', 'slug': 'owl'},
    {'name': '온톨로지', 'slug': 'ontology'},
    {'name': '시맨틱웹', 'slug': 'semantic-web'},
    {'name': 'RDFS', 'slug': 'rdfs'},
    {'name': '추론', 'slug': 'reasoning'},
    {'name': 'RDF', 'slug': 'rdf'},
    {'name': '지식표현', 'slug': 'knowledge-representation'},
]

# 태그 생성
tags = []
for tag_info in tag_data:
    # 먼저 slug로 찾기
    try:
        tag = Tag.objects.get(slug=tag_info['slug'])
        print(f"✓ 기존 태그 사용: {tag.name}")
    except Tag.DoesNotExist:
        # slug로 없으면 name으로 찾기
        try:
            tag = Tag.objects.get(name=tag_info['name'])
            print(f"✓ 기존 태그 사용 (name으로): {tag.name}")
        except Tag.DoesNotExist:
            # 둘 다 없으면 생성
            tag = Tag.objects.create(name=tag_info['name'], slug=tag_info['slug'])
            print(f"✓ 태그 생성됨: {tag.name}")
    tags.append(tag)

# OWL 콘텐츠 생성
content = Content.objects.create(
    title="OWL: 지능형 웹을 위한 온톨로지 언어",
    slug="owl-web-ontology-language",
    category=owl_category,
    author=admin,
    difficulty='ADVANCED',
    estimated_time=50,
    status=Content.Status.PUBLISHED,
    summary="OWL(Web Ontology Language)의 핵심 개념과 RDFS와의 관계, 추론 메커니즘, 그리고 도서관 분야에서의 실제 활용 사례를 학습합니다.",
    prerequisites="RDFS 기초 지식, RDF 트리플 이해, 온톨로지 개념 이해",
    learning_objectives="OWL의 핵심 기능(클래스 표현, 속성 제약) 이해하기, OWL과 RDFS의 관계와 차이점 파악하기, Description Logic 기반 추론 원리 이해하기, RDF/XML, Turtle, JSON-LD로 OWL 표현하기, 도서관 온톨로지 설계 및 추론 활용하기, BIBFRAME 등 실무 사례 분석하기",
    content_html="""
<div style="font-family: 'Noto Sans KR', sans-serif; line-height: 1.8; max-width: 1200px; margin: 0 auto; padding: 20px;">
    <h1 style="color: #1a1a1a; border-bottom: 3px solid #2563eb; padding-bottom: 10px; margin-bottom: 30px;">
        🦉 OWL: 지능형 웹을 위한 온톨로지 언어
    </h1>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; margin-bottom: 30px;">
        <h2 style="color: white; margin-top: 0;">OWL이란 무엇인가?</h2>
        <p style="font-size: 16px; margin: 0;">
            OWL(Web Ontology Language)은 <strong>시맨틱 웹</strong>을 위한 지식 표현 언어입니다.
            RDFS를 확장하여 더 풍부한 의미론과 강력한 추론 능력을 제공합니다.
            도서관, 의료, 생명과학 등 다양한 분야에서 복잡한 지식을 표현하고 자동으로 추론하는 데 사용됩니다.
        </p>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        📊 OWL과 RDFS의 관계
    </h2>

    <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #1e40af; margin-top: 0;">계층 구조</h3>
        <div style="display: flex; flex-direction: column; align-items: center; gap: 15px; padding: 20px;">
            <!-- RDF -->
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 20px 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); min-width: 400px; text-align: center;">
                <div style="font-size: 20px; font-weight: bold; margin-bottom: 5px;">RDF</div>
                <div style="font-size: 14px; opacity: 0.9;">Resource Description Framework</div>
                <div style="font-size: 13px; margin-top: 8px; padding: 8px; background: rgba(255,255,255,0.2); border-radius: 4px;">데이터 표현의 기본 틀</div>
            </div>

            <!-- 화살표 -->
            <div style="font-size: 28px; color: #10b981; font-weight: bold;">⬇</div>
            <div style="background: #dcfce7; padding: 8px 16px; border-radius: 6px; font-weight: bold; color: #166534;">확장</div>

            <!-- RDFS -->
            <div style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); color: white; padding: 20px 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); min-width: 400px; text-align: center;">
                <div style="font-size: 20px; font-weight: bold; margin-bottom: 5px;">RDFS</div>
                <div style="font-size: 14px; opacity: 0.9;">RDF Schema</div>
                <div style="font-size: 13px; margin-top: 8px; padding: 8px; background: rgba(255,255,255,0.2); border-radius: 4px;">클래스와 속성 정의</div>
            </div>

            <!-- 화살표 -->
            <div style="font-size: 28px; color: #10b981; font-weight: bold;">⬇</div>
            <div style="background: #dcfce7; padding: 8px 16px; border-radius: 6px; font-weight: bold; color: #166534;">확장</div>

            <!-- OWL -->
            <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 20px 40px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); min-width: 400px; text-align: center;">
                <div style="font-size: 20px; font-weight: bold; margin-bottom: 5px;">OWL</div>
                <div style="font-size: 14px; opacity: 0.9;">Web Ontology Language</div>
                <div style="font-size: 13px; margin-top: 8px; padding: 8px; background: rgba(255,255,255,0.2); border-radius: 4px;">복잡한 온톨로지와 추론</div>

                <!-- OWL 하위 버전들 -->
                <div style="display: flex; gap: 10px; margin-top: 15px; justify-content: center; flex-wrap: wrap;">
                    <div style="background: rgba(255,255,255,0.3); padding: 10px 15px; border-radius: 6px; font-size: 13px; border: 2px solid rgba(255,255,255,0.5);">
                        <div style="font-weight: bold;">OWL Lite</div>
                        <div style="font-size: 11px; margin-top: 3px;">가벼운 버전</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.3); padding: 10px 15px; border-radius: 6px; font-size: 13px; border: 2px solid rgba(255,255,255,0.5);">
                        <div style="font-weight: bold;">OWL DL</div>
                        <div style="font-size: 11px; margin-top: 3px;">Description Logic</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.3); padding: 10px 15px; border-radius: 6px; font-size: 13px; border: 2px solid rgba(255,255,255,0.5);">
                        <div style="font-weight: bold;">OWL Full</div>
                        <div style="font-size: 11px; margin-top: 3px;">완전한 표현력</div>
                    </div>
                </div>
            </div>

            <!-- 화살표 -->
            <div style="font-size: 28px; color: #10b981; font-weight: bold;">⬇</div>
            <div style="background: #dbeafe; padding: 8px 16px; border-radius: 6px; font-weight: bold; color: #1e40af;">최신 표준</div>

            <!-- OWL 2 -->
            <div style="background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); color: white; padding: 20px 40px; border-radius: 10px; box-shadow: 0 6px 8px rgba(0,0,0,0.15); min-width: 400px; text-align: center; border: 3px solid #fbbf24;">
                <div style="font-size: 22px; font-weight: bold; margin-bottom: 5px;">🎯 OWL 2</div>
                <div style="font-size: 14px; opacity: 0.9;">W3C 표준 (2009)</div>
                <div style="font-size: 13px; margin-top: 8px; padding: 8px; background: rgba(255,255,255,0.2); border-radius: 4px;">향상된 표현력과 추론 능력</div>
            </div>
        </div>
    </div>

    <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0;">
        <h3 style="color: #92400e; margin-top: 0;">🔑 핵심 차이점</h3>
        <table style="width: 100%; border-collapse: collapse; background-color: white;">
            <thead>
                <tr style="background-color: #f59e0b; color: white;">
                    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">특징</th>
                    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">RDFS</th>
                    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">OWL</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>클래스 관계</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">rdfs:subClassOf만 가능</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">교집합, 합집합, 여집합, 동등성 등</td>
                </tr>
                <tr style="background-color: #fffbeb;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>속성 제약</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">domain, range만 가능</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">cardinality, functional, inverse 등</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>추론 능력</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">기본적인 상속 추론</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">Description Logic 기반 강력한 추론</td>
                </tr>
                <tr style="background-color: #fffbeb;">
                    <td style="padding: 10px; border: 1px solid #ddd;"><strong>개체 관계</strong></td>
                    <td style="padding: 10px; border: 1px solid #ddd;">명시적 선언만</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">sameAs, differentFrom 등</td>
                </tr>
            </tbody>
        </table>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        🎯 OWL의 핵심 기능
    </h2>

    <h3 style="color: #1e40af; margin-top: 30px;">1. 클래스 표현력 (Class Expressions)</h3>

    <div style="background-color: #f0f9ff; padding: 20px; border-radius: 8px; margin: 15px 0;">
        <h4 style="color: #0c4a6e; margin-top: 0;">교집합 (Intersection)</h4>
        <p>두 개 이상의 클래스를 모두 만족하는 개체를 정의합니다.</p>

        <div style="background-color: #dbeafe; padding: 15px; border-radius: 6px; margin: 15px 0;">
            <h5 style="color: #1e40af; margin-top: 0;">📖 실생활 예시</h5>
            <p style="margin: 5px 0;">도서관에서 "소설이면서 동시에 베스트셀러인 책"을 별도 클래스로 정의하고 싶을 때 사용합니다.</p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li>✅ 소설이고 베스트셀러 → NovelBestseller에 속함</li>
                <li>❌ 소설이지만 베스트셀러 아님 → 속하지 않음</li>
                <li>❌ 베스트셀러지만 소설 아님 (예: 자기계발서) → 속하지 않음</li>
            </ul>
        </div>

        <div style="font-family: monospace; background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 14px;">
# 예: 소설이면서 베스트셀러인 책
:NovelBestseller owl:equivalentClass [
  rdf:type owl:Class ;
  owl:intersectionOf ( :Novel :Bestseller )
] .
        </div>

        <div style="background-color: #fff; padding: 15px; border-radius: 6px; margin-top: 15px; border-left: 4px solid #3b82f6;">
            <h5 style="color: #1e40af; margin-top: 0;">🔍 코드 설명</h5>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #3b82f6; width: 35%;">:NovelBestseller</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">정의하려는 새로운 클래스 이름</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #3b82f6;">owl:equivalentClass</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">"~와 완전히 같다"는 의미 (동등 클래스)</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #3b82f6;">[ ... ]</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">익명 클래스 정의 (이름 없는 클래스)</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #3b82f6;">rdf:type owl:Class</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">이것이 클래스라는 선언</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-family: monospace; color: #3b82f6;">owl:intersectionOf</td>
                    <td style="padding: 8px;">교집합을 만드는 명령어</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-family: monospace; color: #3b82f6;">( :Novel :Bestseller )</td>
                    <td style="padding: 8px;">교집합을 만들 클래스들의 목록</td>
                </tr>
            </table>
        </div>

        <div style="background-color: #ecfdf5; padding: 15px; border-radius: 6px; margin-top: 15px;">
            <h5 style="color: #065f46; margin-top: 0;">💡 이렇게 읽으세요</h5>
            <p style="margin: 0; font-size: 15px; line-height: 1.8;">
                "NovelBestseller 클래스는 <strong>Novel 클래스</strong>와 <strong>Bestseller 클래스</strong> 둘 다에 속하는 개체들의 집합과 <strong>완전히 동일</strong>합니다."
            </p>
        </div>
    </div>

    <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin: 15px 0;">
        <h4 style="color: #14532d; margin-top: 0;">합집합 (Union)</h4>
        <p>여러 클래스 중 하나라도 만족하는 개체를 정의합니다.</p>

        <div style="background-color: #dcfce7; padding: 15px; border-radius: 6px; margin: 15px 0;">
            <h5 style="color: #166534; margin-top: 0;">📖 실생활 예시</h5>
            <p style="margin: 5px 0;">도서관에서 "책의 창작자"를 표현할 때, 저자이거나 편집자인 사람을 Creator로 정의합니다.</p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li>✅ 저자 → Creator에 속함</li>
                <li>✅ 편집자 → Creator에 속함</li>
                <li>✅ 저자이면서 편집자 → Creator에 속함</li>
                <li>❌ 저자도 편집자도 아님 → 속하지 않음</li>
            </ul>
        </div>

        <div style="font-family: monospace; background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 14px;">
# 예: 저자이거나 편집자인 사람
:Creator owl:equivalentClass [
  rdf:type owl:Class ;
  owl:unionOf ( :Author :Editor )
] .
        </div>

        <div style="background-color: #fff; padding: 15px; border-radius: 6px; margin-top: 15px; border-left: 4px solid #22c55e;">
            <h5 style="color: #166534; margin-top: 0;">🔍 코드 설명</h5>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #22c55e; width: 35%;">owl:unionOf</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">합집합을 만드는 명령어 (OR 조건)</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-family: monospace; color: #22c55e;">( :Author :Editor )</td>
                    <td style="padding: 8px;">합집합을 만들 클래스들의 목록</td>
                </tr>
            </table>
        </div>

        <div style="background-color: #ecfdf5; padding: 15px; border-radius: 6px; margin-top: 15px;">
            <h5 style="color: #065f46; margin-top: 0;">💡 이렇게 읽으세요</h5>
            <p style="margin: 0; font-size: 15px; line-height: 1.8;">
                "Creator 클래스는 <strong>Author 클래스</strong> 또는 <strong>Editor 클래스</strong> 중 하나 이상에 속하는 개체들의 집합과 <strong>완전히 동일</strong>합니다."
            </p>
        </div>
    </div>

    <h3 style="color: #1e40af; margin-top: 30px;">2. 속성 제약 (Property Restrictions)</h3>

    <div style="background-color: #fef2f2; padding: 20px; border-radius: 8px; margin: 15px 0;">
        <h4 style="color: #7f1d1d; margin-top: 0;">Cardinality (수량 제약)</h4>
        <p>속성이 가질 수 있는 값의 개수를 제한합니다.</p>

        <div style="background-color: #fee2e2; padding: 15px; border-radius: 6px; margin: 15px 0;">
            <h5 style="color: #991b1b; margin-top: 0;">📖 실생활 예시</h5>
            <p style="margin: 5px 0;">도서관 시스템에서 데이터 무결성을 보장하기 위해 사용합니다.</p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li><strong>cardinality</strong>: 책은 ISBN을 정확히 1개만 가짐 (0개 안 됨, 2개도 안 됨)</li>
                <li><strong>minCardinality</strong>: 책은 최소 1명의 저자를 가져야 함 (저자 없는 책은 불가능)</li>
                <li><strong>maxCardinality</strong>: 책은 최대 10명까지만 저자를 가질 수 있음</li>
            </ul>
        </div>

        <div style="font-family: monospace; background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 14px;">
# 예: 책은 정확히 1개의 ISBN을 가져야 함
:Book rdfs:subClassOf [
  rdf:type owl:Restriction ;
  owl:onProperty :hasISBN ;
  owl:cardinality "1"^^xsd:nonNegativeInteger
] .

# 예: 책은 최소 1명의 저자를 가져야 함
:Book rdfs:subClassOf [
  rdf:type owl:Restriction ;
  owl:onProperty :hasAuthor ;
  owl:minCardinality "1"^^xsd:nonNegativeInteger
] .
        </div>

        <div style="background-color: #fff; padding: 15px; border-radius: 6px; margin-top: 15px; border-left: 4px solid #ef4444;">
            <h5 style="color: #991b1b; margin-top: 0;">🔍 코드 설명 (첫 번째 예시)</h5>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #ef4444; width: 40%;">:Book rdfs:subClassOf</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">Book 클래스의 특성을 정의</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #ef4444;">owl:Restriction</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">제약 조건을 나타내는 특수 클래스</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #ef4444;">owl:onProperty :hasISBN</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">hasISBN 속성에 대한 제약</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-family: monospace; color: #ef4444;">owl:cardinality "1"</td>
                    <td style="padding: 8px;">정확히 1개의 값을 가져야 함</td>
                </tr>
            </table>
        </div>

        <div style="background-color: #fef2f2; padding: 15px; border-radius: 6px; margin-top: 15px;">
            <h5 style="color: #7f1d1d; margin-top: 0;">💡 이렇게 읽으세요</h5>
            <p style="margin: 0 0 10px 0; font-size: 15px; line-height: 1.8;">
                <strong>첫 번째:</strong> "Book 클래스는 hasISBN 속성의 값을 <strong>정확히 1개</strong> 가져야 하는 제약을 만족하는 클래스의 하위 클래스입니다."
            </p>
            <p style="margin: 0; font-size: 15px; line-height: 1.8;">
                <strong>두 번째:</strong> "Book 클래스는 hasAuthor 속성의 값을 <strong>최소 1개 이상</strong> 가져야 합니다."
            </p>
        </div>
    </div>

    <div style="background-color: #faf5ff; padding: 20px; border-radius: 8px; margin: 15px 0;">
        <h4 style="color: #581c87; margin-top: 0;">Functional Property (함수형 속성)</h4>
        <p>각 개체가 해당 속성에 대해 최대 1개의 값만 가질 수 있습니다.</p>

        <div style="background-color: #f3e8ff; padding: 15px; border-radius: 6px; margin: 15px 0;">
            <h5 style="color: #6b21a8; margin-top: 0;">📖 실생활 예시</h5>
            <p style="margin: 5px 0;">책은 출판연도를 하나만 가집니다. 1997년이면서 동시에 1998년일 수 없습니다.</p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li>✅ 책A의 출판연도 = 2023 → 유효</li>
                <li>❌ 책A의 출판연도 = 2023 AND 2024 → 모순! (추론기가 오류 감지)</li>
            </ul>
            <p style="margin: 10px 0 0 0; font-size: 14px; color: #6b21a8;">
                <strong>💡 활용:</strong> 데이터 검증에 유용합니다. 실수로 중복 입력하면 자동으로 감지됩니다.
            </p>
        </div>

        <div style="font-family: monospace; background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 14px;">
# 예: 책은 하나의 출판연도만 가짐
:publicationYear rdf:type owl:FunctionalProperty ;
                 rdfs:domain :Book ;
                 rdfs:range xsd:gYear .
        </div>

        <div style="background-color: #fff; padding: 15px; border-radius: 6px; margin-top: 15px; border-left: 4px solid #a855f7;">
            <h5 style="color: #6b21a8; margin-top: 0;">🔍 코드 설명</h5>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #a855f7; width: 40%;">owl:FunctionalProperty</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">함수형 속성 선언 (최대 1개 값만 가능)</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #a855f7;">rdfs:domain :Book</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">이 속성의 주체는 Book</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-family: monospace; color: #a855f7;">rdfs:range xsd:gYear</td>
                    <td style="padding: 8px;">값은 연도 데이터 타입</td>
                </tr>
            </table>
        </div>

        <div style="background-color: #faf5ff; padding: 15px; border-radius: 6px; margin-top: 15px;">
            <h5 style="color: #581c87; margin-top: 0;">💡 이렇게 읽으세요</h5>
            <p style="margin: 0; font-size: 15px; line-height: 1.8;">
                "publicationYear는 <strong>함수형 속성</strong>입니다. Book이 publicationYear 값을 가진다면, 그 값은 <strong>최대 1개</strong>여야 하며 연도 형식이어야 합니다."
            </p>
        </div>
    </div>

    <div style="background-color: #fef3c7; padding: 20px; border-radius: 8px; margin: 15px 0;">
        <h4 style="color: #78350f; margin-top: 0;">Inverse Property (역 속성)</h4>
        <p>양방향 관계를 자동으로 추론할 수 있습니다.</p>

        <div style="background-color: #fef08a; padding: 15px; border-radius: 6px; margin: 15px 0;">
            <h5 style="color: #713f12; margin-top: 0;">📖 실생활 예시</h5>
            <p style="margin: 5px 0;">책과 저자의 관계를 양쪽에서 표현할 수 있습니다.</p>
            <ul style="margin: 10px 0; padding-left: 20px;">
                <li><strong>hasAuthor</strong>: "이 책의 저자는 누구인가?" (책 → 저자)</li>
                <li><strong>authorOf</strong>: "이 사람이 쓴 책은 무엇인가?" (저자 → 책)</li>
            </ul>
            <p style="margin: 10px 0 0 0; font-size: 14px; color: #713f12;">
                <strong>💡 장점:</strong> 한 쪽만 입력하면 반대쪽은 자동으로 추론됩니다! 데이터 중복 입력 불필요.
            </p>
        </div>

        <div style="font-family: monospace; background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 14px;">
# 예: hasAuthor와 authorOf는 역관계
:hasAuthor rdf:type owl:ObjectProperty ;
           owl:inverseOf :authorOf .

# 만약 다음이 명시되면:
:Book123 :hasAuthor :JaneSmith .

# 자동으로 추론됨:
:JaneSmith :authorOf :Book123 .
        </div>

        <div style="background-color: #fff; padding: 15px; border-radius: 6px; margin-top: 15px; border-left: 4px solid #f59e0b;">
            <h5 style="color: #92400e; margin-top: 0;">🔍 코드 설명</h5>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #f59e0b; width: 40%;">owl:ObjectProperty</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">객체(개체) 간의 관계를 나타내는 속성</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb; font-family: monospace; color: #f59e0b;">owl:inverseOf</td>
                    <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">역관계를 정의</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-family: monospace; color: #f59e0b;">:authorOf</td>
                    <td style="padding: 8px;">hasAuthor의 역관계 속성</td>
                </tr>
            </table>
        </div>

        <div style="background-color: #fffbeb; padding: 15px; border-radius: 6px; margin-top: 15px;">
            <h5 style="color: #78350f; margin-top: 0;">💡 이렇게 읽으세요</h5>
            <p style="margin: 0; font-size: 15px; line-height: 1.8;">
                "hasAuthor 속성은 authorOf 속성의 <strong>역관계</strong>입니다. 만약 'A hasAuthor B'가 참이면, 'B authorOf A'도 자동으로 참입니다."
            </p>
        </div>

        <div style="background-color: #dbeafe; padding: 15px; border-radius: 6px; margin-top: 15px;">
            <h5 style="color: #1e40af; margin-top: 0;">🔄 추론 과정 시각화</h5>
            <div style="display: flex; align-items: center; gap: 15px; margin-top: 10px; flex-wrap: wrap;">
                <div style="background: white; padding: 12px; border-radius: 6px; border: 2px solid #3b82f6;">
                    <div style="font-family: monospace; color: #1e40af; font-size: 13px;">입력: Book123 → hasAuthor → JaneSmith</div>
                </div>
                <div style="font-size: 24px; color: #10b981;">⟹</div>
                <div style="background: #dcfce7; padding: 12px; border-radius: 6px; border: 2px solid #22c55e;">
                    <div style="font-family: monospace; color: #166534; font-size: 13px;">추론: JaneSmith → authorOf → Book123</div>
                </div>
            </div>
        </div>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        🧠 OWL의 추론 능력
    </h2>

    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: white; margin-top: 0;">추론이 가능한 이유</h3>
        <p style="margin: 10px 0;">
            OWL은 <strong>Description Logic(DL)</strong>을 기반으로 합니다.
            DL은 수학적으로 엄격하게 정의된 논리 체계로, 다음을 보장합니다:
        </p>
        <ul style="margin: 10px 0; padding-left: 20px;">
            <li><strong>Decidability</strong>: 추론이 유한한 시간 내에 완료됨</li>
            <li><strong>Soundness</strong>: 추론된 결과가 논리적으로 올바름</li>
            <li><strong>Completeness</strong>: 추론 가능한 모든 사실을 찾아냄</li>
        </ul>
    </div>

    <h3 style="color: #1e40af; margin-top: 30px;">도서관 분야 추론 예제</h3>

    <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 15px 0; border: 2px solid #3b82f6;">
        <h4 style="color: #1e40af; margin-top: 0;">🔍 시나리오: 도서관 자료 분류</h4>

        <div style="background-color: white; padding: 15px; border-radius: 6px; margin: 10px 0;">
            <h5 style="color: #0c4a6e;">온톨로지 정의</h5>
            <div style="font-family: monospace; background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 13px;">
# 클래스 정의
:LibraryResource rdf:type owl:Class .
:Book rdfs:subClassOf :LibraryResource .
:DigitalResource rdfs:subClassOf :LibraryResource .
:EBook owl:equivalentClass [
  rdf:type owl:Class ;
  owl:intersectionOf ( :Book :DigitalResource )
] .

# 속성 정의
:hasAuthor rdf:type owl:ObjectProperty ;
           owl:inverseOf :authorOf ;
           rdfs:domain :Book ;
           rdfs:range :Person .

:hasCopies rdf:type owl:DatatypeProperty ;
           rdfs:domain :Book ;
           rdfs:range xsd:integer .

# 제약 조건
:RareBook rdfs:subClassOf :Book ;
          rdfs:subClassOf [
            rdf:type owl:Restriction ;
            owl:onProperty :hasCopies ;
            owl:maxCardinality "3"^^xsd:nonNegativeInteger
          ] .
            </div>
        </div>

        <div style="background-color: #dbeafe; padding: 15px; border-radius: 6px; margin: 10px 0;">
            <h5 style="color: #0c4a6e;">명시적 데이터</h5>
            <div style="font-family: monospace; background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 13px;">
:Book456 rdf:type :Book , :DigitalResource ;
         :hasAuthor :KimYuna ;
         dc:title "도서관 정보학 입문" .

:RareBook789 rdf:type :RareBook ;
             :hasCopies "2"^^xsd:integer ;
             :hasAuthor :LeeMinho .
            </div>
        </div>

        <div style="background-color: #dcfce7; padding: 15px; border-radius: 6px; margin: 10px 0;">
            <h5 style="color: #14532d;">✨ 자동 추론 결과</h5>
            <div style="font-family: monospace; background-color: #1e293b; color: #22c55e; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 13px;">
# 1. 교집합 추론
:Book456 rdf:type :EBook .  # Book이면서 DigitalResource이므로

# 2. 역속성 추론
:KimYuna :authorOf :Book456 .  # hasAuthor의 역관계

# 3. 클래스 계층 추론
:RareBook789 rdf:type :Book .  # RareBook은 Book의 하위클래스
:RareBook789 rdf:type :LibraryResource .  # Book은 LibraryResource의 하위클래스

# 4. 제약 조건 검증
# :RareBook789의 hasCopies가 3 이하이므로 제약 조건 만족
            </div>
        </div>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        💻 실제 형식별 OWL 사용법
    </h2>

    <h3 style="color: #1e40af; margin-top: 30px;">1️⃣ RDF/XML 형식</h3>

    <div style="background-color: #fef2f2; padding: 20px; border-radius: 8px; margin: 15px 0;">
        <p style="margin-top: 0;">가장 전통적인 형식으로, XML의 구조화된 표현을 사용합니다.</p>
        <div style="font-family: monospace; background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 13px;">
&lt;?xml version="1.0"?&gt;
&lt;rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:lib="http://example.org/library#"&gt;

  &lt;!-- 온톨로지 선언 --&gt;
  &lt;owl:Ontology rdf:about="http://example.org/library"&gt;
    &lt;rdfs:label&gt;도서관 온톨로지&lt;/rdfs:label&gt;
  &lt;/owl:Ontology&gt;

  &lt;!-- 클래스 정의 --&gt;
  &lt;owl:Class rdf:about="http://example.org/library#Book"&gt;
    &lt;rdfs:label&gt;책&lt;/rdfs:label&gt;
    &lt;rdfs:subClassOf rdf:resource="http://example.org/library#LibraryResource"/&gt;
  &lt;/owl:Class&gt;

  &lt;!-- ObjectProperty 정의 --&gt;
  &lt;owl:ObjectProperty rdf:about="http://example.org/library#hasAuthor"&gt;
    &lt;rdfs:domain rdf:resource="http://example.org/library#Book"/&gt;
    &lt;rdfs:range rdf:resource="http://example.org/library#Person"/&gt;
    &lt;owl:inverseOf rdf:resource="http://example.org/library#authorOf"/&gt;
  &lt;/owl:ObjectProperty&gt;

  &lt;!-- Restriction을 사용한 클래스 정의 --&gt;
  &lt;owl:Class rdf:about="http://example.org/library#RareBook"&gt;
    &lt;rdfs:subClassOf rdf:resource="http://example.org/library#Book"/&gt;
    &lt;rdfs:subClassOf&gt;
      &lt;owl:Restriction&gt;
        &lt;owl:onProperty rdf:resource="http://example.org/library#hasCopies"/&gt;
        &lt;owl:maxCardinality rdf:datatype="http://www.w3.org/2001/XMLSchema#nonNegativeInteger"&gt;3&lt;/owl:maxCardinality&gt;
      &lt;/owl:Restriction&gt;
    &lt;/rdfs:subClassOf&gt;
  &lt;/owl:Class&gt;

  &lt;!-- 개체 선언 --&gt;
  &lt;lib:Book rdf:about="http://example.org/library#Book123"&gt;
    &lt;lib:hasAuthor rdf:resource="http://example.org/library#JohnDoe"/&gt;
    &lt;lib:hasISBN&gt;978-0-123456-78-9&lt;/lib:hasISBN&gt;
    &lt;lib:publicationYear rdf:datatype="http://www.w3.org/2001/XMLSchema#gYear"&gt;2023&lt;/lib:publicationYear&gt;
  &lt;/lib:Book&gt;

&lt;/rdf:RDF&gt;
        </div>
    </div>

    <h3 style="color: #1e40af; margin-top: 30px;">2️⃣ Turtle 형식</h3>

    <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin: 15px 0;">
        <p style="margin-top: 0;">사람이 읽기 쉬운 간결한 표현 방식입니다.</p>
        <div style="font-family: monospace; background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 13px;">
@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .
@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .
@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .
@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .
@prefix lib: &lt;http://example.org/library#&gt; .

# 온톨로지 선언
&lt;http://example.org/library&gt; rdf:type owl:Ontology ;
    rdfs:label "도서관 온톨로지" .

# 클래스 계층
lib:LibraryResource rdf:type owl:Class ;
    rdfs:label "도서관 자료" .

lib:Book rdf:type owl:Class ;
    rdfs:subClassOf lib:LibraryResource ;
    rdfs:label "책" .

lib:DigitalResource rdf:type owl:Class ;
    rdfs:subClassOf lib:LibraryResource ;
    rdfs:label "디지털 자료" .

# 교집합을 사용한 클래스 정의
lib:EBook rdf:type owl:Class ;
    owl:equivalentClass [
        rdf:type owl:Class ;
        owl:intersectionOf ( lib:Book lib:DigitalResource )
    ] ;
    rdfs:label "전자책" .

# ObjectProperty 정의
lib:hasAuthor rdf:type owl:ObjectProperty ;
    rdfs:domain lib:Book ;
    rdfs:range lib:Person ;
    owl:inverseOf lib:authorOf ;
    rdfs:label "저자" .

lib:authorOf rdf:type owl:ObjectProperty ;
    rdfs:domain lib:Person ;
    rdfs:range lib:Book ;
    rdfs:label "저술함" .

# FunctionalProperty
lib:hasISBN rdf:type owl:DatatypeProperty , owl:FunctionalProperty ;
    rdfs:domain lib:Book ;
    rdfs:range xsd:string ;
    rdfs:label "ISBN" .

# Restriction을 사용한 클래스
lib:RareBook rdf:type owl:Class ;
    rdfs:subClassOf lib:Book ;
    rdfs:subClassOf [
        rdf:type owl:Restriction ;
        owl:onProperty lib:hasCopies ;
        owl:maxCardinality "3"^^xsd:nonNegativeInteger
    ] ;
    rdfs:label "희귀본" .

# 개체 및 데이터
lib:Book123 rdf:type lib:Book ;
    lib:hasAuthor lib:JohnDoe ;
    lib:hasISBN "978-0-123456-78-9" ;
    lib:publicationYear "2023"^^xsd:gYear ;
    rdfs:label "시맨틱 웹 입문" .

lib:JohnDoe rdf:type lib:Person ;
    rdfs:label "존 도우" .

# EBook 예제 - 자동으로 EBook으로 추론됨
lib:DigitalBook456 rdf:type lib:Book , lib:DigitalResource ;
    lib:hasAuthor lib:JaneSmith ;
    rdfs:label "디지털 도서관학" .
        </div>
    </div>

    <h3 style="color: #1e40af; margin-top: 30px;">3️⃣ JSON-LD 형식</h3>

    <div style="background-color: #fef3c7; padding: 20px; border-radius: 8px; margin: 15px 0;">
        <p style="margin-top: 0;">웹 개발자에게 친숙한 JSON 형식으로 Linked Data를 표현합니다.</p>
        <div style="font-family: monospace; background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 13px;">
{
  "@context": {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "lib": "http://example.org/library#"
  },
  "@graph": [
    {
      "@id": "http://example.org/library",
      "@type": "owl:Ontology",
      "rdfs:label": "도서관 온톨로지"
    },
    {
      "@id": "lib:Book",
      "@type": "owl:Class",
      "rdfs:subClassOf": {"@id": "lib:LibraryResource"},
      "rdfs:label": "책"
    },
    {
      "@id": "lib:EBook",
      "@type": "owl:Class",
      "owl:equivalentClass": {
        "@type": "owl:Class",
        "owl:intersectionOf": {
          "@list": [
            {"@id": "lib:Book"},
            {"@id": "lib:DigitalResource"}
          ]
        }
      },
      "rdfs:label": "전자책"
    },
    {
      "@id": "lib:hasAuthor",
      "@type": "owl:ObjectProperty",
      "rdfs:domain": {"@id": "lib:Book"},
      "rdfs:range": {"@id": "lib:Person"},
      "owl:inverseOf": {"@id": "lib:authorOf"},
      "rdfs:label": "저자"
    },
    {
      "@id": "lib:hasISBN",
      "@type": ["owl:DatatypeProperty", "owl:FunctionalProperty"],
      "rdfs:domain": {"@id": "lib:Book"},
      "rdfs:range": {"@id": "xsd:string"},
      "rdfs:label": "ISBN"
    },
    {
      "@id": "lib:RareBook",
      "@type": "owl:Class",
      "rdfs:subClassOf": [
        {"@id": "lib:Book"},
        {
          "@type": "owl:Restriction",
          "owl:onProperty": {"@id": "lib:hasCopies"},
          "owl:maxCardinality": {
            "@value": "3",
            "@type": "xsd:nonNegativeInteger"
          }
        }
      ],
      "rdfs:label": "희귀본"
    },
    {
      "@id": "lib:Book123",
      "@type": "lib:Book",
      "lib:hasAuthor": {"@id": "lib:JohnDoe"},
      "lib:hasISBN": "978-0-123456-78-9",
      "lib:publicationYear": {
        "@value": "2023",
        "@type": "xsd:gYear"
      },
      "rdfs:label": "시맨틱 웹 입문"
    },
    {
      "@id": "lib:JohnDoe",
      "@type": "lib:Person",
      "rdfs:label": "존 도우"
    }
  ]
}
        </div>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        🏛️ 실무 활용 사례
    </h2>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px;">
            <h3 style="color: white; margin-top: 0;">📚 BIBFRAME</h3>
            <p style="margin: 10px 0; font-size: 14px;">
                미국 의회도서관이 개발한 서지 프레임워크. OWL을 사용하여
                Work, Instance, Item의 관계를 정의하고, 자동으로 서지 관계를 추론합니다.
            </p>
            <div style="background-color: rgba(255,255,255,0.2); padding: 10px; border-radius: 6px; font-size: 13px; margin-top: 10px;">
                <strong>사용 기술:</strong> OWL 2, SKOS, Dublin Core
            </div>
        </div>

        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 10px;">
            <h3 style="color: white; margin-top: 0;">🏥 SNOMED CT</h3>
            <p style="margin: 10px 0; font-size: 14px;">
                의료 용어 체계. OWL의 추론 능력을 활용하여
                질병, 증상, 치료법 간의 복잡한 관계를 자동으로 추론하고
                임상 의사결정을 지원합니다.
            </p>
            <div style="background-color: rgba(255,255,255,0.2); padding: 10px; border-radius: 6px; font-size: 13px; margin-top: 10px;">
                <strong>추론 활용:</strong> 질병 분류, 약물 상호작용 검출
            </div>
        </div>

        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 20px; border-radius: 10px;">
            <h3 style="color: white; margin-top: 0;">🔬 Gene Ontology</h3>
            <p style="margin: 10px 0; font-size: 14px;">
                생명과학 분야의 유전자 기능 온톨로지.
                OWL을 사용하여 유전자 간의 관계를 정의하고,
                생물학적 프로세스를 자동으로 분류합니다.
            </p>
            <div style="background-color: rgba(255,255,255,0.2); padding: 10px; border-radius: 6px; font-size: 13px; margin-top: 10px;">
                <strong>활용 분야:</strong> 유전자 주석, 단백질 기능 예측
            </div>
        </div>

        <div style="background: linear-gradient(135deg, #30cfd0 0%, #330867 100%); color: white; padding: 20px; border-radius: 10px;">
            <h3 style="color: white; margin-top: 0;">🌐 Schema.org</h3>
            <p style="margin: 10px 0; font-size: 14px;">
                웹 검색 엔진들이 공동으로 만든 온톨로지.
                OWL의 일부 개념을 사용하여 웹 페이지의 구조화된 데이터를
                표현하고, 검색 결과를 향상시킵니다.
            </p>
            <div style="background-color: rgba(255,255,255,0.2); padding: 10px; border-radius: 6px; font-size: 13px; margin-top: 10px;">
                <strong>사용 예:</strong> Book, Person, Organization 등
            </div>
        </div>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        🛠️ OWL 추론기 (Reasoners)
    </h2>

    <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <p style="margin-top: 0;">OWL 온톨로지를 분석하고 추론하는 대표적인 도구들:</p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
            <div style="background-color: white; padding: 15px; border-left: 4px solid #3b82f6; border-radius: 4px;">
                <h4 style="color: #1e40af; margin: 0 0 10px 0;">HermiT</h4>
                <p style="margin: 0; font-size: 14px;">첫 번째 완전한 OWL 2 추론기. Hypertableau 알고리즘 사용</p>
            </div>
            <div style="background-color: white; padding: 15px; border-left: 4px solid #8b5cf6; border-radius: 4px;">
                <h4 style="color: #6d28d9; margin: 0 0 10px 0;">Pellet</h4>
                <p style="margin: 0; font-size: 14px;">Java 기반 추론기. OWL 2, SWRL 규칙 지원</p>
            </div>
            <div style="background-color: white; padding: 15px; border-left: 4px solid #ec4899; border-radius: 4px;">
                <h4 style="color: #be185d; margin: 0 0 10px 0;">Fact++</h4>
                <p style="margin: 0; font-size: 14px;">C++ 기반 고성능 추론기. 대규모 온톨로지에 적합</p>
            </div>
            <div style="background-color: white; padding: 15px; border-left: 4px solid #f59e0b; border-radius: 4px;">
                <h4 style="color: #92400e; margin: 0 0 10px 0;">Apache Jena</h4>
                <p style="margin: 0; font-size: 14px;">Java 프레임워크. 내장 추론기 및 SPARQL 지원</p>
            </div>
        </div>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        📋 OWL 사용 가이드라인
    </h2>

    <div style="background-color: #ecfdf5; border: 2px solid #10b981; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #065f46; margin-top: 0;">✅ OWL을 사용해야 할 때</h3>
        <ul style="margin: 10px 0; padding-left: 25px;">
            <li>복잡한 클래스 관계를 표현해야 할 때</li>
            <li>자동 추론이 필요한 지식 베이스를 구축할 때</li>
            <li>엄격한 제약 조건을 정의해야 할 때</li>
            <li>도메인 전문가와 논리적으로 정확한 의사소통이 필요할 때</li>
        </ul>
    </div>

    <div style="background-color: #fef2f2; border: 2px solid #ef4444; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #991b1b; margin-top: 0;">⚠️ OWL 사용을 재고해야 할 때</h3>
        <ul style="margin: 10px 0; padding-left: 25px;">
            <li>단순한 분류 체계만 필요할 때 (RDFS로 충분)</li>
            <li>추론이 필요하지 않고 데이터 저장만 필요할 때</li>
            <li>성능이 매우 중요하고 대용량 실시간 처리가 필요할 때</li>
            <li>개발팀이 시맨틱 웹 기술에 익숙하지 않을 때</li>
        </ul>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        🎓 학습 정리
    </h2>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: white; margin-top: 0;">핵심 포인트</h3>
        <ol style="margin: 10px 0; padding-left: 25px; line-height: 2;">
            <li><strong>OWL은 RDFS의 확장</strong>이며, 더 풍부한 의미론을 제공합니다.</li>
            <li><strong>Description Logic 기반</strong>으로 수학적으로 정확한 추론이 가능합니다.</li>
            <li><strong>클래스 표현력</strong>: 교집합, 합집합, 여집합 등 복잡한 클래스 정의 가능</li>
            <li><strong>속성 제약</strong>: cardinality, functional, inverse 등 다양한 제약 조건 표현</li>
            <li><strong>자동 추론</strong>: 명시적 지식으로부터 암묵적 지식을 자동으로 도출</li>
            <li><strong>다양한 형식</strong>: RDF/XML, Turtle, JSON-LD로 표현 가능</li>
            <li><strong>실무 활용</strong>: BIBFRAME, SNOMED CT, Gene Ontology 등에서 사용</li>
        </ol>
    </div>

    <div style="background-color: #f0f9ff; border-left: 4px solid #3b82f6; padding: 20px; margin: 20px 0;">
        <h3 style="color: #1e40af; margin-top: 0;">💡 다음 단계</h3>
        <p style="margin: 10px 0;">
            OWL의 기본 개념을 이해했다면, 다음 단계로 나아가세요:
        </p>
        <ul style="margin: 10px 0; padding-left: 25px;">
            <li>Protégé 편집기를 사용하여 직접 온톨로지 설계해보기</li>
            <li>Apache Jena나 RDFLib를 사용하여 프로그래밍하기</li>
            <li>SPARQL을 학습하여 온톨로지 쿼리하기</li>
            <li>SWRL(Semantic Web Rule Language)로 규칙 정의하기</li>
            <li>실제 도메인(도서관, 의료, 교육 등)의 온톨로지 분석하기</li>
        </ul>
    </div>

    <div style="background-color: #fef3c7; padding: 20px; border-radius: 8px; text-align: center; margin-top: 40px;">
        <p style="margin: 0; font-size: 18px; color: #78350f;">
            <strong>🦉 OWL로 지능형 지식 시스템을 구축하세요!</strong>
        </p>
        <p style="margin: 10px 0 0 0; color: #92400e;">
            복잡한 지식도 OWL과 추론기가 자동으로 정리해줍니다.
        </p>
    </div>
</div>
"""
)

# 태그 추가
content.tags.set(tags)
print(f"\n✓ OWL 콘텐츠 생성 완료!")
print(f"  - 제목: {content.title}")
print(f"  - 카테고리: {content.category.name}")
print(f"  - 난이도: {content.difficulty}")
print(f"  - 예상 학습시간: {content.estimated_time}분")
print(f"  - 태그: {', '.join([tag.name for tag in content.tags.all()])}")
print(f"\n콘텐츠가 성공적으로 추가되었습니다!")
