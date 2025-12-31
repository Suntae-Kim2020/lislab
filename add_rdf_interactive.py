"""
RDF 심화학습 (인터랙티브) 콘텐츠 추가 스크립트
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

# RDF 카테고리 가져오기
rdf_category = Category.objects.filter(slug='rdf').first()
if not rdf_category:
    print("❌ RDF 카테고리를 찾을 수 없습니다.")
    exit(1)

print(f"✓ RDF 카테고리 확인: {rdf_category.name}")

# 태그 생성 또는 가져오기
tags_data = ['RDF', 'TURTLE', '직렬화']
tags = []
for tag_name in tags_data:
    tag, created = Tag.objects.get_or_create(
        name=tag_name,
        defaults={'slug': tag_name.lower()}
    )
    tags.append(tag)
    if created:
        print(f"  ✓ 태그 생성: {tag_name}")
    else:
        print(f"  ✓ 태그 확인: {tag_name}")

# RDF 심화학습 콘텐츠 생성
content_html = """
<h2>RDF 심화학습 - 인터랙티브 실습</h2>
<p class="lead">단계별 가이드와 실시간 코드 편집기로 RDF를 직접 배워봅시다!</p>

<div class="alert alert-info">
<strong>💡 이 학습 과정에서 배울 내용:</strong>
<ul>
<li>RDF의 핵심 개념과 트리플 구조</li>
<li>Turtle 문법으로 RDF 작성하기</li>
<li>다양한 RDF 직렬화 형식 (Turtle, RDF/XML, JSON-LD, N-Triples)</li>
<li>SPARQL을 이용한 RDF 데이터 쿼리</li>
<li>실무에서 활용할 수 있는 RDF 어휘와 도구</li>
</ul>
</div>

<hr/>

<h2>학습 방식</h2>

<div class="two-columns">
<div class="feature-box">
<h3>🎯 단계별 학습</h3>
<p>5단계로 구성된 체계적인 커리큘럼:</p>
<ol>
<li><strong>1단계:</strong> RDF가 무엇인지 이해하기</li>
<li><strong>2단계:</strong> 트리플의 주어-서술어-목적어 구조</li>
<li><strong>3단계:</strong> Turtle 문법 완전 정복</li>
<li><strong>4단계:</strong> 실전 예제로 실습하기</li>
<li><strong>5단계:</strong> 관계와 네트워크 표현하기</li>
</ol>
</div>

<div class="feature-box">
<h3>⚡ 인터랙티브 실습</h3>
<p>직접 코드를 작성하고 즉시 결과를 확인:</p>
<ul>
<li>실시간 Turtle 코드 편집기</li>
<li>문법 유효성 검사</li>
<li>5개 이상의 실습 예제</li>
<li>단계별 힌트 시스템</li>
<li>빠른 시작 템플릿 제공</li>
</ul>
</div>
</div>

<hr/>

<h2>학습 내용</h2>

<h3>1️⃣ RDF 기초 개념</h3>
<div class="content-box">
<p>시맨틱 웹의 핵심인 RDF가 왜 필요한지, 어떤 문제를 해결하는지 배웁니다.</p>
<ul>
<li>웹 데이터의 의미를 컴퓨터가 이해하는 방법</li>
<li>RDF 트리플의 개념과 구조</li>
<li>리소스, 속성, 값의 관계</li>
</ul>
</div>

<h3>2️⃣ Turtle 문법 마스터</h3>
<div class="content-box">
<p>가장 읽기 쉬운 RDF 표현 형식인 Turtle을 완전히 익힙니다.</p>
<ul>
<li>네임스페이스와 접두어 사용법</li>
<li>기본 트리플 작성</li>
<li>세미콜론(;)과 쉼표(,) 활용</li>
<li>리터럴과 타입 표현</li>
<li>빈 노드(Blank Node) 사용</li>
</ul>
</div>

<h3>3️⃣ RDF 직렬화 형식</h3>
<div class="content-box">
<p>다양한 RDF 표현 형식을 이해하고 변환할 수 있습니다.</p>
<ul>
<li><strong>Turtle:</strong> 사람이 읽기 쉬운 형식</li>
<li><strong>RDF/XML:</strong> XML 기반 표준 형식</li>
<li><strong>JSON-LD:</strong> JSON 형태의 링크드 데이터</li>
<li><strong>N-Triples:</strong> 가장 단순한 형식</li>
<li><strong>N-Quads:</strong> 그래프 정보를 포함한 형식</li>
</ul>
</div>

<h3>4️⃣ 표준 어휘 활용</h3>
<div class="content-box">
<p>실무에서 널리 사용되는 RDF 어휘들을 배웁니다.</p>
<ul>
<li><strong>FOAF:</strong> 사람과 관계 표현</li>
<li><strong>Dublin Core:</strong> 문서 메타데이터</li>
<li><strong>Schema.org:</strong> 웹 구조화 데이터</li>
<li><strong>SKOS:</strong> 개념 체계와 어휘</li>
<li><strong>OWL:</strong> 온톨로지 정의</li>
</ul>
</div>

<h3>5️⃣ SPARQL 쿼리</h3>
<div class="content-box">
<p>RDF 데이터를 조회하고 분석하는 쿼리 언어를 익힙니다.</p>
<ul>
<li>기본 SELECT 쿼리</li>
<li>필터와 정렬</li>
<li>집계와 그룹화</li>
<li>OPTIONAL과 UNION</li>
<li>실제 DBpedia 쿼리 예제</li>
</ul>
</div>

<hr/>

<h2>실습 예제</h2>

<div class="example-grid">
<div class="example-card">
<h4>📚 도서 정보 표현</h4>
<p>책의 제목, 저자, 출판사, ISBN을 RDF로 표현합니다.</p>
</div>

<div class="example-card">
<h4>👨‍🏫 연구자 프로필</h4>
<p>연구자의 소속, 연구 분야, 논문을 구조화합니다.</p>
</div>

<div class="example-card">
<h4>🌐 소셜 네트워크</h4>
<p>사람들 간의 관계와 친구 네트워크를 표현합니다.</p>
</div>

<div class="example-card">
<h4>🎓 교육 콘텐츠</h4>
<p>강의, 커리큘럼, 학습 목표를 RDF로 구조화합니다.</p>
</div>
</div>

<hr/>

<h2>학습 도구</h2>

<div class="tools-list">
<h4>🛠️ 제공되는 도구:</h4>
<ul>
<li><strong>코드 편집기:</strong> 실시간 Turtle 코드 작성 및 검증</li>
<li><strong>예제 갤러리:</strong> 5개 이상의 실전 예제 제공</li>
<li><strong>템플릿:</strong> 빠른 시작을 위한 코드 템플릿</li>
<li><strong>힌트 시스템:</strong> 막힐 때 도움을 주는 단계별 힌트</li>
<li><strong>진행 표시:</strong> 학습 진도를 한눈에 확인</li>
</ul>
</div>

<hr/>

<h2>이런 분들께 추천합니다</h2>

<div class="target-audience">
<div class="audience-card">
<h4>🎓 도서관 정보학 전공자</h4>
<p>시맨틱 웹과 링크드 데이터의 실무 활용을 배우고 싶은 분</p>
</div>

<div class="audience-card">
<h4>💻 개발자</h4>
<p>지식 그래프나 온톨로지를 프로젝트에 도입하려는 분</p>
</div>

<div class="audience-card">
<h4>📊 데이터 과학자</h4>
<p>구조화된 데이터와 의미 기반 검색에 관심 있는 분</p>
</div>

<div class="audience-card">
<h4>🔬 연구자</h4>
<p>연구 데이터를 표준화하고 공유하고 싶은 분</p>
</div>
</div>

<hr/>

<h2>학습 후 기대 효과</h2>

<div class="outcomes">
<ul class="checkmark-list">
<li>✓ RDF의 개념과 트리플 구조를 완벽히 이해</li>
<li>✓ Turtle 형식으로 RDF 문서를 자유롭게 작성</li>
<li>✓ 다양한 직렬화 형식 간 변환 가능</li>
<li>✓ 표준 RDF 어휘(FOAF, DC 등)를 실무에 적용</li>
<li>✓ SPARQL로 RDF 데이터를 쿼리하고 분석</li>
<li>✓ 실제 프로젝트에서 RDF를 활용할 수 있는 실무 능력</li>
</ul>
</div>

<hr/>

<div class="alert alert-success">
<h3>🚀 지금 바로 시작하세요!</h3>
<p>이론과 실습이 결합된 인터랙티브 학습 환경에서 RDF를 마스터하세요.</p>
<p><strong>소요 시간:</strong> 약 45분</p>
<p><strong>난이도:</strong> 중급 (RDF 기초 지식이 있으면 더 좋습니다)</p>
</div>

<style>
.lead {
    font-size: 1.15em;
    color: #6B7280;
    margin-bottom: 20px;
}

.alert {
    padding: 15px;
    border-radius: 8px;
    margin: 20px 0;
}

.alert-info {
    background-color: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1E40AF;
}

.alert-success {
    background-color: #F0FDF4;
    border: 1px solid #BBF7D0;
    color: #166534;
}

.two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin: 20px 0;
}

@media (max-width: 768px) {
    .two-columns {
        grid-template-columns: 1fr;
    }
}

.feature-box, .content-box, .audience-card {
    background-color: #F9FAFB;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #3B82F6;
}

.example-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin: 20px 0;
}

@media (max-width: 768px) {
    .example-grid {
        grid-template-columns: 1fr;
    }
}

.example-card {
    background: linear-gradient(to right, #EFF6FF, #F5F3FF);
    padding: 15px;
    border-radius: 8px;
    border-left: 3px solid #8B5CF6;
}

.tools-list {
    background-color: #FFFBEB;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #F59E0B;
}

.target-audience {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin: 20px 0;
}

@media (max-width: 768px) {
    .target-audience {
        grid-template-columns: 1fr;
    }
}

.outcomes {
    background: linear-gradient(to bottom right, #F0FDF4, #ECFDF5);
    padding: 20px;
    border-radius: 8px;
    margin: 20px 0;
}

.checkmark-list {
    list-style: none;
    padding: 0;
}

.checkmark-list li {
    padding: 8px 0;
    font-size: 1.05em;
}
</style>
"""

# 기존 콘텐츠 확인
existing_content = Content.objects.filter(slug='rdf-interactive').first()
if existing_content:
    print(f"\n⚠️  'rdf-interactive' 슬러그를 가진 콘텐츠가 이미 존재합니다.")
    print(f"   기존 콘텐츠를 업데이트합니다: {existing_content.title}")

    existing_content.title = "RDF 심화학습 (인터랙티브)"
    existing_content.slug = "rdf-interactive"
    existing_content.summary = "단계별 가이드와 실시간 코드 편집기로 RDF Turtle 문법과 직렬화를 마스터하세요. 5단계 인터랙티브 학습으로 실무 능력을 키웁니다."
    existing_content.content_html = content_html
    existing_content.category = rdf_category
    existing_content.difficulty = 'INTERMEDIATE'
    existing_content.estimated_time = 45
    existing_content.save()

    existing_content.tags.set(tags)

    print(f"✅ 콘텐츠가 업데이트되었습니다!")
else:
    # 새 콘텐츠 생성
    content = Content.objects.create(
        title="RDF 심화학습 (인터랙티브)",
        slug="rdf-interactive",
        summary="단계별 가이드와 실시간 코드 편집기로 RDF Turtle 문법과 직렬화를 마스터하세요. 5단계 인터랙티브 학습으로 실무 능력을 키웁니다.",
        content_html=content_html,
        category=rdf_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=45,
        prerequisites="RDF 기본 개념 이해",
        learning_objectives="Turtle 문법 완전 습득, RDF 직렬화 형식 이해, SPARQL 쿼리 기초, 표준 어휘 활용",
        version="1.0",
    )

    content.tags.set(tags)

    print(f"\n✅ RDF 심화학습 콘텐츠가 생성되었습니다!")

print(f"\n📊 콘텐츠 정보:")
print(f"  - 제목: RDF 심화학습 (인터랙티브)")
print(f"  - 슬러그: rdf-interactive")
print(f"  - 카테고리: {rdf_category.name}")
print(f"  - 난이도: 중급")
print(f"  - 소요시간: 45분")
print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
print(f"\n💡 확인:")
print(f"  - 콘텐츠 목록: http://localhost:3000/contents")
print(f"  - 상세 페이지: http://localhost:3000/contents/rdf-interactive")
print(f"  - 심화학습 페이지: http://localhost:3000/data-model/rdf")
