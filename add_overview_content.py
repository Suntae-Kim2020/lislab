"""
한눈에 보기 카테고리와 FRBR/LRM/RDA/BIBFRAME 관계 학습 콘텐츠 추가 스크립트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content, Category, Tag
from apps.accounts.models import User

# Admin 사용자 가져오기
admin = User.objects.filter(username='admin').first()
if not admin:
    print("❌ Admin 사용자를 찾을 수 없습니다.")
    exit(1)

print("✓ Admin 사용자 확인")

# 1. 한눈에 보기 카테고리 생성 (상위 카테고리)
overview_category, created = Category.objects.get_or_create(
    slug='overview',
    defaults={
        'name': '한눈에 보기',
        'description': '도서관 정보학의 핵심 개념을 한눈에 이해하기',
        'parent': None,
        'is_active': True
    }
)
if created:
    print(f"✓ 상위 카테고리 생성: {overview_category.name}")
else:
    print(f"✓ 상위 카테고리 확인: {overview_category.name}")

# 2. 서지 모델 비교 하위 카테고리 생성
comparison_category, created = Category.objects.get_or_create(
    slug='bibliographic-models-comparison',
    defaults={
        'name': '서지 모델 비교',
        'description': 'FRBR, LRM, RDA, BIBFRAME 한눈에 이해하기',
        'parent': overview_category,
        'is_active': True
    }
)
if created:
    print(f"✓ 하위 카테고리 생성: {comparison_category.name}")
else:
    print(f"✓ 하위 카테고리 확인: {comparison_category.name}")

# 3. 태그 생성 (주요 키워드 추출)
tag_names = ['FRBR', 'LRM', 'RDA', 'BIBFRAME', '서지데이터', '목록규칙', 'Linked Data', '개념모델']
tags = []
for tag_name in tag_names:
    tag, created = Tag.objects.get_or_create(
        name=tag_name,
        defaults={'slug': tag_name.lower().replace(' ', '-')}
    )
    tags.append(tag)
    if created:
        print(f"  ✓ 태그 생성: {tag_name}")
    else:
        print(f"  ✓ 태그 확인: {tag_name}")

# 4. 학습 콘텐츠 HTML
content_html = """
<h2>도서관 핵심 모델 한눈에 이해하기</h2>
<p class="lead">FRBR, LRM, RDA, BIBFRAME... 헷갈리는 용어들을 명쾌하게 정리해드립니다!</p>

<div class="alert alert-info">
<strong>💡 이 강의를 마치면:</strong>
<ul>
<li>네 가지 모델(FRBR, LRM, RDA, BIBFRAME)의 위치와 역할을 명확히 구분할 수 있습니다</li>
<li>실제 도서관 업무에서 어떻게 활용되는지 이해합니다</li>
<li>하나의 책이 네 가지 관점에서 어떻게 표현되는지 알게 됩니다</li>
</ul>
</div>

<hr/>

<h2>🎯 왜 이렇게 많은 개념이 필요할까요?</h2>

<div class="why-box">
<p>도서관에서 책을 정리하고 찾기 위해서는...</p>
<div class="why-steps">
<div class="why-step">
<div class="step-icon">🤔</div>
<div class="step-text">
<strong>1단계: 어떻게 생각할까?</strong><br/>
책과 저자를 어떤 구조로 이해할 것인가<br/>
<span class="model-name">→ 개념 모델 (FRBR, LRM)</span>
</div>
</div>

<div class="why-step">
<div class="step-icon">📝</div>
<div class="step-text">
<strong>2단계: 어떻게 기록할까?</strong><br/>
저자 이름, 출판년도 등을 어떤 규칙으로 쓸 것인가<br/>
<span class="model-name">→ 목록 규칙 (RDA)</span>
</div>
</div>

<div class="why-step">
<div class="step-icon">💾</div>
<div class="step-text">
<strong>3단계: 어떻게 저장·공유할까?</strong><br/>
컴퓨터에서 읽고 다른 도서관과 공유하려면<br/>
<span class="model-name">→ 데이터 형식 (BIBFRAME)</span>
</div>
</div>
</div>
</div>

<hr/>

<h2>📍 한눈에 보는 위치 관계</h2>

<div class="position-diagram">
<div class="position-row">
<div class="position-card past">
<div class="badge">과거</div>
<h3>FRBR</h3>
<p class="role">개념적 서지 데이터 모델</p>
<p class="desc">1998년 등장. Work-Expression-Manifestation-Item 구조 제시</p>
<p class="status">→ 현재는 LRM으로 통합됨</p>
</div>

<div class="position-card current">
<div class="badge">현재</div>
<h3>LRM</h3>
<p class="role">개념적 참조 모델</p>
<p class="desc">2017년 발표. FRBR/FRAD/FRSAD를 하나로 통합</p>
<p class="status">→ 가장 상위의 기준 모델</p>
</div>
</div>

<div class="position-row">
<div class="position-card standard">
<div class="badge">규칙</div>
<h3>RDA</h3>
<p class="role">콘텐츠 표준 (목록 규칙)</p>
<p class="desc">LRM 기반으로 "무엇을 어떻게 기록할지" 정의</p>
<p class="status">→ 실제 목록 작성 지침</p>
</div>

<div class="position-card implementation">
<div class="badge">구현</div>
<h3>BIBFRAME</h3>
<p class="role">데이터 교환 모델</p>
<p class="desc">Linked Data(RDF) 기반으로 웹 환경에 최적화</p>
<p class="status">→ MARC 대체 목표</p>
</div>
</div>
</div>

<hr/>

<h2>🔍 각자 무슨 일을 하나요?</h2>

<div class="roles-section">
<div class="role-card frbr-card">
<h3>1️⃣ FRBR (Functional Requirements for Bibliographic Records)</h3>
<div class="role-content">
<div class="what-is">
<h4>무엇인가요?</h4>
<p>1998년 IFLA가 만든 <strong>서지 세계의 청사진</strong></p>
<p>책, 저자, 출판사 같은 것들을 어떻게 구조화할지 정의</p>
</div>

<div class="key-concept">
<h4>핵심 개념: WEMI</h4>
<div class="wemi-boxes">
<div class="wemi-box">
<strong>W</strong>ork<br/><span>저작</span>
</div>
<div class="wemi-box">
<strong>E</strong>xpression<br/><span>표현형</span>
</div>
<div class="wemi-box">
<strong>M</strong>anifestation<br/><span>구현형</span>
</div>
<div class="wemi-box">
<strong>I</strong>tem<br/><span>개별자료</span>
</div>
</div>
</div>

<div class="current-status">
<h4>현재 상태</h4>
<p>✅ 개념은 여전히 중요하지만...</p>
<p>⚠️ <strong>LRM으로 통합·발전</strong>되어 과거 모델로 분류됨</p>
</div>
</div>
</div>

<div class="role-card lrm-card">
<h3>2️⃣ LRM (IFLA Library Reference Model)</h3>
<div class="role-content">
<div class="what-is">
<h4>무엇인가요?</h4>
<p>2017년 IFLA가 발표한 <strong>최신 통합 참조 모델</strong></p>
<p>FRBR, FRAD, FRSAD 3개를 하나로 합쳤어요</p>
</div>

<div class="key-concept">
<h4>주요 특징</h4>
<ul>
<li>📊 엔티티를 33개 → 11개로 단순화</li>
<li>🔗 모든 개념을 일관성 있게 통합</li>
<li>🌐 국제 표준급 "상위 뼈대" 역할</li>
<li>✨ Nomen(명칭) 개념 새로 도입</li>
</ul>
</div>

<div class="current-status">
<h4>역할</h4>
<p><strong>"규칙(RDA)이나 시스템(BIBFRAME)을 만들 때 참고하는 기준"</strong></p>
<p>직접 목록을 작성하는 규칙은 아니고, 더 상위의 개념 틀!</p>
</div>
</div>
</div>

<div class="role-card rda-card">
<h3>3️⃣ RDA (Resource Description and Access)</h3>
<div class="role-content">
<div class="what-is">
<h4>무엇인가요?</h4>
<p><strong>실제로 목록을 작성할 때 쓰는 규칙집</strong></p>
<p>"저자 이름은 이렇게, 출판연도는 저렇게" 같은 구체적 지침</p>
</div>

<div class="key-concept">
<h4>주요 내용</h4>
<ul>
<li>📝 LRM 기반으로 13개 엔티티·요소 구조화</li>
<li>📖 어떤 정보를 어떤 형식으로 기록할지 정의</li>
<li>🔤 "성, 이름" vs "이름 성" 같은 세부 규칙 제공</li>
<li>🌍 국제적으로 통일된 목록 작성 가능</li>
</ul>
</div>

<div class="current-status">
<h4>역할</h4>
<p><strong>"사서가 실제 목록을 작성할 때 보는 매뉴얼"</strong></p>
<p>RDA Toolkit에서 온라인으로 제공됨</p>
</div>
</div>
</div>

<div class="role-card bibframe-card">
<h3>4️⃣ BIBFRAME (Bibliographic Framework)</h3>
<div class="role-content">
<div class="what-is">
<h4>무엇인가요?</h4>
<p>미국 의회도서관(LOC) 주도로 만든 <strong>웹 시대의 데이터 형식</strong></p>
<p>Linked Data(RDF) 기반으로 서지데이터를 표현</p>
</div>

<div class="key-concept">
<h4>주요 특징</h4>
<ul>
<li>🌐 웹 환경에 최적화 (URI, HTTP, RDF)</li>
<li>🔄 MARC를 대체하는 것이 목표</li>
<li>🔗 다른 데이터와 연결(Link) 쉬움</li>
<li>📊 Work - Instance - Item 구조</li>
</ul>
</div>

<div class="current-status">
<h4>역할</h4>
<p><strong>"기록한 정보를 컴퓨터가 이해하고 웹에서 공유하는 형식"</strong></p>
<p>JSON-LD, RDF/XML 등으로 실제 데이터 교환</p>
</div>
</div>
</div>
</div>

<hr/>

<h2>🔄 실제 업무 흐름</h2>

<div class="workflow-diagram">
<div class="workflow-step">
<div class="workflow-num">1</div>
<div class="workflow-content">
<h4>LRM/FRBR: 개념화</h4>
<p>"세상을 이렇게 보자"</p>
<div class="workflow-example">
이 책은 Work이고, 한국어 번역은 Expression이야
</div>
</div>
</div>

<div class="workflow-arrow">⬇</div>

<div class="workflow-step">
<div class="workflow-num">2</div>
<div class="workflow-content">
<h4>RDA: 기록 규칙</h4>
<p>"그 개념을 바탕으로 이렇게 기록하자"</p>
<div class="workflow-example">
저자: 톨킨, J. R. R. (John Ronald Reuel), 1892-1973
</div>
</div>
</div>

<div class="workflow-arrow">⬇</div>

<div class="workflow-step">
<div class="workflow-num">3</div>
<div class="workflow-content">
<h4>BIBFRAME: 데이터 표현</h4>
<p>"그 기록을 웹에서 이렇게 표현·교환하자"</p>
<div class="workflow-example">
&lt;bf:Work&gt; &lt;bf:creator&gt; &lt;bf:Person&gt; ...
</div>
</div>
</div>
</div>

<hr/>

<h2>📚 실전 예제: "82년생 김지영" 완전 분석</h2>

<div class="example-intro">
<p>하나의 책을 네 가지 관점으로 분석해봅시다!</p>
<p class="book-title">📖 <strong>82년생 김지영</strong> (조남주 지음, 민음사, 2016)</p>
</div>

<div class="example-analysis">
<div class="analysis-panel frbr-panel">
<h3>1️⃣ FRBR/LRM 관점: 엔티티 분해</h3>

<div class="entity-breakdown">
<div class="entity-item work-item">
<div class="entity-label">Work (저작)</div>
<div class="entity-value">조남주가 창작한 소설 "82년생 김지영"</div>
<div class="entity-note">→ 추상적 창작물 자체</div>
</div>

<div class="entity-item expression-item">
<div class="entity-label">Expression (표현형)</div>
<div class="entity-value">
• 한국어 텍스트 (조남주 저술)<br/>
• 영어 번역본 (Jamie Chang 번역)<br/>
• 영화 각본 (김도영 각색)
</div>
<div class="entity-note">→ 언어·형태별 실현</div>
</div>

<div class="entity-item manifestation-item">
<div class="entity-label">Manifestation (구현형)</div>
<div class="entity-value">
• 민음사, 2016년 초판<br/>
• 민음사, 2020년 개정판<br/>
• Scribner, 2020년 (영어판)
</div>
<div class="entity-note">→ 구체적 출판물</div>
</div>

<div class="entity-item item-item">
<div class="entity-label">Item (개별자료)</div>
<div class="entity-value">
• 국립중앙도서관 소장본 (등록번호: CM0123456)<br/>
• 서울도서관 소장본 (등록번호: SL9876543)
</div>
<div class="entity-note">→ 실제 물리적 책</div>
</div>
</div>

<div class="additional-entities">
<h4>관련 엔티티 (LRM)</h4>
<ul>
<li><strong>Agent (행위주체):</strong> 조남주 (Person), 민음사 (Collective Agent)</li>
<li><strong>Nomen (명칭):</strong> "82년생 김지영", "Kim Jiyoung, Born 1982"</li>
<li><strong>Place (장소):</strong> 서울</li>
<li><strong>Timespan (시간):</strong> 2016년</li>
<li><strong>Res (주제):</strong> 성차별, 여성의 삶</li>
</ul>
</div>
</div>

<div class="analysis-panel rda-panel">
<h3>2️⃣ RDA 관점: 목록 기록</h3>

<div class="rda-record">
<table class="record-table">
<tr>
<th>RDA 요소</th>
<th>기록 내용</th>
</tr>
<tr>
<td><strong>저작의 우선 제목</strong></td>
<td>82년생 김지영</td>
</tr>
<tr>
<td><strong>책임표시</strong></td>
<td>조남주 지음</td>
</tr>
<tr>
<td><strong>전거형 접근점</strong></td>
<td>조남주, 1978-</td>
</tr>
<tr>
<td><strong>출판표시</strong></td>
<td>서울 : 민음사, 2016</td>
</tr>
<tr>
<td><strong>형태사항</strong></td>
<td>215 p. ; 21 cm</td>
</tr>
<tr>
<td><strong>ISBN</strong></td>
<td>978-89-374-3763-2 (03810)</td>
</tr>
<tr>
<td><strong>내용유형</strong></td>
<td>텍스트</td>
</tr>
<tr>
<td><strong>매체유형</strong></td>
<td>무매개</td>
</tr>
<tr>
<td><strong>수록매체유형</strong></td>
<td>책</td>
</tr>
<tr>
<td><strong>주제</strong></td>
<td>한국 소설; 여성 문제; 성차별</td>
</tr>
</table>

<div class="rda-note">
<p>💡 <strong>RDA의 역할:</strong></p>
<p>각 항목을 어떤 형식으로 기록할지 세세하게 정의합니다.</p>
<p>예: 저자 이름은 "성, 이름, 생몰연" 형식으로</p>
</div>
</div>
</div>

<div class="analysis-panel bibframe-panel">
<h3>3️⃣ BIBFRAME 관점: 데이터 구조</h3>

<div class="bibframe-structure">
<div class="bf-entity bf-work">
<h4>bf:Work</h4>
<pre class="code-block">&lt;http://example.org/work/82born&gt; a bf:Work ;
  bf:title "82년생 김지영" ;
  bf:creator &lt;http://example.org/agent/cho-namjoo&gt; ;
  bf:subject "성차별"@ko, "여성의 삶"@ko ;
  bf:language &lt;http://id.loc.gov/vocabulary/languages/kor&gt; ;
  bf:genreForm &lt;http://id.loc.gov/authorities/genreForms/gf2014026339&gt; .
  # 소설</pre>
</div>

<div class="bf-entity bf-instance">
<h4>bf:Instance</h4>
<pre class="code-block">&lt;http://example.org/instance/82born-2016&gt; a bf:Instance ;
  bf:instanceOf &lt;http://example.org/work/82born&gt; ;
  bf:title "82년생 김지영" ;
  bf:provisionActivity [
    a bf:Publication ;
    bf:agent &lt;http://example.org/agent/minumsa&gt; ; # 민음사
    bf:place &lt;http://id.loc.gov/vocabulary/countries/ko&gt; ;
    bf:date "2016"
  ] ;
  bf:extent "215 p." ;
  bf:dimensions "21 cm" ;
  bf:identifiedBy [
    a bf:Isbn ;
    rdf:value "9788937437632"
  ] .</pre>
</div>

<div class="bf-entity bf-item">
<h4>bf:Item</h4>
<pre class="code-block">&lt;http://example.org/item/nlk-cm0123456&gt; a bf:Item ;
  bf:itemOf &lt;http://example.org/instance/82born-2016&gt; ;
  bf:heldBy &lt;http://example.org/org/national-library-korea&gt; ;
  bf:shelfMark "813.7-조211ㅍ" ;
  bf:barcode "CM0123456" ;
  bf:status "available" .</pre>
</div>
</div>

<div class="bibframe-note">
<p>💡 <strong>BIBFRAME의 역할:</strong></p>
<p>웹에서 이해할 수 있는 RDF 형식으로 표현하여,</p>
<p>다른 도서관·시스템과 쉽게 데이터를 공유할 수 있습니다.</p>
</div>
</div>
</div>

<hr/>

<h2>📊 핵심 비교표</h2>

<div class="comparison-table-container">
<table class="comparison-table">
<thead>
<tr>
<th>구분</th>
<th>FRBR</th>
<th>LRM</th>
<th>RDA</th>
<th>BIBFRAME</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>역할</strong></td>
<td>개념 모델<br/>(과거)</td>
<td>참조 모델<br/>(현재)</td>
<td>목록 규칙</td>
<td>데이터 형식</td>
</tr>
<tr>
<td><strong>발표</strong></td>
<td>1998년</td>
<td>2017년</td>
<td>2010년<br/>(계속 갱신)</td>
<td>2012년~</td>
</tr>
<tr>
<td><strong>주관 기관</strong></td>
<td>IFLA</td>
<td>IFLA</td>
<td>RSC/ALA</td>
<td>미국 의회도서관</td>
</tr>
<tr>
<td><strong>주요 내용</strong></td>
<td>WEMI 구조</td>
<td>11개 엔티티<br/>통합 모델</td>
<td>기술 요소<br/>작성 규칙</td>
<td>Linked Data<br/>어휘·구조</td>
</tr>
<tr>
<td><strong>사용 목적</strong></td>
<td>개념 이해</td>
<td>기준 제시</td>
<td>목록 작성</td>
<td>데이터 교환</td>
</tr>
<tr>
<td><strong>적용 대상</strong></td>
<td>서지 레코드</td>
<td>서지+전거+주제<br/>모두</td>
<td>모든 자원</td>
<td>서지+소장</td>
</tr>
<tr>
<td><strong>현재 상태</strong></td>
<td>LRM으로 통합</td>
<td>현행 표준</td>
<td>현행 표준</td>
<td>개발 진행 중</td>
</tr>
<tr>
<td><strong>예시</strong></td>
<td>Work, Expression</td>
<td>Agent, Nomen</td>
<td>저자명 기술 규칙</td>
<td>&lt;bf:Work&gt;</td>
</tr>
</tbody>
</table>
</div>

<hr/>

<h2>🎓 관계 정리: 층위별 역할</h2>

<div class="layer-diagram">
<div class="layer layer-1">
<div class="layer-number">Layer 1</div>
<div class="layer-content">
<h4>개념 모델</h4>
<p><strong>LRM</strong> (과거: FRBR)</p>
<p class="layer-desc">"무엇을 어떻게 생각할까?"</p>
<div class="layer-example">
예: Work는 저작, Agent는 행위주체라고 정의
</div>
</div>
</div>

<div class="layer-arrow">⬇ 기반</div>

<div class="layer layer-2">
<div class="layer-number">Layer 2</div>
<div class="layer-content">
<h4>콘텐츠 표준</h4>
<p><strong>RDA</strong></p>
<p class="layer-desc">"무엇을 어떻게 기록할까?"</p>
<div class="layer-example">
예: 저자 이름은 "성, 이름, 생몰연" 형식으로 기술
</div>
</div>
</div>

<div class="layer-arrow">⬇ 구현</div>

<div class="layer layer-3">
<div class="layer-number">Layer 3</div>
<div class="layer-content">
<h4>데이터 형식</h4>
<p><strong>BIBFRAME</strong></p>
<p class="layer-desc">"어떻게 표현하고 공유할까?"</p>
<div class="layer-example">
예: RDF 형식으로 &lt;bf:creator&gt; 사용
</div>
</div>
</div>
</div>

<hr/>

<h2>💡 실무 활용 시나리오</h2>

<div class="scenario-section">
<h3>상황: 새 책이 도서관에 들어왔어요!</h3>

<div class="scenario-steps">
<div class="scenario-step">
<div class="step-label">Step 1</div>
<div class="step-content">
<h4>사서의 생각 (LRM 활용)</h4>
<p>"이건 Work고, 한국어 번역이니 Expression이 다르네."</p>
<p>"저자와 번역자는 모두 Agent야."</p>
<p class="step-note">→ 개념적으로 이해하고 구조화</p>
</div>
</div>

<div class="scenario-step">
<div class="step-label">Step 2</div>
<div class="step-content">
<h4>목록 작성 (RDA 활용)</h4>
<p>RDA Toolkit을 열어서...</p>
<p>"저자명: 롤링, J. K. (Joanne Kathleen), 1965-"</p>
<p>"번역자: 최인자"</p>
<p>"출판: 서울 : 문학수첩, 2014"</p>
<p class="step-note">→ 규칙에 따라 정확히 기록</p>
</div>
</div>

<div class="scenario-step">
<div class="step-label">Step 3</div>
<div class="step-content">
<h4>시스템 입력 (BIBFRAME 활용)</h4>
<p>도서관 시스템이 BIBFRAME을 지원하면...</p>
<p>RDF 형식으로 자동 변환되어 웹에 공개</p>
<p>다른 도서관과 데이터 연계 가능</p>
<p class="step-note">→ 데이터 공유 및 활용</p>
</div>
</div>
</div>
</div>

<hr/>

<h2>🔗 참고 자료</h2>

<div class="references">
<div class="ref-category">
<h4>공식 문서</h4>
<ul>
<li><strong>IFLA LRM:</strong> <a href="https://www.ifla.org/publications/node/11412" target="_blank">https://www.ifla.org/publications/node/11412</a></li>
<li><strong>RDA Toolkit:</strong> <a href="https://www.rdatoolkit.org/" target="_blank">https://www.rdatoolkit.org/</a></li>
<li><strong>BIBFRAME:</strong> <a href="https://www.loc.gov/bibframe/" target="_blank">https://www.loc.gov/bibframe/</a></li>
</ul>
</div>

<div class="ref-category">
<h4>한국어 자료</h4>
<ul>
<li>국립중앙도서관 서지정보유통지원시스템</li>
<li>한국도서관협회 RDA 한국목록규칙</li>
<li>국가서지 LOD (Linked Open Data)</li>
</ul>
</div>
</div>

<hr/>

<h2>📝 학습 정리</h2>

<div class="summary-box">
<h3>🎯 핵심 요약</h3>
<ul class="checkmark-list">
<li>✓ <strong>LRM (현재)</strong> ← FRBR (과거): 개념적으로 "어떻게 생각할까"</li>
<li>✓ <strong>RDA:</strong> 콘텐츠 표준, "어떻게 기록할까"</li>
<li>✓ <strong>BIBFRAME:</strong> 데이터 형식, "어떻게 표현하고 공유할까"</li>
<li>✓ 세 가지는 <strong>층위가 다른 역할</strong>을 하며 상호 연계됩니다</li>
<li>✓ 하나의 책도 네 가지 관점에서 다르게 바라볼 수 있습니다</li>
</ul>
</div>

<div class="final-diagram">
<h3>🔄 전체 흐름 한 번 더!</h3>
<div class="flow-chain">
<div class="flow-item">LRM/FRBR<br/><small>(개념화)</small></div>
<div class="flow-arrow">→</div>
<div class="flow-item">RDA<br/><small>(규칙화)</small></div>
<div class="flow-arrow">→</div>
<div class="flow-item">BIBFRAME<br/><small>(구현화)</small></div>
</div>
<p class="flow-note">이 순서로 도서관의 서지 데이터가 만들어집니다!</p>
</div>

<hr/>

<div class="alert alert-success">
<h3>🎉 학습 완료!</h3>
<p>축하합니다! 도서관 정보학의 핵심 모델들을 모두 이해했습니다.</p>
<p>이제 FRBR, LRM, RDA, BIBFRAME을 헷갈리지 않고 설명할 수 있어요! 💪</p>
<p>각 모델을 더 깊이 공부하고 싶다면, 개별 학습 콘텐츠를 참고하세요.</p>
</div>

<style>
.lead {
    font-size: 1.15em;
    color: #6B7280;
    margin-bottom: 20px;
}

.alert {
    padding: 15px 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.alert-info {
    background-color: #EFF6FF;
    border-left: 4px solid #3B82F6;
    color: #1E40AF;
}

.alert-success {
    background-color: #F0FDF4;
    border-left: 4px solid #10B981;
    color: #166534;
}

.why-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    border-radius: 12px;
    margin: 30px 0;
}

.why-steps {
    margin-top: 25px;
}

.why-step {
    display: flex;
    align-items: flex-start;
    margin: 20px 0;
    padding: 20px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 10px;
}

.step-icon {
    font-size: 2em;
    margin-right: 20px;
}

.step-text {
    flex: 1;
}

.step-text strong {
    display: block;
    font-size: 1.1em;
    margin-bottom: 8px;
}

.model-name {
    color: #FEF3C7;
    font-weight: 600;
    display: block;
    margin-top: 8px;
}

.position-diagram {
    margin: 30px 0;
}

.position-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 20px;
}

@media (max-width: 768px) {
    .position-row {
        grid-template-columns: 1fr;
    }
}

.position-card {
    padding: 25px;
    border-radius: 12px;
    border: 3px solid;
    position: relative;
}

.position-card .badge {
    position: absolute;
    top: 15px;
    right: 15px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 600;
}

.position-card.past {
    background-color: #FEF2F2;
    border-color: #F87171;
}

.position-card.past .badge {
    background-color: #FCA5A5;
    color: #7F1D1D;
}

.position-card.current {
    background-color: #ECFDF5;
    border-color: #34D399;
}

.position-card.current .badge {
    background-color: #6EE7B7;
    color: #064E3B;
}

.position-card.standard {
    background-color: #EFF6FF;
    border-color: #60A5FA;
}

.position-card.standard .badge {
    background-color: #93C5FD;
    color: #1E3A8A;
}

.position-card.implementation {
    background-color: #F5F3FF;
    border-color: #A78BFA;
}

.position-card.implementation .badge {
    background-color: #C4B5FD;
    color: #4C1D95;
}

.position-card h3 {
    margin: 0 0 10px 0;
    font-size: 1.5em;
}

.role {
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 10px;
}

.desc {
    font-size: 0.95em;
    color: #4B5563;
    margin-bottom: 10px;
}

.status {
    font-size: 0.9em;
    color: #6B7280;
    font-style: italic;
}

.roles-section {
    margin: 30px 0;
}

.role-card {
    margin: 25px 0;
    padding: 25px;
    border-radius: 12px;
    border-left: 5px solid;
}

.frbr-card {
    background-color: #FEF3C7;
    border-color: #F59E0B;
}

.lrm-card {
    background-color: #D1FAE5;
    border-color: #10B981;
}

.rda-card {
    background-color: #DBEAFE;
    border-color: #3B82F6;
}

.bibframe-card {
    background-color: #E9D5FF;
    border-color: #A855F7;
}

.role-card h3 {
    margin-top: 0;
    margin-bottom: 20px;
}

.role-content {
    display: grid;
    gap: 20px;
}

.what-is, .key-concept, .current-status {
    background-color: rgba(255, 255, 255, 0.6);
    padding: 15px;
    border-radius: 8px;
}

.what-is h4, .key-concept h4, .current-status h4 {
    margin-top: 0;
    margin-bottom: 10px;
    color: #1F2937;
}

.wemi-boxes {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-top: 15px;
}

@media (max-width: 768px) {
    .wemi-boxes {
        grid-template-columns: repeat(2, 1fr);
    }
}

.wemi-box {
    background-color: white;
    padding: 15px;
    text-align: center;
    border-radius: 6px;
    font-weight: 600;
}

.wemi-box span {
    display: block;
    font-size: 0.85em;
    font-weight: 400;
    color: #6B7280;
    margin-top: 5px;
}

.workflow-diagram {
    background-color: #F9FAFB;
    padding: 30px;
    border-radius: 12px;
    margin: 30px 0;
}

.workflow-step {
    display: flex;
    align-items: flex-start;
    margin: 20px 0;
}

.workflow-num {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.2em;
    flex-shrink: 0;
    margin-right: 20px;
}

.workflow-content {
    flex: 1;
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.workflow-content h4 {
    margin-top: 0;
    margin-bottom: 5px;
}

.workflow-example {
    background-color: #F3F4F6;
    padding: 12px;
    border-radius: 6px;
    margin-top: 10px;
    font-family: monospace;
    font-size: 0.9em;
}

.workflow-arrow {
    text-align: center;
    font-size: 1.5em;
    color: #6B7280;
    margin: 10px 0;
}

.example-intro {
    background: linear-gradient(to right, #FEF3C7, #DBEAFE);
    padding: 20px;
    border-radius: 10px;
    margin: 25px 0;
    text-align: center;
}

.book-title {
    font-size: 1.3em;
    margin-top: 10px;
}

.example-analysis {
    margin: 30px 0;
}

.analysis-panel {
    margin: 25px 0;
    padding: 25px;
    border-radius: 12px;
    border-left: 5px solid;
}

.frbr-panel {
    background-color: #FEF3C7;
    border-color: #F59E0B;
}

.rda-panel {
    background-color: #DBEAFE;
    border-color: #3B82F6;
}

.bibframe-panel {
    background-color: #E9D5FF;
    border-color: #A855F7;
}

.analysis-panel h3 {
    margin-top: 0;
    margin-bottom: 20px;
}

.entity-breakdown {
    margin: 20px 0;
}

.entity-item {
    margin: 15px 0;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid;
}

.work-item {
    background-color: rgba(245, 158, 11, 0.1);
    border-color: #F59E0B;
}

.expression-item {
    background-color: rgba(59, 130, 246, 0.1);
    border-color: #3B82F6;
}

.manifestation-item {
    background-color: rgba(16, 185, 129, 0.1);
    border-color: #10B981;
}

.item-item {
    background-color: rgba(168, 85, 247, 0.1);
    border-color: #A855F7;
}

.entity-label {
    font-weight: 700;
    color: #1F2937;
    margin-bottom: 8px;
}

.entity-value {
    color: #4B5563;
    margin-bottom: 5px;
}

.entity-note {
    font-size: 0.85em;
    color: #6B7280;
    font-style: italic;
}

.additional-entities {
    margin-top: 20px;
    padding: 15px;
    background-color: rgba(255, 255, 255, 0.6);
    border-radius: 8px;
}

.additional-entities h4 {
    margin-top: 0;
}

.record-table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
    margin: 15px 0;
}

.record-table th,
.record-table td {
    padding: 12px;
    text-align: left;
    border: 1px solid #E5E7EB;
}

.record-table th {
    background-color: #F3F4F6;
    font-weight: 600;
}

.rda-note {
    background-color: rgba(255, 255, 255, 0.6);
    padding: 15px;
    border-radius: 8px;
    margin-top: 20px;
}

.bibframe-structure {
    margin: 20px 0;
}

.bf-entity {
    margin: 15px 0;
    padding: 15px;
    background-color: rgba(255, 255, 255, 0.6);
    border-radius: 8px;
}

.bf-entity h4 {
    margin-top: 0;
    margin-bottom: 10px;
}

.code-block {
    background-color: #1F2937;
    color: #F9FAFB;
    padding: 15px;
    border-radius: 6px;
    overflow-x: auto;
    font-family: 'Courier New', monospace;
    font-size: 0.85em;
    line-height: 1.6;
}

.bibframe-note {
    background-color: rgba(255, 255, 255, 0.6);
    padding: 15px;
    border-radius: 8px;
    margin-top: 20px;
}

.comparison-table-container {
    overflow-x: auto;
    margin: 25px 0;
}

.comparison-table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
}

.comparison-table th,
.comparison-table td {
    padding: 12px;
    text-align: left;
    border: 1px solid #E5E7EB;
}

.comparison-table thead {
    background: linear-gradient(to right, #667eea, #764ba2);
    color: white;
}

.comparison-table tbody tr:nth-child(even) {
    background-color: #F9FAFB;
}

.layer-diagram {
    margin: 30px 0;
}

.layer {
    margin: 20px 0;
    padding: 25px;
    border-radius: 12px;
    position: relative;
}

.layer-1 {
    background: linear-gradient(to right, #ECFDF5, #D1FAE5);
    border: 3px solid #10B981;
}

.layer-2 {
    background: linear-gradient(to right, #EFF6FF, #DBEAFE);
    border: 3px solid #3B82F6;
}

.layer-3 {
    background: linear-gradient(to right, #F5F3FF, #E9D5FF);
    border: 3px solid #A855F7;
}

.layer-number {
    position: absolute;
    top: -15px;
    left: 20px;
    background-color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: 700;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.layer-content h4 {
    margin: 0 0 10px 0;
    font-size: 1.2em;
}

.layer-desc {
    color: #4B5563;
    margin: 10px 0;
}

.layer-example {
    background-color: rgba(255, 255, 255, 0.8);
    padding: 12px;
    border-radius: 6px;
    margin-top: 10px;
    font-size: 0.9em;
}

.layer-arrow {
    text-align: center;
    font-size: 1.3em;
    color: #6B7280;
    font-weight: 600;
    margin: 15px 0;
}

.scenario-section {
    background-color: #FFFBEB;
    padding: 30px;
    border-radius: 12px;
    margin: 30px 0;
}

.scenario-section h3 {
    margin-top: 0;
    color: #92400E;
}

.scenario-steps {
    margin-top: 20px;
}

.scenario-step {
    margin: 20px 0;
    display: flex;
    align-items: flex-start;
}

.step-label {
    background: linear-gradient(135deg, #F59E0B, #D97706);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9em;
    margin-right: 15px;
    flex-shrink: 0;
}

.step-content {
    flex: 1;
    background-color: white;
    padding: 20px;
    border-radius: 10px;
}

.step-content h4 {
    margin-top: 0;
    margin-bottom: 10px;
}

.step-note {
    display: block;
    margin-top: 10px;
    font-size: 0.9em;
    color: #6B7280;
    font-style: italic;
}

.references {
    background-color: #F3F4F6;
    padding: 25px;
    border-radius: 10px;
    margin: 25px 0;
}

.ref-category {
    margin: 15px 0;
}

.ref-category h4 {
    color: #1F2937;
    margin-bottom: 10px;
}

.summary-box {
    background: linear-gradient(to bottom right, #EFF6FF, #F0FDFA);
    padding: 25px;
    border-radius: 12px;
    border: 2px solid #93C5FD;
    margin: 25px 0;
}

.summary-box h3 {
    margin-top: 0;
    color: #1E40AF;
}

.checkmark-list {
    list-style: none;
    padding: 0;
}

.checkmark-list li {
    padding: 8px 0;
    font-size: 1.05em;
}

.final-diagram {
    background-color: #F5F3FF;
    padding: 25px;
    border-radius: 10px;
    margin: 25px 0;
    text-align: center;
}

.flow-chain {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
    margin: 20px 0;
}

.flow-item {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px 25px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 1.1em;
}

.flow-item small {
    display: block;
    font-size: 0.75em;
    font-weight: 400;
    margin-top: 5px;
}

.flow-arrow {
    font-size: 1.5em;
    color: #6B7280;
    font-weight: bold;
}

.flow-note {
    margin-top: 15px;
    color: #5B21B6;
    font-weight: 500;
}
</style>
"""

# 5. 학습 콘텐츠 생성 또는 업데이트
existing_content = Content.objects.filter(slug='bibliographic-models-overview').first()

if existing_content:
    print(f"\n⚠️  'bibliographic-models-overview' 슬러그를 가진 콘텐츠가 이미 존재합니다.")
    print(f"   기존 콘텐츠를 업데이트합니다: {existing_content.title}")

    existing_content.title = "FRBR/LRM/RDA/BIBFRAME 한눈에 이해하기"
    existing_content.summary = "헷갈리는 도서관 핵심 모델들(FRBR, LRM, RDA, BIBFRAME)의 역할과 관계를 명쾌하게 정리하고, 실전 예제로 쉽게 배웁니다."
    existing_content.content_html = content_html
    existing_content.category = comparison_category
    existing_content.difficulty = 'BEGINNER'
    existing_content.estimated_time = 50
    existing_content.prerequisites = None
    existing_content.learning_objectives = "FRBR, LRM, RDA, BIBFRAME의 역할과 위치 관계 이해, 실제 책을 네 가지 관점으로 분석, 도서관 업무 흐름 파악"
    existing_content.status = Content.Status.PUBLISHED
    existing_content.save()

    existing_content.tags.clear()
    existing_content.tags.set(tags)

    print(f"✅ 콘텐츠가 업데이트되었습니다!")
else:
    content = Content.objects.create(
        title="FRBR/LRM/RDA/BIBFRAME 한눈에 이해하기",
        slug="bibliographic-models-overview",
        summary="헷갈리는 도서관 핵심 모델들(FRBR, LRM, RDA, BIBFRAME)의 역할과 관계를 명쾌하게 정리하고, 실전 예제로 쉽게 배웁니다.",
        content_html=content_html,
        category=comparison_category,
        author=admin,
        difficulty='BEGINNER',
        estimated_time=50,
        prerequisites="",
        learning_objectives="FRBR, LRM, RDA, BIBFRAME의 역할과 위치 관계 이해, 실제 책을 네 가지 관점으로 분석, 도서관 업무 흐름 파악",
        version="1.0",
        status=Content.Status.PUBLISHED
    )

    content.tags.set(tags)

    print(f"\n✅ 학습 콘텐츠가 생성되었습니다!")

print(f"\n📊 콘텐츠 정보:")
print(f"  - 제목: FRBR/LRM/RDA/BIBFRAME 한눈에 이해하기")
print(f"  - 슬러그: bibliographic-models-overview")
print(f"  - 카테고리: {comparison_category.name} (상위: {overview_category.name})")
print(f"  - 난이도: 초급 (대학 신입생 대상)")
print(f"  - 소요시간: 50분")
print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
print(f"  - 공개 상태: 공개")
print(f"\n💡 확인:")
print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=overview")
print(f"  - 상세 페이지: http://localhost:3000/contents/bibliographic-models-overview")
