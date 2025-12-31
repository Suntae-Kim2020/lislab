#!/usr/bin/env python
"""
RDFS 학습 콘텐츠 추가 스크립트
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

def create_rdfs_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 생성 또는 가져오기: 온톨로지
    ontology_category, created = Category.objects.get_or_create(
        slug='ontology',
        defaults={
            'name': '온톨로지',
            'description': '온톨로지와 시맨틱 웹',
            'parent': None
        }
    )
    if created:
        print("✓ 상위 카테고리 생성: 온톨로지")
    else:
        print("✓ 상위 카테고리 확인: 온톨로지")

    # 하위 카테고리 생성 또는 가져오기: RDFS
    rdfs_category, created = Category.objects.get_or_create(
        slug='rdfs',
        defaults={
            'name': 'RDFS',
            'description': 'RDF Schema',
            'parent': ontology_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: RDFS")
    else:
        print("✓ 하위 카테고리 확인: RDFS")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': 'RDFS', 'slug': 'rdfs'},
        {'name': 'RDF Schema', 'slug': 'rdf-schema'},
        {'name': '온톨로지', 'slug': 'ontology'},
        {'name': 'RDF', 'slug': 'rdf'},
        {'name': '시맨틱 웹', 'slug': 'semantic-web'},
        {'name': '추론', 'slug': 'inference'},
        {'name': 'OWL', 'slug': 'owl'},
        {'name': '링크드 데이터', 'slug': 'linked-data'}
    ]
    tags = []
    for tag_info in tag_data:
        # slug로 먼저 찾기
        try:
            tag = Tag.objects.get(slug=tag_info['slug'])
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=tag_info['name'], slug=tag_info['slug'])
        tags.append(tag)
        print(f"  ✓ 태그 확인: {tag.name}")

    # 학습 콘텐츠 생성
    content = Content.objects.create(
        title="RDFS: RDF에 의미를 더하는 스키마",
        slug="rdfs-rdf-schema",
        summary="RDFS로 도서관 데이터에 구조와 의미를 부여하세요! 클래스, 속성, 상속을 정의하고 자동 추론까지 가능한 RDFS의 모든 것을 배웁니다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>RDFS가 무엇인지, RDF와 어떻게 다른지 이해하기</li>
    <li>RDFS로 클래스와 속성을 선언하는 방법 배우기</li>
    <li>RDFS 클래스/관계와 RDF 그래프의 관계 파악하기</li>
    <li>RDFS로 간단한 추론이 왜 가능한지 알기</li>
    <li>RDFS와 OWL의 차이점 이해하기</li>
    <li>RDF/XML, Turtle, JSON-LD에서 RDFS 사용하기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. RDFS를 한 문장으로</h2>

  <div class="hero-definition">
    <h3>📚 RDFS란?</h3>
    <p class="big-statement">
      <strong>RDFS (RDF Schema)</strong>는<br>
      RDF 데이터에 <strong>구조와 의미</strong>를 부여하는<br>
      <strong>어휘 정의 언어</strong>입니다.
    </p>
  </div>

  <div class="simple-analogy">
    <h4>🏗️ 쉬운 비유</h4>
    <div class="analogy-grid">
      <div class="analogy-box">
        <h5>RDF</h5>
        <p class="analogy-desc">자유롭게 쌓는 레고 블록</p>
        <div class="analogy-example">
          <p>"이것"과 "저것"이 "관계있다"</p>
          <p class="small">아무 관계나 막 만들 수 있어요</p>
        </div>
      </div>

      <div class="arrow">+</div>

      <div class="analogy-box">
        <h5>RDFS</h5>
        <p class="analogy-desc">레고 조립 설명서</p>
        <div class="analogy-example">
          <p>"이런 종류의 블록들이 있고"</p>
          <p>"이렇게 연결할 수 있어요"</p>
          <p class="small">규칙과 의미를 정의</p>
        </div>
      </div>

      <div class="arrow">=</div>

      <div class="analogy-box highlight">
        <h5>RDF + RDFS</h5>
        <p class="analogy-desc">의미있는 구조물</p>
        <div class="analogy-example">
          <p>자유로우면서도 체계적!</p>
          <p class="small">컴퓨터가 의미를 이해</p>
        </div>
      </div>
    </div>
  </div>

  <div class="rdf-vs-rdfs">
    <h4>🤔 RDF vs RDFS</h4>
    <table class="comparison-table">
      <thead>
        <tr>
          <th>RDF</th>
          <th>RDFS</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>데이터를 표현</td>
          <td>데이터의 구조를 정의</td>
        </tr>
        <tr>
          <td>"해리포터는 책이다"</td>
          <td>"책은 출판물의 한 종류다"</td>
        </tr>
        <tr>
          <td>개별 사실(인스턴스)</td>
          <td>클래스와 관계 정의</td>
        </tr>
        <tr>
          <td>주어-술어-목적어</td>
          <td>술어와 클래스의 의미</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="content-section">
  <h2>2. RDFS의 핵심 개념: 클래스와 속성</h2>

  <div class="core-concepts">
    <div class="concept-card class-concept">
      <div class="concept-icon">📦</div>
      <h4>1. 클래스 (Class)</h4>
      <p class="concept-desc">비슷한 것들의 집합</p>

      <div class="concept-example">
        <h5>🏷️ 도서관 예시</h5>
        <div class="example-hierarchy">
          <div class="class-item top">
            <strong>rdfs:Resource</strong>
            <p class="small">모든 것의 최상위</p>
          </div>
          <div class="hierarchy-arrow">⬇️</div>
          <div class="class-item">
            <strong>출판물 (Publication)</strong>
            <p class="small">출판된 모든 것</p>
          </div>
          <div class="hierarchy-arrow">⬇️</div>
          <div class="class-group">
            <div class="class-item sub">
              <strong>책 (Book)</strong>
            </div>
            <div class="class-item sub">
              <strong>잡지 (Magazine)</strong>
            </div>
            <div class="class-item sub">
              <strong>논문 (Article)</strong>
            </div>
          </div>
        </div>

        <div class="code-example-mini">
          <h6>RDFS로 선언하기:</h6>
          <pre class="code-tiny">
# Turtle 형식
:Book a rdfs:Class ;
    rdfs:subClassOf :Publication ;
    rdfs:label "책" .

:Magazine a rdfs:Class ;
    rdfs:subClassOf :Publication ;
    rdfs:label "잡지" .
          </pre>
        </div>
      </div>
    </div>

    <div class="concept-card property-concept">
      <div class="concept-icon">🔗</div>
      <h4>2. 속성 (Property)</h4>
      <p class="concept-desc">관계를 정의</p>

      <div class="concept-example">
        <h5>🔗 도서관 예시</h5>
        <div class="property-examples">
          <div class="prop-item">
            <strong>저자 (author)</strong>
            <p>책 → 사람</p>
            <code>domain: Book, range: Person</code>
          </div>
          <div class="prop-item">
            <strong>출판사 (publisher)</strong>
            <p>출판물 → 조직</p>
            <code>domain: Publication, range: Organization</code>
          </div>
          <div class="prop-item">
            <strong>출판일 (publicationDate)</strong>
            <p>출판물 → 날짜</p>
            <code>domain: Publication, range: xsd:date</code>
          </div>
        </div>

        <div class="code-example-mini">
          <h6>RDFS로 선언하기:</h6>
          <pre class="code-tiny">
:author a rdf:Property ;
    rdfs:domain :Book ;
    rdfs:range :Person ;
    rdfs:label "저자" .

:publisher a rdf:Property ;
    rdfs:domain :Publication ;
    rdfs:range :Organization ;
    rdfs:label "출판사" .
          </pre>
        </div>
      </div>
    </div>
  </div>

  <div class="key-terms">
    <h4>🔑 핵심 용어</h4>
    <div class="terms-grid">
      <div class="term-box">
        <strong>rdfs:Class</strong>
        <p>클래스를 선언할 때 사용</p>
      </div>
      <div class="term-box">
        <strong>rdfs:subClassOf</strong>
        <p>상위 클래스 지정 (상속)</p>
      </div>
      <div class="term-box">
        <strong>rdfs:domain</strong>
        <p>속성의 주체(주어) 지정</p>
      </div>
      <div class="term-box">
        <strong>rdfs:range</strong>
        <p>속성의 값(목적어) 지정</p>
      </div>
      <div class="term-box">
        <strong>rdfs:label</strong>
        <p>사람이 읽을 레이블</p>
      </div>
      <div class="term-box">
        <strong>rdfs:comment</strong>
        <p>설명 추가</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>3. RDFS와 RDF 그래프의 관계</h2>

  <div class="graph-relationship">
    <h4>💡 핵심: RDFS는 RDF 그래프를 설명하는 RDF 그래프입니다!</h4>
    <p>RDFS 자체도 RDF 트리플로 표현됩니다. 메타데이터의 메타데이터인 셈이죠.</p>
  </div>

  <div class="two-layer">
    <h4>🎭 두 개의 레이어</h4>

    <div class="layer-example">
      <div class="layer-box schema-layer">
        <h5>📋 스키마 레이어 (RDFS)</h5>
        <p class="layer-desc">구조와 규칙 정의</p>
        <pre class="code-block">
# RDFS로 도서관 온톨로지 정의
@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .
@prefix lib: &lt;http://library.org/vocab/&gt; .

# 클래스 정의
lib:Book a rdfs:Class ;
    rdfs:label "책" ;
    rdfs:comment "인쇄된 도서" .

lib:Person a rdfs:Class ;
    rdfs:label "사람" .

# 속성 정의
lib:author a rdf:Property ;
    rdfs:label "저자" ;
    rdfs:domain lib:Book ;
    rdfs:range lib:Person .

lib:title a rdf:Property ;
    rdfs:label "제목" ;
    rdfs:domain lib:Book ;
    rdfs:range xsd:string .
        </pre>
      </div>

      <div class="connection-arrow">⬇️ 이 스키마를 사용하여</div>

      <div class="layer-box data-layer">
        <h5>📊 데이터 레이어 (RDF)</h5>
        <p class="layer-desc">실제 데이터</p>
        <pre class="code-block">
# RDF로 실제 책 데이터
@prefix lib: &lt;http://library.org/vocab/&gt; .
@prefix data: &lt;http://library.org/data/&gt; .

# 해리포터 책
data:book1 a lib:Book ;
    lib:title "해리포터와 마법사의 돌" ;
    lib:author data:person1 .

# J.K. 롤링
data:person1 a lib:Person ;
    foaf:name "J.K. 롤링" .
        </pre>
      </div>
    </div>
  </div>

  <div class="graph-visualization">
    <h4>🕸️ 그래프로 보기</h4>
    <div class="graph-container">
      <div class="graph-part schema-graph">
        <h5>스키마 그래프</h5>
        <div class="visual-graph">
          <div class="node class-node">Book</div>
          <div class="edge">rdfs:subClassOf</div>
          <div class="node class-node">Publication</div>
          <br>
          <div class="node prop-node">author</div>
          <div class="edge">rdfs:domain</div>
          <div class="node class-node">Book</div>
          <br>
          <div class="node prop-node">author</div>
          <div class="edge">rdfs:range</div>
          <div class="node class-node">Person</div>
        </div>
      </div>

      <div class="plus">+</div>

      <div class="graph-part data-graph">
        <h5>데이터 그래프</h5>
        <div class="visual-graph">
          <div class="node instance-node">book1</div>
          <div class="edge">rdf:type</div>
          <div class="node class-node">Book</div>
          <br>
          <div class="node instance-node">book1</div>
          <div class="edge">author</div>
          <div class="node instance-node">person1</div>
          <br>
          <div class="node instance-node">person1</div>
          <div class="edge">rdf:type</div>
          <div class="node class-node">Person</div>
        </div>
      </div>
    </div>

    <div class="insight">
      <p>💡 <strong>핵심 인사이트:</strong> RDFS 정의(스키마)와 RDF 데이터가 같은 그래프에서 함께 존재하며,
      모두 트리플로 표현됩니다!</p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>4. RDFS로 추론이 가능한 이유</h2>

  <div class="inference-intro">
    <h4>🤖 자동 추론이란?</h4>
    <p>명시적으로 작성하지 않은 정보를 <strong>규칙을 바탕으로 자동으로 유추</strong>하는 것입니다.</p>
  </div>

  <div class="inference-examples">
    <div class="inference-card">
      <h5>📚 추론 예시 1: 클래스 상속</h5>

      <div class="inference-flow">
        <div class="given">
          <h6>✅ 우리가 알고 있는 것:</h6>
          <pre class="code-mini">
# RDFS 정의
:Book rdfs:subClassOf :Publication .
:Publication rdfs:subClassOf :CreativeWork .

# RDF 데이터
:HarryPotter a :Book .
          </pre>
        </div>

        <div class="reasoning">
          <h6>🧠 추론 과정:</h6>
          <ol>
            <li>HarryPotter는 Book이다 (명시적)</li>
            <li>Book은 Publication이다 (RDFS)</li>
            <li><strong>→ HarryPotter는 Publication이다</strong> (추론!)</li>
            <li>Publication은 CreativeWork이다 (RDFS)</li>
            <li><strong>→ HarryPotter는 CreativeWork이다</strong> (추론!)</li>
          </ol>
        </div>

        <div class="result">
          <h6>🎉 추론된 결과:</h6>
          <pre class="code-mini">
# 자동으로 추가되는 트리플들
:HarryPotter a :Book .          # 원래 있던 것
:HarryPotter a :Publication .   # 추론됨!
:HarryPotter a :CreativeWork .  # 추론됨!
          </pre>
        </div>
      </div>
    </div>

    <div class="inference-card">
      <h5>🔗 추론 예시 2: 속성의 domain과 range</h5>

      <div class="inference-flow">
        <div class="given">
          <h6>✅ 우리가 알고 있는 것:</h6>
          <pre class="code-mini">
# RDFS 정의
:author rdfs:domain :Book ;
        rdfs:range :Person .

# RDF 데이터
:HarryPotter :author :JKRowling .
          </pre>
        </div>

        <div class="reasoning">
          <h6>🧠 추론 과정:</h6>
          <ol>
            <li>HarryPotter의 author는 JKRowling이다 (명시적)</li>
            <li>author의 domain은 Book이다 (RDFS)</li>
            <li><strong>→ HarryPotter는 Book이다</strong> (추론!)</li>
            <li>author의 range는 Person이다 (RDFS)</li>
            <li><strong>→ JKRowling은 Person이다</strong> (추론!)</li>
          </ol>
        </div>

        <div class="result">
          <h6>🎉 추론된 결과:</h6>
          <pre class="code-mini">
# 자동으로 추가되는 트리플들
:HarryPotter a :Book .     # 추론됨!
:JKRowling a :Person .     # 추론됨!
          </pre>
        </div>
      </div>
    </div>

    <div class="inference-card">
      <h5>🔄 추론 예시 3: 속성 상속</h5>

      <div class="inference-flow">
        <div class="given">
          <h6>✅ 우리가 알고 있는 것:</h6>
          <pre class="code-mini">
# RDFS 정의
:hasPart rdfs:domain :Publication .
:hasChapter rdfs:subPropertyOf :hasPart ;
            rdfs:domain :Book .

# RDF 데이터
:HarryPotter :hasChapter :Chapter1 .
          </pre>
        </div>

        <div class="reasoning">
          <h6>🧠 추론 과정:</h6>
          <ol>
            <li>HarryPotter의 hasChapter는 Chapter1이다 (명시적)</li>
            <li>hasChapter는 hasPart의 하위속성이다 (RDFS)</li>
            <li><strong>→ HarryPotter의 hasPart는 Chapter1이다</strong> (추론!)</li>
          </ol>
        </div>

        <div class="result">
          <h6>🎉 추론된 결과:</h6>
          <pre class="code-mini">
# 자동으로 추가되는 트리플
:HarryPotter :hasPart :Chapter1 .  # 추론됨!
          </pre>
        </div>
      </div>
    </div>
  </div>

  <div class="why-inference">
    <h4>💡 왜 추론이 가능할까?</h4>
    <div class="reason-grid">
      <div class="reason-box">
        <h5>1. 명확한 규칙</h5>
        <p>RDFS는 <strong>정확한 의미론</strong>을 가지고 있습니다.</p>
        <ul>
          <li>subClassOf의 의미 명확</li>
          <li>domain/range의 역할 명확</li>
          <li>컴퓨터가 이해 가능</li>
        </ul>
      </div>

      <div class="reason-box">
        <h5>2. 논리적 일관성</h5>
        <p>추론 규칙이 <strong>수학적으로 증명</strong>되었습니다.</p>
        <ul>
          <li>A는 B다, B는 C다 → A는 C다</li>
          <li>전이적 관계 (transitivity)</li>
          <li>모순 없는 결과</li>
        </ul>
      </div>

      <div class="reason-box">
        <h5>3. 표준 추론 엔진</h5>
        <p>검증된 도구들이 있습니다.</p>
        <ul>
          <li>Apache Jena</li>
          <li>RDFLib (Python)</li>
          <li>Stardog, GraphDB</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="practical-benefit">
    <h4>🎯 실무에서의 장점</h4>
    <div class="benefit-scenario">
      <h5>시나리오: 도서관 검색 시스템</h5>
      <p><strong>사용자 질의:</strong> "모든 출판물을 찾아줘"</p>

      <div class="without-inference">
        <h6>❌ 추론 없이:</h6>
        <p>명시적으로 <code>a :Publication</code>이라고 된 것만 찾음</p>
        <p class="result-count">→ 결과 10개</p>
      </div>

      <div class="with-inference">
        <h6>✅ 추론 사용:</h6>
        <p>Book, Magazine, Article 등 Publication의 하위클래스도 모두 찾음</p>
        <p class="result-count">→ 결과 1,000개!</p>
      </div>

      <div class="insight-box">
        <p>💡 <strong>한 번 스키마를 정의하면, 자동으로 지능적인 검색이 가능합니다!</strong></p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>5. RDFS vs OWL</h2>

  <div class="owl-intro">
    <h4>🦉 OWL이란?</h4>
    <p><strong>OWL (Web Ontology Language)</strong>은 RDFS를 확장한 더 강력한 온톨로지 언어입니다.</p>
  </div>

  <table class="rdfs-owl-comparison">
    <thead>
      <tr>
        <th>항목</th>
        <th>RDFS</th>
        <th>OWL</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>복잡도</strong></td>
        <td>⭐⭐ 간단</td>
        <td>⭐⭐⭐⭐⭐ 복잡</td>
      </tr>
      <tr>
        <td><strong>표현력</strong></td>
        <td>⭐⭐⭐ 기본적</td>
        <td>⭐⭐⭐⭐⭐ 매우 강력</td>
      </tr>
      <tr>
        <td><strong>클래스</strong></td>
        <td>✅ 기본 클래스, 상속</td>
        <td>✅ 합집합, 교집합, 부정 등</td>
      </tr>
      <tr>
        <td><strong>속성</strong></td>
        <td>✅ domain, range, subProperty</td>
        <td>✅ 역관계, 대칭, 전이, 함수 등</td>
      </tr>
      <tr>
        <td><strong>제약조건</strong></td>
        <td>❌ 제한적</td>
        <td>✅ 매우 다양 (cardinality 등)</td>
      </tr>
      <tr>
        <td><strong>추론</strong></td>
        <td>✅ 기본 추론</td>
        <td>✅ 복잡한 추론</td>
      </tr>
      <tr>
        <td><strong>학습 난이도</strong></td>
        <td>⭐⭐ 쉬움</td>
        <td>⭐⭐⭐⭐⭐ 어려움</td>
      </tr>
      <tr>
        <td><strong>성능</strong></td>
        <td>⭐⭐⭐⭐⭐ 빠름</td>
        <td>⭐⭐ 느릴 수 있음</td>
      </tr>
      <tr>
        <td><strong>용도</strong></td>
        <td>간단한 온톨로지, 어휘 정의</td>
        <td>복잡한 도메인 모델링</td>
      </tr>
    </tbody>
  </table>

  <div class="capability-examples">
    <h4>🔍 무엇이 다를까? 실제 예시</h4>

    <div class="capability-grid">
      <div class="capability-card rdfs-can">
        <h5>RDFS로 가능한 것</h5>
        <pre class="code-mini">
# 클래스 정의
:Book rdfs:subClassOf :Publication .

# 속성 정의
:author rdfs:domain :Book ;
        rdfs:range :Person .

# 속성 상속
:writtenBy rdfs:subPropertyOf :creator .
        </pre>
        <p class="capability-note">✅ 기본적인 분류와 관계 정의</p>
      </div>

      <div class="capability-card owl-can">
        <h5>OWL만 가능한 것</h5>
        <pre class="code-mini">
# 역관계 정의
:author owl:inverseOf :authorOf .

# 제약조건
:Book owl:hasValue :copyrighted "true" ;
      owl:cardinality 1 .  # 정확히 1개

# 복잡한 클래스
:BestSeller owl:intersectionOf (
    :Book
    [ :soldCopies > 1000000 ]
) .
        </pre>
        <p class="capability-note">✅ 복잡한 논리와 제약조건</p>
      </div>
    </div>
  </div>

  <div class="relationship">
    <h4>🔗 RDFS와 OWL의 관계</h4>
    <div class="relationship-diagram">
      <div class="level">
        <div class="tech-box">RDF</div>
        <p class="level-desc">데이터 표현 기본</p>
      </div>
      <div class="arrow-up">⬆️ 확장</div>
      <div class="level">
        <div class="tech-box">RDFS</div>
        <p class="level-desc">간단한 스키마, 기본 추론</p>
      </div>
      <div class="arrow-up">⬆️ 확장</div>
      <div class="level">
        <div class="tech-box">OWL</div>
        <p class="level-desc">복잡한 온톨로지, 고급 추론</p>
      </div>
    </div>

    <div class="compatibility">
      <p>💡 <strong>중요:</strong> OWL은 RDFS를 포함합니다! RDFS로 작성한 것은 모두 OWL에서도 유효합니다.</p>
    </div>
  </div>

  <div class="when-what">
    <h4>🎯 언제 무엇을 쓸까?</h4>
    <div class="choice-grid">
      <div class="choice-card rdfs-choice">
        <h5>RDFS를 쓰세요</h5>
        <ul>
          <li>✅ 간단한 어휘 정의</li>
          <li>✅ 빠른 성능 필요</li>
          <li>✅ 기본적인 분류만 필요</li>
          <li>✅ 초보자도 쉽게 사용</li>
          <li>✅ Dublin Core, FOAF 같은 어휘</li>
        </ul>
      </div>

      <div class="choice-card owl-choice">
        <h5>OWL을 쓰세요</h5>
        <ul>
          <li>✅ 복잡한 도메인 모델</li>
          <li>✅ 정교한 제약조건 필요</li>
          <li>✅ 고급 추론 필요</li>
          <li>✅ 의료, 생물정보학 등</li>
          <li>✅ 데이터 일관성 검증</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>6. RDFS를 RDF/XML로 표현하기</h2>

  <div class="format-intro">
    <p>RDFS도 RDF이므로 다양한 형식으로 표현할 수 있습니다. 먼저 RDF/XML부터 봅시다!</p>
  </div>

  <div class="code-example">
    <h4>📝 도서관 온톨로지 (RDF/XML)</h4>
    <pre class="code-block">
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:lib="http://library.org/vocab/"&gt;

  &lt;!-- 클래스 정의 --&gt;
  &lt;rdfs:Class rdf:about="http://library.org/vocab/Book"&gt;
    &lt;rdfs:label xml:lang="ko"&gt;책&lt;/rdfs:label&gt;
    &lt;rdfs:label xml:lang="en"&gt;Book&lt;/rdfs:label&gt;
    &lt;rdfs:comment&gt;인쇄된 도서 자료&lt;/rdfs:comment&gt;
    &lt;rdfs:subClassOf rdf:resource="http://library.org/vocab/Publication"/&gt;
  &lt;/rdfs:Class&gt;

  &lt;rdfs:Class rdf:about="http://library.org/vocab/Publication"&gt;
    &lt;rdfs:label xml:lang="ko"&gt;출판물&lt;/rdfs:label&gt;
    &lt;rdfs:comment&gt;출판된 모든 자료&lt;/rdfs:comment&gt;
  &lt;/rdfs:Class&gt;

  &lt;rdfs:Class rdf:about="http://library.org/vocab/Person"&gt;
    &lt;rdfs:label xml:lang="ko"&gt;사람&lt;/rdfs:label&gt;
  &lt;/rdfs:Class&gt;

  &lt;rdfs:Class rdf:about="http://library.org/vocab/Organization"&gt;
    &lt;rdfs:label xml:lang="ko"&gt;조직&lt;/rdfs:label&gt;
  &lt;/rdfs:Class&gt;

  &lt;!-- 속성 정의 --&gt;
  &lt;rdf:Property rdf:about="http://library.org/vocab/author"&gt;
    &lt;rdfs:label xml:lang="ko"&gt;저자&lt;/rdfs:label&gt;
    &lt;rdfs:label xml:lang="en"&gt;author&lt;/rdfs:label&gt;
    &lt;rdfs:comment&gt;책의 저자&lt;/rdfs:comment&gt;
    &lt;rdfs:domain rdf:resource="http://library.org/vocab/Book"/&gt;
    &lt;rdfs:range rdf:resource="http://library.org/vocab/Person"/&gt;
  &lt;/rdf:Property&gt;

  &lt;rdf:Property rdf:about="http://library.org/vocab/publisher"&gt;
    &lt;rdfs:label xml:lang="ko"&gt;출판사&lt;/rdfs:label&gt;
    &lt;rdfs:comment&gt;출판물의 발행자&lt;/rdfs:comment&gt;
    &lt;rdfs:domain rdf:resource="http://library.org/vocab/Publication"/&gt;
    &lt;rdfs:range rdf:resource="http://library.org/vocab/Organization"/&gt;
  &lt;/rdf:Property&gt;

  &lt;rdf:Property rdf:about="http://library.org/vocab/publicationDate"&gt;
    &lt;rdfs:label xml:lang="ko"&gt;출판일&lt;/rdfs:label&gt;
    &lt;rdfs:domain rdf:resource="http://library.org/vocab/Publication"/&gt;
    &lt;rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#date"/&gt;
  &lt;/rdf:Property&gt;

&lt;/rdf:RDF&gt;
    </pre>
  </div>

  <div class="usage-example">
    <h4>📚 이 스키마를 사용하는 데이터 (RDF/XML)</h4>
    <pre class="code-block">
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:lib="http://library.org/vocab/"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"&gt;

  &lt;!-- 해리포터 책 --&gt;
  &lt;lib:Book rdf:about="http://library.org/data/book/harry-potter-1"&gt;
    &lt;lib:title&gt;해리포터와 마법사의 돌&lt;/lib:title&gt;
    &lt;lib:author rdf:resource="http://library.org/data/person/jk-rowling"/&gt;
    &lt;lib:publisher rdf:resource="http://library.org/data/org/munhak"/&gt;
    &lt;lib:publicationDate&gt;1997-06-26&lt;/lib:publicationDate&gt;
  &lt;/lib:Book&gt;

  &lt;!-- J.K. 롤링 --&gt;
  &lt;lib:Person rdf:about="http://library.org/data/person/jk-rowling"&gt;
    &lt;foaf:name&gt;J.K. 롤링&lt;/foaf:name&gt;
  &lt;/lib:Person&gt;

  &lt;!-- 문학수첩 출판사 --&gt;
  &lt;lib:Organization rdf:about="http://library.org/data/org/munhak"&gt;
    &lt;foaf:name&gt;문학수첩&lt;/foaf:name&gt;
  &lt;/lib:Organization&gt;

&lt;/rdf:RDF&gt;
    </pre>
  </div>
</div>

<div class="content-section">
  <h2>7. RDFS를 Turtle로 표현하기</h2>

  <div class="format-intro">
    <p>Turtle은 RDF/XML보다 훨씬 읽기 쉬운 형식입니다!</p>
  </div>

  <div class="code-example">
    <h4>📝 도서관 온톨로지 (Turtle)</h4>
    <pre class="code-block">
@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .
@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .
@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .
@prefix lib: &lt;http://library.org/vocab/&gt; .

# ========================================
# 클래스 정의
# ========================================

lib:Publication a rdfs:Class ;
    rdfs:label "출판물"@ko, "Publication"@en ;
    rdfs:comment "출판된 모든 자료" .

lib:Book a rdfs:Class ;
    rdfs:label "책"@ko, "Book"@en ;
    rdfs:comment "인쇄된 도서 자료" ;
    rdfs:subClassOf lib:Publication .

lib:Magazine a rdfs:Class ;
    rdfs:label "잡지"@ko, "Magazine"@en ;
    rdfs:subClassOf lib:Publication .

lib:Article a rdfs:Class ;
    rdfs:label "논문"@ko, "Article"@en ;
    rdfs:subClassOf lib:Publication .

lib:Person a rdfs:Class ;
    rdfs:label "사람"@ko, "Person"@en .

lib:Organization a rdfs:Class ;
    rdfs:label "조직"@ko, "Organization"@en .

# ========================================
# 속성 정의
# ========================================

lib:author a rdf:Property ;
    rdfs:label "저자"@ko, "author"@en ;
    rdfs:comment "저작물의 창작자" ;
    rdfs:domain lib:Publication ;
    rdfs:range lib:Person .

lib:publisher a rdf:Property ;
    rdfs:label "출판사"@ko, "publisher"@en ;
    rdfs:domain lib:Publication ;
    rdfs:range lib:Organization .

lib:publicationDate a rdf:Property ;
    rdfs:label "출판일"@ko, "publication date"@en ;
    rdfs:domain lib:Publication ;
    rdfs:range xsd:date .

lib:title a rdf:Property ;
    rdfs:label "제목"@ko, "title"@en ;
    rdfs:domain lib:Publication ;
    rdfs:range xsd:string .

lib:isbn a rdf:Property ;
    rdfs:label "ISBN"@ko, "ISBN"@en ;
    rdfs:domain lib:Book ;
    rdfs:range xsd:string .

# 계층적 속성
lib:hasPart a rdf:Property ;
    rdfs:label "부분을 가짐"@ko ;
    rdfs:domain lib:Publication ;
    rdfs:range rdfs:Resource .

lib:hasChapter a rdf:Property ;
    rdfs:label "장을 가짐"@ko ;
    rdfs:subPropertyOf lib:hasPart ;
    rdfs:domain lib:Book .
    </pre>
  </div>

  <div class="usage-example">
    <h4>📚 이 스키마를 사용하는 데이터 (Turtle)</h4>
    <pre class="code-block">
@prefix lib: &lt;http://library.org/vocab/&gt; .
@prefix data: &lt;http://library.org/data/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .

# ========================================
# 책 데이터
# ========================================

data:book1 a lib:Book ;
    lib:title "해리포터와 마법사의 돌" ;
    lib:author data:person1 ;
    lib:publisher data:org1 ;
    lib:publicationDate "1997-06-26"^^xsd:date ;
    lib:isbn "978-89-01234-56-7" ;
    lib:hasChapter data:chapter1, data:chapter2 .

data:book2 a lib:Book ;
    lib:title "클린 코드" ;
    lib:author data:person2 ;
    lib:publicationDate "2013"^^xsd:date .

# ========================================
# 사람 데이터
# ========================================

data:person1 a lib:Person ;
    foaf:name "J.K. 롤링" ;
    foaf:givenName "Joanne" ;
    foaf:familyName "Rowling" .

data:person2 a lib:Person ;
    foaf:name "Robert C. Martin" .

# ========================================
# 조직 데이터
# ========================================

data:org1 a lib:Organization ;
    foaf:name "문학수첩" .

# ========================================
# 챕터 데이터
# ========================================

data:chapter1 a lib:Chapter ;
    lib:title "살아남은 소년" .
    </pre>
  </div>

  <div class="turtle-benefits">
    <h4>✅ Turtle의 장점</h4>
    <ul>
      <li>📖 <strong>읽기 쉬움:</strong> XML보다 훨씬 간결</li>
      <li>✍️ <strong>쓰기 쉬움:</strong> 수작업 편집 가능</li>
      <li>🎯 <strong>간결한 문법:</strong> <code>a</code>는 <code>rdf:type</code>의 축약</li>
      <li>🔗 <strong>접두사:</strong> URI를 짧게 표현</li>
      <li>🌐 <strong>다국어:</strong> <code>@ko</code>, <code>@en</code> 태그</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>8. RDFS를 JSON-LD로 표현하기</h2>

  <div class="format-intro">
    <p>JSON-LD는 JSON에 링크드 데이터 기능을 더한 형식입니다. 모던 웹 개발자들에게 친숙합니다!</p>
  </div>

  <div class="code-example">
    <h4>📝 도서관 온톨로지 (JSON-LD)</h4>
    <pre class="code-block">
{
  "@context": {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "lib": "http://library.org/vocab/"
  },
  "@graph": [
    {
      "@id": "lib:Publication",
      "@type": "rdfs:Class",
      "rdfs:label": [
        {"@value": "출판물", "@language": "ko"},
        {"@value": "Publication", "@language": "en"}
      ],
      "rdfs:comment": "출판된 모든 자료"
    },
    {
      "@id": "lib:Book",
      "@type": "rdfs:Class",
      "rdfs:label": [
        {"@value": "책", "@language": "ko"},
        {"@value": "Book", "@language": "en"}
      ],
      "rdfs:subClassOf": {"@id": "lib:Publication"}
    },
    {
      "@id": "lib:Magazine",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "잡지", "@language": "ko"},
      "rdfs:subClassOf": {"@id": "lib:Publication"}
    },
    {
      "@id": "lib:Person",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "사람", "@language": "ko"}
    },
    {
      "@id": "lib:Organization",
      "@type": "rdfs:Class",
      "rdfs:label": {"@value": "조직", "@language": "ko"}
    },
    {
      "@id": "lib:author",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "저자", "@language": "ko"},
      "rdfs:domain": {"@id": "lib:Publication"},
      "rdfs:range": {"@id": "lib:Person"}
    },
    {
      "@id": "lib:publisher",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "출판사", "@language": "ko"},
      "rdfs:domain": {"@id": "lib:Publication"},
      "rdfs:range": {"@id": "lib:Organization"}
    },
    {
      "@id": "lib:publicationDate",
      "@type": "rdf:Property",
      "rdfs:label": {"@value": "출판일", "@language": "ko"},
      "rdfs:domain": {"@id": "lib:Publication"},
      "rdfs:range": {"@id": "xsd:date"}
    }
  ]
}
    </pre>
  </div>

  <div class="usage-example">
    <h4>📚 이 스키마를 사용하는 데이터 (JSON-LD)</h4>
    <pre class="code-block">
{
  "@context": {
    "lib": "http://library.org/vocab/",
    "data": "http://library.org/data/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",

    "Book": "lib:Book",
    "Person": "lib:Person",
    "Organization": "lib:Organization",
    "title": "lib:title",
    "author": {"@id": "lib:author", "@type": "@id"},
    "publisher": {"@id": "lib:publisher", "@type": "@id"},
    "publicationDate": {"@id": "lib:publicationDate", "@type": "xsd:date"},
    "isbn": "lib:isbn",
    "name": "foaf:name"
  },
  "@graph": [
    {
      "@id": "data:book1",
      "@type": "Book",
      "title": "해리포터와 마법사의 돌",
      "author": {
        "@id": "data:person1",
        "@type": "Person",
        "name": "J.K. 롤링"
      },
      "publisher": {
        "@id": "data:org1",
        "@type": "Organization",
        "name": "문학수첩"
      },
      "publicationDate": "1997-06-26",
      "isbn": "978-89-01234-56-7"
    },
    {
      "@id": "data:book2",
      "@type": "Book",
      "title": "클린 코드",
      "author": {
        "@id": "data:person2",
        "@type": "Person",
        "name": "Robert C. Martin"
      },
      "publicationDate": "2013"
    }
  ]
}
    </pre>
  </div>

  <div class="jsonld-benefits">
    <h4>✅ JSON-LD의 장점</h4>
    <ul>
      <li>🌐 <strong>웹 친화적:</strong> REST API에 바로 사용</li>
      <li>💻 <strong>개발자 친화적:</strong> JavaScript로 바로 파싱</li>
      <li>🔗 <strong>링크드 데이터:</strong> RDF의 모든 기능 지원</li>
      <li>📱 <strong>모던 웹:</strong> React, Vue 등에서 쉽게 사용</li>
      <li>🔄 <strong>변환 용이:</strong> RDF/XML, Turtle과 상호 변환</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>9. 실제 사례: 도서관 시스템에 RDFS 적용하기</h2>

  <div class="real-world-scenario">
    <h4>🏛️ 시나리오: 대학 도서관 통합 검색 시스템</h4>
    <p>여러 도서관의 데이터를 통합하여 검색하는 시스템을 만든다고 가정해봅시다.</p>
  </div>

  <div class="implementation-steps">
    <div class="step-card">
      <div class="step-number">1</div>
      <h5>RDFS로 공통 온톨로지 정의</h5>
      <pre class="code-block">
@prefix lib: &lt;http://university.edu/library/vocab/&gt; .

# 자료 유형 계층
lib:Resource a rdfs:Class .
lib:PhysicalResource rdfs:subClassOf lib:Resource .
lib:DigitalResource rdfs:subClassOf lib:Resource .

lib:Book rdfs:subClassOf lib:PhysicalResource .
lib:EBook rdfs:subClassOf lib:DigitalResource .
lib:Journal rdfs:subClassOf lib:PhysicalResource .
lib:EJournal rdfs:subClassOf lib:DigitalResource .

# 공통 속성
lib:creator rdfs:domain lib:Resource ;
            rdfs:range foaf:Person .
lib:subject rdfs:domain lib:Resource .
lib:available rdfs:domain lib:Resource ;
              rdfs:range xsd:boolean .
      </pre>
    </div>

    <div class="step-card">
      <div class="step-number">2</div>
      <h5>각 도서관이 데이터 제공</h5>
      <pre class="code-block">
# 중앙도서관 데이터
&lt;http://central.lib/book123&gt; a lib:Book ;
    lib:title "해리포터" ;
    lib:creator &lt;http://central.lib/author/rowling&gt; ;
    lib:available true .

# 공대 도서관 데이터
&lt;http://eng.lib/ebook456&gt; a lib:EBook ;
    lib:title "Python Programming" ;
    lib:creator &lt;http://eng.lib/author/martin&gt; ;
    lib:available true .
      </pre>
    </div>

    <div class="step-card">
      <div class="step-number">3</div>
      <h5>RDFS 추론으로 통합 검색</h5>
      <div class="query-example">
        <h6>사용자 질의: "이용 가능한 모든 자료 찾기"</h6>
        <pre class="code-mini">
SELECT ?resource ?title
WHERE {
  ?resource a lib:Resource ;
            lib:available true ;
            lib:title ?title .
}
        </pre>
        <div class="query-result">
          <p><strong>결과:</strong></p>
          <ul>
            <li>✅ Book (추론: Book은 PhysicalResource, PhysicalResource는 Resource)</li>
            <li>✅ EBook (추론: EBook은 DigitalResource, DigitalResource는 Resource)</li>
            <li>✅ Journal, EJournal 등 모두 포함!</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="step-card">
      <div class="step-number">4</div>
      <h5>이점</h5>
      <ul>
        <li>✅ 각 도서관은 자기 방식대로 데이터 관리</li>
        <li>✅ RDFS 스키마만 공유하면 자동 통합</li>
        <li>✅ 새로운 자료 유형 추가 용이</li>
        <li>✅ 추론으로 지능적 검색</li>
      </ul>
    </div>
  </div>

  <div class="another-example">
    <h4>📖 또 다른 예: BIBFRAME</h4>
    <p>미국 의회도서관의 <strong>BIBFRAME</strong>도 RDFS로 정의된 온톨로지입니다!</p>

    <div class="bibframe-example">
      <pre class="code-block">
# BIBFRAME 클래스 정의 (일부)
bf:Work a rdfs:Class ;
    rdfs:label "Work" ;
    rdfs:comment "저작물의 개념적 본질" .

bf:Instance a rdfs:Class ;
    rdfs:label "Instance" ;
    rdfs:comment "저작물의 구체적 구현" .

bf:hasInstance a rdf:Property ;
    rdfs:domain bf:Work ;
    rdfs:range bf:Instance .

# 실제 사용
&lt;http://id.loc.gov/resources/works/12345&gt; a bf:Work ;
    bf:title "해리포터와 마법사의 돌" ;
    bf:hasInstance &lt;http://id.loc.gov/resources/instances/67890&gt; .

&lt;http://id.loc.gov/resources/instances/67890&gt; a bf:Instance ;
    bf:isbn "978-89-01234-56-7" .
      </pre>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>10. 요약: 한눈에 정리</h2>

  <div class="summary-grid">
    <div class="summary-main">
      <h3>📚 RDFS란?</h3>
      <p class="definition">
        RDF 데이터에 <strong>구조와 의미</strong>를 부여하는 어휘 정의 언어
      </p>

      <div class="key-features">
        <div class="feature">
          <strong>핵심 개념:</strong> 클래스, 속성, 상속
        </div>
        <div class="feature">
          <strong>주요 어휘:</strong> rdfs:Class, subClassOf, domain, range
        </div>
        <div class="feature">
          <strong>추론:</strong> 자동으로 지식 확장
        </div>
        <div class="feature">
          <strong>형식:</strong> RDF/XML, Turtle, JSON-LD
        </div>
      </div>
    </div>

    <div class="summary-comparison">
      <h4>계층 구조</h4>
      <div class="hierarchy-summary">
        <div class="hier-item">RDF</div>
        <div class="hier-arrow">⬆️</div>
        <div class="hier-item">RDFS</div>
        <div class="hier-arrow">⬆️</div>
        <div class="hier-item">OWL</div>
      </div>
      <p class="hier-desc">간단 → 복잡<br>빠름 → 강력</p>
    </div>
  </div>

  <div class="key-takeaways">
    <h4>🎯 핵심 포인트</h4>
    <div class="takeaway-grid">
      <div class="takeaway-box">
        <h5>1. RDFS = RDF의 스키마</h5>
        <p>RDF 데이터의 구조를 정의하지만, 그 자체도 RDF입니다</p>
      </div>

      <div class="takeaway-box">
        <h5>2. 클래스와 속성 정의</h5>
        <p>rdfs:Class로 분류를, rdf:Property로 관계를 정의합니다</p>
      </div>

      <div class="takeaway-box">
        <h5>3. 자동 추론 가능</h5>
        <p>subClassOf, domain, range 등으로 새로운 지식을 유추합니다</p>
      </div>

      <div class="takeaway-box">
        <h5>4. OWL의 기초</h5>
        <p>RDFS로 시작해서 필요시 OWL로 확장할 수 있습니다</p>
      </div>

      <div class="takeaway-box">
        <h5>5. 다양한 형식 지원</h5>
        <p>RDF/XML, Turtle, JSON-LD 모두 사용 가능합니다</p>
      </div>

      <div class="takeaway-box">
        <h5>6. 도서관에 필수</h5>
        <p>BIBFRAME, Dublin Core 등 도서관 표준의 기반입니다</p>
      </div>
    </div>
  </div>

  <div class="final-message">
    <h3>🌟 마치며</h3>
    <div class="message-box">
      <p class="big-text">
        <strong>RDFS로 데이터에 의미를 부여하세요!</strong>
      </p>
      <p>
        간단하면서도 강력한 RDFS는<br>
        링크드 데이터와 시맨틱 웹의 핵심입니다.<br>
        도서관 데이터를 더욱 지능적으로 만들 수 있습니다.
      </p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>11. 학습 점검 퀴즈</h2>

  <div class="quiz-section">
    <div class="quiz-item">
      <p><strong>Q1.</strong> RDFS와 RDF의 가장 큰 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>RDF는 데이터를 표현</strong>하고, <strong>RDFS는 데이터의 구조를 정의</strong>합니다. RDF는 개별 사실(인스턴스)을 기술하고, RDFS는 클래스와 속성의 의미를 정의합니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> rdfs:domain과 rdfs:range의 역할은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>rdfs:domain</strong>은 속성의 주체(주어)가 어떤 클래스인지 지정하고, <strong>rdfs:range</strong>는 속성의 값(목적어)이 어떤 클래스인지 지정합니다. 예: <code>:author rdfs:domain :Book ; rdfs:range :Person</code></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> RDFS로 추론이 가능한 이유는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ RDFS는 <strong>명확한 의미론</strong>을 가지고 있어서 컴퓨터가 이해할 수 있습니다. subClassOf는 전이적 관계이므로 "A는 B, B는 C → A는 C"와 같은 논리적 추론이 가능합니다. domain과 range도 자동으로 타입을 추론할 수 있게 합니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> RDFS와 OWL의 관계는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>OWL은 RDFS를 확장</strong>한 것입니다. RDFS는 기본적인 클래스와 속성 정의를 제공하고, OWL은 더 복잡한 제약조건과 논리를 추가합니다. RDFS로 작성한 것은 모두 OWL에서도 유효합니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> 다음 중 틀린 것은?</p>
      <pre class="code-mini">
:Book rdfs:subClassOf :Publication .
:HarryPotter a :Book .
      </pre>
      <p>위 정보로부터 추론할 수 있는 것은?</p>
      <ol type="a">
        <li>HarryPotter는 Publication이다</li>
        <li>Book은 Publication의 하위클래스다</li>
        <li>Publication은 Book의 상위클래스다</li>
        <li>Book은 Publication보다 더 일반적이다</li>
      </ol>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>d번이 틀렸습니다.</strong> subClassOf는 하위클래스가 상위클래스보다 <strong>더 구체적</strong>임을 의미합니다. Book은 Publication의 <strong>특수한 경우</strong>이므로 더 구체적입니다. a, b, c는 모두 맞습니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q6.</strong> JSON-LD에서 <code>"@type": "rdfs:Class"</code>의 의미는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ 이 자원이 <strong>클래스를 정의</strong>한다는 것을 나타냅니다. RDF/Turtle의 <code>a rdfs:Class</code>나 RDF/XML의 <code>&lt;rdfs:Class&gt;</code>와 같은 의미입니다.</p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 더 알아보기</h2>
  <ul>
    <li><strong>RDFS 스펙</strong> - W3C RDF Schema 1.1 공식 문서</li>
    <li><strong>Apache Jena</strong> - RDFS 추론을 지원하는 Java 프레임워크</li>
    <li><strong>RDFLib</strong> - Python RDF 라이브러리</li>
    <li><strong>Protégé</strong> - 온톨로지 편집 도구</li>
    <li><strong>BIBFRAME</strong> - 도서관 분야의 RDFS 온톨로지 예시</li>
    <li><strong>Schema.org</strong> - 웹을 위한 RDFS/OWL 어휘</li>
  </ul>
</div>

<style>
.content-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.hero-definition {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2.5rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
}

.hero-definition h3,
.hero-definition p {
  color: white;
}

.big-statement {
  font-size: 1.4rem;
  line-height: 1.8;
  margin: 1rem 0;
}

.simple-analogy {
  margin: 2rem 0;
}

.analogy-grid {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin: 2rem 0;
  flex-wrap: wrap;
  justify-content: center;
}

.analogy-box {
  flex: 1;
  min-width: 200px;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 3px solid #ddd;
  text-align: center;
}

.analogy-box.highlight {
  border-color: #4caf50;
  background: #e8f5e9;
}

.analogy-desc {
  color: #666;
  font-weight: bold;
  margin: 0.5rem 0;
}

.analogy-example {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.small {
  font-size: 0.85rem;
  color: #666;
  margin-top: 0.5rem;
}

.arrow {
  font-size: 2rem;
  font-weight: bold;
  color: #4caf50;
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
}

.core-concepts {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin: 2rem 0;
}

.concept-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  border: 3px solid #ddd;
}

.class-concept {
  border-color: #2196f3;
}

.property-concept {
  border-color: #4caf50;
}

.concept-icon {
  font-size: 3rem;
  text-align: center;
  margin-bottom: 1rem;
}

.concept-card h4 {
  color: #1976d2;
  margin: 0.5rem 0;
}

.concept-desc {
  color: #666;
  margin-bottom: 1.5rem;
}

.example-hierarchy {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.class-item {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  border: 2px solid #2196f3;
  margin: 0.5rem 0;
  text-align: center;
}

.class-item.top {
  border-color: #9c27b0;
  background: #f3e5f5;
}

.class-item.sub {
  display: inline-block;
  margin: 0.5rem;
}

.class-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.hierarchy-arrow {
  text-align: center;
  font-size: 1.5rem;
  color: #4caf50;
  margin: 0.5rem 0;
}

.property-examples {
  margin: 1rem 0;
}

.prop-item {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin: 0.75rem 0;
  border-left: 4px solid #4caf50;
}

.prop-item code {
  background: #263238;
  color: #aed581;
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  font-size: 0.8rem;
  display: block;
  margin-top: 0.5rem;
}

.code-example-mini {
  background: #263238;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.code-example-mini h6 {
  color: #aed581;
  margin-bottom: 0.75rem;
}

.code-tiny {
  color: #aed581;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  line-height: 1.5;
  white-space: pre;
}

.key-terms {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.terms-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;
}

.term-box {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  border: 2px solid #ff9800;
  text-align: center;
}

.term-box strong {
  color: #e65100;
  display: block;
  margin-bottom: 0.5rem;
}

.graph-relationship {
  background: #e8f5e9;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
  text-align: center;
}

.layer-example {
  margin: 2rem 0;
}

.layer-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 1.5rem 0;
}

.schema-layer {
  border: 3px solid #2196f3;
}

.data-layer {
  border: 3px solid #4caf50;
}

.layer-box h5 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.layer-desc {
  color: #666;
  margin-bottom: 1.5rem;
}

.connection-arrow {
  text-align: center;
  font-size: 1.5rem;
  color: #4caf50;
  font-weight: bold;
  margin: 1rem 0;
}

.code-block {
  background: #263238;
  color: #aed581;
  padding: 1.5rem;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  line-height: 1.6;
  margin: 1rem 0;
}

.graph-visualization {
  margin: 2rem 0;
}

.graph-container {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin: 2rem 0;
  justify-content: center;
}

.graph-part {
  flex: 1;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #ddd;
}

.schema-graph {
  border-color: #2196f3;
}

.data-graph {
  border-color: #4caf50;
}

.visual-graph {
  text-align: center;
}

.node {
  display: inline-block;
  padding: 0.5rem 1rem;
  margin: 0.25rem;
  border-radius: 4px;
  font-weight: bold;
}

.class-node {
  background: #e3f2fd;
  border: 2px solid #2196f3;
  color: #1976d2;
}

.prop-node {
  background: #e8f5e9;
  border: 2px solid #4caf50;
  color: #2e7d32;
}

.instance-node {
  background: #fff3e0;
  border: 2px solid #ff9800;
  color: #e65100;
}

.edge {
  display: inline-block;
  margin: 0 0.5rem;
  color: #666;
  font-size: 0.85rem;
}

.plus {
  font-size: 2rem;
  font-weight: bold;
  color: #4caf50;
}

.insight {
  background: #fff3e0;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 2rem;
  border-left: 4px solid #ff9800;
}

.inference-intro {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.inference-examples {
  margin: 2rem 0;
}

.inference-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
  border-left: 4px solid #4caf50;
}

.inference-card h5 {
  color: #2e7d32;
  margin-bottom: 1.5rem;
}

.inference-flow {
  margin: 1.5rem 0;
}

.given,
.reasoning,
.result {
  margin: 1.5rem 0;
}

.given h6,
.reasoning h6,
.result h6 {
  color: #1976d2;
  margin-bottom: 0.75rem;
}

.code-mini {
  background: #263238;
  color: #aed581;
  padding: 1rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  line-height: 1.5;
  overflow-x: auto;
  white-space: pre;
}

.reasoning ol {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 4px;
}

.reasoning li {
  margin: 0.75rem 0;
}

.why-inference {
  margin: 2rem 0;
}

.reason-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.reason-box {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #2196f3;
}

.reason-box h5 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.practical-benefit {
  background: #e8f5e9;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.benefit-scenario {
  margin-top: 1.5rem;
}

.without-inference,
.with-inference {
  background: white;
  padding: 1.5rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.without-inference {
  border-left: 4px solid #f44336;
}

.with-inference {
  border-left: 4px solid #4caf50;
}

.result-count {
  font-weight: bold;
  font-size: 1.1rem;
  margin-top: 0.5rem;
}

.insight-box {
  background: #fff3e0;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1.5rem;
  border-left: 4px solid #ff9800;
}

.rdfs-owl-comparison {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  background: white;
}

.rdfs-owl-comparison th,
.rdfs-owl-comparison td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.rdfs-owl-comparison th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.rdfs-owl-comparison tr:nth-child(even) {
  background: #f5f5f5;
}

.capability-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin: 2rem 0;
}

.capability-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  border: 2px solid #ddd;
}

.rdfs-can {
  border-color: #4caf50;
}

.owl-can {
  border-color: #ff9800;
}

.capability-note {
  margin-top: 1rem;
  font-weight: bold;
}

.relationship-diagram {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
  text-align: center;
}

.level {
  margin: 1rem 0;
}

.tech-box {
  display: inline-block;
  padding: 1rem 2rem;
  background: #e3f2fd;
  border: 3px solid #2196f3;
  border-radius: 8px;
  font-weight: bold;
  font-size: 1.2rem;
  color: #1976d2;
}

.level-desc {
  color: #666;
  margin-top: 0.5rem;
}

.arrow-up {
  font-size: 2rem;
  color: #4caf50;
  margin: 1rem 0;
}

.compatibility {
  background: #fff3e0;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 2rem;
}

.choice-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-top: 1.5rem;
}

.choice-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  border: 3px solid #ddd;
}

.rdfs-choice {
  border-color: #4caf50;
  background: #e8f5e9;
}

.owl-choice {
  border-color: #ff9800;
  background: #fff3e0;
}

.choice-card h5 {
  color: #1976d2;
  margin-bottom: 1.5rem;
}

.format-intro {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
  text-align: center;
}

.code-example {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
  border-left: 4px solid #4caf50;
}

.code-example h4 {
  color: #2e7d32;
  margin-bottom: 1rem;
}

.usage-example {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.usage-example h4 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.turtle-benefits,
.jsonld-benefits {
  background: #e8f5e9;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.real-world-scenario {
  background: #e3f2fd;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.implementation-steps {
  margin: 2rem 0;
}

.step-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
  position: relative;
  border-left: 4px solid #4caf50;
}

.step-number {
  position: absolute;
  top: -15px;
  left: 15px;
  width: 40px;
  height: 40px;
  background: #4caf50;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
}

.step-card h5 {
  color: #2e7d32;
  margin: 0 0 1.5rem 0;
}

.query-example {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.query-result {
  background: #e8f5e9;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.another-example {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.bibframe-example {
  margin-top: 1.5rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.summary-main {
  background: white;
  padding: 2rem;
  border: 3px solid #4caf50;
  border-radius: 8px;
}

.definition {
  font-size: 1.1rem;
  color: #333;
  margin: 1rem 0;
}

.key-features {
  display: grid;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.feature {
  background: #f5f5f5;
  padding: 0.75rem;
  border-radius: 4px;
}

.summary-comparison {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
}

.hierarchy-summary {
  text-align: center;
  margin-top: 1rem;
}

.hier-item {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: white;
  border: 2px solid #2196f3;
  border-radius: 4px;
  font-weight: bold;
  margin: 0.25rem;
}

.hier-arrow {
  font-size: 1.5rem;
  color: #4caf50;
  margin: 0.5rem 0;
}

.hier-desc {
  margin-top: 1rem;
  color: #666;
  font-size: 0.9rem;
}

.key-takeaways {
  margin: 2rem 0;
}

.takeaway-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.takeaway-box {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #4caf50;
}

.takeaway-box h5 {
  color: #2e7d32;
  margin-bottom: 1rem;
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

.message-box {
  background: rgba(255,255,255,0.2);
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.big-text {
  font-size: 1.5rem;
  margin: 1rem 0;
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

code {
  background: #263238;
  color: #aed581;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

@media (max-width: 1200px) {
  .terms-grid,
  .reason-grid,
  .takeaway-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .analogy-grid,
  .core-concepts,
  .terms-grid,
  .graph-container,
  .reason-grid,
  .capability-grid,
  .choice-grid,
  .summary-grid,
  .takeaway-grid {
    grid-template-columns: 1fr;
  }

  .class-group {
    flex-direction: column;
  }
}
</style>
        """,
        category=rdfs_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=47,
        prerequisites="RDF 기초 지식, XML과 JSON 기본 이해",
        learning_objectives="RDFS의 핵심 개념(클래스, 속성, 상속) 이해하기, RDFS 선언과 RDF 그래프의 관계 파악하기, RDFS 기반 추론의 원리와 실제 사례 이해하기, RDFS와 OWL의 차이점과 선택 기준 알기, RDF/XML, Turtle, JSON-LD로 RDFS 표현하고 사용하기, 도서관 시스템에서 RDFS를 활용하는 실무 능력 기르기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {rdfs_category.name} (상위: {ontology_category.name})")
    print(f"  - 난이도: 중급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=ontology")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_rdfs_content()
