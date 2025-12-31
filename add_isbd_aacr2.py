#!/usr/bin/env python
"""
ISBD vs AACR2 비교 콘텐츠 생성 스크립트
"""
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

# 한눈에 보기 카테고리 찾기
overview_category = Category.objects.filter(slug='overview').first()
if not overview_category:
    print("한눈에 보기 카테고리를 찾을 수 없습니다.")
    sys.exit(1)

# 태그 데이터
tag_data = [
    {'name': 'ISBD', 'slug': 'isbd'},
    {'name': 'AACR2', 'slug': 'aacr2'},
    {'name': '목록규칙', 'slug': 'cataloging-rules'},
    {'name': '서지기술', 'slug': 'bibliographic-description'},
    {'name': 'RDA', 'slug': 'rda'},
    {'name': '비교', 'slug': 'comparison'},
]

# 태그 생성
tags = []
for tag_info in tag_data:
    try:
        tag = Tag.objects.get(slug=tag_info['slug'])
        print(f"✓ 기존 태그 사용 (slug): {tag.name}")
    except Tag.DoesNotExist:
        try:
            tag = Tag.objects.get(name=tag_info['name'])
            print(f"✓ 기존 태그 사용 (name): {tag.name}")
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=tag_info['name'], slug=tag_info['slug'])
            print(f"✓ 태그 생성됨: {tag.name}")
    tags.append(tag)

# 콘텐츠 생성
content, created = Content.objects.update_or_create(
    slug='isbd-vs-aacr2',
    defaults={
        'title': 'ISBD와 AACR2는 뭐가 달라?',
        'category': overview_category,
        'author': admin,
        'difficulty': 'BEGINNER',
        'estimated_time': 25,
        'status': Content.Status.PUBLISHED,
        'summary': 'ISBD와 AACR2의 차이점을 쉽고 명확하게 이해합니다. 표시 표준과 목록 규칙의 차이, 실제 예제를 통한 비교, RDA로의 발전 과정까지 한눈에 파악할 수 있습니다.',
        'prerequisites': '없음 (처음 배우는 분도 쉽게 이해할 수 있습니다)',
        'learning_objectives': 'ISBD와 AACR2의 핵심 차이 이해하기, 표시 표준과 목록 규칙의 역할 구분하기, 실제 예제로 차이점 확인하기, RDA와 BIBFRAME으로의 발전 흐름 파악하기',
        'content_html': """
<div style="font-family: 'Noto Sans KR', sans-serif; line-height: 1.8; max-width: 1200px; margin: 0 auto; padding: 20px;">

  <h1 style="color: #1a1a1a; border-bottom: 3px solid #2563eb; padding-bottom: 10px; margin-bottom: 30px;">
    📚 ISBD와 AACR2는 뭐가 달라?
  </h1>

  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; margin-bottom: 30px;">
    <h2 style="color: white; margin-top: 0;">💡 한 줄 요약</h2>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
      <div style="background-color: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px;">
        <h3 style="color: white; margin-top: 0; font-size: 18px;">ISBD (국제표준서지기술)</h3>
        <p style="margin: 0; font-size: 15px;">
          서지기술을 <strong>"어떤 순서·구두점으로 보여줄지"</strong> 정한 <strong>국제 표시 표준</strong>
        </p>
      </div>
      <div style="background-color: rgba(255,255,255,0.2); padding: 15px; border-radius: 8px;">
        <h3 style="color: white; margin-top: 0; font-size: 18px;">AACR2 (영미목록규칙 2판)</h3>
        <p style="margin: 0; font-size: 15px;">
          서지를 <strong>"무엇을·어떻게 기록하고 접근점을 어떻게 정할지"</strong> 정한 <strong>목록 규칙</strong>
        </p>
      </div>
    </div>
  </div>

  <div class="content-section">
    <h2>🎯 핵심 차이 한눈에 보기</h2>

    <div style="background-color: #f0f9ff; padding: 25px; border-radius: 10px; margin: 20px 0;">
      <p style="font-size: 18px; font-weight: bold; color: #1e40af; margin-top: 0;">
        핵심은 <span style="color: #dc2626;">"표시 방식 중심이냐, 목록 규칙 전반이냐"</span>의 차이입니다!
      </p>
    </div>

    <table class="comparison-table">
      <thead>
        <tr>
          <th>구분</th>
          <th style="background-color: #3b82f6;">ISBD (SBD)</th>
          <th style="background-color: #8b5cf6;">AACR2</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>성격</strong></td>
          <td>서지 <strong>표시(표기) 표준</strong></td>
          <td><strong>목록 규칙</strong> (기술 + 접근점)</td>
        </tr>
        <tr>
          <td><strong>제정 기관</strong></td>
          <td>IFLA (국제도서관연맹)</td>
          <td>Anglo-American (ALA/LC 등)</td>
        </tr>
        <tr>
          <td><strong>핵심 초점</strong></td>
          <td><strong>순서 + 구두점</strong></td>
          <td><strong>기술 규칙 + 접근점 규칙</strong></td>
        </tr>
        <tr>
          <td><strong>구두점 규정</strong></td>
          <td>✔️ 매우 중요 (<code>: / ; , . —</code>)</td>
          <td>✔️ ISBD와 정합 고려</td>
        </tr>
        <tr>
          <td><strong>접근점(저자/표목)</strong></td>
          <td>❌ 다루지 않음</td>
          <td>✔️ 핵심 내용</td>
        </tr>
        <tr>
          <td><strong>MARC와 관계</strong></td>
          <td>표시 원칙 제공</td>
          <td>실제 목록 작성에 직접 사용</td>
        </tr>
        <tr>
          <td><strong>현재 위치</strong></td>
          <td>여전히 참고/유지</td>
          <td><strong>RDA로 대체됨</strong></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="content-section">
    <h2>🔍 조금 더 자세히 알아보기</h2>

    <div class="info-card" style="background-color: #dbeafe; border-left: 4px solid #3b82f6;">
      <h3 style="color: #1e40af; margin-top: 0;">1️⃣ ISBD는 무엇을 하나요?</h3>

      <p><strong>서지기술의 "출력 모습"을 국제적으로 통일</strong>합니다.</p>

      <ul>
        <li>요소를 <strong>영역(Area)</strong>으로 나누고</li>
        <li>각 영역 사이를 <strong>표준 구두점</strong>으로 구분합니다</li>
      </ul>

      <div style="background-color: white; padding: 15px; border-radius: 8px; margin: 15px 0;">
        <h4 style="color: #1e40af; margin-top: 0;">ISBD 구두점 예시</h4>
        <div style="font-family: monospace; font-size: 14px; line-height: 2; background-color: #f8fafc; padding: 15px; border-radius: 6px;">
          <strong style="color: #dc2626;">82년생 김지영</strong> <span style="color: #059669;">:</span>
          <em style="color: #7c3aed;">소설</em> <span style="color: #059669;">/</span>
          조남주 지음. <span style="color: #059669;">—</span>
          서울 <span style="color: #059669;">:</span>
          민음사, <span style="color: #059669;">2016</span>
        </div>
        <div style="margin-top: 10px; font-size: 14px; color: #475569;">
          <ul style="list-style: none; padding-left: 0;">
            <li>• <code>:</code> = 기타표제정보 앞</li>
            <li>• <code>/</code> = 책임표시 앞</li>
            <li>• <code>. —</code> = 영역 구분</li>
            <li>• <code>:</code> = 발행처 앞</li>
            <li>• <code>,</code> = 발행연도 앞</li>
          </ul>
        </div>
      </div>

      <div style="background-color: #fef3c7; padding: 15px; border-radius: 8px;">
        <p style="margin: 0; color: #92400e;">
          <strong>👉 ISBD는 "이 정보를 이렇게 <u>보이게</u> 하자"에 초점</strong>
        </p>
      </div>
    </div>

    <div class="info-card" style="background-color: #ede9fe; border-left: 4px solid #8b5cf6; margin-top: 25px;">
      <h3 style="color: #5b21b6; margin-top: 0;">2️⃣ AACR2는 무엇을 하나요?</h3>

      <p>목록 작성의 <strong>전 과정</strong>을 규정합니다:</p>

      <ul>
        <li>✅ <strong>어떤 요소를 기록할지</strong></li>
        <li>✅ <strong>어떤 형태로 전사할지</strong></li>
        <li>✅ <strong>주표목/부출표목을 무엇으로 잡을지</strong></li>
        <li>✅ 자료 유형별(단행본, 연속간행물, 지도, 음반 등) 규칙 제공</li>
      </ul>

      <div style="background-color: white; padding: 15px; border-radius: 8px; margin: 15px 0;">
        <h4 style="color: #5b21b6; margin-top: 0;">AACR2가 다루는 내용 예시</h4>

        <table style="width: 100%; border-collapse: collapse; background-color: #fafafa;">
          <tr style="background-color: #8b5cf6; color: white;">
            <th style="padding: 10px; text-align: left;">질문</th>
            <th style="padding: 10px; text-align: left;">AACR2의 답변</th>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">저자가 3명일 때?</td>
            <td style="padding: 10px; border: 1px solid #ddd;">첫 번째 저자를 주표목으로, 나머지는 부출표목</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">제2판을 어떻게 표기?</td>
            <td style="padding: 10px; border: 1px solid #ddd;">자료에 나타난 대로 "제2판" 또는 "2nd ed."</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">발행지가 없으면?</td>
            <td style="padding: 10px; border: 1px solid #ddd;">[S.l.] (Sine loco) 사용</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">단체명이 저자면?</td>
            <td style="padding: 10px; border: 1px solid #ddd;">일정 조건 만족 시 주표목으로 선정</td>
          </tr>
        </table>
      </div>

      <div style="background-color: #fef3c7; padding: 15px; border-radius: 8px;">
        <p style="margin: 0; color: #92400e;">
          <strong>👉 AACR2는 "이 자료를 어떻게 <u>목록으로 만들지</u>" 전반을 다룸</strong>
        </p>
      </div>
    </div>
  </div>

  <div class="content-section">
    <h2>🎨 비유로 이해하기</h2>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
      <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 20px; border-radius: 10px;">
        <h3 style="color: white; margin-top: 0; text-align: center;">📐 ISBD</h3>
        <div style="text-align: center; font-size: 48px; margin: 20px 0;">📄</div>
        <p style="text-align: center; font-size: 15px; margin: 0;">
          <strong>"출판물 표지 디자인 가이드"</strong><br/>
          (레이아웃·구두점 규칙)
        </p>
      </div>

      <div style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); color: white; padding: 20px; border-radius: 10px;">
        <h3 style="color: white; margin-top: 0; text-align: center;">📋 AACR2</h3>
        <div style="text-align: center; font-size: 48px; margin: 20px 0;">📚</div>
        <p style="text-align: center; font-size: 15px; margin: 0;">
          <strong>"편집·편성·저자 표기까지<br/>포함한 편집 규칙집"</strong>
        </p>
      </div>
    </div>

    <div style="background-color: #ecfdf5; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981; margin-top: 20px;">
      <h4 style="color: #065f46; margin-top: 0;">📌 역사적으로는</h4>
      <p style="font-size: 16px; margin: 10px 0;">
        <strong style="color: #047857;">AACR2로 기술하되, ISBD의 표시·구두점을 따르는</strong> 방식이 널리 쓰였습니다.
      </p>
      <p style="margin: 10px 0; color: #065f46;">
        즉, AACR2가 "무엇을 어떻게 기록할지" 정하고, ISBD가 "그것을 어떻게 표시할지" 정한 것이죠!
      </p>
    </div>
  </div>

  <div class="content-section">
    <h2>📖 실제 예제로 비교하기</h2>

    <div style="background-color: #fff7ed; padding: 20px; border-radius: 10px; margin: 20px 0;">
      <h3 style="color: #9a3412; margin-top: 0;">예제 도서</h3>
      <div style="background-color: white; padding: 15px; border-radius: 8px;">
        <ul>
          <li><strong>표제</strong>: 해리 포터와 마법사의 돌</li>
          <li><strong>저자</strong>: J. K. Rowling</li>
          <li><strong>역자</strong>: 김혜원</li>
          <li><strong>출판사</strong>: 문학수첩</li>
          <li><strong>출판연도</strong>: 1999</li>
          <li><strong>페이지</strong>: 416 p.</li>
        </ul>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
      <div style="background-color: #dbeafe; padding: 20px; border-radius: 10px;">
        <h4 style="color: #1e40af; margin-top: 0;">ISBD의 관심사</h4>
        <ul style="line-height: 2;">
          <li>표제와 책임표시 사이에 <code>/</code> 넣기</li>
          <li>각 영역을 <code>. —</code>으로 구분하기</li>
          <li>발행지와 발행처를 <code>:</code>으로 구분하기</li>
          <li>발행처와 발행연도를 <code>,</code>로 구분하기</li>
          <li>페이지와 크기를 <code>;</code>로 구분하기</li>
        </ul>
        <div style="background-color: white; padding: 12px; border-radius: 6px; margin-top: 10px; font-family: monospace; font-size: 13px; line-height: 1.8;">
          해리 포터와 마법사의 돌 / J. K. Rowling 지음 ; 김혜원 옮김. — 서울 : 문학수첩, 1999. — 416 p.
        </div>
      </div>

      <div style="background-color: #ede9fe; padding: 20px; border-radius: 10px;">
        <h4 style="color: #5b21b6; margin-top: 0;">AACR2의 관심사</h4>
        <ul style="line-height: 2;">
          <li>저자를 주표목으로 할지 결정</li>
          <li>저자명을 "성, 이름" 형식으로 정리</li>
          <li>역자를 부출표목으로 추가</li>
          <li>표제의 전사 규칙 적용</li>
          <li>발행사항의 정보원 확인</li>
        </ul>
        <div style="background-color: white; padding: 12px; border-radius: 6px; margin-top: 10px; font-size: 13px; line-height: 1.8;">
          <strong style="color: #7c3aed;">주표목:</strong> Rowling, J. K.<br/>
          <strong style="color: #7c3aed;">표제:</strong> 해리 포터와 마법사의 돌<br/>
          <strong style="color: #7c3aed;">책임표시:</strong> J. K. Rowling 지음 ; 김혜원 옮김<br/>
          <strong style="color: #7c3aed;">부출표목:</strong> 김혜원 (역자)
        </div>
      </div>
    </div>
  </div>

  <div class="content-section">
    <h2>🔄 현재 관점에서의 위치</h2>

    <div style="background-color: #f0fdf4; padding: 20px; border-radius: 10px; margin: 20px 0;">
      <h3 style="color: #065f46; margin-top: 0;">현재 상황</h3>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
        <div style="background-color: white; padding: 15px; border-radius: 8px; border-left: 3px solid #3b82f6;">
          <h4 style="color: #1e40af; margin-top: 0;">ISBD</h4>
          <p style="margin: 0;">여전히 <strong>'표시 원칙'으로 참고</strong>됩니다.</p>
          <p style="margin: 10px 0 0 0; font-size: 14px; color: #64748b;">
            MARC 환경에서는 ISBD 구두점 관행이 관성적으로 유지되는 경우가 많습니다.
          </p>
        </div>

        <div style="background-color: white; padding: 15px; border-radius: 8px; border-left: 3px solid #8b5cf6;">
          <h4 style="color: #5b21b6; margin-top: 0;">AACR2</h4>
          <p style="margin: 0;"><strong>RDA로 대체</strong>되었습니다.</p>
          <p style="margin: 10px 0 0 0; font-size: 14px; color: #64748b;">
            2010년대부터 RDA(Resource Description and Access)가 새로운 표준이 되었습니다.
          </p>
        </div>
      </div>
    </div>

    <div style="background-color: #fef3c7; padding: 20px; border-radius: 10px; margin: 20px 0;">
      <h3 style="color: #92400e; margin-top: 0;">💡 왜 AACR2가 RDA로 바뀌었나요?</h3>

      <table class="comparison-table">
        <thead>
          <tr>
            <th>구분</th>
            <th>AACR2</th>
            <th>RDA</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>기반 모델</strong></td>
            <td>없음 (경험 기반 규칙)</td>
            <td>FRBR/FRAD 개념 모델</td>
          </tr>
          <tr>
            <td><strong>초점</strong></td>
            <td>카드 목록 중심</td>
            <td>디지털 환경 중심</td>
          </tr>
          <tr>
            <td><strong>유연성</strong></td>
            <td>규정적 (prescriptive)</td>
            <td>원칙 기반 (principle-based)</td>
          </tr>
          <tr>
            <td><strong>구두점</strong></td>
            <td>ISBD 구두점 필수</td>
            <td>선택사항 (표시 규칙과 분리)</td>
          </tr>
          <tr>
            <td><strong>관계 표현</strong></td>
            <td>제한적</td>
            <td>명시적 관계 표현</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div style="background-color: #fef2f2; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #dc2626;">
      <h3 style="color: #991b1b; margin-top: 0;">🚀 그럼 BIBFRAME은?</h3>
      <p style="margin: 10px 0;">
        <strong>BIBFRAME</strong>은 MARC을 대체하기 위한 <strong>데이터 모델</strong>입니다.
      </p>
      <ul>
        <li><strong>ISBD 구두점이 약해지는 이유:</strong> BIBFRAME은 구조화된 데이터를 사용하므로 "보이는 방식"보다 "데이터 관계"가 중요합니다.</li>
        <li><strong>RDA와의 관계:</strong> RDA는 목록 규칙, BIBFRAME은 데이터 표현 방식</li>
        <li><strong>미래 방향:</strong> RDA 규칙 + BIBFRAME 데이터 모델 조합이 차세대 표준</li>
      </ul>
    </div>
  </div>

  <div class="content-section">
    <h2>📝 최종 정리</h2>

    <div style="background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin: 30px 0;">
      <h3 style="color: white; font-size: 24px; margin-top: 0;">핵심 한 문장</h3>
      <p style="font-size: 20px; line-height: 1.8; margin: 20px 0;">
        <strong>ISBD는 "어떻게 보이게 할지",<br/>
        AACR2는 "무엇을 어떻게 목록으로 만들지"를 정합니다.</strong>
      </p>
    </div>

    <div class="summary-box">
      <h3 style="color: #1e40af;">🎯 요약 체크리스트</h3>
      <ul style="line-height: 2;">
        <li>✅ <strong>ISBD</strong>: 국제 표시 표준 (순서 + 구두점)</li>
        <li>✅ <strong>AACR2</strong>: 목록 규칙 (기술 + 접근점)</li>
        <li>✅ 역사적으로 <strong>AACR2 + ISBD 구두점</strong> 조합 사용</li>
        <li>✅ AACR2는 <strong>RDA로 계승</strong>됨</li>
        <li>✅ ISBD는 여전히 <strong>표시 원칙으로 참고</strong></li>
        <li>✅ 미래는 <strong>RDA + BIBFRAME</strong> 조합</li>
      </ul>
    </div>
  </div>

  <div class="content-section">
    <h2>🎓 퀴즈로 확인하기</h2>

    <div class="quiz-section">
      <div class="quiz-item">
        <p><strong>Q1.</strong> "245 필드에서 $c 앞에 / 를 넣는 규칙"은 어디에서 나온 것인가요?</p>
        <details>
          <summary>정답 보기</summary>
          <p>✓ <strong>ISBD</strong>입니다. 책임표시 앞에 <code>/</code>를 넣는 것은 ISBD의 표시 규칙입니다.</p>
        </details>
      </div>

      <div class="quiz-item">
        <p><strong>Q2.</strong> "저자가 3명일 때 누구를 주표목으로 할지"는 어디에서 정하나요?</p>
        <details>
          <summary>정답 보기</summary>
          <p>✓ <strong>AACR2 (또는 RDA)</strong>입니다. 접근점(표목) 선정은 목록 규칙의 영역입니다.</p>
        </details>
      </div>

      <div class="quiz-item">
        <p><strong>Q3.</strong> AACR2를 대체한 새로운 목록 규칙은 무엇인가요?</p>
        <details>
          <summary>정답 보기</summary>
          <p>✓ <strong>RDA (Resource Description and Access)</strong>입니다.</p>
        </details>
      </div>

      <div class="quiz-item">
        <p><strong>Q4.</strong> MARC을 대체하기 위한 차세대 데이터 모델은?</p>
        <details>
          <summary>정답 보기</summary>
          <p>✓ <strong>BIBFRAME (Bibliographic Framework)</strong>입니다.</p>
        </details>
      </div>

      <div class="quiz-item">
        <p><strong>Q5.</strong> "영역 구분자 . —"는 어느 표준에서 정의하나요?</p>
        <details>
          <summary>정답 보기</summary>
          <p>✓ <strong>ISBD</strong>입니다. 각 영역(Area)을 구분하는 구두점입니다.</p>
        </details>
      </div>
    </div>
  </div>

  <div class="content-section">
    <h2>📚 더 알아보기</h2>
    <ul>
      <li><strong>ISBD</strong> - International Standard Bibliographic Description (IFLA)</li>
      <li><strong>AACR2</strong> - Anglo-American Cataloguing Rules, 2nd edition</li>
      <li><strong>RDA</strong> - Resource Description and Access</li>
      <li><strong>BIBFRAME</strong> - Bibliographic Framework (Library of Congress)</li>
      <li><strong>FRBR</strong> - Functional Requirements for Bibliographic Records</li>
    </ul>
  </div>

</div>

<style>
.content-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.comparison-table th,
.comparison-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.comparison-table th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.comparison-table tr:nth-child(even) {
  background: #f5f5f5;
}

.info-card {
  padding: 20px;
  border-radius: 10px;
  margin: 20px 0;
}

.summary-box {
  background-color: #e0f2fe;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #0284c7;
  margin: 20px 0;
}

.quiz-section {
  background-color: #f1f8e9;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.quiz-item {
  background: white;
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
  border-left: 3px solid #8bc34a;
}

.quiz-item details {
  margin-top: 0.5rem;
}

.quiz-item summary {
  cursor: pointer;
  color: #558b2f;
  font-weight: bold;
}

h2 {
  color: #1565c0;
  border-bottom: 2px solid #1565c0;
  padding-bottom: 0.5rem;
  margin-top: 2rem;
}

h3 {
  color: #1976d2;
  margin-top: 1.5rem;
}

code {
  background-color: #f3f4f6;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: monospace;
  color: #dc2626;
  font-size: 0.95em;
}

ul, ol {
  line-height: 1.8;
}

@media (max-width: 768px) {
  div[style*="grid-template-columns"] {
    grid-template-columns: 1fr !important;
  }
}
</style>
"""
    }
)

# 태그 연결
content.tags.set(tags)

if created:
    print("\n✓ ISBD vs AACR2 콘텐츠 생성 완료!")
else:
    print("\n✓ ISBD vs AACR2 콘텐츠 업데이트 완료!")

print(f"  - 제목: {content.title}")
print(f"  - 카테고리: {content.category.name}")
print(f"  - 난이도: {content.difficulty}")
print(f"  - 예상 학습시간: {content.estimated_time}분")
print(f"  - 태그: {', '.join([tag.name for tag in content.tags.all()])}")
print(f"\n확인: http://localhost:3000/contents/{content.slug}")
