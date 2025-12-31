#!/usr/bin/env python
"""
RDA vs MARC 비교 학습 콘텐츠 추가 스크립트
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

def create_rda_marc_comparison():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 가져오기: 한눈에 보기
    overview_category = Category.objects.get(slug='overview')
    print("✓ 상위 카테고리 확인: 한눈에 보기")

    # 하위 카테고리 가져오기: 포맷 비교
    comparison_category = Category.objects.get(slug='format-comparison')
    print("✓ 하위 카테고리 확인: 포맷 비교")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': 'RDA', 'slug': 'rda'},
        {'name': 'MARC', 'slug': 'marc'},
        {'name': '목록규칙', 'slug': 'cataloging-rules'},
        {'name': '메타데이터', 'slug': 'metadata'},
        {'name': '인코딩', 'slug': 'encoding'},
        {'name': '서지기술', 'slug': 'bibliographic-description'}
    ]
    tags = []
    for tag_info in tag_data:
        tag, created = Tag.objects.get_or_create(
            name=tag_info['name'],
            defaults={'slug': tag_info['slug']}
        )
        tags.append(tag)
        print(f"  ✓ 태그 확인: {tag_info['name']}")

    # 학습 콘텐츠 생성
    content = Content.objects.create(
        title="RDA랑 MARC는 뭐가 달라?",
        slug="rda-vs-marc-comparison",
        summary="같이 쓰는데 헷갈리는 RDA와 MARC! 하나는 '규칙'이고 하나는 '포맷'이에요. 둘의 관계를 쉽게 이해하고 실전 예제로 명쾌하게 배워봅시다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>RDA와 MARC의 근본적인 차이 이해하기</li>
    <li>RDA는 2층, MARC는 4층임을 알기</li>
    <li>RDA 규칙이 MARC 필드로 어떻게 바뀌는지 알기</li>
    <li>실전에서 RDA와 MARC를 함께 사용하는 방법 익히기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. 한 줄 정리: 둘이 뭐가 달라?</h2>

  <div class="one-liner">
    <div class="concept-box rda-box">
      <h3>📋 RDA</h3>
      <p class="role">규칙 (Rule)</p>
      <p class="description"><strong>"무엇을 어떻게 기술할지"</strong> 정하는 가이드북</p>
      <div class="example-box">
        <p class="example-title">💡 예시</p>
        <p>"저자 이름은 <strong>'성, 이름'</strong> 순서로 쓴다"<br>
        "출판사는 <strong>생략하지 말고 정식 명칭</strong>으로 쓴다"</p>
      </div>
    </div>

    <div class="concept-box marc-box">
      <h3>💾 MARC</h3>
      <p class="role">포맷 (Format)</p>
      <p class="description"><strong>"그 내용을 어느 필드에 담을지"</strong> 정하는 상자</p>
      <div class="example-box">
        <p class="example-title">💡 예시</p>
        <p>저자 이름은 <strong>100 필드 $a</strong>에 넣는다<br>
        출판사는 <strong>264 필드 $b</strong>에 넣는다</p>
      </div>
    </div>
  </div>

  <div class="relationship-box">
    <h4>🔗 둘의 관계</h4>
    <p class="big-text">RDA로 <strong>내용을 작성</strong>하고, MARC로 <strong>필드에 담는다</strong>!</p>
    <p>마치 <strong>레시피(RDA)</strong>대로 요리한 다음, <strong>도시락통(MARC)</strong>에 담는 것과 같아요.</p>
  </div>
</div>

<div class="content-section">
  <h2>2. 4층 구조에서 보는 위치</h2>

  <div class="architecture-visual">
    <div class="layer layer-1">
      <div class="layer-number">1층</div>
      <div class="layer-title">개념 모델</div>
      <div class="layer-tech">FRBR / LRM</div>
      <div class="layer-desc">"책이란 무엇인가?" 철학적 틀</div>
    </div>

    <div class="layer layer-2 highlighted">
      <div class="layer-number">2층</div>
      <div class="layer-title">콘텐츠 표준 (규칙)</div>
      <div class="layer-tech rda-highlight">⭐ RDA ⭐</div>
      <div class="layer-desc">"어떻게 기술할까?" 작업 매뉴얼</div>
    </div>

    <div class="layer layer-3">
      <div class="layer-number">3층</div>
      <div class="layer-title">데이터 모델</div>
      <div class="layer-tech">BIBFRAME (RDF)</div>
      <div class="layer-desc">"웹에서 어떻게 연결할까?" 그래프</div>
    </div>

    <div class="layer layer-4 highlighted">
      <div class="layer-number">4층</div>
      <div class="layer-title">인코딩 포맷</div>
      <div class="layer-tech marc-highlight">⭐ MARC 21 ⭐</div>
      <div class="layer-desc">"어떻게 담아 보낼까?" 교환 상자</div>
    </div>
  </div>

  <div class="key-point">
    <h4>💡 핵심 포인트</h4>
    <ul>
      <li><strong>RDA (2층)</strong>: 목록 담당자가 따라야 할 <strong>규칙·지침</strong></li>
      <li><strong>MARC (4층)</strong>: 그 규칙대로 쓴 내용을 담을 <strong>필드 구조</strong></li>
      <li>둘은 <strong>2개 층을 건너뛰고</strong> 함께 사용됩니다!</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>3. 구체적으로 뭐가 다른데?</h2>

  <table class="comparison-table">
    <thead>
      <tr>
        <th>비교 항목</th>
        <th>RDA<br>(2층: 규칙)</th>
        <th>MARC 21<br>(4층: 포맷)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>정체</strong></td>
        <td>목록 작성 규칙</td>
        <td>레코드 교환 포맷</td>
      </tr>
      <tr>
        <td><strong>목적</strong></td>
        <td><em>무엇을</em> 쓸지 정함</td>
        <td><em>어디에</em> 담을지 정함</td>
      </tr>
      <tr>
        <td><strong>형태</strong></td>
        <td>텍스트 지침서<br>(RDA Toolkit)</td>
        <td>태그-필드 구조<br>(001, 100, 245...)</td>
      </tr>
      <tr>
        <td><strong>사용자</strong></td>
        <td>목록 담당자<br>(사서)</td>
        <td>시스템 개발자<br>+ 목록 담당자</td>
      </tr>
      <tr>
        <td><strong>역할</strong></td>
        <td>내용 결정</td>
        <td>구조 제공</td>
      </tr>
      <tr>
        <td><strong>예시</strong></td>
        <td>"저자명은 성, 이름 순"</td>
        <td>"저자명은 100 $a에"</td>
      </tr>
    </tbody>
  </table>

  <div class="analogy-box">
    <h4>🎨 쉬운 비유</h4>
    <div class="analogy-grid">
      <div class="analogy-item">
        <p class="analogy-title">RDA</p>
        <p>=</p>
        <p class="analogy-example">🍳 요리 레시피</p>
        <p class="analogy-desc">"당근은 어슷썰기, 소금 1스푼"</p>
      </div>
      <div class="analogy-item">
        <p class="analogy-title">MARC</p>
        <p>=</p>
        <p class="analogy-example">🍱 도시락통</p>
        <p class="analogy-desc">"밥은 왼쪽, 반찬은 오른쪽"</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>4. 실전: RDA 규칙이 MARC 필드가 되는 과정</h2>

  <div class="workflow-example">
    <h3>📕 예제 도서: "82년생 김지영"</h3>

    <div class="step-box">
      <div class="step-header step-1">
        <span class="step-number">STEP 1</span>
        <span class="step-title">RDA 규칙 확인</span>
      </div>
      <div class="step-content">
        <table class="rule-table">
          <tr>
            <th>요소</th>
            <th>RDA 규칙</th>
            <th>적용 결과</th>
          </tr>
          <tr>
            <td>저자</td>
            <td>개인명은 "성, 이름" 순</td>
            <td>조남주 → <strong>조남주</strong> (한국식은 그대로)</td>
          </tr>
          <tr>
            <td>표제</td>
            <td>본표제 + 책임표시 기술</td>
            <td><strong>82년생 김지영 / 조남주 지음</strong></td>
          </tr>
          <tr>
            <td>출판사</td>
            <td>정식 명칭 사용</td>
            <td><strong>민음사</strong></td>
          </tr>
          <tr>
            <td>출판연도</td>
            <td>서기 연도 4자리</td>
            <td><strong>2016</strong></td>
          </tr>
        </table>
      </div>
    </div>

    <div class="arrow-down">⬇️ RDA 규칙대로 작성 완료!</div>

    <div class="step-box">
      <div class="step-header step-2">
        <span class="step-number">STEP 2</span>
        <span class="step-title">MARC 필드에 입력</span>
      </div>
      <div class="step-content">
        <table class="marc-table">
          <tr>
            <th>MARC 필드</th>
            <th>입력 내용</th>
            <th>설명</th>
          </tr>
          <tr>
            <td><strong>100 1_ $a</strong></td>
            <td>조남주</td>
            <td>개인저자명</td>
          </tr>
          <tr>
            <td><strong>245 10 $a</strong></td>
            <td>82년생 김지영 /</td>
            <td>본표제</td>
          </tr>
          <tr>
            <td><strong>245 __ $c</strong></td>
            <td>조남주 지음.</td>
            <td>책임표시</td>
          </tr>
          <tr>
            <td><strong>264 _1 $a</strong></td>
            <td>서울 :</td>
            <td>출판지</td>
          </tr>
          <tr>
            <td><strong>264 __ $b</strong></td>
            <td>민음사,</td>
            <td>출판사</td>
          </tr>
          <tr>
            <td><strong>264 __ $c</strong></td>
            <td>2016.</td>
            <td>출판연도</td>
          </tr>
        </table>
      </div>
    </div>

    <div class="result-box">
      <h4>✅ 완성된 MARC 레코드 (일부)</h4>
      <pre class="code-block">
100 1_ $a 조남주
245 10 $a 82년생 김지영 / $c 조남주 지음.
264 _1 $a 서울 : $b 민음사, $c 2016.
      </pre>
    </div>
  </div>

  <div class="insight-box">
    <h4>💡 이해했나요?</h4>
    <p><strong>RDA</strong>는 "조남주"라고 <strong>쓰라고 알려주고</strong>,<br>
    <strong>MARC</strong>는 그걸 <strong>100 $a 필드에 넣으라고</strong> 알려줍니다!</p>
  </div>
</div>

<div class="content-section">
  <h2>5. 더 많은 예시: RDA 규칙 → MARC 필드</h2>

  <div class="mapping-examples">
    <div class="mapping-card">
      <div class="mapping-header">저자가 2명일 때</div>
      <div class="mapping-rda">
        <p class="label">RDA 규칙</p>
        <p>"주저자는 필수, 추가 저자는 선택적으로 기술"</p>
      </div>
      <div class="mapping-marc">
        <p class="label">MARC 적용</p>
        <pre>100 1_ $a 김철수
700 1_ $a 이영희</pre>
        <p class="note">100 = 주저자, 700 = 추가 저자</p>
      </div>
    </div>

    <div class="mapping-card">
      <div class="mapping-header">번역서인 경우</div>
      <div class="mapping-rda">
        <p class="label">RDA 규칙</p>
        <p>"원저자와 역자를 모두 기술, 원표제는 주기로"</p>
      </div>
      <div class="mapping-marc">
        <p class="label">MARC 적용</p>
        <pre>100 1_ $a Rowling, J. K.
240 10 $a Harry Potter and the philosopher's stone
245 10 $a 해리 포터와 마법사의 돌 / $c J. K. 롤링 지음 ; 김혜원 옮김
700 1_ $a 김혜원, $e 역</pre>
        <p class="note">240 = 원표제, 700 $e = 역할</p>
      </div>
    </div>

    <div class="mapping-card">
      <div class="mapping-header">판차가 있을 때</div>
      <div class="mapping-rda">
        <p class="label">RDA 규칙</p>
        <p>"판차는 자료에 표기된 그대로 기술"</p>
      </div>
      <div class="mapping-marc">
        <p class="label">MARC 적용</p>
        <pre>250 __ $a 개정 3판.</pre>
        <p class="note">250 = 판사항</p>
      </div>
    </div>

    <div class="mapping-card">
      <div class="mapping-header">시리즈물일 때</div>
      <div class="mapping-rda">
        <p class="label">RDA 규칙</p>
        <p>"총서명과 총서 내 번호를 기술"</p>
      </div>
      <div class="mapping-marc">
        <p class="label">MARC 적용</p>
        <pre>490 1_ $a 민음사 세계문학전집 ; $v 347</pre>
        <p class="note">490 = 총서사항</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>6. 실무에서는 어떻게 쓰나요?</h2>

  <div class="workflow-diagram">
    <h3>📖 도서관 목록 작성 과정</h3>

    <div class="workflow-step">
      <div class="step-circle">1</div>
      <div class="step-detail">
        <h4>📚 새 책이 들어왔다!</h4>
        <p>사서가 책을 받아서 목록을 만들기 시작</p>
      </div>
    </div>

    <div class="workflow-arrow">⬇️</div>

    <div class="workflow-step highlighted">
      <div class="step-circle">2</div>
      <div class="step-detail">
        <h4>📋 RDA 규칙 참고</h4>
        <p>"RDA Toolkit"을 보면서 각 요소를 어떻게 기술할지 확인</p>
        <div class="example-mini">
          예: "저자 이름 어떻게 쓰지?" → RDA 참고
        </div>
      </div>
    </div>

    <div class="workflow-arrow">⬇️</div>

    <div class="workflow-step highlighted">
      <div class="step-circle">3</div>
      <div class="step-detail">
        <h4>💾 MARC 필드에 입력</h4>
        <p>도서관 시스템(ILS)에서 MARC 필드에 하나씩 입력</p>
        <div class="example-mini">
          예: 100 필드에 "조남주" 입력
        </div>
      </div>
    </div>

    <div class="workflow-arrow">⬇️</div>

    <div class="workflow-step">
      <div class="step-circle">4</div>
      <div class="step-detail">
        <h4>✅ 완성!</h4>
        <p>MARC 레코드가 만들어지고 다른 도서관과 공유 가능</p>
      </div>
    </div>
  </div>

  <div class="practice-tip">
    <h4>💼 실무 팁</h4>
    <ul>
      <li><strong>RDA</strong>는 "매뉴얼"처럼 옆에 두고 수시로 참고</li>
      <li><strong>MARC</strong>는 시스템 화면에서 필드별로 입력</li>
      <li>대부분의 목록 시스템(ILS)은 MARC 필드 형식으로 되어 있음</li>
      <li>RDA 규칙을 모르면 MARC에 뭘 써야 할지 모름!</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>7. 자주 하는 질문 (FAQ)</h2>

  <div class="faq-list">
    <div class="faq-item">
      <div class="faq-q">Q1. RDA 없이 MARC만 쓸 수 없나요?</div>
      <div class="faq-a">
        <p><strong>A:</strong> 불가능해요! MARC는 그냥 "빈 상자"예요. <strong>무엇을 쓸지는 RDA 규칙</strong>이 알려줍니다.</p>
        <p class="example-text">📦 예: "100 $a에 뭘 쓰지?" → RDA가 "저자 성명을 성, 이름 순으로"라고 알려줌</p>
      </div>
    </div>

    <div class="faq-item">
      <div class="faq-q">Q2. RDA 이전에는 뭘 썼나요?</div>
      <div class="faq-a">
        <p><strong>A:</strong> <strong>AACR2 (영미목록규칙 2판)</strong>를 썼어요. 2010년부터 RDA로 전환했습니다.</p>
        <p class="timeline">1967 AACR → 1978 AACR2 → 2010 RDA</p>
      </div>
    </div>

    <div class="faq-item">
      <div class="faq-q">Q3. 한국은 RDA를 안 쓰나요?</div>
      <div class="faq-a">
        <p><strong>A:</strong> 한국은 <strong>KCR (한국목록규칙)</strong>을 주로 써요. 하지만 KCR도 RDA를 참고해서 만들어졌어요!</p>
        <p class="note-text">국립중앙도서관, 대학도서관 등에서 KCR 사용</p>
      </div>
    </div>

    <div class="faq-item">
      <div class="faq-q">Q4. MARC 대신 RDA만 배우면 안 되나요?</div>
      <div class="faq-a">
        <p><strong>A:</strong> 실무에서는 <strong>둘 다 필요</strong>해요! RDA로 내용을 결정하고, MARC로 시스템에 입력합니다.</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>8. 요약: 한눈에 정리</h2>

  <div class="summary-grid">
    <div class="summary-card rda-card">
      <h3>📋 RDA</h3>
      <ul>
        <li><strong>층위</strong>: 2층 (콘텐츠 표준)</li>
        <li><strong>정체</strong>: 목록 작성 규칙</li>
        <li><strong>역할</strong>: "무엇을 어떻게" 쓸지 정함</li>
        <li><strong>형태</strong>: 텍스트 지침 (RDA Toolkit)</li>
        <li><strong>사용 시점</strong>: 내용 작성할 때</li>
        <li><strong>예시</strong>: "저자명은 성, 이름 순"</li>
      </ul>
    </div>

    <div class="summary-card marc-card">
      <h3>💾 MARC 21</h3>
      <ul>
        <li><strong>층위</strong>: 4층 (인코딩 포맷)</li>
        <li><strong>정체</strong>: 레코드 교환 포맷</li>
        <li><strong>역할</strong>: "어디에" 담을지 정함</li>
        <li><strong>형태</strong>: 태그-필드 구조</li>
        <li><strong>사용 시점</strong>: 시스템 입력할 때</li>
        <li><strong>예시</strong>: "저자명은 100 $a에"</li>
      </ul>
    </div>
  </div>

  <div class="final-message">
    <h3>🎯 최종 정리</h3>
    <p class="big-emphasis">
      <strong>RDA</strong>는 "레시피" (무엇을 어떻게 만들지)<br>
      <strong>MARC</strong>는 "도시락통" (어디에 담을지)
    </p>
    <p class="conclusion">
      사서는 <strong>RDA 규칙</strong>대로 서지정보를 작성하고,<br>
      그 내용을 <strong>MARC 필드</strong>에 담아서 시스템에 입력하고 다른 도서관과 공유합니다!
    </p>
  </div>
</div>

<div class="content-section">
  <h2>9. 학습 점검 퀴즈</h2>

  <div class="quiz-section">
    <div class="quiz-item">
      <p><strong>Q1.</strong> RDA와 MARC의 근본적인 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ RDA는 <strong>"무엇을 어떻게 기술할지"</strong> 정하는 규칙 (2층)<br>
        MARC는 <strong>"어디에 담을지"</strong> 정하는 포맷 (4층)</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> "저자 이름은 성, 이름 순서로 쓴다"는 무엇의 규칙인가요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>RDA</strong> (목록 작성 규칙)</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> "100 $a"는 무엇이고, 여기에 무엇을 넣나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ MARC의 <strong>개인저자명 필드</strong>, <strong>주저자 이름</strong>을 넣음</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> 도서관에서 새 책을 받았을 때 순서는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ ① 책 확인 → ② <strong>RDA 규칙 참고</strong> → ③ <strong>MARC 필드에 입력</strong> → ④ 완성</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> RDA 없이 MARC만 사용할 수 있나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>불가능</strong>. MARC는 빈 상자이고, 무엇을 쓸지는 RDA가 알려줌</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q6.</strong> 한국에서 주로 사용하는 목록 규칙은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>KCR (한국목록규칙)</strong> - RDA를 참고하여 제작됨</p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 더 알아보기</h2>
  <ul>
    <li><strong>RDA Toolkit</strong> - RDA 공식 온라인 도구 (유료)</li>
    <li><strong>KCR (한국목록규칙)</strong> - 국립중앙도서관 한국목록규칙</li>
    <li><strong>MARC 21 Format</strong> - Library of Congress 공식 문서</li>
    <li><strong>목록 실무 가이드</strong> - 각 도서관별 작성 지침</li>
  </ul>
</div>

<style>
.content-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.one-liner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.concept-box {
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
}

.rda-box {
  background: #e3f2fd;
  border: 3px solid #2196f3;
}

.marc-box {
  background: #fff3e0;
  border: 3px solid #ff9800;
}

.role {
  font-size: 1.3rem;
  font-weight: bold;
  color: #333;
  margin: 0.5rem 0;
}

.description {
  font-size: 1.1rem;
  margin: 1rem 0;
  line-height: 1.6;
}

.example-box {
  background: white;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 4px;
  text-align: left;
}

.example-title {
  font-weight: bold;
  color: #666;
  margin-bottom: 0.5rem;
}

.relationship-box {
  background: #f1f8e9;
  border: 3px solid #8bc34a;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
  text-align: center;
}

.big-text {
  font-size: 1.5rem;
  margin: 1rem 0;
}

.architecture-visual {
  margin: 2rem 0;
}

.layer {
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  border: 2px solid #ddd;
  padding: 1.5rem;
  display: grid;
  grid-template-columns: 80px 1fr 150px;
  gap: 1rem;
  align-items: center;
}

.layer.highlighted {
  border: 3px solid #ff5722;
  box-shadow: 0 4px 8px rgba(255,87,34,0.3);
}

.layer-number {
  font-size: 2rem;
  font-weight: bold;
  color: #666;
  text-align: center;
}

.layer-title {
  font-weight: bold;
  color: #333;
}

.layer-tech {
  text-align: right;
  font-weight: bold;
  font-size: 1.1rem;
}

.rda-highlight {
  color: #2196f3;
  font-size: 1.3rem;
}

.marc-highlight {
  color: #ff9800;
  font-size: 1.3rem;
}

.layer-desc {
  grid-column: 2 / 4;
  color: #666;
  font-size: 0.9rem;
}

.key-point {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
  padding: 1.5rem;
  margin: 1.5rem 0;
  border-radius: 4px;
}

.comparison-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  background: white;
}

.comparison-table th,
.comparison-table td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.comparison-table th {
  background: #1976d2;
  color: white;
  font-weight: bold;
  text-align: center;
}

.comparison-table tr:nth-child(even) {
  background: #f5f5f5;
}

.analogy-box {
  background: #e1f5fe;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.analogy-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 1rem;
}

.analogy-item {
  text-align: center;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
}

.analogy-title {
  font-weight: bold;
  font-size: 1.2rem;
  color: #1976d2;
}

.analogy-example {
  font-size: 2rem;
  margin: 0.5rem 0;
}

.analogy-desc {
  color: #666;
  font-size: 0.9rem;
}

.workflow-example {
  margin: 2rem 0;
}

.step-box {
  margin: 2rem 0;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid #ddd;
}

.step-header {
  padding: 1rem 1.5rem;
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.step-1 {
  background: #2196f3;
}

.step-2 {
  background: #ff9800;
}

.step-number {
  background: rgba(255,255,255,0.3);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
}

.step-content {
  padding: 1.5rem;
  background: white;
}

.rule-table,
.marc-table {
  width: 100%;
  border-collapse: collapse;
}

.rule-table th,
.rule-table td,
.marc-table th,
.marc-table td {
  border: 1px solid #ddd;
  padding: 0.75rem;
  text-align: left;
}

.rule-table th,
.marc-table th {
  background: #f5f5f5;
  font-weight: bold;
}

.arrow-down {
  text-align: center;
  font-size: 2rem;
  margin: 1rem 0;
  color: #4caf50;
}

.result-box {
  background: #f1f8e9;
  border-left: 4px solid #8bc34a;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.code-block {
  background: #263238;
  color: #aed581;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-top: 1rem;
}

.insight-box {
  background: #fff3e0;
  border: 2px solid #ff9800;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
  text-align: center;
}

.mapping-examples {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin: 2rem 0;
}

.mapping-card {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.mapping-header {
  background: #1976d2;
  color: white;
  padding: 1rem;
  font-weight: bold;
  text-align: center;
}

.mapping-rda,
.mapping-marc {
  padding: 1rem;
}

.mapping-rda {
  background: #e3f2fd;
}

.mapping-marc {
  background: #fff3e0;
}

.label {
  font-weight: bold;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.mapping-marc pre {
  background: #263238;
  color: #aed581;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  margin: 0.5rem 0;
}

.note {
  font-size: 0.85rem;
  color: #666;
  font-style: italic;
  margin-top: 0.5rem;
}

.workflow-diagram {
  margin: 2rem 0;
}

.workflow-step {
  display: grid;
  grid-template-columns: 60px 1fr;
  gap: 1.5rem;
  margin: 1rem 0;
  align-items: start;
}

.step-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #2196f3;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.workflow-step.highlighted .step-circle {
  background: #ff9800;
}

.step-detail {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #ddd;
}

.workflow-step.highlighted .step-detail {
  border-color: #ff9800;
  box-shadow: 0 2px 4px rgba(255,152,0,0.2);
}

.example-mini {
  background: #f5f5f5;
  padding: 0.75rem;
  margin-top: 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
  border-left: 3px solid #2196f3;
}

.workflow-arrow {
  text-align: center;
  font-size: 2rem;
  color: #4caf50;
  margin: 0.5rem 0;
}

.practice-tip {
  background: #e8f5e9;
  border-left: 4px solid #4caf50;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.faq-list {
  margin: 1.5rem 0;
}

.faq-item {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  margin: 1rem 0;
  overflow: hidden;
}

.faq-q {
  background: #1976d2;
  color: white;
  padding: 1rem 1.5rem;
  font-weight: bold;
}

.faq-a {
  padding: 1.5rem;
}

.example-text {
  background: #fffde7;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 4px;
  border-left: 3px solid #ffc107;
}

.timeline {
  background: #f5f5f5;
  padding: 0.75rem;
  margin-top: 0.75rem;
  border-radius: 4px;
  font-family: monospace;
  text-align: center;
}

.note-text {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
  font-style: italic;
}

.summary-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.summary-card {
  padding: 2rem;
  border-radius: 8px;
  background: white;
}

.rda-card {
  border: 3px solid #2196f3;
}

.marc-card {
  border: 3px solid #ff9800;
}

.final-message {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
}

.final-message h3,
.final-message p {
  color: white;
}

.big-emphasis {
  font-size: 1.5rem;
  margin: 1.5rem 0;
  line-height: 1.8;
}

.conclusion {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-top: 1.5rem;
}

.quiz-section {
  background: #f1f8e9;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.quiz-item {
  background: white;
  padding: 1rem;
  margin: 0.75rem 0;
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

h4 {
  color: #1e88e5;
  margin-top: 1rem;
}

ul {
  line-height: 1.8;
}

strong {
  color: #0d47a1;
}

@media (max-width: 768px) {
  .one-liner,
  .analogy-grid,
  .mapping-examples,
  .summary-grid {
    grid-template-columns: 1fr;
  }

  .layer {
    grid-template-columns: 1fr;
  }

  .layer-tech {
    text-align: left;
  }
}
</style>
        """,
        category=comparison_category,
        author=admin,
        difficulty='BEGINNER',
        estimated_time=30,
        prerequisites="",
        learning_objectives="RDA와 MARC의 근본적인 차이 이해하기, 4층 구조에서 RDA와 MARC의 위치 파악하기, RDA 규칙이 MARC 필드로 어떻게 변환되는지 알기, 실무에서 RDA와 MARC를 함께 사용하는 방법 익히기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {comparison_category.name} (상위: {overview_category.name})")
    print(f"  - 난이도: 초급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=overview")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_rda_marc_comparison()
