"""
LRM (Library Reference Model) 학습 콘텐츠 추가 스크립트
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

# 1. 개념 모델 카테고리 가져오기
conceptual_model_category = Category.objects.filter(slug='conceptual-model').first()
if not conceptual_model_category:
    print("❌ 개념 모델 카테고리를 찾을 수 없습니다.")
    exit(1)

print(f"✓ 상위 카테고리 확인: {conceptual_model_category.name}")

# 2. LRM 하위 카테고리 생성
lrm_category, created = Category.objects.get_or_create(
    slug='lrm',
    defaults={
        'name': 'LRM',
        'description': '도서관 참조 모델',
        'parent': conceptual_model_category,
        'is_active': True
    }
)
if created:
    print(f"✓ 하위 카테고리 생성: {lrm_category.name}")
else:
    print(f"✓ 하위 카테고리 확인: {lrm_category.name}")

# 3. 태그 생성
tag, created = Tag.objects.get_or_create(
    name='개념 참조 모델',
    defaults={'slug': 'conceptual-reference-model'}
)
if created:
    print(f"✓ 태그 생성: {tag.name}")
else:
    print(f"✓ 태그 확인: {tag.name}")

# 4. LRM 학습 콘텐츠 HTML
content_html = """
<h2>LRM 완전 정복</h2>
<p class="lead">FRBR을 더욱 발전시킨 차세대 도서관 참조 모델을 배워봅시다!</p>

<div class="alert alert-info">
<strong>💡 학습 목표:</strong>
<ul>
<li>LRM이 무엇이고 왜 필요한지 이해합니다</li>
<li>FRBR과 LRM의 차이점을 파악합니다</li>
<li>LRM의 핵심 엔티티와 관계를 활용할 수 있습니다</li>
<li>실제 도서관 데이터를 LRM으로 모델링할 수 있습니다</li>
</ul>
</div>

<hr/>

<h2>LRM이 뭔가요?</h2>

<div class="intro-box">
<p><strong>LRM (Library Reference Model)</strong>은 2017년 IFLA가 발표한 도서관 정보 자원의 최신 개념 모델입니다.</p>
<p>FRBR, FRAD, FRSAD 3개 모델을 통합하고 단순화했습니다.</p>
</div>

<h3>📜 역사적 배경</h3>

<div class="timeline">
<div class="timeline-item">
<div class="year">1998년</div>
<div class="event"><strong>FRBR</strong> 발표 - 서지 레코드의 기능 요건</div>
</div>

<div class="timeline-item">
<div class="year">2009년</div>
<div class="event"><strong>FRAD</strong> 발표 - 전거 데이터의 기능 요건</div>
</div>

<div class="timeline-item">
<div class="year">2010년</div>
<div class="event"><strong>FRSAD</strong> 발표 - 주제 전거 데이터의 기능 요건</div>
</div>

<div class="timeline-item">
<div class="year">2017년</div>
<div class="event"><strong>LRM</strong> 발표 - 3개 모델 통합 및 개선! 🎉</div>
</div>
</div>

<h3>🤔 왜 LRM이 필요했을까요?</h3>

<div class="problem-solution-grid">
<div class="problem-box">
<h4>😰 기존의 문제</h4>
<ul>
<li>FRBR, FRAD, FRSAD가 각각 독립적</li>
<li>모델 간 중복과 불일치</li>
<li>총 33개의 엔티티로 너무 복잡</li>
<li>용어와 개념이 일관성 없음</li>
<li>실무 적용이 어려움</li>
</ul>
</div>

<div class="solution-box">
<h4>✨ LRM의 해결</h4>
<ul>
<li>하나로 통합된 일관성 있는 모델</li>
<li>엔티티를 11개로 단순화</li>
<li>더 명확하고 일관된 용어</li>
<li>RDA(목록 규칙)와 완벽 연계</li>
<li>실무 적용 용이</li>
</ul>
</div>
</div>

<hr/>

<h2>LRM의 핵심 엔티티</h2>

<p>LRM은 <strong>11개의 엔티티</strong>로 도서관 세계를 설명합니다.</p>

<div class="entities-overview">
<div class="entity-category">
<h3>📚 제1그룹: 정보 자원</h3>
<div class="entity-grid">
<div class="entity-card work-card">
<h4>Work (저작)</h4>
<p>창작된 지적·예술적 내용</p>
<p class="example">예: 톨스토이의 "전쟁과 평화"</p>
</div>

<div class="entity-card expression-card">
<h4>Expression (표현형)</h4>
<p>저작의 실현</p>
<p class="example">예: 한국어 번역본</p>
</div>

<div class="entity-card manifestation-card">
<h4>Manifestation (구현형)</h4>
<p>표현형의 물리적/디지털 구현</p>
<p class="example">예: 민음사 2015년판</p>
</div>

<div class="entity-card item-card">
<h4>Item (개별자료)</h4>
<p>구현형의 개별 예시</p>
<p class="example">예: 서울도서관 소장본</p>
</div>
</div>
</div>

<div class="entity-category">
<h3>👥 제2그룹: 행위주체</h3>
<div class="entity-grid">
<div class="entity-card agent-card">
<h4>Agent (행위주체)</h4>
<p>행동하는 존재</p>
<div class="sub-entities">
<div><strong>Person:</strong> 개인 (예: 톨스토이)</div>
<div><strong>Collective Agent:</strong> 집단 (예: 민음사)</div>
</div>
</div>
</div>
</div>

<div class="entity-category">
<h3>🏷️ 제3그룹: 부가 정보</h3>
<div class="entity-grid">
<div class="entity-card nomen-card">
<h4>Nomen (명칭)</h4>
<p>엔티티를 지칭하는 이름</p>
<p class="example">예: "War and Peace", "전쟁과 평화"</p>
</div>

<div class="entity-card place-card">
<h4>Place (장소)</h4>
<p>지리적 위치</p>
<p class="example">예: 러시아, 서울</p>
</div>

<div class="entity-card timespan-card">
<h4>Timespan (시간범위)</h4>
<p>시간적 범위</p>
<p class="example">예: 1869년, 2015년</p>
</div>
</div>
</div>

<div class="entity-category">
<h3>🎯 제4그룹: 개념적 대상</h3>
<div class="entity-grid">
<div class="entity-card res-card">
<h4>Res (사물/개념)</h4>
<p>주제로서의 모든 것</p>
<p class="example">예: 전쟁, 평화, 사랑</p>
</div>
</div>
</div>
</div>

<hr/>

<h2>FRBR에서 LRM으로: 무엇이 달라졌나?</h2>

<h3>1️⃣ 엔티티 통합 및 단순화</h3>

<div class="comparison-box">
<div class="before">
<h4>FRBR 패밀리 (통합 전)</h4>
<ul>
<li>FRBR: 10개 엔티티</li>
<li>FRAD: 10개 엔티티</li>
<li>FRSAD: 13개 엔티티</li>
<li><strong>총 33개 엔티티</strong> 😵</li>
</ul>
</div>

<div class="arrow-right">→</div>

<div class="after">
<h4>LRM (통합 후)</h4>
<ul>
<li>핵심 엔티티: 11개</li>
<li>명확한 계층 구조</li>
<li>일관된 용어</li>
<li><strong>훨씬 단순! 😊</strong></li>
</ul>
</div>
</div>

<h3>2️⃣ Nomen: 새로운 개념</h3>

<div class="highlight-box">
<p><strong>LRM의 가장 큰 혁신: Nomen (명칭)</strong></p>
<p>FRBR에서는 제목, 이름 등이 단순한 속성이었습니다.</p>
<p>LRM에서는 <strong>Nomen을 별도 엔티티</strong>로 취급합니다!</p>
</div>

<div class="nomen-example">
<h4>📖 예시: "해리포터와 마법사의 돌"</h4>

<div class="nomen-cards">
<div class="nomen-item">
<div class="label">영어 원제</div>
<div class="value">"Harry Potter and the Philosopher's Stone"</div>
<div class="note">Nomen 1</div>
</div>

<div class="nomen-item">
<div class="label">한국어 제목</div>
<div class="value">"해리포터와 마법사의 돌"</div>
<div class="note">Nomen 2</div>
</div>

<div class="nomen-item">
<div class="label">미국판 제목</div>
<div class="value">"Harry Potter and the Sorcerer's Stone"</div>
<div class="note">Nomen 3</div>
</div>
</div>

<p class="insight">💡 각 제목을 <strong>독립된 엔티티</strong>로 관리하여 다국어, 이형 처리가 쉬워졌습니다!</p>
</div>

<h3>3️⃣ Person과 Collective Agent 통합</h3>

<div class="integration-example">
<p>FRBR에서 Person과 Corporate Body가 별개였던 것을</p>
<p>LRM에서는 <strong>Agent</strong> 하나로 통합하고 하위 분류했습니다.</p>

<div class="agent-hierarchy">
<div class="agent-root">Agent (행위주체)</div>
<div class="agent-children">
<div class="agent-child person">Person (개인)</div>
<div class="agent-child collective">Collective Agent (집단)</div>
</div>
</div>
</div>

<hr/>

<h2>실전 예제: "82년생 김지영" 분석</h2>

<div class="practice-example">
<h3>📚 LRM으로 완전 분해하기</h3>

<div class="lrm-analysis">
<div class="analysis-section work-section">
<h4>🎨 Work (저작)</h4>
<p><strong>조남주가 창작한 소설 "82년생 김지영"</strong></p>
<div class="relations">
<div class="relation">
<span class="rel-label">created by</span>
<span class="rel-value">→ Agent: 조남주 (Person)</span>
</div>
<div class="relation">
<span class="rel-label">has subject</span>
<span class="rel-value">→ Res: 성차별, 여성의 삶</span>
</div>
<div class="relation">
<span class="rel-label">has nomen</span>
<span class="rel-value">→ Nomen: "82년생 김지영"</span>
</div>
</div>
</div>

<div class="analysis-section expression-section">
<h4>📝 Expression (표현형)</h4>
<div class="expressions">
<div class="expr-item">
<strong>한국어 텍스트</strong> (조남주 저술)
<div class="expr-relation">
<span class="rel-label">expressed in</span>
<span class="rel-value">→ 한국어</span>
</div>
</div>
<div class="expr-item">
<strong>영어 번역본</strong> (Jamie Chang 번역)
<div class="expr-relation">
<span class="rel-label">created by</span>
<span class="rel-value">→ Agent: Jamie Chang (Person)</span>
</div>
<div class="expr-relation">
<span class="rel-label">has nomen</span>
<span class="rel-value">→ Nomen: "Kim Jiyoung, Born 1982"</span>
</div>
</div>
<div class="expr-item">
<strong>영화 각본</strong> (김도영 각색)
</div>
</div>
</div>

<div class="analysis-section manifestation-section">
<h4>📖 Manifestation (구현형)</h4>
<div class="manifestations">
<div class="manif-item">
<strong>민음사, 2016년 초판</strong>
<div class="manif-details">
<div>출판사: Agent (Collective Agent) - 민음사</div>
<div>출판지: Place - 서울</div>
<div>출판연도: Timespan - 2016년</div>
<div>ISBN: Nomen - 9788937437632</div>
</div>
</div>
<div class="manif-item">
<strong>영어판: Scribner, 2020년</strong>
<div class="manif-details">
<div>출판사: Agent - Scribner</div>
<div>출판지: Place - New York</div>
</div>
</div>
</div>
</div>

<div class="analysis-section item-section">
<h4>📕 Item (개별자료)</h4>
<div class="items">
<div class="item-box">
국립중앙도서관 소장본
<div class="item-detail">등록번호: CM0123456</div>
<div class="item-detail">상태: 양호</div>
</div>
<div class="item-box">
서울도서관 소장본
<div class="item-detail">등록번호: SL9876543</div>
<div class="item-detail">상태: 대출 중</div>
</div>
</div>
</div>
</div>
</div>

<hr/>

<h2>LRM의 핵심 관계</h2>

<p>LRM은 엔티티 간의 <strong>관계</strong>를 명확하게 정의합니다.</p>

<h3>1️⃣ 생성 관계 (Creation Relationships)</h3>

<div class="relationship-examples">
<div class="rel-example">
<div class="rel-name">created by / created</div>
<div class="rel-desc">Work ↔ Agent</div>
<div class="rel-sample">
예: "해리포터" <strong>created by</strong> J.K. 롤링<br/>
J.K. 롤링 <strong>created</strong> "해리포터"
</div>
</div>

<div class="rel-example">
<div class="rel-name">realized by / realized</div>
<div class="rel-desc">Expression ↔ Agent</div>
<div class="rel-sample">
예: 한국어 번역본 <strong>realized by</strong> 최인자<br/>
최인자 <strong>realized</strong> 한국어 번역본
</div>
</div>

<div class="rel-example">
<div class="rel-name">published by / published</div>
<div class="rel-desc">Manifestation ↔ Agent</div>
<div class="rel-sample">
예: 2020년판 <strong>published by</strong> 민음사<br/>
민음사 <strong>published</strong> 2020년판
</div>
</div>
</div>

<h3>2️⃣ 명칭 관계 (Appellation Relationships)</h3>

<div class="appellation-box">
<p>모든 엔티티는 <strong>Nomen (명칭)</strong>을 가질 수 있습니다.</p>

<div class="appellation-examples">
<div class="app-item">
<strong>Work has nomen:</strong> "반지의 제왕", "The Lord of the Rings"
</div>
<div class="app-item">
<strong>Agent has nomen:</strong> "톨킨", "J.R.R. Tolkien", "존 로널드 루엘 톨킨"
</div>
<div class="app-item">
<strong>Place has nomen:</strong> "서울", "Seoul", "漢城"
</div>
</div>
</div>

<h3>3️⃣ 주제 관계 (Subject Relationships)</h3>

<div class="subject-examples">
<p>Work는 어떤 것이든 <strong>주제</strong>로 가질 수 있습니다.</p>

<div class="subject-grid">
<div class="subject-item">
Work → <strong>Work</strong><br/>
<span class="example">"돈키호테 해설서"의 주제는 "돈키호테"</span>
</div>
<div class="subject-item">
Work → <strong>Person</strong><br/>
<span class="example">"스티브 잡스 전기"의 주제는 스티브 잡스</span>
</div>
<div class="subject-item">
Work → <strong>Place</strong><br/>
<span class="example">"서울 가이드북"의 주제는 서울</span>
</div>
<div class="subject-item">
Work → <strong>Res</strong><br/>
<span class="example">"사랑의 철학"의 주제는 사랑(개념)</span>
</div>
</div>
</div>

<hr/>

<h2>LRM의 실무 적용</h2>

<h3>🔗 RDA와의 연계</h3>

<div class="rda-connection">
<p><strong>RDA (Resource Description and Access)</strong>는 LRM을 기반으로 한 최신 목록 규칙입니다.</p>

<div class="rda-lrm-mapping">
<table class="table">
<thead>
<tr>
<th>LRM 엔티티</th>
<th>RDA 적용</th>
<th>목록 작성 예시</th>
</tr>
</thead>
<tbody>
<tr>
<td>Work</td>
<td>Authorized Access Point</td>
<td>톨스토이. 전쟁과 평화</td>
</tr>
<tr>
<td>Expression</td>
<td>언어, 형태 기록</td>
<td>한국어 번역. 텍스트</td>
</tr>
<tr>
<td>Manifestation</td>
<td>서지사항 기술</td>
<td>서울 : 민음사, 2015</td>
</tr>
<tr>
<td>Agent</td>
<td>전거 형식</td>
<td>톨스토이, 레프, 1828-1910</td>
</tr>
</tbody>
</table>
</div>
</div>

<h3>📊 도서관 시스템 구현</h3>

<div class="implementation-examples">
<h4>LRM을 적용한 검색 시나리오:</h4>

<div class="search-scenario">
<div class="scenario-step">
<div class="step-num">1</div>
<div class="step-content">
<strong>사용자가 "해리포터" 검색</strong><br/>
→ Work 수준에서 검색
</div>
</div>

<div class="scenario-step">
<div class="step-num">2</div>
<div class="step-content">
<strong>관련된 모든 Expression 표시</strong><br/>
→ 한국어판, 영어판, 오디오북, 영화 등
</div>
</div>

<div class="scenario-step">
<div class="step-num">3</div>
<div class="step-content">
<strong>원하는 Expression 선택</strong><br/>
→ 예: 한국어 번역본
</div>
</div>

<div class="scenario-step">
<div class="step-num">4</div>
<div class="step-content">
<strong>해당 Manifestation 목록</strong><br/>
→ 문학수첩 2000년판, 민음사 2014년판 등
</div>
</div>

<div class="scenario-step">
<div class="step-num">5</div>
<div class="step-content">
<strong>소장 Item 확인</strong><br/>
→ 서울도서관 대출 가능, 강남도서관 대출 중
</div>
</div>
</div>
</div>

<hr/>

<h2>LRM vs FRBR 비교표</h2>

<div class="comparison-table">
<table class="table">
<thead>
<tr>
<th>항목</th>
<th>FRBR</th>
<th>LRM</th>
<th>개선 사항</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>발표 연도</strong></td>
<td>1998년</td>
<td>2017년</td>
<td>최신 기술 환경 반영</td>
</tr>
<tr>
<td><strong>모델 범위</strong></td>
<td>서지 레코드만</td>
<td>서지+전거+주제 통합</td>
<td>포괄적</td>
</tr>
<tr>
<td><strong>엔티티 수</strong></td>
<td>10개 (Group 1~3)</td>
<td>11개 (통합)</td>
<td>단순화</td>
</tr>
<tr>
<td><strong>명칭 처리</strong></td>
<td>속성으로 처리</td>
<td>Nomen 엔티티</td>
<td>다국어 지원 강화</td>
</tr>
<tr>
<td><strong>행위주체</strong></td>
<td>Person, Corporate Body, Family 분리</td>
<td>Agent로 통합</td>
<td>일관성 향상</td>
</tr>
<tr>
<td><strong>용어 일관성</strong></td>
<td>모델 간 불일치</td>
<td>전체 통일</td>
<td>이해 용이</td>
</tr>
<tr>
<td><strong>RDA 연계</strong></td>
<td>부분적</td>
<td>완전 연계</td>
<td>실무 적용성 ↑</td>
</tr>
</tbody>
</table>
</div>

<hr/>

<h2>LRM의 장점</h2>

<div class="benefits-grid">
<div class="benefit-card">
<h4>✅ 1. 단순성</h4>
<p>3개 모델을 하나로 통합하여 이해하기 쉬워졌습니다.</p>
</div>

<div class="benefit-card">
<h4>✅ 2. 일관성</h4>
<p>모든 엔티티와 관계가 일관된 원칙으로 정의되었습니다.</p>
</div>

<div class="benefit-card">
<h4>✅ 3. 확장성</h4>
<p>Nomen 개념으로 다국어, 이형 처리가 유연해졌습니다.</p>
</div>

<div class="benefit-card">
<h4>✅ 4. 실용성</h4>
<p>RDA와 완벽 연계로 실제 목록 작성에 바로 적용 가능합니다.</p>
</div>

<div class="benefit-card">
<h4>✅ 5. 상호운용성</h4>
<p>국제 표준으로 전 세계 도서관과 데이터 공유가 쉬워졌습니다.</p>
</div>

<div class="benefit-card">
<h4>✅ 6. 미래 지향성</h4>
<p>디지털 환경, 링크드 데이터에 최적화되었습니다.</p>
</div>
</div>

<hr/>

<h2>학습 정리</h2>

<div class="summary-box">
<h3>🎯 핵심 요약</h3>
<ul class="checkmark-list">
<li>✓ <strong>LRM은 FRBR의 발전형:</strong> 3개 모델(FRBR, FRAD, FRSAD) 통합</li>
<li>✓ <strong>11개 엔티티로 단순화:</strong> Work, Expression, Manifestation, Item, Agent, Nomen, Place, Timespan, Res 등</li>
<li>✓ <strong>Nomen이 핵심:</strong> 명칭을 별도 엔티티로 관리 → 다국어 지원 강화</li>
<li>✓ <strong>RDA와 완벽 연계:</strong> 실무에 바로 적용 가능</li>
<li>✓ <strong>FRBR보다 실용적:</strong> 일관성, 단순성, 확장성 모두 개선</li>
</ul>
</div>

<div class="comparison-summary">
<h3>📊 한눈에 보는 FRBR → LRM</h3>
<div class="evolution-diagram">
<div class="evo-before">
<strong>FRBR 시대</strong>
<ul>
<li>3개 모델 분리</li>
<li>33개 엔티티</li>
<li>복잡하고 불일치</li>
</ul>
</div>
<div class="evo-arrow">⟹</div>
<div class="evo-after">
<strong>LRM 시대</strong>
<ul>
<li>1개 통합 모델</li>
<li>11개 엔티티</li>
<li>단순하고 일관성</li>
</ul>
</div>
</div>
</div>

<div class="next-steps">
<h3>📚 다음 학습</h3>
<ul>
<li><strong>RDA (Resource Description and Access):</strong> LRM 기반 목록 규칙</li>
<li><strong>BIBFRAME:</strong> 미국 의회도서관의 LRM 구현</li>
<li><strong>링크드 데이터:</strong> LRM의 웹 환경 적용</li>
<li><strong>실전 목록 작성:</strong> RDA를 이용한 서지 레코드 작성</li>
</ul>
</div>

<hr/>

<div class="alert alert-success">
<h3>🎉 학습 완료!</h3>
<p>축하합니다! LRM의 모든 핵심 개념을 학습했습니다.</p>
<p>이제 현대 도서관의 최신 표준을 이해하게 되었어요! 🌟</p>
<p>FRBR을 이미 학습했다면, 두 모델을 비교하며 발전 과정을 되짚어보세요.</p>
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

.intro-box {
    background: linear-gradient(to right, #EFF6FF, #F5F3FF);
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #6366F1;
    margin: 20px 0;
}

.timeline {
    margin: 25px 0;
    padding-left: 20px;
    border-left: 3px solid #3B82F6;
}

.timeline-item {
    margin: 15px 0;
    padding-left: 20px;
    position: relative;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: -23px;
    top: 5px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #3B82F6;
}

.year {
    font-weight: 700;
    color: #1E40AF;
    font-size: 1.1em;
}

.event {
    color: #4B5563;
    margin-top: 5px;
}

.problem-solution-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin: 25px 0;
}

@media (max-width: 768px) {
    .problem-solution-grid {
        grid-template-columns: 1fr;
    }
}

.problem-box {
    background-color: #FEF2F2;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #EF4444;
}

.solution-box {
    background-color: #F0FDF4;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #10B981;
}

.entities-overview {
    margin: 30px 0;
}

.entity-category {
    margin: 30px 0;
}

.entity-category h3 {
    color: #1F2937;
    margin-bottom: 15px;
}

.entity-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
}

.entity-card {
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid;
}

.entity-card h4 {
    margin-top: 0;
    margin-bottom: 8px;
}

.work-card {
    background-color: #FEF3C7;
    border-color: #F59E0B;
}

.expression-card {
    background-color: #DBEAFE;
    border-color: #3B82F6;
}

.manifestation-card {
    background-color: #D1FAE5;
    border-color: #10B981;
}

.item-card {
    background-color: #E9D5FF;
    border-color: #A855F7;
}

.agent-card {
    background-color: #FCE7F3;
    border-color: #EC4899;
}

.nomen-card {
    background-color: #FEF3C7;
    border-color: #FBBF24;
}

.place-card {
    background-color: #DBEAFE;
    border-color: #60A5FA;
}

.timespan-card {
    background-color: #E9D5FF;
    border-color: #C084FC;
}

.res-card {
    background-color: #D1FAE5;
    border-color: #34D399;
}

.example {
    font-size: 0.9em;
    color: #6B7280;
    font-style: italic;
    margin-top: 5px;
}

.sub-entities {
    margin-top: 10px;
    font-size: 0.9em;
}

.sub-entities div {
    margin: 5px 0;
}

.comparison-box {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 20px;
    align-items: center;
    margin: 25px 0;
    padding: 20px;
    background-color: #F9FAFB;
    border-radius: 10px;
}

@media (max-width: 768px) {
    .comparison-box {
        grid-template-columns: 1fr;
    }
    .arrow-right {
        display: none;
    }
}

.before, .after {
    padding: 15px;
    border-radius: 8px;
}

.before {
    background-color: #FEF2F2;
    border-left: 4px solid #EF4444;
}

.after {
    background-color: #F0FDF4;
    border-left: 4px solid #10B981;
}

.arrow-right {
    font-size: 2em;
    color: #6B7280;
    font-weight: bold;
}

.highlight-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 25px 0;
}

.highlight-box strong {
    color: #FEF3C7;
}

.nomen-example {
    background-color: #FFFBEB;
    padding: 25px;
    border-radius: 10px;
    margin: 25px 0;
}

.nomen-cards {
    display: grid;
    gap: 15px;
    margin: 20px 0;
}

.nomen-item {
    background-color: white;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #F59E0B;
}

.label {
    font-weight: 600;
    color: #92400E;
    font-size: 0.9em;
}

.value {
    font-size: 1.1em;
    margin: 8px 0;
    color: #1F2937;
}

.note {
    font-size: 0.85em;
    color: #6B7280;
    font-style: italic;
}

.insight {
    background-color: #FEF3C7;
    padding: 15px;
    border-radius: 6px;
    margin-top: 15px;
    font-weight: 500;
}

.integration-example {
    background-color: #F3F4F6;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.agent-hierarchy {
    margin: 20px 0;
    text-align: center;
}

.agent-root {
    background-color: #EC4899;
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    display: inline-block;
    font-weight: 600;
    margin-bottom: 20px;
}

.agent-children {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
}

.agent-child {
    padding: 10px 18px;
    border-radius: 6px;
    font-weight: 500;
}

.agent-child.person {
    background-color: #FBCFE8;
    color: #831843;
}

.agent-child.collective {
    background-color: #FCE7F3;
    color: #9F1239;
}

.practice-example {
    background-color: #F0FDFA;
    padding: 30px;
    border-radius: 12px;
    margin: 30px 0;
    border: 2px solid #5EEAD4;
}

.lrm-analysis {
    margin-top: 25px;
}

.analysis-section {
    margin: 20px 0;
    padding: 20px;
    border-radius: 10px;
}

.work-section {
    background-color: #FEF3C7;
    border-left: 5px solid #F59E0B;
}

.expression-section {
    background-color: #DBEAFE;
    border-left: 5px solid #3B82F6;
}

.manifestation-section {
    background-color: #D1FAE5;
    border-left: 5px solid #10B981;
}

.item-section {
    background-color: #E9D5FF;
    border-left: 5px solid #A855F7;
}

.analysis-section h4 {
    margin-top: 0;
    margin-bottom: 15px;
}

.relations, .expressions, .manifestations, .items {
    margin-top: 15px;
}

.relation, .expr-item, .manif-item, .item-box {
    margin: 10px 0;
    padding: 10px;
    background-color: rgba(255, 255, 255, 0.6);
    border-radius: 6px;
}

.rel-label, .expr-relation .rel-label {
    font-weight: 600;
    color: #6B7280;
    font-size: 0.85em;
}

.rel-value, .expr-relation .rel-value {
    color: #1F2937;
}

.manif-details, .item-detail {
    font-size: 0.9em;
    color: #4B5563;
    margin-top: 5px;
}

.relationship-examples {
    display: grid;
    gap: 20px;
    margin: 25px 0;
}

.rel-example {
    background-color: #F3F4F6;
    padding: 18px;
    border-radius: 8px;
    border-left: 4px solid #6366F1;
}

.rel-name {
    font-weight: 700;
    color: #4338CA;
    font-size: 1.05em;
}

.rel-desc {
    color: #6B7280;
    font-size: 0.9em;
    margin: 5px 0;
}

.rel-sample {
    background-color: white;
    padding: 12px;
    border-radius: 6px;
    margin-top: 10px;
    font-size: 0.95em;
}

.appellation-box {
    background-color: #FFFBEB;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.appellation-examples {
    margin-top: 15px;
}

.app-item {
    padding: 12px;
    margin: 10px 0;
    background-color: white;
    border-radius: 6px;
    border-left: 3px solid #F59E0B;
}

.subject-examples {
    background-color: #F5F3FF;
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.subject-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 15px;
    margin-top: 15px;
}

.subject-item {
    background-color: white;
    padding: 15px;
    border-radius: 6px;
    border-left: 3px solid #8B5CF6;
}

.subject-item .example {
    display: block;
    margin-top: 8px;
    font-size: 0.85em;
}

.rda-connection {
    background-color: #EFF6FF;
    padding: 25px;
    border-radius: 10px;
    margin: 25px 0;
}

.rda-lrm-mapping {
    margin-top: 20px;
    overflow-x: auto;
}

.table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
}

.table th,
.table td {
    padding: 12px;
    text-align: left;
    border: 1px solid #E5E7EB;
}

.table thead {
    background-color: #DBEAFE;
    font-weight: 600;
}

.implementation-examples {
    background-color: #F0FDF4;
    padding: 25px;
    border-radius: 10px;
    margin: 25px 0;
}

.search-scenario {
    margin-top: 20px;
}

.scenario-step {
    display: flex;
    align-items: flex-start;
    margin: 15px 0;
    padding: 15px;
    background-color: white;
    border-radius: 8px;
}

.step-num {
    background-color: #10B981;
    color: white;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    flex-shrink: 0;
    margin-right: 15px;
}

.step-content {
    flex: 1;
}

.comparison-table {
    margin: 25px 0;
    overflow-x: auto;
}

.benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.benefit-card {
    background: linear-gradient(to bottom, white, #F9FAFB);
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #E5E7EB;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.benefit-card h4 {
    margin-top: 0;
    color: #10B981;
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

.comparison-summary {
    background-color: #F5F3FF;
    padding: 25px;
    border-radius: 10px;
    margin: 25px 0;
}

.evolution-diagram {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 20px;
    align-items: center;
    margin-top: 20px;
}

@media (max-width: 768px) {
    .evolution-diagram {
        grid-template-columns: 1fr;
    }
    .evo-arrow {
        display: none;
    }
}

.evo-before, .evo-after {
    padding: 20px;
    border-radius: 10px;
}

.evo-before {
    background-color: #FEF2F2;
    border: 2px solid #FCA5A5;
}

.evo-after {
    background-color: #F0FDF4;
    border: 2px solid #86EFAC;
}

.evo-before strong, .evo-after strong {
    display: block;
    font-size: 1.1em;
    margin-bottom: 10px;
}

.evo-arrow {
    font-size: 2.5em;
    color: #6B7280;
    font-weight: bold;
}

.next-steps {
    background-color: #F5F3FF;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #8B5CF6;
    margin: 20px 0;
}

.next-steps h3 {
    margin-top: 0;
    color: #5B21B6;
}
</style>
"""

# 5. LRM 콘텐츠 생성 또는 업데이트
existing_content = Content.objects.filter(slug='lrm').first()

if existing_content:
    print(f"\n⚠️  'lrm' 슬러그를 가진 콘텐츠가 이미 존재합니다.")
    print(f"   기존 콘텐츠를 업데이트합니다: {existing_content.title}")

    existing_content.title = "LRM (도서관 참조 모델)"
    existing_content.summary = "FRBR을 발전시킨 최신 도서관 개념 모델 LRM을 실제 예제로 쉽게 배우고, FRBR과의 차이점을 명확히 이해합니다."
    existing_content.content_html = content_html
    existing_content.category = lrm_category
    existing_content.difficulty = 'INTERMEDIATE'
    existing_content.estimated_time = 25
    existing_content.prerequisites = "FRBR 기본 개념"
    existing_content.learning_objectives = "LRM의 11개 엔티티 이해, FRBR과의 차이점 파악, Nomen 개념 습득, 실제 도서관 데이터를 LRM으로 모델링"
    existing_content.status = Content.Status.PUBLISHED  # 공개로 설정
    existing_content.save()

    existing_content.tags.clear()
    existing_content.tags.add(tag)

    print(f"✅ 콘텐츠가 업데이트되었습니다!")
else:
    content = Content.objects.create(
        title="LRM (도서관 참조 모델)",
        slug="lrm",
        summary="FRBR을 발전시킨 최신 도서관 개념 모델 LRM을 실제 예제로 쉽게 배우고, FRBR과의 차이점을 명확히 이해합니다.",
        content_html=content_html,
        category=lrm_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=25,
        prerequisites="FRBR 기본 개념",
        learning_objectives="LRM의 11개 엔티티 이해, FRBR과의 차이점 파악, Nomen 개념 습득, 실제 도서관 데이터를 LRM으로 모델링",
        version="1.0",
        status=Content.Status.PUBLISHED  # 공개로 설정
    )

    content.tags.add(tag)

    print(f"\n✅ LRM 학습 콘텐츠가 생성되었습니다!")

print(f"\n📊 콘텐츠 정보:")
print(f"  - 제목: LRM (도서관 참조 모델)")
print(f"  - 슬러그: lrm")
print(f"  - 카테고리: {lrm_category.name} (상위: {conceptual_model_category.name})")
print(f"  - 난이도: 중급")
print(f"  - 소요시간: 25분")
print(f"  - 태그: {tag.name}")
print(f"  - 공개 상태: 공개")
print(f"\n💡 확인:")
print(f"  - 콘텐츠 목록: http://localhost:3000/contents")
print(f"  - 상세 페이지: http://localhost:3000/contents/lrm")
