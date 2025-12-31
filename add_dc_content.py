#!/usr/bin/env python
"""
Dublin Core 학습 콘텐츠 추가 스크립트
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

def create_dc_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 가져오기: 메타데이터
    metadata_category = Category.objects.get(slug='metadata')
    print("✓ 상위 카테고리 확인: 메타데이터")

    # 하위 카테고리 생성 또는 가져오기: Dublin Core
    dc_category, created = Category.objects.get_or_create(
        slug='dublin-core',
        defaults={
            'name': 'Dublin Core',
            'description': 'Dublin Core Metadata Element Set',
            'parent': metadata_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: Dublin Core")
    else:
        print("✓ 하위 카테고리 확인: Dublin Core")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': 'Dublin Core', 'slug': 'dublin-core'},
        {'name': 'DC', 'slug': 'dc'},
        {'name': '메타데이터', 'slug': 'metadata'},
        {'name': 'RDF', 'slug': 'rdf'},
        {'name': 'HTML', 'slug': 'html'},
        {'name': 'XML', 'slug': 'xml'},
        {'name': 'JSON', 'slug': 'json'},
        {'name': '상호운용성', 'slug': 'interoperability'}
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
        title="Dublin Core: 가장 단순하고 보편적인 메타데이터",
        slug="dublin-core-metadata",
        summary="15개 요소만으로 모든 자원을 기술하는 Dublin Core! HTML, XML, RDF, JSON 등 다양한 형식으로 어떻게 표현되는지 배워봅시다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>Dublin Core가 무엇인지, 왜 필요한지 이해하기</li>
    <li>Dublin Core의 15가지 핵심 요소 배우기</li>
    <li>DC를 HTML, XML, RDF, JSON 형식으로 표현하는 방법 알기</li>
    <li>실제 웹사이트와 도서관에서 DC가 어떻게 사용되는지 파악하기</li>
    <li>MARC, MODS와 DC의 차이점 이해하기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. Dublin Core를 한 문장으로</h2>

  <div class="hero-definition">
    <h3>🌍 Dublin Core란?</h3>
    <p class="big-statement">
      <strong>Dublin Core (DC)</strong>는<br>
      누구나 쉽게 사용할 수 있는<br>
      <strong>15개 요소로 이루어진 간단한 메타데이터 표준</strong>입니다.
    </p>
  </div>

  <div class="origin-story">
    <h4>📖 Dublin Core의 탄생</h4>
    <div class="timeline-box">
      <div class="timeline-item">
        <div class="year">1995년</div>
        <div class="place">📍 미국 오하이오주 더블린(Dublin)</div>
        <div class="event">
          <p><strong>OCLC/NCSA 메타데이터 워크샵</strong></p>
          <p class="problem">❌ <strong>문제:</strong> 웹이 폭발적으로 성장하는데<br>
          자원을 기술할 표준이 없었어요!</p>
        </div>
      </div>

      <div class="arrow-right">→</div>

      <div class="timeline-item">
        <div class="year">1995년</div>
        <div class="solution">
          <p>💡 <strong>해결책:</strong> 간단하고 보편적인 메타데이터 만들기!</p>
          <ul>
            <li>✅ 누구나 쉽게 사용</li>
            <li>✅ 모든 자원에 적용</li>
            <li>✅ 국제 표준</li>
          </ul>
        </div>
      </div>

      <div class="arrow-right">→</div>

      <div class="timeline-item">
        <div class="year">현재</div>
        <div class="result">
          <p>🌟 <strong>결과:</strong></p>
          <p>세계에서 가장 널리 사용되는<br>
          메타데이터 표준!</p>
        </div>
      </div>
    </div>

    <div class="name-origin">
      <h5>🏷️ 이름의 유래</h5>
      <p><strong>"Dublin"</strong>은 워크샵이 열린 도시 이름이고,<br>
      <strong>"Core"</strong>는 핵심(core) 요소만 담았다는 의미입니다.</p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>2. Dublin Core의 15가지 요소</h2>

  <div class="elements-intro">
    <p>Dublin Core는 <strong>딱 15개의 요소</strong>만 있으면 됩니다!<br>
    모든 요소는 <strong>선택사항(optional)</strong>이고, <strong>반복 가능(repeatable)</strong>합니다.</p>
  </div>

  <div class="elements-grid">
    <div class="element-card">
      <div class="element-number">1</div>
      <h4>Title (제목)</h4>
      <p class="element-desc">자원에 부여된 이름</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"해리포터와 마법사의 돌"</p>
        <p>"Mona Lisa"</p>
        <p>"Dublin Core 가이드"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">2</div>
      <h4>Creator (창작자)</h4>
      <p class="element-desc">자원 생성에 주로 책임이 있는 개체</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"J.K. 롤링"</p>
        <p>"Leonardo da Vinci"</p>
        <p>"김철수"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">3</div>
      <h4>Subject (주제)</h4>
      <p class="element-desc">자원의 주제나 키워드</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"판타지"</p>
        <p>"메타데이터"</p>
        <p>"웹 기술"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">4</div>
      <h4>Description (설명)</h4>
      <p class="element-desc">자원의 내용에 대한 설명</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"마법사 학교에 입학한 소년의 모험 이야기"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">5</div>
      <h4>Publisher (발행자)</h4>
      <p class="element-desc">자원을 이용 가능하게 만든 개체</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"문학수첩"</p>
        <p>"Oxford University Press"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">6</div>
      <h4>Contributor (기여자)</h4>
      <p class="element-desc">자원 생성에 기여한 개체</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"김영희 (번역)"</p>
        <p>"이철수 (편집)"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">7</div>
      <h4>Date (날짜)</h4>
      <p class="element-desc">자원의 생명주기와 관련된 날짜</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"1997-06-26"</p>
        <p>"2024"</p>
        <p>"2024-01-15"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">8</div>
      <h4>Type (유형)</h4>
      <p class="element-desc">자원의 성격이나 장르</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"Text"</p>
        <p>"Image"</p>
        <p>"Dataset"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">9</div>
      <h4>Format (형식)</h4>
      <p class="element-desc">자원의 물리적 또는 디지털 형태</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"application/pdf"</p>
        <p>"text/html"</p>
        <p>"image/jpeg"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">10</div>
      <h4>Identifier (식별자)</h4>
      <p class="element-desc">자원에 대한 명확한 참조</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"ISBN: 978-89-01234-56-7"</p>
        <p>"https://example.com/book1"</p>
        <p>"DOI: 10.1000/123456"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">11</div>
      <h4>Source (출처)</h4>
      <p class="element-desc">현재 자원이 유래된 관련 자원</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"원본: 대영박물관 소장품 No. 1234"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">12</div>
      <h4>Language (언어)</h4>
      <p class="element-desc">자원의 언어</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"ko" (한국어)</p>
        <p>"en" (영어)</p>
        <p>"fr" (프랑스어)</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">13</div>
      <h4>Relation (관계)</h4>
      <p class="element-desc">관련된 자원에 대한 참조</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"시리즈의 2권"</p>
        <p>"번역본: https://..."</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">14</div>
      <h4>Coverage (범위)</h4>
      <p class="element-desc">자원의 시공간적 범위</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"대한민국 서울"</p>
        <p>"1900-2000"</p>
        <p>"위도: 37.5, 경도: 127.0"</p>
      </div>
    </div>

    <div class="element-card">
      <div class="element-number">15</div>
      <h4>Rights (권리)</h4>
      <p class="element-desc">자원의 권리 관리 정보</p>
      <div class="element-example">
        <strong>예시:</strong>
        <p>"CC BY 4.0"</p>
        <p>"Copyright 2024 홍길동"</p>
        <p>"Public Domain"</p>
      </div>
    </div>
  </div>

  <div class="memory-tip">
    <h4>💡 외우기 쉽게 그룹화</h4>
    <div class="groups">
      <div class="group-box">
        <h5>🎨 콘텐츠 그룹</h5>
        <p>Title, Subject, Description, Type, Source, Relation, Coverage</p>
      </div>
      <div class="group-box">
        <h5>👥 지적 재산 그룹</h5>
        <p>Creator, Publisher, Contributor, Rights</p>
      </div>
      <div class="group-box">
        <h5>🔧 인스턴스 그룹</h5>
        <p>Date, Format, Identifier, Language</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>3. DC를 HTML로 표현하기</h2>

  <div class="html-intro">
    <p>웹페이지 <code>&lt;head&gt;</code> 안에 메타태그로 넣으면 검색엔진이 읽을 수 있어요!</p>
  </div>

  <div class="code-example">
    <h4>📝 HTML 메타태그 예시</h4>
    <pre class="code-block">
&lt;!DOCTYPE html&gt;
&lt;html lang="ko"&gt;
&lt;head&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;title&gt;해리포터와 마법사의 돌&lt;/title&gt;

  &lt;!-- Dublin Core 메타데이터 --&gt;
  &lt;meta name="DC.title" content="해리포터와 마법사의 돌"&gt;
  &lt;meta name="DC.creator" content="J.K. 롤링"&gt;
  &lt;meta name="DC.subject" content="판타지"&gt;
  &lt;meta name="DC.subject" content="마법"&gt;
  &lt;meta name="DC.subject" content="청소년"&gt;
  &lt;meta name="DC.description" content="마법사 학교에 입학한 소년 해리포터의 모험 이야기"&gt;
  &lt;meta name="DC.publisher" content="문학수첩"&gt;
  &lt;meta name="DC.contributor" content="김혜원 (번역)"&gt;
  &lt;meta name="DC.date" content="1997-06-26"&gt;
  &lt;meta name="DC.type" content="Text"&gt;
  &lt;meta name="DC.format" content="text/html"&gt;
  &lt;meta name="DC.identifier" content="ISBN:978-89-01234-56-7"&gt;
  &lt;meta name="DC.language" content="ko"&gt;
  &lt;meta name="DC.rights" content="Copyright 1997 J.K. Rowling"&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;h1&gt;해리포터와 마법사의 돌&lt;/h1&gt;
  &lt;!-- 본문 내용 --&gt;
&lt;/body&gt;
&lt;/html&gt;
    </pre>
  </div>

  <div class="html-benefits">
    <h4>✅ HTML에서 DC를 쓰는 이유</h4>
    <ul>
      <li>🔍 <strong>검색엔진 최적화 (SEO):</strong> 구글이 더 잘 이해</li>
      <li>📱 <strong>소셜 미디어 공유:</strong> 링크 공유 시 미리보기</li>
      <li>📚 <strong>디지털 아카이브:</strong> 자동 메타데이터 수집</li>
      <li>♿ <strong>접근성:</strong> 스크린 리더가 정보 파악</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>4. DC를 XML로 표현하기</h2>

  <div class="xml-intro">
    <p>구조화된 데이터 교환에 적합한 XML 형식입니다.</p>
  </div>

  <div class="code-example">
    <h4>📝 Simple DC (단순 DC XML)</h4>
    <pre class="code-block">
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;metadata
    xmlns="http://example.org/myapp/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"&gt;

  &lt;dc:title&gt;해리포터와 마법사의 돌&lt;/dc:title&gt;
  &lt;dc:creator&gt;J.K. 롤링&lt;/dc:creator&gt;
  &lt;dc:subject&gt;판타지&lt;/dc:subject&gt;
  &lt;dc:subject&gt;마법&lt;/dc:subject&gt;
  &lt;dc:subject&gt;청소년&lt;/dc:subject&gt;
  &lt;dc:description&gt;
    마법사 학교에 입학한 소년 해리포터의 모험 이야기
  &lt;/dc:description&gt;
  &lt;dc:publisher&gt;문학수첩&lt;/dc:publisher&gt;
  &lt;dc:contributor&gt;김혜원 (번역)&lt;/dc:contributor&gt;
  &lt;dc:date&gt;1997-06-26&lt;/dc:date&gt;
  &lt;dc:type&gt;Text&lt;/dc:type&gt;
  &lt;dc:format&gt;application/pdf&lt;/dc:format&gt;
  &lt;dc:identifier&gt;ISBN:978-89-01234-56-7&lt;/dc:identifier&gt;
  &lt;dc:language&gt;ko&lt;/dc:language&gt;
  &lt;dc:rights&gt;Copyright 1997 J.K. Rowling&lt;/dc:rights&gt;

&lt;/metadata&gt;
    </pre>
  </div>

  <div class="oai-example">
    <h4>🌐 OAI-PMH에서 사용되는 DC</h4>
    <p>도서관들이 메타데이터를 수확(harvesting)할 때 가장 많이 쓰는 형식!</p>
    <pre class="code-block">
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"&gt;
  &lt;GetRecord&gt;
    &lt;record&gt;
      &lt;metadata&gt;
        &lt;oai_dc:dc
            xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
            xmlns:dc="http://purl.org/dc/elements/1.1/"&gt;

          &lt;dc:title&gt;해리포터와 마법사의 돌&lt;/dc:title&gt;
          &lt;dc:creator&gt;J.K. 롤링&lt;/dc:creator&gt;
          &lt;dc:date&gt;1997&lt;/dc:date&gt;
          &lt;dc:identifier&gt;ISBN:978-89-01234-56-7&lt;/dc:identifier&gt;

        &lt;/oai_dc:dc&gt;
      &lt;/metadata&gt;
    &lt;/record&gt;
  &lt;/GetRecord&gt;
&lt;/OAI-PMH&gt;
    </pre>
  </div>
</div>

<div class="content-section">
  <h2>5. DC를 RDF로 표현하기</h2>

  <div class="rdf-intro">
    <p>시맨틱 웹과 링크드 데이터를 위한 RDF 형식!<br>
    DC는 RDF와 함께 쓰기에 완벽합니다.</p>
  </div>

  <div class="code-example">
    <h4>📝 RDF/XML 형식</h4>
    <pre class="code-block">
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:dc="http://purl.org/dc/elements/1.1/"&gt;

  &lt;rdf:Description rdf:about="http://example.org/books/harry-potter-1"&gt;
    &lt;dc:title&gt;해리포터와 마법사의 돌&lt;/dc:title&gt;
    &lt;dc:creator&gt;J.K. 롤링&lt;/dc:creator&gt;
    &lt;dc:subject&gt;판타지&lt;/dc:subject&gt;
    &lt;dc:subject&gt;마법&lt;/dc:subject&gt;
    &lt;dc:publisher&gt;문학수첩&lt;/dc:publisher&gt;
    &lt;dc:date&gt;1997-06-26&lt;/dc:date&gt;
    &lt;dc:type&gt;Text&lt;/dc:type&gt;
    &lt;dc:format&gt;application/pdf&lt;/dc:format&gt;
    &lt;dc:identifier&gt;ISBN:978-89-01234-56-7&lt;/dc:identifier&gt;
    &lt;dc:language&gt;ko&lt;/dc:language&gt;
  &lt;/rdf:Description&gt;

&lt;/rdf:RDF&gt;
    </pre>
  </div>

  <div class="code-example">
    <h4>📝 Turtle 형식 (더 읽기 쉬운 RDF)</h4>
    <pre class="code-block">
@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .
@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .

&lt;http://example.org/books/harry-potter-1&gt;
    dc:title "해리포터와 마법사의 돌" ;
    dc:creator "J.K. 롤링" ;
    dc:subject "판타지", "마법", "청소년" ;
    dc:publisher "문학수첩" ;
    dc:date "1997-06-26" ;
    dc:type "Text" ;
    dc:format "application/pdf" ;
    dc:identifier "ISBN:978-89-01234-56-7" ;
    dc:language "ko" .
    </pre>
  </div>

  <div class="rdf-benefits">
    <h4>🌟 RDF에서 DC를 쓰는 장점</h4>
    <ul>
      <li>🔗 <strong>링크드 데이터:</strong> 다른 자원과 연결 가능</li>
      <li>🤖 <strong>기계 처리:</strong> AI가 의미를 이해</li>
      <li>🌐 <strong>시맨틱 웹:</strong> 지식 그래프 구축</li>
      <li>🔄 <strong>상호운용성:</strong> 다양한 시스템과 호환</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>6. DC를 JSON으로 표현하기</h2>

  <div class="json-intro">
    <p>현대 웹 API에서 가장 많이 쓰는 JSON 형식!<br>
    간단하고 JavaScript와 완벽 호환됩니다.</p>
  </div>

  <div class="code-example">
    <h4>📝 단순 JSON</h4>
    <pre class="code-block">
{
  "title": "해리포터와 마법사의 돌",
  "creator": "J.K. 롤링",
  "subject": ["판타지", "마법", "청소년"],
  "description": "마법사 학교에 입학한 소년 해리포터의 모험 이야기",
  "publisher": "문학수첩",
  "contributor": ["김혜원 (번역)"],
  "date": "1997-06-26",
  "type": "Text",
  "format": "application/pdf",
  "identifier": "ISBN:978-89-01234-56-7",
  "language": "ko",
  "rights": "Copyright 1997 J.K. Rowling"
}
    </pre>
  </div>

  <div class="code-example">
    <h4>📝 JSON-LD (Linked Data)</h4>
    <p>JSON에 RDF의 링크드 데이터 기능을 더한 형식!</p>
    <pre class="code-block">
{
  "@context": {
    "dc": "http://purl.org/dc/elements/1.1/",
    "title": "dc:title",
    "creator": "dc:creator",
    "subject": "dc:subject",
    "date": "dc:date"
  },
  "@id": "http://example.org/books/harry-potter-1",
  "title": "해리포터와 마법사의 돌",
  "creator": "J.K. 롤링",
  "subject": ["판타지", "마법", "청소년"],
  "date": "1997-06-26",
  "dc:identifier": "ISBN:978-89-01234-56-7",
  "dc:language": "ko"
}
    </pre>
  </div>

  <div class="api-example">
    <h4>🌐 REST API 응답 예시</h4>
    <pre class="code-block">
{
  "status": "success",
  "data": {
    "id": 1234,
    "metadata": {
      "dc": {
        "title": "해리포터와 마법사의 돌",
        "creator": "J.K. 롤링",
        "date": "1997",
        "identifier": "ISBN:978-89-01234-56-7"
      }
    }
  }
}
    </pre>
  </div>
</div>

<div class="content-section">
  <h2>7. 형식 비교: HTML vs XML vs RDF vs JSON</h2>

  <table class="format-comparison">
    <thead>
      <tr>
        <th>특징</th>
        <th>HTML</th>
        <th>XML</th>
        <th>RDF</th>
        <th>JSON</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>주 용도</strong></td>
        <td>웹페이지 메타데이터</td>
        <td>데이터 교환</td>
        <td>시맨틱 웹</td>
        <td>웹 API</td>
      </tr>
      <tr>
        <td><strong>가독성</strong></td>
        <td>⭐⭐⭐⭐</td>
        <td>⭐⭐⭐</td>
        <td>⭐⭐</td>
        <td>⭐⭐⭐⭐⭐</td>
      </tr>
      <tr>
        <td><strong>기계 처리</strong></td>
        <td>⭐⭐⭐</td>
        <td>⭐⭐⭐⭐</td>
        <td>⭐⭐⭐⭐⭐</td>
        <td>⭐⭐⭐⭐⭐</td>
      </tr>
      <tr>
        <td><strong>링크드 데이터</strong></td>
        <td>❌</td>
        <td>❌</td>
        <td>✅</td>
        <td>✅ (JSON-LD)</td>
      </tr>
      <tr>
        <td><strong>파일 크기</strong></td>
        <td>작음</td>
        <td>중간</td>
        <td>큼</td>
        <td>작음</td>
      </tr>
      <tr>
        <td><strong>도구 지원</strong></td>
        <td>⭐⭐⭐⭐⭐</td>
        <td>⭐⭐⭐⭐</td>
        <td>⭐⭐⭐</td>
        <td>⭐⭐⭐⭐⭐</td>
      </tr>
      <tr>
        <td><strong>언제 쓸까?</strong></td>
        <td>웹사이트 SEO</td>
        <td>도서관 시스템</td>
        <td>지식 그래프</td>
        <td>모던 웹 앱</td>
      </tr>
    </tbody>
  </table>

  <div class="choose-format">
    <h4>🎯 어떤 형식을 선택할까?</h4>
    <div class="format-grid">
      <div class="format-card">
        <h5>HTML 메타태그</h5>
        <p class="use-when">다음과 같을 때:</p>
        <ul>
          <li>웹사이트 만들 때</li>
          <li>SEO 최적화 필요</li>
          <li>간단한 메타데이터</li>
        </ul>
      </div>

      <div class="format-card">
        <h5>XML</h5>
        <p class="use-when">다음과 같을 때:</p>
        <ul>
          <li>도서관 시스템 연동</li>
          <li>OAI-PMH 사용</li>
          <li>표준 데이터 교환</li>
        </ul>
      </div>

      <div class="format-card">
        <h5>RDF</h5>
        <p class="use-when">다음과 같을 때:</p>
        <ul>
          <li>링크드 데이터 구축</li>
          <li>시맨틱 웹 프로젝트</li>
          <li>복잡한 관계 표현</li>
        </ul>
      </div>

      <div class="format-card">
        <h5>JSON</h5>
        <p class="use-when">다음과 같을 때:</p>
        <ul>
          <li>REST API 개발</li>
          <li>모던 웹 앱</li>
          <li>JavaScript 사용</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>8. Dublin Core 실제 활용 사례</h2>

  <div class="use-cases">
    <div class="use-case-card">
      <div class="case-icon">🌐</div>
      <h4>1. 웹사이트 메타데이터</h4>
      <p class="case-desc">거의 모든 웹사이트가 DC를 사용합니다!</p>

      <div class="case-example">
        <h5>실제 사례: 위키피디아</h5>
        <pre class="code-mini">
&lt;meta name="DC.title" content="Dublin Core"&gt;
&lt;meta name="DC.subject" content="Metadata"&gt;
&lt;meta name="DC.publisher" content="Wikimedia Foundation"&gt;
&lt;meta name="DC.language" content="en"&gt;
        </pre>
        <p class="case-note">→ 검색엔진이 이 정보로 검색 결과 최적화</p>
      </div>
    </div>

    <div class="use-case-card">
      <div class="case-icon">📚</div>
      <h4>2. 디지털 도서관</h4>
      <p class="case-desc">OAI-PMH로 메타데이터 수확</p>

      <div class="case-example">
        <h5>실제 사례: 국립중앙도서관</h5>
        <p>디지털 컬렉션의 모든 자료에 DC 메타데이터 적용</p>
        <ul>
          <li>고문서 디지털화 → DC로 기술</li>
          <li>다른 도서관과 메타데이터 공유</li>
          <li>통합검색 시스템 구축</li>
        </ul>
      </div>
    </div>

    <div class="use-case-card">
      <div class="case-icon">🎓</div>
      <h4>3. 교육 자원 (Learning Objects)</h4>
      <p class="case-desc">온라인 강의와 교육 콘텐츠</p>

      <div class="case-example">
        <h5>실제 사례: K-MOOC</h5>
        <p>모든 강의에 DC 메타데이터</p>
        <pre class="code-mini">
{
  "dc:title": "Python 프로그래밍",
  "dc:creator": "홍길동 교수",
  "dc:subject": ["프로그래밍", "Python"],
  "dc:type": "Course",
  "dc:language": "ko"
}
        </pre>
      </div>
    </div>

    <div class="use-case-card">
      <div class="case-icon">🖼️</div>
      <h4>4. 디지털 아카이브</h4>
      <p class="case-desc">박물관, 미술관의 디지털 컬렉션</p>

      <div class="case-example">
        <h5>실제 사례: 국립현대미술관</h5>
        <p>작품 메타데이터를 DC로 표준화</p>
        <ul>
          <li>Title: 작품명</li>
          <li>Creator: 작가</li>
          <li>Date: 제작년도</li>
          <li>Type: Image</li>
          <li>Format: image/jpeg</li>
        </ul>
      </div>
    </div>

    <div class="use-case-card">
      <div class="case-icon">🔬</div>
      <h4>5. 연구 데이터</h4>
      <p class="case-desc">학술 논문과 연구 데이터셋</p>

      <div class="case-example">
        <h5>실제 사례: 학술 저장소</h5>
        <pre class="code-mini">
dc:title = "COVID-19 확산 데이터"
dc:creator = "김연구"
dc:date = "2024-01-15"
dc:type = "Dataset"
dc:format = "text/csv"
dc:identifier = "DOI:10.1234/data.2024.001"
        </pre>
      </div>
    </div>

    <div class="use-case-card">
      <div class="case-icon">🎵</div>
      <h4>6. 멀티미디어 자원</h4>
      <p class="case-desc">음악, 영상, 이미지 파일</p>

      <div class="case-example">
        <h5>실제 사례: 음원 플랫폼</h5>
        <p>MP3 파일 안의 ID3 태그도 DC 기반</p>
        <ul>
          <li>Title → 곡 제목</li>
          <li>Creator → 아티스트</li>
          <li>Date → 발매일</li>
          <li>Publisher → 레이블</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>9. DC vs MARC vs MODS: 무엇이 다를까?</h2>

  <table class="standard-comparison">
    <thead>
      <tr>
        <th>항목</th>
        <th>Dublin Core</th>
        <th>MARC21</th>
        <th>MODS</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>요소 수</strong></td>
        <td>15개 (핵심)</td>
        <td>수백 개</td>
        <td>20여 개</td>
      </tr>
      <tr>
        <td><strong>복잡도</strong></td>
        <td>⭐ 매우 간단</td>
        <td>⭐⭐⭐⭐⭐ 매우 복잡</td>
        <td>⭐⭐⭐ 보통</td>
      </tr>
      <tr>
        <td><strong>배우기</strong></td>
        <td>⭐⭐⭐⭐⭐ 쉬움</td>
        <td>⭐ 어려움</td>
        <td>⭐⭐⭐ 보통</td>
      </tr>
      <tr>
        <td><strong>범용성</strong></td>
        <td>✅ 모든 자원</td>
        <td>⚠️ 주로 도서</td>
        <td>✅ 모든 자원</td>
      </tr>
      <tr>
        <td><strong>세밀함</strong></td>
        <td>❌ 간단</td>
        <td>✅ 매우 세밀</td>
        <td>✅ 세밀</td>
      </tr>
      <tr>
        <td><strong>형식</strong></td>
        <td>HTML, XML, RDF, JSON</td>
        <td>MARC</td>
        <td>XML</td>
      </tr>
      <tr>
        <td><strong>주 사용처</strong></td>
        <td>웹, 일반 자원</td>
        <td>도서관 목록</td>
        <td>디지털 도서관</td>
      </tr>
      <tr>
        <td><strong>상호운용성</strong></td>
        <td>⭐⭐⭐⭐⭐ 최고</td>
        <td>⭐⭐ 낮음</td>
        <td>⭐⭐⭐⭐ 높음</td>
      </tr>
      <tr>
        <td><strong>탄생 시기</strong></td>
        <td>1995년</td>
        <td>1960년대</td>
        <td>2002년</td>
      </tr>
    </tbody>
  </table>

  <div class="mapping-example">
    <h4>🔄 MARC → DC 매핑 예시</h4>
    <p>MARC 레코드를 DC로 간단하게 변환할 수 있어요!</p>

    <table class="mapping-table">
      <thead>
        <tr>
          <th>MARC 필드</th>
          <th>Dublin Core</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>245 $a (본 제목)</td>
          <td>dc:title</td>
        </tr>
        <tr>
          <td>100 $a (개인저자)</td>
          <td>dc:creator</td>
        </tr>
        <tr>
          <td>260 $b (발행처)</td>
          <td>dc:publisher</td>
        </tr>
        <tr>
          <td>260 $c (발행년)</td>
          <td>dc:date</td>
        </tr>
        <tr>
          <td>020 $a (ISBN)</td>
          <td>dc:identifier</td>
        </tr>
        <tr>
          <td>041 $a (언어코드)</td>
          <td>dc:language</td>
        </tr>
        <tr>
          <td>650 $a (주제명)</td>
          <td>dc:subject</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="when-what">
    <h4>🎯 언제 무엇을 쓸까?</h4>
    <div class="recommendation-grid">
      <div class="rec-card dc-rec">
        <h5>Dublin Core를 쓰세요</h5>
        <ul>
          <li>✅ 간단한 메타데이터만 필요</li>
          <li>✅ 웹사이트, 블로그</li>
          <li>✅ 빠르게 시작하고 싶을 때</li>
          <li>✅ 다양한 형식 지원 필요</li>
          <li>✅ 비도서관 사람도 사용</li>
        </ul>
      </div>

      <div class="rec-card marc-rec">
        <h5>MARC21을 쓰세요</h5>
        <ul>
          <li>✅ 전통적인 도서관 목록</li>
          <li>✅ 매우 세밀한 기술 필요</li>
          <li>✅ 기존 MARC 시스템 연동</li>
          <li>✅ 전문 사서가 작업</li>
        </ul>
      </div>

      <div class="rec-card mods-rec">
        <h5>MODS를 쓰세요</h5>
        <ul>
          <li>✅ DC보다 세밀, MARC보다 간단</li>
          <li>✅ 디지털 아카이브</li>
          <li>✅ XML 기반 시스템</li>
          <li>✅ MARC 변환 가능성 유지</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>10. Dublin Core 작성 실습</h2>

  <div class="practice-intro">
    <p>직접 Dublin Core 메타데이터를 작성해봅시다!</p>
  </div>

  <div class="practice-exercise">
    <h4>✍️ 실습 1: 웹사이트를 위한 DC HTML 메타태그</h4>

    <div class="exercise-scenario">
      <p><strong>시나리오:</strong> 당신의 블로그 글에 DC 메타데이터 추가하기</p>
      <div class="scenario-info">
        <p><strong>글 정보:</strong></p>
        <ul>
          <li>제목: "JavaScript 완벽 가이드"</li>
          <li>작성자: 당신의 이름</li>
          <li>주제: JavaScript, 프로그래밍, 웹 개발</li>
          <li>작성일: 2024-01-15</li>
          <li>언어: 한국어</li>
        </ul>
      </div>
    </div>

    <div class="exercise-answer">
      <h5>정답 예시:</h5>
      <pre class="code-block">
&lt;!DOCTYPE html&gt;
&lt;html lang="ko"&gt;
&lt;head&gt;
  &lt;meta name="DC.title" content="JavaScript 완벽 가이드"&gt;
  &lt;meta name="DC.creator" content="김철수"&gt;
  &lt;meta name="DC.subject" content="JavaScript"&gt;
  &lt;meta name="DC.subject" content="프로그래밍"&gt;
  &lt;meta name="DC.subject" content="웹 개발"&gt;
  &lt;meta name="DC.date" content="2024-01-15"&gt;
  &lt;meta name="DC.type" content="Text"&gt;
  &lt;meta name="DC.format" content="text/html"&gt;
  &lt;meta name="DC.language" content="ko"&gt;
&lt;/head&gt;
      </pre>
    </div>
  </div>

  <div class="practice-exercise">
    <h4>✍️ 실습 2: 도서를 위한 DC JSON</h4>

    <div class="exercise-scenario">
      <p><strong>시나리오:</strong> 도서관 API 응답 데이터 만들기</p>
      <div class="scenario-info">
        <p><strong>책 정보:</strong></p>
        <ul>
          <li>제목: "클린 코드"</li>
          <li>저자: Robert C. Martin</li>
          <li>출판사: 인사이트</li>
          <li>출판일: 2013</li>
          <li>ISBN: 978-89-6626-066-6</li>
          <li>주제: 소프트웨어 공학, 프로그래밍</li>
        </ul>
      </div>
    </div>

    <div class="exercise-answer">
      <h5>정답 예시:</h5>
      <pre class="code-block">
{
  "dc": {
    "title": "클린 코드",
    "creator": "Robert C. Martin",
    "publisher": "인사이트",
    "date": "2013",
    "identifier": "ISBN:978-89-6626-066-6",
    "subject": ["소프트웨어 공학", "프로그래밍"],
    "type": "Text",
    "language": "ko"
  }
}
      </pre>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>11. 요약: 한눈에 정리</h2>

  <div class="summary-grid">
    <div class="summary-main">
      <h3>🌍 Dublin Core란?</h3>
      <p class="definition">
        15개 요소로 이루어진 <strong>간단하고 보편적인 메타데이터 표준</strong>
      </p>

      <div class="key-features">
        <div class="feature">
          <strong>특징:</strong> 간단, 유연, 범용적
        </div>
        <div class="feature">
          <strong>요소:</strong> 15개 (모두 선택, 모두 반복 가능)
        </div>
        <div class="feature">
          <strong>형식:</strong> HTML, XML, RDF, JSON
        </div>
        <div class="feature">
          <strong>용도:</strong> 웹, 도서관, 아카이브, API
        </div>
      </div>
    </div>

    <div class="summary-15">
      <h4>15개 요소</h4>
      <div class="elements-list">
        <div class="element-group">
          <strong>콘텐츠</strong>
          <p>Title, Subject, Description, Type, Source, Relation, Coverage</p>
        </div>
        <div class="element-group">
          <strong>지적재산</strong>
          <p>Creator, Publisher, Contributor, Rights</p>
        </div>
        <div class="element-group">
          <strong>인스턴스</strong>
          <p>Date, Format, Identifier, Language</p>
        </div>
      </div>
    </div>
  </div>

  <div class="final-message">
    <h3>🎯 핵심 메시지</h3>
    <div class="message-box">
      <p class="big-text">
        <strong>Dublin Core = 메타데이터의 "만국 공통어"</strong>
      </p>
      <p>
        복잡한 MARC보다 간단하고,<br>
        HTML, XML, RDF, JSON 어디서나 사용 가능하며,<br>
        전 세계가 함께 쓰는 <strong>보편적 표준</strong>입니다.
      </p>
      <p class="action">
        💡 지금 당장 웹사이트에 DC 메타태그를 추가해보세요!
      </p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>12. 학습 점검 퀴즈</h2>

  <div class="quiz-section">
    <div class="quiz-item">
      <p><strong>Q1.</strong> Dublin Core는 몇 개의 핵심 요소로 이루어져 있나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>15개</strong>입니다. 모든 요소는 선택사항(optional)이고 반복 가능(repeatable)합니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> Dublin Core에서 "저자"를 나타내는 요소는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>Creator (창작자)</strong>입니다. 자원 생성에 주로 책임이 있는 개체를 나타냅니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> HTML에서 DC 메타데이터를 어디에 넣나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <code>&lt;head&gt;</code> 태그 안에 <code>&lt;meta name="DC.요소명" content="값"&gt;</code> 형태로 넣습니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> DC를 JSON으로 표현할 때 배열을 사용할 수 있나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>예</strong>, 가능합니다! DC 요소는 반복 가능하므로 subject처럼 여러 값이 필요한 경우 배열로 표현합니다.<br>
        예: <code>"subject": ["판타지", "마법", "청소년"]</code></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> MARC21과 Dublin Core의 가장 큰 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>복잡도</strong>입니다. MARC21은 수백 개의 필드로 매우 세밀하지만 복잡하고, Dublin Core는 15개 요소로 간단하지만 범용적입니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q6.</strong> RDF에서 DC를 사용하는 이유는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>링크드 데이터</strong>와 <strong>시맨틱 웹</strong>을 구현하기 위해서입니다. RDF는 데이터 간 관계를 표현하고, DC는 자원을 기술하는 표준 어휘를 제공합니다.</p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 더 알아보기</h2>
  <ul>
    <li><strong>Dublin Core 공식 사이트</strong> - dublincore.org</li>
    <li><strong>DCMI (Dublin Core Metadata Initiative)</strong> - 표준 관리 기구</li>
    <li><strong>DC Terms</strong> - 확장된 Dublin Core 용어집</li>
    <li><strong>OAI-PMH</strong> - DC를 사용한 메타데이터 수확 프로토콜</li>
    <li><strong>JSON-LD Playground</strong> - JSON-LD 테스트 도구</li>
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

.origin-story {
  margin: 2rem 0;
}

.timeline-box {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 1.5rem 0;
  flex-wrap: wrap;
  justify-content: center;
}

.timeline-item {
  flex: 1;
  min-width: 200px;
  padding: 1.5rem;
  background: #f5f5f5;
  border-radius: 8px;
  text-align: center;
}

.year {
  font-weight: bold;
  color: #1976d2;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.place {
  color: #666;
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

.event,
.solution,
.result {
  margin-top: 1rem;
}

.problem {
  color: #d32f2f;
  font-weight: bold;
  margin: 0.5rem 0;
}

.arrow-right {
  font-size: 2rem;
  color: #4caf50;
  font-weight: bold;
}

.name-origin {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1.5rem;
}

.name-origin h5 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.elements-intro {
  background: #e8f5e9;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  font-size: 1.1rem;
  margin: 2rem 0;
}

.elements-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

.element-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #ddd;
  position: relative;
}

.element-number {
  position: absolute;
  top: -12px;
  left: 12px;
  width: 32px;
  height: 32px;
  background: #1976d2;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
}

.element-card h4 {
  color: #1976d2;
  margin: 0.5rem 0;
}

.element-desc {
  color: #666;
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

.element-example {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-size: 0.85rem;
}

.element-example strong {
  color: #1976d2;
}

.memory-tip {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.memory-tip h4 {
  color: #e65100;
  margin-bottom: 1.5rem;
}

.groups {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.group-box {
  background: white;
  padding: 1.5rem;
  border-radius: 4px;
  border-left: 4px solid #ff9800;
}

.group-box h5 {
  color: #e65100;
  margin-bottom: 0.75rem;
}

.html-intro,
.xml-intro,
.rdf-intro,
.json-intro {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
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

.code-mini {
  background: #263238;
  color: #aed581;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  line-height: 1.5;
  margin: 0.5rem 0;
}

.html-benefits,
.rdf-benefits {
  background: #e8f5e9;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.html-benefits h4,
.rdf-benefits h4 {
  color: #2e7d32;
  margin-bottom: 1rem;
}

.oai-example,
.api-example {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.oai-example h4,
.api-example h4 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.format-comparison,
.standard-comparison,
.mapping-table {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  background: white;
}

.format-comparison th,
.format-comparison td,
.standard-comparison th,
.standard-comparison td,
.mapping-table th,
.mapping-table td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.format-comparison th,
.standard-comparison th,
.mapping-table th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.format-comparison tr:nth-child(even),
.standard-comparison tr:nth-child(even) {
  background: #f5f5f5;
}

.choose-format,
.when-what {
  margin: 2rem 0;
}

.format-grid,
.recommendation-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.format-card,
.rec-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #ddd;
}

.format-card h5,
.rec-card h5 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.use-when {
  font-weight: bold;
  color: #666;
  margin: 0.5rem 0;
}

.dc-rec {
  border-color: #4caf50;
  background: #e8f5e9;
}

.marc-rec {
  border-color: #2196f3;
  background: #e3f2fd;
}

.mods-rec {
  border-color: #ff9800;
  background: #fff3e0;
}

.use-cases {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin: 2rem 0;
}

.use-case-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  border: 2px solid #ddd;
}

.case-icon {
  font-size: 3rem;
  text-align: center;
  margin-bottom: 1rem;
}

.use-case-card h4 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.case-desc {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.case-example {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.case-example h5 {
  color: #2e7d32;
  margin-bottom: 1rem;
}

.case-note {
  color: #666;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  font-style: italic;
}

.mapping-example {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.mapping-example h4 {
  color: #e65100;
  margin-bottom: 1.5rem;
}

.practice-intro {
  background: #e8f5e9;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  font-size: 1.1rem;
  margin: 2rem 0;
}

.practice-exercise {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
  border-left: 4px solid #4caf50;
}

.practice-exercise h4 {
  color: #2e7d32;
  margin-bottom: 1.5rem;
}

.exercise-scenario {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 4px;
  margin: 1.5rem 0;
}

.scenario-info {
  margin-top: 1rem;
}

.exercise-answer {
  margin-top: 1.5rem;
}

.exercise-answer h5 {
  color: #1976d2;
  margin-bottom: 1rem;
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

.summary-15 {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
}

.elements-list {
  margin-top: 1rem;
}

.element-group {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  margin: 0.75rem 0;
}

.element-group strong {
  color: #1976d2;
  display: block;
  margin-bottom: 0.5rem;
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

.action {
  font-size: 1.1rem;
  margin-top: 1rem;
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
  .elements-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .format-grid,
  .recommendation-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .timeline-box,
  .groups,
  .elements-grid,
  .format-grid,
  .recommendation-grid,
  .use-cases,
  .summary-grid {
    grid-template-columns: 1fr;
  }

  .arrow-right {
    transform: rotate(90deg);
  }
}
</style>
        """,
        category=dc_category,
        author=admin,
        difficulty='BASIC',
        estimated_time=30,
        prerequisites="HTML과 XML 기초 지식",
        learning_objectives="Dublin Core의 15가지 요소 이해하기, DC를 HTML, XML, RDF, JSON 형식으로 표현하는 방법 배우기, 실제 웹사이트와 도서관에서 DC 활용 사례 파악하기, MARC, MODS와의 차이점 명확히 알기, 직접 Dublin Core 메타데이터 작성할 수 있기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {dc_category.name} (상위: {metadata_category.name})")
    print(f"  - 난이도: 초급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=metadata")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_dc_content()
