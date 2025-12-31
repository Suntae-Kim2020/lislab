#!/usr/bin/env python
"""
RDF vs MARC 비교 학습 콘텐츠 추가 스크립트
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

def create_comparison_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 가져오기: 한눈에 보기
    overview_category = Category.objects.get(slug='overview')
    print("✓ 상위 카테고리 확인: 한눈에 보기")

    # 하위 카테고리 생성 또는 가져오기: 포맷 비교
    comparison_category, created = Category.objects.get_or_create(
        slug='format-comparison',
        defaults={
            'name': '포맷 비교',
            'description': '다양한 메타데이터 포맷의 차이점과 특징',
            'parent': overview_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: 포맷 비교")
    else:
        print("✓ 하위 카테고리 확인: 포맷 비교")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': 'RDF', 'slug': 'rdf'},
        {'name': 'MARC', 'slug': 'marc'},
        {'name': 'BIBFRAME', 'slug': 'bibframe'},
        {'name': '메타데이터', 'slug': 'metadata'},
        {'name': '인코딩', 'slug': 'encoding'},
        {'name': 'Linked Data', 'slug': 'linked-data'},
        {'name': '데이터 모델', 'slug': 'data-model'},
        {'name': 'RDA', 'slug': 'rda'}
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
        title="RDF랑 MARC는 뭐가 달라?",
        slug="rdf-vs-marc-comparison",
        summary="헷갈리는 RDF와 MARC! 둘의 차이를 4층 구조로 명쾌하게 이해하고, 같은 책 정보가 어떻게 다르게 표현되는지 실전 예제로 배웁니다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>RDF와 MARC의 근본적인 차이 이해하기</li>
    <li>4층 구조에서 각 기술의 위치 파악하기</li>
    <li>같은 데이터가 RDF와 MARC에서 어떻게 다르게 표현되는지 알기</li>
    <li>언제 RDF를 쓰고 언제 MARC를 쓰는지 판단하기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. 먼저 간단하게: 둘이 뭐가 달라?</h2>

  <div class="comparison-intro">
    <div class="format-box marc-box">
      <h3>📁 MARC</h3>
      <p class="big-text">"파일 포맷"</p>
      <p>데이터를 <strong>파일로 담아서 주고받는 방식</strong></p>
      <p class="example">💾 엑셀 파일(.xlsx), 워드 문서(.docx)처럼<br>정해진 구조로 정보를 저장</p>
    </div>

    <div class="format-box rdf-box">
      <h3>🕸️ RDF</h3>
      <p class="big-text">"웹 언어"</p>
      <p>데이터를 <strong>웹에서 연결하는 방식</strong></p>
      <p class="example">🌐 HTML처럼 웹에서 데이터를 연결하고<br>컴퓨터가 의미를 이해할 수 있게</p>
    </div>
  </div>

  <div class="key-difference">
    <h4>🔑 핵심 차이 한 줄 정리</h4>
    <ul>
      <li><strong>MARC</strong>: "이 책 정보를 <strong>파일로 만들어서</strong> 다른 도서관에 보내자"</li>
      <li><strong>RDF</strong>: "이 책 정보를 <strong>웹에 올려서</strong> 누구나 연결해서 쓸 수 있게 하자"</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>2. 4층 구조로 보는 위치</h2>

  <p>도서관 세계에는 여러 기술들이 4층 건물처럼 쌓여있어요:</p>

  <div class="architecture-diagram">
    <div class="layer layer-1">
      <div class="layer-header">🏢 1층: 개념 모델</div>
      <div class="layer-content">
        <p><strong>FRBR → LRM</strong></p>
        <p>"책이란 무엇인가?" 같은 <strong>철학적 틀</strong></p>
        <p class="example">예: 작품-표현형-구현형-개별자료</p>
      </div>
    </div>

    <div class="layer layer-2">
      <div class="layer-header">📋 2층: 콘텐츠 표준 (규칙)</div>
      <div class="layer-content">
        <p><strong>RDA</strong></p>
        <p>"저자 이름을 어떻게 쓸까?" 같은 <strong>작업 규칙</strong></p>
        <p class="example">예: 성, 이름 순서 / 출판사 표기 방법</p>
      </div>
    </div>

    <div class="layer layer-3">
      <div class="layer-header">🌐 3층: 데이터 모델 (Linked Data)</div>
      <div class="layer-content">
        <p><strong>BIBFRAME (RDF 기반)</strong></p>
        <p>"데이터를 웹에서 <strong>어떻게 연결할까</strong>"</p>
        <p class="example">예: Work → hasExpression → Expression</p>
      </div>
    </div>

    <div class="layer layer-4">
      <div class="layer-header">💾 4층: 인코딩 포맷 (교환)</div>
      <div class="layer-content">
        <p><strong>MARC 21</strong></p>
        <p>"데이터를 파일로 <strong>어떻게 담아 보낼까</strong>"</p>
        <p class="example">예: 245 $a (표제) / 100 $a (저자)</p>
      </div>
    </div>
  </div>

  <div class="highlight-box">
    <h4>💡 쉽게 비유하면</h4>
    <ul>
      <li><strong>1층 (LRM)</strong>: 설계 도면 - "집을 어떻게 지을까?"</li>
      <li><strong>2층 (RDA)</strong>: 시공 지침 - "벽돌을 어떻게 쌓을까?"</li>
      <li><strong>3층 (RDF/BIBFRAME)</strong>: 웹 공간 - "온라인에 어떻게 올릴까?"</li>
      <li><strong>4층 (MARC)</strong>: 이사 상자 - "다른 곳으로 어떻게 옮길까?"</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>3. RDA vs MARC: 자주 묻는 질문</h2>

  <div class="qa-box">
    <h4>Q: "RDA랑 MARC는 뭐가 달라?"</h4>
    <div class="answer">
      <p><strong>A:</strong></p>
      <ul>
        <li><strong>RDA</strong> (2층): <em>무엇을 어떻게 기술할지</em> 정하는 <strong>규칙</strong></li>
        <li><strong>MARC</strong> (4층): 그 내용을 <em>어떤 필드에 담아 보낼지</em> 정하는 <strong>포맷</strong></li>
      </ul>
      <p class="example-text">📖 예시: "저자 이름을 '성, 이름' 순서로 쓴다" → <strong>RDA 규칙</strong><br>
      그 저자 이름을 "100 필드 $a 서브필드"에 넣는다 → <strong>MARC 포맷</strong></p>
    </div>
  </div>

  <div class="qa-box">
    <h4>Q: "RDF랑 MARC는 뭐가 달라?"</h4>
    <div class="answer">
      <p><strong>A:</strong></p>
      <ul>
        <li><strong>RDF</strong> (3층): 웹에서 데이터를 <strong>그래프로 연결</strong>하는 방식</li>
        <li><strong>MARC</strong> (4층): 데이터를 <strong>레코드 파일로 교환</strong>하는 방식</li>
      </ul>
      <p class="example-text">🌐 RDF: "이 책 URI → 저자 URI → 사람 정보 URI" (웹에서 클릭하듯 연결)<br>
      💾 MARC: "245 표제 / 100 저자" (정해진 필드에 값 입력)</p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>4. 실전 예제: 같은 책, 다른 표현</h2>

  <div class="book-example">
    <h3>📕 예제 도서: "82년생 김지영"</h3>
    <ul>
      <li>저자: 조남주</li>
      <li>출판사: 민음사</li>
      <li>출판연도: 2016</li>
    </ul>
  </div>

  <h3>방식 1: MARC 21 (레코드 포맷)</h3>
  <div class="format-example marc-example">
    <pre class="code-block">
100 1  $a 조남주
245 10 $a 82년생 김지영 / $c 조남주 지음
260    $a 서울 : $b 민음사, $c 2016
    </pre>
    <p class="explanation">
      ✅ <strong>장점</strong>: 정해진 필드에 딱딱 넣으면 끝! 간단명료<br>
      ❌ <strong>단점</strong>: 다른 시스템과 연결 어려움, 확장성 낮음
    </p>
  </div>

  <h3>방식 2: RDF (BIBFRAME)</h3>
  <div class="format-example rdf-example">
    <pre class="code-block">
&lt;Work rdf:about="http://example.org/work/82년생김지영"&gt;
  &lt;bf:title&gt;82년생 김지영&lt;/bf:title&gt;
  &lt;bf:contribution&gt;
    &lt;Contribution&gt;
      &lt;bf:agent rdf:resource="http://example.org/person/조남주"/&gt;
      &lt;bf:role&gt;저자&lt;/bf:role&gt;
    &lt;/Contribution&gt;
  &lt;/bf:contribution&gt;
&lt;/Work&gt;

&lt;Instance rdf:about="http://example.org/instance/82년생김지영-2016"&gt;
  &lt;bf:instanceOf rdf:resource="http://example.org/work/82년생김지영"/&gt;
  &lt;bf:provisionActivity&gt;
    &lt;Publication&gt;
      &lt;bf:agent rdf:resource="http://example.org/org/민음사"/&gt;
      &lt;bf:date&gt;2016&lt;/bf:date&gt;
    &lt;/Publication&gt;
  &lt;/bf:provisionActivity&gt;
&lt;/Instance&gt;
    </pre>
    <p class="explanation">
      ✅ <strong>장점</strong>: 웹에서 연결 가능, 의미 명확, 확장 쉬움<br>
      ❌ <strong>단점</strong>: 복잡해 보임, 기존 시스템 전환 필요
    </p>
  </div>
</div>

<div class="content-section">
  <h2>5. RDA 요소가 MARC와 BIBFRAME에서 어떻게 매핑되나?</h2>

  <table class="mapping-table">
    <thead>
      <tr>
        <th>RDA 요소<br>(2층: 규칙)</th>
        <th>MARC 21<br>(4층: 포맷)</th>
        <th>BIBFRAME (RDF)<br>(3층: 데이터 모델)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>저자</strong><br>(Creator)</td>
        <td>100 $a<br>(주저자명)</td>
        <td>bf:contribution<br>→ bf:agent</td>
      </tr>
      <tr>
        <td><strong>표제</strong><br>(Title)</td>
        <td>245 $a<br>(본표제)</td>
        <td>bf:title<br>(Work/Instance)</td>
      </tr>
      <tr>
        <td><strong>출판사</strong><br>(Publisher)</td>
        <td>260 $b / 264 $b<br>(발행처)</td>
        <td>bf:provisionActivity<br>→ bf:agent</td>
      </tr>
      <tr>
        <td><strong>출판연도</strong><br>(Publication Date)</td>
        <td>260 $c / 264 $c<br>(발행년)</td>
        <td>bf:provisionActivity<br>→ bf:date</td>
      </tr>
      <tr>
        <td><strong>ISBN</strong></td>
        <td>020 $a</td>
        <td>bf:identifiedBy<br>→ bf:Isbn</td>
      </tr>
      <tr>
        <td><strong>주제</strong><br>(Subject)</td>
        <td>650 $a<br>(주제명)</td>
        <td>bf:subject<br>→ bf:Topic</td>
      </tr>
    </tbody>
  </table>

  <div class="highlight-box">
    <h4>💡 이해 포인트</h4>
    <p><strong>RDA</strong>는 "저자를 어떻게 기술할까?"라는 <strong>규칙</strong>을 정하고,<br>
    그 규칙을 <strong>MARC는 100 필드</strong>에, <strong>BIBFRAME은 bf:agent 속성</strong>에 담습니다!</p>
  </div>
</div>

<div class="content-section">
  <h2>6. 언제 뭘 써야 할까?</h2>

  <div class="use-case-grid">
    <div class="use-case marc-case">
      <h4>💾 MARC를 쓰는 경우</h4>
      <ul>
        <li>✅ 기존 도서관 시스템과 호환</li>
        <li>✅ 다른 도서관과 레코드 교환</li>
        <li>✅ 검증된 안정적인 시스템</li>
        <li>✅ 대량의 기존 데이터 활용</li>
      </ul>
      <p class="example-tag">📌 예: 국립중앙도서관 ↔ 대학도서관 서지데이터 교환</p>
    </div>

    <div class="use-case rdf-case">
      <h4>🌐 RDF (BIBFRAME)를 쓰는 경우</h4>
      <ul>
        <li>✅ 웹에서 데이터 공개·공유</li>
        <li>✅ 다른 분야 데이터와 연결</li>
        <li>✅ 의미 검색, AI 활용</li>
        <li>✅ 미래 지향적 시스템 구축</li>
      </ul>
      <p class="example-tag">📌 예: 도서관 데이터 + 위키데이터 + DBpedia 연결</p>
    </div>
  </div>

  <div class="future-box">
    <h4>🔮 미래는?</h4>
    <p><strong>MARC → BIBFRAME 전환 진행 중!</strong></p>
    <p>미국 의회도서관(LC)을 중심으로 MARC 21을 RDF 기반 BIBFRAME으로 바꾸는 작업이 진행되고 있어요.</p>
    <p>하지만 전 세계 수십억 건의 MARC 레코드가 있어서, 완전한 전환은 10년 이상 걸릴 예정입니다.</p>
  </div>
</div>

<div class="content-section">
  <h2>7. 요약: 한 장으로 정리</h2>

  <div class="summary-table">
    <table class="data-table">
      <thead>
        <tr>
          <th>비교 항목</th>
          <th>MARC 21</th>
          <th>RDF (BIBFRAME)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>층위</strong></td>
          <td>4층 (인코딩 포맷)</td>
          <td>3층 (데이터 모델)</td>
        </tr>
        <tr>
          <td><strong>목적</strong></td>
          <td>레코드 교환</td>
          <td>웹 데이터 연결</td>
        </tr>
        <tr>
          <td><strong>형태</strong></td>
          <td>평면 레코드<br>(태그-서브필드)</td>
          <td>그래프<br>(주어-술어-목적어)</td>
        </tr>
        <tr>
          <td><strong>가독성</strong></td>
          <td>전문가용<br>(코드 위주)</td>
          <td>의미 명확<br>(URI 연결)</td>
        </tr>
        <tr>
          <td><strong>확장성</strong></td>
          <td>제한적</td>
          <td>높음</td>
        </tr>
        <tr>
          <td><strong>현재 사용</strong></td>
          <td>대부분 도서관<br>(주력)</td>
          <td>일부 선도 도서관<br>(시범 운영)</td>
        </tr>
        <tr>
          <td><strong>미래</strong></td>
          <td>점진적 단계 축소</td>
          <td>주류로 전환 예정</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="key-message">
    <h4>🎯 핵심 메시지</h4>
    <p class="big-text">MARC는 <strong>"파일 교환"</strong>, RDF는 <strong>"웹 연결"</strong>!</p>
    <p>둘 다 같은 RDA 규칙을 따르지만,<br>
    <strong>MARC는 레코드 파일로 담고</strong>, <strong>RDF는 웹 그래프로 연결</strong>합니다.</p>
  </div>
</div>

<div class="content-section">
  <h2>8. 학습 점검 퀴즈</h2>

  <div class="quiz-section">
    <div class="quiz-item">
      <p><strong>Q1.</strong> MARC와 RDF의 근본적인 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ MARC는 <strong>레코드 파일 교환 포맷</strong> (4층), RDF는 <strong>웹 데이터 연결 방식</strong> (3층)</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> RDA는 몇 층에 위치하나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>2층 (콘텐츠 표준/규칙)</strong> - "무엇을 어떻게 기술할지" 정하는 규칙</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> "245 $a"는 무엇이고, BIBFRAME에서는 무엇에 해당하나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ MARC의 <strong>표제(본제목) 필드</strong>, BIBFRAME에서는 <strong>bf:title 속성</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> 도서관끼리 서지 데이터를 파일로 주고받으려면?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>MARC 21</strong> 사용 (레코드 교환 포맷)</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> 도서관 데이터를 위키데이터나 다른 웹 데이터와 연결하려면?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>RDF (BIBFRAME)</strong> 사용 (Linked Data)</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q6.</strong> 4층 구조를 아래부터 순서대로 나열하면?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ 1층: <strong>LRM</strong> (개념 모델) → 2층: <strong>RDA</strong> (규칙) → 3층: <strong>BIBFRAME</strong> (데이터 모델) → 4층: <strong>MARC</strong> (인코딩)</p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 더 알아보기</h2>
  <ul>
    <li><strong>MARC 21 공식 문서</strong> - Library of Congress</li>
    <li><strong>BIBFRAME 소개</strong> - Library of Congress BIBFRAME Initiative</li>
    <li><strong>RDA Toolkit</strong> - RDA 규칙 상세 가이드</li>
    <li><strong>Linked Data for Libraries (LD4L)</strong> - 도서관 Linked Data 프로젝트</li>
  </ul>
</div>

<style>
.content-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.comparison-intro {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin: 2rem 0;
}

.format-box {
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.marc-box {
  background: #fff3e0;
  border: 3px solid #ff9800;
}

.rdf-box {
  background: #e3f2fd;
  border: 3px solid #2196f3;
}

.big-text {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 1rem 0;
}

.example {
  font-size: 0.9rem;
  color: #666;
  margin-top: 1rem;
  line-height: 1.6;
}

.key-difference {
  background: #f1f8e9;
  border-left: 4px solid #8bc34a;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.architecture-diagram {
  margin: 2rem 0;
}

.layer {
  margin: 1rem 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.layer-header {
  padding: 1rem;
  font-weight: bold;
  color: white;
  font-size: 1.1rem;
}

.layer-content {
  padding: 1.5rem;
  background: white;
}

.layer-1 .layer-header { background: #9c27b0; }
.layer-2 .layer-header { background: #2196f3; }
.layer-3 .layer-header { background: #4caf50; }
.layer-4 .layer-header { background: #ff9800; }

.highlight-box {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 1.5rem;
  margin: 1.5rem 0;
  border-radius: 4px;
}

.qa-box {
  background: #fff;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1.5rem 0;
}

.qa-box h4 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.answer {
  margin-top: 1rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 4px;
}

.example-text {
  margin-top: 1rem;
  padding: 1rem;
  background: #fffde7;
  border-left: 3px solid #ffc107;
  font-size: 0.95rem;
}

.book-example {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
}

.format-example {
  margin: 1.5rem 0;
  border-radius: 8px;
  overflow: hidden;
}

.marc-example {
  border: 2px solid #ff9800;
}

.rdf-example {
  border: 2px solid #2196f3;
}

.code-block {
  background: #263238;
  color: #aed581;
  padding: 1.5rem;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
  margin: 0;
}

.explanation {
  padding: 1rem;
  background: white;
  font-size: 0.95rem;
}

.mapping-table {
  width: 100%;
  margin: 1.5rem 0;
}

.data-table, .mapping-table table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.data-table th,
.data-table td,
.mapping-table th,
.mapping-table td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.data-table th,
.mapping-table th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.data-table tr:nth-child(even),
.mapping-table tr:nth-child(even) {
  background: #f5f5f5;
}

.use-case-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.use-case {
  padding: 1.5rem;
  border-radius: 8px;
  background: white;
}

.marc-case {
  border: 3px solid #ff9800;
}

.rdf-case {
  border: 3px solid #2196f3;
}

.example-tag {
  background: #fffde7;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.future-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.future-box h4 {
  color: white;
  margin-bottom: 1rem;
}

.summary-table {
  margin: 2rem 0;
}

.key-message {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
}

.key-message h4,
.key-message p {
  color: white;
}

.key-message .big-text {
  font-size: 1.8rem;
  margin: 1.5rem 0;
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
  .comparison-intro,
  .use-case-grid {
    grid-template-columns: 1fr;
  }
}
</style>
        """,
        category=comparison_category,
        author=admin,
        difficulty='BEGINNER',
        estimated_time=30,
        prerequisites="",
        learning_objectives="RDF와 MARC의 근본적인 차이 이해하기, 4층 구조에서 각 기술의 위치 파악하기, RDA 요소가 MARC와 BIBFRAME에 어떻게 매핑되는지 알기, 실무에서 언제 어떤 기술을 사용해야 하는지 판단하기",
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
    create_comparison_content()
