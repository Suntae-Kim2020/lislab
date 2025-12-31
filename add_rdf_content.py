"""
RDF 교육 콘텐츠 등록 스크립트
데이터 모델 카테고리와 RDF 하위 카테고리 및 콘텐츠를 추가합니다.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User
from apps.contents.models import Category, Tag, Content
from django.utils.text import slugify

# 관리자 계정 가져오기
admin = User.objects.filter(username='admin').first()
if not admin:
    print("❌ Admin user not found.")
    exit(1)

print(f"✓ Admin user: {admin.username}")

# 상위 카테고리 생성
print("\n📁 Creating parent category...")
data_model_category, created = Category.objects.get_or_create(
    slug='data-model',
    defaults={
        'name': '데이터 모델',
        'description': '데이터 구조 및 모델링',
        'order': 3,
        'parent': None,
    }
)
print(f"  {'✓ Created' if created else '○ Exists'} category: {data_model_category.name}")

# 하위 카테고리 생성
print("\n📁 Creating sub-category...")
rdf_category, created = Category.objects.get_or_create(
    slug='rdf',
    defaults={
        'name': 'RDF',
        'description': 'Resource Description Framework - 시맨틱 웹 데이터 모델',
        'parent': data_model_category,
        'order': 1,
    }
)
print(f"  {'✓ Created' if created else '○ Exists'} sub-category: {rdf_category.name} (under {data_model_category.name})")

# 태그 생성
print("\n🏷️  Creating tags...")
tags_data = ["데이터 모델링", "온톨로지", "시맨틱웹"]

tags = {}
for tag_name in tags_data:
    tag, created = Tag.objects.get_or_create(
        slug=slugify(tag_name),
        defaults={'name': tag_name}
    )
    tags[tag_name] = tag
    print(f"  {'✓ Created' if created else '○ Exists'} tag: {tag.name}")

# RDF 콘텐츠 생성
print("\n📝 Creating RDF content...")

content_data = {
    "title": "RDF 기초 학습",
    "summary": "시맨틱 웹의 핵심 기술인 RDF의 개념과 구조를 학습하고, 실제 RDF 데이터를 작성해봅니다.",
    "category": rdf_category,
    "tags": ["데이터 모델링", "온톨로지", "시맨틱웹"],
    "difficulty": "INTERMEDIATE",
    "estimated_time": 30,
    "prerequisites": "XML 기본 지식",
    "learning_objectives": "RDF의 개념과 트리플 구조를 이해하고, 간단한 RDF 문서를 작성할 수 있습니다.",
    "content": """
<h2>RDF란?</h2>
<p><strong>RDF (Resource Description Framework)</strong>는 웹상의 자원(리소스)을 기술하기 위한 표준 모델입니다.
시맨틱 웹의 핵심 기술로, 데이터를 구조화하여 컴퓨터가 이해하고 처리할 수 있도록 합니다.</p>

<h2>RDF의 핵심 개념</h2>

<h3>1. 트리플 (Triple) 구조</h3>
<p>RDF는 <strong>주어(Subject) - 서술어(Predicate) - 목적어(Object)</strong>의 3요소로 데이터를 표현합니다.</p>

<div style="background:#f5f5f5; padding:15px; border-radius:8px; margin:15px 0;">
<strong>예시:</strong><br>
<code>홍길동 - 작성했다 - 논문</code><br>
<ul style="margin-top:10px;">
    <li><strong>주어(Subject):</strong> 홍길동 (리소스)</li>
    <li><strong>서술어(Predicate):</strong> 작성했다 (속성/관계)</li>
    <li><strong>목적어(Object):</strong> 논문 (값 또는 리소스)</li>
</ul>
</div>

<h3>2. URI (Uniform Resource Identifier)</h3>
<p>RDF에서는 리소스를 식별하기 위해 URI를 사용합니다.</p>
<pre><code>http://example.org/person/홍길동
http://example.org/property/작성했다
http://example.org/paper/논문123</code></pre>

<h3>3. 네임스페이스 (Namespace)</h3>
<p>긴 URI를 간단하게 표현하기 위해 접두어를 사용합니다.</p>
<pre><code>@prefix ex: &lt;http://example.org/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .
@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .</code></pre>

<h2>RDF 직렬화 형식</h2>

<h3>1. Turtle (Terse RDF Triple Language)</h3>
<p>가장 읽기 쉬운 RDF 형식입니다.</p>

<pre><code>@prefix ex: &lt;http://example.org/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .

ex:홍길동 foaf:name "홍길동" ;
          foaf:age 30 ;
          foaf:knows ex:김철수 .

ex:김철수 foaf:name "김철수" ;
          foaf:age 28 .</code></pre>

<h3>2. RDF/XML</h3>
<p>XML 형식의 RDF 표현입니다.</p>

<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:foaf="http://xmlns.com/foaf/0.1/"
         xmlns:ex="http://example.org/"&gt;

  &lt;rdf:Description rdf:about="http://example.org/홍길동"&gt;
    &lt;foaf:name&gt;홍길동&lt;/foaf:name&gt;
    &lt;foaf:age&gt;30&lt;/foaf:age&gt;
    &lt;foaf:knows rdf:resource="http://example.org/김철수"/&gt;
  &lt;/rdf:Description&gt;

  &lt;rdf:Description rdf:about="http://example.org/김철수"&gt;
    &lt;foaf:name&gt;김철수&lt;/foaf:name&gt;
    &lt;foaf:age&gt;28&lt;/foaf:age&gt;
  &lt;/rdf:Description&gt;

&lt;/rdf:RDF&gt;</code></pre>

<h3>3. JSON-LD (JSON for Linking Data)</h3>
<p>JSON 기반의 RDF 표현입니다.</p>

<pre><code>{
  "@context": {
    "foaf": "http://xmlns.com/foaf/0.1/",
    "ex": "http://example.org/"
  },
  "@graph": [
    {
      "@id": "ex:홍길동",
      "foaf:name": "홍길동",
      "foaf:age": 30,
      "foaf:knows": { "@id": "ex:김철수" }
    },
    {
      "@id": "ex:김철수",
      "foaf:name": "김철수",
      "foaf:age": 28
    }
  ]
}</code></pre>

<h2>주요 RDF 어휘 (Vocabulary)</h2>

<h3>1. FOAF (Friend of a Friend)</h3>
<p>사람과 관계를 표현하는 어휘</p>
<ul>
    <li><code>foaf:Person</code> - 사람</li>
    <li><code>foaf:name</code> - 이름</li>
    <li><code>foaf:knows</code> - ~을 안다</li>
    <li><code>foaf:mbox</code> - 이메일</li>
</ul>

<h3>2. Dublin Core (DC)</h3>
<p>문서 메타데이터를 표현하는 어휘</p>
<ul>
    <li><code>dc:title</code> - 제목</li>
    <li><code>dc:creator</code> - 작성자</li>
    <li><code>dc:date</code> - 날짜</li>
    <li><code>dc:subject</code> - 주제</li>
</ul>

<h3>3. Schema.org</h3>
<p>검색엔진 최적화를 위한 구조화된 데이터</p>
<ul>
    <li><code>schema:Person</code> - 사람</li>
    <li><code>schema:Organization</code> - 조직</li>
    <li><code>schema:Event</code> - 이벤트</li>
    <li><code>schema:Article</code> - 기사/문서</li>
</ul>

<h2>실습 예제</h2>

<h3>예제 1: 도서 정보 표현</h3>
<pre><code>@prefix ex: &lt;http://example.org/&gt; .
@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .
@prefix schema: &lt;http://schema.org/&gt; .

ex:book123 a schema:Book ;
           dc:title "시맨틱 웹 입문" ;
           dc:creator "홍길동" ;
           dc:publisher "출판사" ;
           dc:date "2024-01-15" ;
           schema:isbn "978-1234567890" ;
           schema:numberOfPages 350 .</code></pre>

<h3>예제 2: 조직과 사람 관계</h3>
<pre><code>@prefix ex: &lt;http://example.org/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .
@prefix org: &lt;http://www.w3.org/ns/org#&gt; .

ex:한국대학교 a foaf:Organization ;
              foaf:name "한국대학교" ;
              org:hasMember ex:홍길동 .

ex:홍길동 a foaf:Person ;
          foaf:name "홍길동" ;
          foaf:title "교수" ;
          org:memberOf ex:한국대학교 .</code></pre>

<h3>예제 3: 학술 논문 메타데이터</h3>
<pre><code>@prefix ex: &lt;http://example.org/&gt; .
@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .
@prefix bibo: &lt;http://purl.org/ontology/bibo/&gt; .

ex:paper001 a bibo:AcademicArticle ;
            dc:title "인공지능 윤리 연구" ;
            dc:creator ex:홍길동 ;
            dc:date "2024-03-15" ;
            dc:subject "인공지능", "윤리" ;
            bibo:abstract "본 논문은 인공지능의 윤리적 문제를 다룬다." ;
            bibo:doi "10.1234/example.2024.001" .</code></pre>

<h2>RDF의 장점</h2>

<ul>
    <li>✓ <strong>상호운용성:</strong> 서로 다른 시스템 간 데이터 교환이 용이</li>
    <li>✓ <strong>확장성:</strong> 새로운 속성과 관계를 쉽게 추가 가능</li>
    <li>✓ <strong>의미 표현:</strong> 데이터의 의미를 명확하게 표현</li>
    <li>✓ <strong>연결성:</strong> 데이터 간의 관계를 네트워크로 표현</li>
    <li>✓ <strong>추론:</strong> 명시되지 않은 정보를 논리적으로 유추 가능</li>
</ul>

<h2>RDF의 활용 분야</h2>

<h3>1. 지식 그래프 (Knowledge Graph)</h3>
<ul>
    <li>Google Knowledge Graph</li>
    <li>DBpedia - 위키피디아의 구조화된 데이터</li>
    <li>Wikidata - 협업 지식 베이스</li>
</ul>

<h3>2. 학술 데이터 관리</h3>
<ul>
    <li>연구자 프로필 (ORCID)</li>
    <li>학술 논문 메타데이터</li>
    <li>연구 프로젝트 관리</li>
</ul>

<h3>3. 도서관 및 문화유산</h3>
<ul>
    <li>서지 정보 (BIBFRAME)</li>
    <li>박물관 소장품 정보 (CIDOC-CRM)</li>
    <li>디지털 아카이브</li>
</ul>

<h3>4. 정부 공공 데이터</h3>
<ul>
    <li>Linked Open Data (LOD)</li>
    <li>통계 데이터 (RDF Data Cube)</li>
    <li>공공기관 정보</li>
</ul>

<h2>SPARQL - RDF 쿼리 언어</h2>
<p>SPARQL은 RDF 데이터를 검색하기 위한 쿼리 언어입니다.</p>

<h3>기본 쿼리 예제</h3>
<pre><code>PREFIX foaf: &lt;http://xmlns.com/foaf/0.1/&gt;

SELECT ?name ?age
WHERE {
  ?person foaf:name ?name ;
          foaf:age ?age .
  FILTER (?age > 25)
}
ORDER BY DESC(?age)</code></pre>

<p>이 쿼리는 나이가 25세 이상인 사람들의 이름과 나이를 나이 내림차순으로 검색합니다.</p>

<h2>RDF 도구</h2>

<h3>1. RDF 편집 및 검증 도구</h3>
<ul>
    <li><strong>Protégé:</strong> 온톨로지 편집기</li>
    <li><strong>RDF Validator:</strong> W3C RDF 검증 도구</li>
    <li><strong>EasyRDF Converter:</strong> RDF 형식 변환</li>
</ul>

<h3>2. RDF 저장소 (Triple Store)</h3>
<ul>
    <li><strong>Apache Jena:</strong> Java 기반 RDF 프레임워크</li>
    <li><strong>RDF4J:</strong> Java RDF 데이터베이스</li>
    <li><strong>Virtuoso:</strong> 고성능 RDF 저장소</li>
    <li><strong>GraphDB:</strong> 상용 RDF 데이터베이스</li>
</ul>

<h3>3. SPARQL 엔드포인트</h3>
<ul>
    <li><strong>DBpedia SPARQL:</strong> http://dbpedia.org/sparql</li>
    <li><strong>Wikidata Query Service:</strong> https://query.wikidata.org/</li>
</ul>

<h2>학습 팁</h2>
<ul>
    <li>✓ Turtle 형식으로 먼저 시작하세요 (가장 읽기 쉬움)</li>
    <li>✓ 간단한 트리플부터 작성해보세요</li>
    <li>✓ 표준 어휘(FOAF, DC 등)를 먼저 익히세요</li>
    <li>✓ DBpedia나 Wikidata에서 실제 데이터를 살펴보세요</li>
    <li>✓ SPARQL 쿼리를 직접 작성하고 실행해보세요</li>
</ul>

<h2>다음 학습 단계</h2>
<ul>
    <li><strong>RDFS (RDF Schema):</strong> 클래스와 속성 정의</li>
    <li><strong>OWL (Web Ontology Language):</strong> 복잡한 온톨로지 표현</li>
    <li><strong>SPARQL:</strong> 고급 쿼리 기법</li>
    <li><strong>추론 (Reasoning):</strong> 규칙 기반 지식 추론</li>
</ul>

<h2>참고 자료</h2>
<ul>
    <li>W3C RDF 1.1 Primer: <a href="https://www.w3.org/TR/rdf11-primer/" target="_blank">https://www.w3.org/TR/rdf11-primer/</a></li>
    <li>DBpedia: <a href="https://www.dbpedia.org/" target="_blank">https://www.dbpedia.org/</a></li>
    <li>Linked Open Vocabularies: <a href="https://lov.linkeddata.es/" target="_blank">https://lov.linkeddata.es/</a></li>
</ul>
"""
}

content_tags = [tags[tag_name] for tag_name in content_data['tags']]

content, created = Content.objects.get_or_create(
    slug=slugify(content_data['title']),
    defaults={
        'title': content_data['title'],
        'summary': content_data['summary'],
        'category': content_data['category'],
        'author': admin,
        'difficulty': content_data['difficulty'],
        'estimated_time': content_data['estimated_time'],
        'prerequisites': content_data['prerequisites'],
        'learning_objectives': content_data['learning_objectives'],
        'content_html': content_data['content'],
        'status': 'PUBLISHED',
        'version': '1.0',
    }
)

if created:
    content.tags.set(content_tags)
    print(f"  ✓ Created content: {content.title}")
else:
    print(f"  ○ Exists content: {content.title}")

print("\n🎉 RDF content created successfully!")
print("\n📊 Summary:")
print(f"  - Parent Category: 데이터 모델")
print(f"  - Sub Category: RDF")
print(f"  - Tags: {', '.join(content_data['tags'])}")
print(f"  - Content: {content_data['title']}")
print(f"  - Difficulty: 중급")
print(f"  - Estimated Time: 30분")
