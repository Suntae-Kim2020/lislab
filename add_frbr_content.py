"""
개념 모델 카테고리와 FRBR 학습 콘텐츠 추가 스크립트
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

# 1. 개념 모델 카테고리 생성 (상위 카테고리)
conceptual_model_category, created = Category.objects.get_or_create(
    slug='conceptual-model',
    defaults={
        'name': '개념 모델',
        'description': '도서관 정보 자원의 개념적 모델링',
        'parent': None,
        'is_active': True
    }
)
if created:
    print(f"✓ 상위 카테고리 생성: {conceptual_model_category.name}")
else:
    print(f"✓ 상위 카테고리 확인: {conceptual_model_category.name}")

# 2. FRBR 하위 카테고리 생성
frbr_category, created = Category.objects.get_or_create(
    slug='frbr',
    defaults={
        'name': 'FRBR',
        'description': '서지 레코드의 기능 요건',
        'parent': conceptual_model_category,
        'is_active': True
    }
)
if created:
    print(f"✓ 하위 카테고리 생성: {frbr_category.name}")
else:
    print(f"✓ 하위 카테고리 확인: {frbr_category.name}")

# 3. 태그 생성
tag, created = Tag.objects.get_or_create(
    name='개념적 모델',
    defaults={'slug': 'conceptual-modeling'}
)
if created:
    print(f"✓ 태그 생성: {tag.name}")
else:
    print(f"✓ 태그 확인: {tag.name}")

# 4. FRBR 학습 콘텐츠 HTML
content_html = """
<h2>FRBR 쉽게 이해하기</h2>
<p class="lead">도서관의 정보 자원을 체계적으로 정리하는 개념 모델을 배워봅시다!</p>

<div class="alert alert-info">
<strong>💡 학습 목표:</strong>
<ul>
<li>FRBR의 4가지 핵심 개체를 이해합니다</li>
<li>실제 도서관 자료를 FRBR로 분석할 수 있습니다</li>
<li>FRBR이 도서관 목록에 왜 중요한지 알게 됩니다</li>
</ul>
</div>

<hr/>

<h2>FRBR이 뭔가요?</h2>

<div class="intro-box">
<p><strong>FRBR (Functional Requirements for Bibliographic Records)</strong>은 도서관 자료를 4단계로 나누어 설명하는 개념 모델입니다.</p>
<p>1998년 IFLA(국제도서관연맹)에서 발표했으며, 도서관 목록의 새로운 패러다임이 되었습니다.</p>
</div>

<h3>🤔 왜 필요할까요?</h3>

<div class="problem-box">
<p><strong>기존 방식의 문제:</strong></p>
<p>예를 들어 "해리포터와 마법사의 돌"을 검색하면...</p>
<ul>
<li>영어 원서</li>
<li>한국어 번역본</li>
<li>큰글자 도서</li>
<li>오디오북</li>
<li>전자책</li>
<li>점자책</li>
</ul>
<p>이 모든 것들이 별개의 자료로 나열됩니다. 😵</p>
<p>사용자는 "같은 이야기인데 왜 이렇게 많지?"라고 혼란스러워합니다.</p>
</div>

<div class="solution-box">
<p><strong>FRBR의 해결책:</strong></p>
<p>이 모든 자료들이 <strong>하나의 저작</strong>에서 나왔다는 것을 명확히 보여줍니다!</p>
<p>사용자는 "어떤 형태로 이용할까?"를 쉽게 선택할 수 있습니다. ✨</p>
</div>

<hr/>

<h2>FRBR의 4가지 핵심 개체</h2>

<p>FRBR은 정보 자원을 <strong>4단계</strong>로 구분합니다. 위에서 아래로 갈수록 구체화됩니다.</p>

<div class="frbr-hierarchy">
<div class="frbr-level level-1">
<h3>1️⃣ Work (저작)</h3>
<p class="definition"><strong>정의:</strong> 추상적인 지적·예술적 창작물</p>
<p class="description">작가의 머릿속에 있는 아이디어, 이야기 자체</p>
<div class="example">
<strong>예시:</strong> J.K. 롤링이 쓴 "해리포터와 마법사의 돌"이라는 <em>이야기 자체</em>
</div>
</div>

<div class="arrow">⬇ 실현되면</div>

<div class="frbr-level level-2">
<h3>2️⃣ Expression (표현형)</h3>
<p class="definition"><strong>정의:</strong> 저작의 지적·예술적 실현</p>
<p class="description">저작이 특정 언어, 형태로 표현된 것</p>
<div class="example">
<strong>예시:</strong>
<ul>
<li>영어 원문</li>
<li>한국어 번역본 (최인자 번역)</li>
<li>오디오북 (성우 김OO 낭독)</li>
<li>점자 텍스트</li>
</ul>
<p class="note">💡 같은 Work이지만 언어, 형태가 다르면 다른 Expression입니다.</p>
</div>
</div>

<div class="arrow">⬇ 출판되면</div>

<div class="frbr-level level-3">
<h3>3️⃣ Manifestation (구현형)</h3>
<p class="definition"><strong>정의:</strong> 표현형의 물리적 구현</p>
<p class="description">특정 출판사가 특정 시점에 만든 판본</p>
<div class="example">
<strong>예시:</strong>
<ul>
<li>문학수첩, 2000년 초판</li>
<li>문학수첩, 2014년 개정판</li>
<li>민음사, 2021년판</li>
<li>Bloomsbury, 1997년 영국 초판</li>
</ul>
<p class="note">💡 같은 Expression이지만 출판사, 발행연도, 디자인이 다르면 다른 Manifestation입니다.</p>
</div>
</div>

<div class="arrow">⬇ 소장하면</div>

<div class="frbr-level level-4">
<h3>4️⃣ Item (개별자료)</h3>
<p class="definition"><strong>정의:</strong> 구현형의 단일 예시</p>
<p class="description">도서관이 실제로 소장하고 있는 개별 책</p>
<div class="example">
<strong>예시:</strong>
<ul>
<li>서울도서관 소장 - 청구기호: 843.6-R719h-2000, 등록번호: EM12345</li>
<li>국립중앙도서관 소장 - 청구기호: 843.6-R719h-2000, 등록번호: CM67890</li>
</ul>
<p class="note">💡 같은 Manifestation이지만 물리적으로 다른 책입니다.</p>
</div>
</div>
</div>

<hr/>

<h2>실전 예제: "나의 문화유산답사기"</h2>

<div class="practice-example">
<h3>📚 시나리오</h3>
<p>유홍준 교수의 "나의 문화유산답사기"를 FRBR로 분석해봅시다.</p>

<div class="frbr-analysis">
<div class="analysis-card work-card">
<h4>🎨 Work (저작)</h4>
<p><strong>나의 문화유산답사기 1권 - 남도답사 일번지</strong></p>
<p class="small">유홍준이 쓴 한국 문화유산에 대한 답사기</p>
</div>

<div class="analysis-card expression-card">
<h4>📝 Expression (표현형)</h4>
<ul>
<li><strong>초판 텍스트</strong> (1993년 원본)</li>
<li><strong>개정증보판 텍스트</strong> (2012년, 내용 추가)</li>
<li><strong>오디오북</strong> (유홍준 직접 낭독)</li>
<li><strong>전자책 버전</strong></li>
</ul>
</div>

<div class="analysis-card manifestation-card">
<h4>📖 Manifestation (구현형)</h4>
<ul>
<li>창비, 1993년 초판</li>
<li>창비, 2012년 개정증보판</li>
<li>창비, 2018년 20주년 기념 특별판</li>
<li>리디북스 전자책 (2015년)</li>
</ul>
</div>

<div class="analysis-card item-card">
<h4>📕 Item (개별자료)</h4>
<ul>
<li>서울시립도서관 소장본 (등록번호: 981234)</li>
<li>국립중앙도서관 소장본 (등록번호: CM554321)</li>
<li>제 책장에 있는 책 (개인 소장)</li>
</ul>
</div>
</div>
</div>

<hr/>

<h2>다른 예제: "오만과 편견"</h2>

<div class="comparison-table">
<table class="table">
<thead>
<tr>
<th>단계</th>
<th>설명</th>
<th>예시</th>
</tr>
</thead>
<tbody>
<tr class="work-row">
<td><strong>Work</strong></td>
<td>제인 오스틴의 소설 "오만과 편견"</td>
<td>작가가 창조한 엘리자베스와 다시의 이야기</td>
</tr>
<tr class="expression-row">
<td><strong>Expression</strong></td>
<td>다양한 실현 형태</td>
<td>• 영어 원문<br/>• 한국어 번역 (조선경 번역)<br/>• 한국어 번역 (윤지관 번역)<br/>• 영화 각본 (2005년 영화)<br/>• 오디오북</td>
</tr>
<tr class="manifestation-row">
<td><strong>Manifestation</strong></td>
<td>구체적인 출판물</td>
<td>• 민음사 세계문학전집 (2003년)<br/>• 열린책들 (2008년)<br/>• Penguin Classics (2003년)<br/>• 전자책 (교보문고, 2012년)</td>
</tr>
<tr class="item-row">
<td><strong>Item</strong></td>
<td>실제 소장 자료</td>
<td>• 연세대학교 도서관 소장 (청구기호: 823-A9p-2003)<br/>• 강남도서관 소장 (바코드: 5512345)</td>
</tr>
</tbody>
</table>
</div>

<hr/>

<h2>FRBR의 관계 (Relationships)</h2>

<p>FRBR은 단순히 4단계로 나누는 것뿐만 아니라, <strong>관계</strong>도 정의합니다.</p>

<h3>1️⃣ Group 1 개체 간 관계</h3>

<div class="relationships-grid">
<div class="relationship-card">
<h4>저작 간 관계</h4>
<p><strong>후속 저작 (Successor):</strong></p>
<p>"해리포터와 비밀의 방"은 "해리포터와 마법사의 돌"의 후속작</p>
</div>

<div class="relationship-card">
<h4>저작 간 관계</h4>
<p><strong>각색 (Adaptation):</strong></p>
<p>"반지의 제왕" 영화는 "반지의 제왕" 소설의 각색</p>
</div>

<div class="relationship-card">
<h4>저작 간 관계</h4>
<p><strong>요약 (Summarization):</strong></p>
<p>"셜록 홈즈 단편 모음집"은 완전판의 요약본</p>
</div>
</div>

<h3>2️⃣ 저작과 책임자 관계</h3>

<div class="responsibility-examples">
<ul>
<li><strong>창작자 (Creator):</strong> J.K. 롤링 → "해리포터" Work를 <em>창작</em></li>
<li><strong>실현자 (Realizer):</strong> 최인자 → 한국어 Expression을 <em>번역</em></li>
<li><strong>제작자 (Producer):</strong> 문학수첩 → Manifestation을 <em>출판</em></li>
</ul>
</div>

<hr/>

<h2>FRBR의 장점</h2>

<div class="benefits-grid">
<div class="benefit-card">
<h4>✅ 1. 사용자 편의성 향상</h4>
<p>같은 저작의 다양한 형태를 한눈에 볼 수 있습니다.</p>
<p class="example-text">"영어 원서는 어렵고, 오디오북으로 들을까?"</p>
</div>

<div class="benefit-card">
<h4>✅ 2. 검색 효율성</h4>
<p>저작 수준에서 검색하면 모든 형태를 한번에 찾을 수 있습니다.</p>
<p class="example-text">"반지의 제왕" 검색 → 소설, 영화, 오디오북 모두 나옴</p>
</div>

<div class="benefit-card">
<h4>✅ 3. 데이터 중복 감소</h4>
<p>공통 정보는 상위 단계에 한 번만 기록합니다.</p>
<p class="example-text">저자, 원제목은 Work에만 기록</p>
</div>

<div class="benefit-card">
<h4>✅ 4. 의미 있는 관계 표현</h4>
<p>"원작-번역", "원작-각색" 같은 관계를 명확히 합니다.</p>
<p class="example-text">소설 "설국열차" ↔ 영화 "설국열차"</p>
</div>
</div>

<hr/>

<h2>실제 적용 사례</h2>

<h3>📚 주요 도서관 시스템</h3>

<div class="applications">
<ul>
<li><strong>OCLC WorldCat:</strong> 전 세계 도서관 목록에 FRBR 적용</li>
<li><strong>국립중앙도서관:</strong> 국가서지 구축에 FRBR 개념 활용</li>
<li><strong>RDA (Resource Description and Access):</strong> FRBR을 기반으로 한 새로운 목록 규칙</li>
</ul>
</div>

<h3>🔍 FRBR 이후: LRM 모델</h3>

<div class="info-box">
<p>2017년 IFLA는 FRBR을 발전시킨 <strong>LRM (Library Reference Model)</strong>을 발표했습니다.</p>
<p>LRM은 FRBR을 더 간소화하고, 최신 기술 환경에 맞게 개선했습니다.</p>
</div>

<hr/>

<h2>퀴즈로 복습하기</h2>

<div class="quiz-section">
<div class="quiz-card">
<h4>Q1. 다음 중 Expression에 해당하는 것은?</h4>
<ol type="a">
<li>셰익스피어의 "햄릿"이라는 작품</li>
<li>한국어로 번역된 "햄릿"</li>
<li>민음사에서 2010년에 출판한 "햄릿"</li>
<li>서울도서관 소장 "햄릿" 책</li>
</ol>
<p class="answer">정답: b) 한국어로 번역된 "햄릿"</p>
</div>

<div class="quiz-card">
<h4>Q2. Work와 Manifestation의 가장 큰 차이는?</h4>
<ol type="a">
<li>Work는 추상적이고, Manifestation은 물리적이다</li>
<li>Work는 오래되고, Manifestation은 최신이다</li>
<li>Work는 원본이고, Manifestation은 복사본이다</li>
</ol>
<p class="answer">정답: a) Work는 추상적이고, Manifestation은 물리적이다</p>
</div>

<div class="quiz-card">
<h4>Q3. "토지" 소설과 "토지" 드라마의 관계는?</h4>
<ol type="a">
<li>같은 Work의 다른 Expression</li>
<li>다른 Work이지만 각색 관계</li>
<li>같은 Manifestation의 다른 Item</li>
</ol>
<p class="answer">정답: b) 다른 Work이지만 각색 관계 (소설 Work → 드라마 Work로 각색)</p>
</div>
</div>

<hr/>

<h2>학습 정리</h2>

<div class="summary-box">
<h3>🎯 핵심 요약</h3>
<ul class="checkmark-list">
<li>✓ <strong>FRBR은 4단계:</strong> Work → Expression → Manifestation → Item</li>
<li>✓ <strong>위에서 아래로 갈수록</strong> 추상적 → 구체적</li>
<li>✓ <strong>같은 이야기도</strong> 언어, 형태, 판본, 개별 자료로 구분</li>
<li>✓ <strong>사용자에게는</strong> 더 명확하고 편리한 검색 환경 제공</li>
<li>✓ <strong>도서관에는</strong> 효율적인 데이터 관리 가능</li>
</ul>
</div>

<div class="next-steps">
<h3>📚 다음 학습</h3>
<ul>
<li><strong>RDA:</strong> FRBR을 실제로 적용한 목록 규칙</li>
<li><strong>LRM:</strong> FRBR의 발전 모델</li>
<li><strong>BIBFRAME:</strong> FRBR을 웹 환경에 맞게 변형한 모델</li>
<li><strong>서지 레코드:</strong> 실제 목록 작성 실습</li>
</ul>
</div>

<hr/>

<div class="alert alert-success">
<h3>🎉 학습 완료!</h3>
<p>축하합니다! FRBR의 기본 개념을 모두 학습했습니다.</p>
<p>이제 도서관 목록을 볼 때 "이건 Work인가, Expression인가?" 생각하게 될 거예요! 😊</p>
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

.intro-box, .problem-box, .solution-box {
    padding: 20px;
    margin: 20px 0;
    border-radius: 8px;
}

.intro-box {
    background: linear-gradient(to right, #EFF6FF, #F5F3FF);
    border-left: 4px solid #6366F1;
}

.problem-box {
    background-color: #FEF2F2;
    border-left: 4px solid #EF4444;
}

.solution-box {
    background-color: #F0FDF4;
    border-left: 4px solid #10B981;
}

.frbr-hierarchy {
    margin: 30px 0;
}

.frbr-level {
    padding: 20px;
    margin: 15px 0;
    border-radius: 8px;
    border-left: 5px solid;
}

.level-1 {
    background-color: #FEF3C7;
    border-color: #F59E0B;
}

.level-2 {
    background-color: #DBEAFE;
    border-color: #3B82F6;
}

.level-3 {
    background-color: #D1FAE5;
    border-color: #10B981;
}

.level-4 {
    background-color: #E9D5FF;
    border-color: #A855F7;
}

.frbr-level h3 {
    margin-top: 0;
    color: #1F2937;
}

.definition {
    font-size: 0.95em;
    color: #4B5563;
    margin: 8px 0;
}

.description {
    font-size: 0.9em;
    color: #6B7280;
    font-style: italic;
}

.example {
    background-color: rgba(255, 255, 255, 0.6);
    padding: 12px;
    border-radius: 6px;
    margin-top: 12px;
}

.note {
    font-size: 0.85em;
    color: #6B7280;
    margin-top: 8px;
}

.arrow {
    text-align: center;
    font-size: 1.2em;
    margin: 10px 0;
    color: #6B7280;
    font-weight: 600;
}

.practice-example {
    background-color: #F9FAFB;
    padding: 25px;
    border-radius: 12px;
    margin: 25px 0;
}

.frbr-analysis {
    display: grid;
    gap: 15px;
    margin-top: 20px;
}

.analysis-card {
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid;
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

.analysis-card h4 {
    margin-top: 0;
    margin-bottom: 10px;
}

.small {
    font-size: 0.9em;
    color: #6B7280;
}

.comparison-table {
    margin: 20px 0;
    overflow-x: auto;
}

.table {
    width: 100%;
    border-collapse: collapse;
}

.table th,
.table td {
    padding: 12px;
    text-align: left;
    border: 1px solid #E5E7EB;
}

.table thead {
    background-color: #F3F4F6;
}

.work-row {
    background-color: #FEF3C7;
}

.expression-row {
    background-color: #DBEAFE;
}

.manifestation-row {
    background-color: #D1FAE5;
}

.item-row {
    background-color: #E9D5FF;
}

.relationships-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

.relationship-card {
    background-color: #F3F4F6;
    padding: 15px;
    border-radius: 8px;
    border-left: 3px solid #6366F1;
}

.relationship-card h4 {
    margin-top: 0;
    color: #4B5563;
}

.responsibility-examples {
    background-color: #F9FAFB;
    padding: 20px;
    border-radius: 8px;
    margin: 15px 0;
}

.benefits-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin: 25px 0;
}

.benefit-card {
    background: linear-gradient(to bottom, #FFFFFF, #F9FAFB);
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #E5E7EB;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.benefit-card h4 {
    margin-top: 0;
    color: #10B981;
}

.example-text {
    font-style: italic;
    color: #6B7280;
    font-size: 0.9em;
    margin-top: 8px;
}

.applications {
    background-color: #F0FDFA;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #14B8A6;
}

.info-box {
    background-color: #EFF6FF;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #3B82F6;
    margin: 20px 0;
}

.quiz-section {
    display: grid;
    gap: 20px;
    margin: 25px 0;
}

.quiz-card {
    background-color: #FFFBEB;
    padding: 20px;
    border-radius: 10px;
    border-left: 4px solid #F59E0B;
}

.quiz-card h4 {
    margin-top: 0;
    color: #92400E;
}

.quiz-card ol {
    margin: 15px 0;
}

.quiz-card .answer {
    background-color: #FEF3C7;
    padding: 10px;
    border-radius: 6px;
    margin-top: 12px;
    font-weight: 600;
    color: #78350F;
}

.summary-box {
    background: linear-gradient(to bottom right, #EFF6FF, #F0FDFA);
    padding: 25px;
    border-radius: 12px;
    border: 2px solid #93C5FD;
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

@media (max-width: 768px) {
    .benefits-grid,
    .relationships-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""

# 5. FRBR 콘텐츠 생성 또는 업데이트
existing_content = Content.objects.filter(slug='frbr').first()

if existing_content:
    print(f"\n⚠️  'frbr' 슬러그를 가진 콘텐츠가 이미 존재합니다.")
    print(f"   기존 콘텐츠를 업데이트합니다: {existing_content.title}")

    existing_content.title = "FRBR 기초 학습"
    existing_content.summary = "도서관 정보 자원을 체계적으로 분석하는 FRBR 개념 모델을 실제 예제로 쉽게 배워봅시다."
    existing_content.content_html = content_html
    existing_content.category = frbr_category
    existing_content.difficulty = 'INTERMEDIATE'
    existing_content.estimated_time = 25
    existing_content.prerequisites = "기본적인 도서관 목록 개념"
    existing_content.learning_objectives = "FRBR의 4가지 핵심 개체(Work, Expression, Manifestation, Item) 이해, 실제 도서를 FRBR로 분석할 수 있는 능력"
    existing_content.save()

    existing_content.tags.clear()
    existing_content.tags.add(tag)

    print(f"✅ 콘텐츠가 업데이트되었습니다!")
else:
    content = Content.objects.create(
        title="FRBR 기초 학습",
        slug="frbr",
        summary="도서관 정보 자원을 체계적으로 분석하는 FRBR 개념 모델을 실제 예제로 쉽게 배워봅시다.",
        content_html=content_html,
        category=frbr_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=25,
        prerequisites="기본적인 도서관 목록 개념",
        learning_objectives="FRBR의 4가지 핵심 개체(Work, Expression, Manifestation, Item) 이해, 실제 도서를 FRBR로 분석할 수 있는 능력",
        version="1.0",
    )

    content.tags.add(tag)

    print(f"\n✅ FRBR 학습 콘텐츠가 생성되었습니다!")

print(f"\n📊 콘텐츠 정보:")
print(f"  - 제목: FRBR 기초 학습")
print(f"  - 슬러그: frbr")
print(f"  - 카테고리: {frbr_category.name} (상위: {conceptual_model_category.name})")
print(f"  - 난이도: 중급")
print(f"  - 소요시간: 25분")
print(f"  - 태그: {tag.name}")
print(f"\n💡 확인:")
print(f"  - 콘텐츠 목록: http://localhost:3000/contents")
print(f"  - 상세 페이지: http://localhost:3000/contents/frbr")
