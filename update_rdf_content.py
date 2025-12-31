"""
RDF 교육 콘텐츠 내용 업데이트 스크립트
개선된 단계별 학습 내용으로 교체합니다.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content

# RDF 콘텐츠 찾기
rdf_content = Content.objects.filter(slug='rdf').first()

if not rdf_content:
    print("❌ RDF 콘텐츠를 찾을 수 없습니다.")
    exit(1)

print(f"✓ RDF 콘텐츠 발견: {rdf_content.title}")

# 새로운 학습 내용
new_content = """
<h2>RDF 쉽게 배우기</h2>
<p class="lead">시맨틱 웹의 핵심! 데이터를 연결하는 방법을 단계별로 배워봅시다.</p>

<div class="alert alert-info">
<strong>💡 학습 목표:</strong> 이 강의를 마치면 RDF의 개념을 이해하고, Turtle 형식으로 간단한 RDF 문서를 작성할 수 있습니다.
</div>

<hr/>

<h2>1단계: RDF가 뭔가요?</h2>
<p class="subtitle">시맨틱 웹의 기초를 이해해봅시다</p>

<div class="info-box blue">
<h4>🤔 문제 상황</h4>
<p>웹에는 엄청난 정보가 있지만, 컴퓨터는 그 의미를 이해하지 못합니다.</p>
<p>예를 들어 "홍길동이 논문을 작성했다"라는 문장을 사람은 이해하지만, 컴퓨터는 단순한 텍스트로만 봅니다.</p>
</div>

<div class="info-box green">
<h4>💡 해결책: RDF</h4>
<p><strong>RDF (Resource Description Framework)</strong>는 데이터를 컴퓨터가 이해할 수 있는 형태로 표현하는 방법입니다.</p>
</div>

<div class="key-concept">
<h4>핵심 아이디어</h4>
<p>모든 정보를 <strong>"누가 - 무엇을 - 어떻게"</strong> 형태로 쪼개서 표현합니다.</p>
<p>이것을 <strong>트리플(Triple)</strong>이라고 부릅니다.</p>
</div>

<pre><code># 이것은 우리가 이해하는 방식:
"홍길동이 인공지능 논문을 작성했다"

# RDF로 표현하면:
주어(Subject):    홍길동
서술어(Predicate): 작성했다
목적어(Object):   인공지능 논문</code></pre>

<hr/>

<h2>2단계: 트리플 이해하기</h2>
<p class="subtitle">주어-서술어-목적어 구조</p>

<p>RDF의 기본 단위는 <strong>트리플(Triple)</strong>입니다. 항상 3개의 요소로 구성됩니다.</p>

<table class="table">
<thead>
<tr>
<th style="background-color: #DBEAFE; text-align: center;">주어 (Subject)</th>
<th style="background-color: #D1FAE5; text-align: center;">서술어 (Predicate)</th>
<th style="background-color: #E9D5FF; text-align: center;">목적어 (Object)</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: center;">누가/무엇이</td>
<td style="text-align: center;">어떤 관계/속성</td>
<td style="text-align: center;">무엇을/값</td>
</tr>
</tbody>
</table>

<div class="examples-box">
<h4>📝 실제 예시들:</h4>
<ul>
<li><span class="subject">홍길동</span> → <span class="predicate">나이</span> → <span class="object">30</span></li>
<li><span class="subject">홍길동</span> → <span class="predicate">직업</span> → <span class="object">교수</span></li>
<li><span class="subject">홍길동</span> → <span class="predicate">알고있다</span> → <span class="object">김철수</span></li>
</ul>
</div>

<div class="info-box yellow">
<h4>💡 왜 이렇게 표현할까요?</h4>
<p>컴퓨터가 데이터 간의 관계를 이해하고 연결할 수 있습니다!</p>
</div>

<pre><code># 사람이 읽는 방식:
홍길동은 30살이고, 교수이며, 김철수를 안다.

# RDF 트리플로 분해:
1. 홍길동 - 나이 - 30
2. 홍길동 - 직업 - 교수
3. 홍길동 - 알고있다 - 김철수</code></pre>

<hr/>

<h2>3단계: Turtle 문법 배우기</h2>
<p class="subtitle">RDF를 작성하는 가장 쉬운 방법</p>

<p><strong>Turtle</strong>은 RDF를 작성하는 가장 읽기 쉬운 형식입니다.</p>

<h3>1️⃣ 네임스페이스 선언 (접두어 정의)</h3>
<p>긴 URL을 짧게 줄이기 위한 약어를 만듭니다.</p>

<pre><code>@prefix ex: &lt;http://example.org/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .</code></pre>

<p class="small-note">이제 긴 URL 대신 ex:, foaf: 같은 짧은 접두어를 쓸 수 있어요!</p>

<h3>2️⃣ 트리플 작성</h3>
<p>주어, 서술어, 목적어를 공백으로 구분하고 마침표(.)로 끝냅니다.</p>

<pre><code>ex:홍길동 foaf:name "홍길동" .</code></pre>

<h3>3️⃣ 같은 주어 여러 속성 (세미콜론 ; 사용)</h3>
<p>같은 사람의 여러 정보를 한번에 쓸 수 있습니다.</p>

<pre><code>ex:홍길동 foaf:name "홍길동" ;
          foaf:age 30 ;
          foaf:title "교수" .</code></pre>

<p class="small-note">세미콜론(;)을 쓰면 주어를 반복하지 않아도 돼요!</p>

<h3>4️⃣ 여러 값 나열 (쉼표 , 사용)</h3>

<pre><code>ex:홍길동 foaf:knows ex:김철수, ex:이영희, ex:박민수 .</code></pre>

<p class="small-note">홍길동이 여러 사람을 안다는 것을 간단하게 표현!</p>

<div class="info-box green">
<h4>✨ 기억하세요!</h4>
<ul>
<li><strong>마침표(.)</strong> = 트리플 끝</li>
<li><strong>세미콜론(;)</strong> = 같은 주어, 다른 서술어</li>
<li><strong>쉼표(,)</strong> = 같은 주어와 서술어, 여러 목적어</li>
</ul>
</div>

<pre><code>@prefix ex: &lt;http://example.org/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .

# 간단한 방식
ex:홍길동 foaf:name "홍길동" .
ex:홍길동 foaf:age 30 .
ex:홍길동 foaf:title "교수" .

# 똑같은 내용을 더 깔끔하게!
ex:홍길동 foaf:name "홍길동" ;
          foaf:age 30 ;
          foaf:title "교수" .</code></pre>

<hr/>

<h2>4단계: 실전 예제</h2>
<p class="subtitle">실제로 작성해봅시다</p>

<div class="info-box blue">
<h4>📖 시나리오</h4>
<p>홍길동 교수님이 "인공지능 윤리"라는 논문을 2024년에 작성했습니다.</p>
<p>이 논문은 한국대학교에서 발행되었고, 주제는 "AI"와 "윤리"입니다.</p>
</div>

<h3>🔍 이 정보를 트리플로 분해하면:</h3>

<ol>
<li>논문 - 제목 - "인공지능 윤리"</li>
<li>논문 - 작성자 - 홍길동</li>
<li>논문 - 발행년도 - 2024</li>
<li>논문 - 발행기관 - 한국대학교</li>
<li>논문 - 주제 - "AI"</li>
<li>논문 - 주제 - "윤리"</li>
</ol>

<h3>📝 Turtle로 작성하면:</h3>

<pre><code>@prefix ex: &lt;http://example.org/&gt; .
@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .

ex:논문001 dc:title "인공지능 윤리" ;
          dc:creator "홍길동" ;
          dc:date "2024" ;
          dc:publisher "한국대학교" ;
          dc:subject "AI", "윤리" .</code></pre>

<div class="info-box yellow">
<h4>💡 포인트</h4>
<ul>
<li><strong>dc:</strong>는 Dublin Core의 약자 (도서관에서 많이 쓰는 표준 어휘)</li>
<li>같은 주어의 여러 속성을 세미콜론(;)으로 연결</li>
<li>여러 주제는 쉼표(,)로 나열</li>
</ul>
</div>

<hr/>

<h2>5단계: 관계 표현하기</h2>
<p class="subtitle">사람들 사이의 연결을 나타내봅시다</p>

<p>RDF의 진짜 힘은 <strong>관계를 표현</strong>하는 것입니다!</p>

<div class="info-box gradient">
<h4>👥 소셜 네트워크 예제</h4>
<p>홍길동, 김철수, 이영희가 서로를 알고 있습니다.</p>
<p style="text-align: center; font-size: 1.2em; margin: 10px 0;">
홍길동 ↔ 김철수 ↔ 이영희
</p>
</div>

<h3>RDF로 표현:</h3>

<pre><code>@prefix ex: &lt;http://example.org/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .

ex:홍길동 a foaf:Person ;
          foaf:name "홍길동" ;
          foaf:age 30 ;
          foaf:knows ex:김철수, ex:이영희 .

ex:김철수 a foaf:Person ;
          foaf:name "김철수" ;
          foaf:age 28 ;
          foaf:knows ex:홍길동, ex:이영희 .

ex:이영희 a foaf:Person ;
          foaf:name "이영희" ;
          foaf:age 25 ;
          foaf:knows ex:홍길동, ex:김철수 .</code></pre>

<div class="two-columns">
<div class="info-box blue">
<h4>🔤 a 는 무엇?</h4>
<p><code>a</code>는 "타입이다"라는 뜻입니다.</p>
<p><code>ex:홍길동 a foaf:Person</code> = "홍길동은 사람이다"</p>
</div>

<div class="info-box green">
<h4>🔗 foaf:knows</h4>
<p>FOAF (Friend of a Friend)의 "안다"는 관계</p>
<p>소셜 네트워크를 표현하는 표준 어휘</p>
</div>
</div>

<div class="info-box green">
<h4>✨ 이렇게 하면 뭐가 좋을까요?</h4>
<ul>
<li>컴퓨터가 "홍길동이 아는 사람들"을 자동으로 찾을 수 있어요</li>
<li>"친구의 친구" 같은 간접 관계도 추적 가능해요</li>
<li>여러 데이터베이스를 연결할 수 있어요</li>
</ul>
</div>

<hr/>

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

<hr/>

<h2>RDF의 장점</h2>

<ul>
<li>✓ <strong>상호운용성:</strong> 서로 다른 시스템 간 데이터 교환이 용이</li>
<li>✓ <strong>확장성:</strong> 새로운 속성과 관계를 쉽게 추가 가능</li>
<li>✓ <strong>의미 표현:</strong> 데이터의 의미를 명확하게 표현</li>
<li>✓ <strong>연결성:</strong> 데이터 간의 관계를 네트워크로 표현</li>
<li>✓ <strong>추론:</strong> 명시되지 않은 정보를 논리적으로 유추 가능</li>
</ul>

<hr/>

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

<hr/>

<h2>학습 팁</h2>

<div class="two-columns">
<div>
<h4>✓ 학습 방법</h4>
<ul>
<li>Turtle 형식으로 먼저 시작하세요</li>
<li>간단한 트리플부터 작성해보세요</li>
<li>표준 어휘(FOAF, DC)를 먼저 익히세요</li>
<li>DBpedia에서 실제 데이터를 살펴보세요</li>
<li>SPARQL 쿼리를 직접 작성해보세요</li>
</ul>
</div>

<div>
<h4>📚 다음 단계</h4>
<ul>
<li><strong>RDFS</strong> (RDF Schema) - 클래스 정의</li>
<li><strong>OWL</strong> (Web Ontology Language) - 온톨로지</li>
<li><strong>SPARQL</strong> - 고급 쿼리</li>
<li><strong>추론</strong> (Reasoning)</li>
<li><strong>지식 그래프</strong> 구축</li>
</ul>
</div>
</div>

<hr/>

<h2>참고 자료</h2>

<h3>공식 문서</h3>
<ul>
<li>W3C RDF 1.1 Primer: <a href="https://www.w3.org/TR/rdf11-primer/" target="_blank">https://www.w3.org/TR/rdf11-primer/</a></li>
<li>W3C Turtle Specification: <a href="https://www.w3.org/TR/turtle/" target="_blank">https://www.w3.org/TR/turtle/</a></li>
</ul>

<h3>실습 데이터</h3>
<ul>
<li>DBpedia: <a href="https://www.dbpedia.org/" target="_blank">https://www.dbpedia.org/</a></li>
<li>Wikidata: <a href="https://www.wikidata.org/" target="_blank">https://www.wikidata.org/</a></li>
<li>Linked Open Vocabularies: <a href="https://lov.linkeddata.es/" target="_blank">https://lov.linkeddata.es/</a></li>
</ul>

<h3>도구</h3>
<ul>
<li><strong>W3C RDF Validator:</strong> RDF 문법 검증</li>
<li><strong>EasyRDF Converter:</strong> RDF 형식 변환</li>
<li><strong>Apache Jena:</strong> Java 기반 RDF 프레임워크</li>
<li><strong>Protégé:</strong> 온톨로지 편집기</li>
</ul>

<hr/>

<div class="alert alert-success">
<h3>🎉 학습을 마치며</h3>
<p>축하합니다! RDF의 기초를 모두 배우셨습니다.</p>
<p>이제 실제 프로젝트에서 RDF를 활용하여 데이터를 연결하고, 의미 있는 정보를 만들어보세요!</p>
<p>더 자세한 실습은 <strong>http://localhost:3000/data-model/rdf</strong> 페이지에서 단계별로 진행할 수 있습니다.</p>
</div>

<style>
.info-box {
    padding: 15px;
    margin: 15px 0;
    border-radius: 8px;
    border-left: 4px solid;
}
.info-box.blue {
    background-color: #EFF6FF;
    border-color: #3B82F6;
}
.info-box.green {
    background-color: #F0FDF4;
    border-color: #10B981;
}
.info-box.yellow {
    background-color: #FFFBEB;
    border-color: #F59E0B;
}
.info-box.gradient {
    background: linear-gradient(to right, #EFF6FF, #F5F3FF);
    border-color: #8B5CF6;
}
.key-concept {
    border-left: 4px solid #6366F1;
    padding-left: 15px;
    margin: 15px 0;
}
.examples-box {
    background-color: #F9FAFB;
    padding: 15px;
    border-radius: 8px;
    margin: 15px 0;
}
.subject {
    background-color: #BFDBFE;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 500;
}
.predicate {
    background-color: #BBF7D0;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 500;
}
.object {
    background-color: #DDD6FE;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 500;
}
.small-note {
    font-size: 0.85em;
    color: #6B7280;
    margin-top: 5px;
}
.two-columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
    margin: 15px 0;
}
@media (max-width: 768px) {
    .two-columns {
        grid-template-columns: 1fr;
    }
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
.lead {
    font-size: 1.15em;
    color: #6B7280;
    margin-bottom: 20px;
}
.subtitle {
    font-size: 1.1em;
    color: #6B7280;
    font-weight: 400;
    margin-top: -10px;
    margin-bottom: 15px;
}
</style>
"""

# 콘텐츠 업데이트
rdf_content.content_html = new_content
rdf_content.save()

print(f"\n✅ RDF 콘텐츠가 성공적으로 업데이트되었습니다!")
print(f"\n📊 업데이트 정보:")
print(f"  - 제목: {rdf_content.title}")
print(f"  - 카테고리: {rdf_content.category.name}")
print(f"  - 난이도: {rdf_content.get_difficulty_display()}")
print(f"  - 소요시간: {rdf_content.estimated_time}분")
print(f"\n💡 확인:")
print(f"  - 교육 콘텐츠 상세: http://localhost:3000/contents/{rdf_content.slug}")
print(f"  - RDF 학습 페이지: http://localhost:3000/data-model/rdf")
