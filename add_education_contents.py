"""
교육 웹페이지 콘텐츠 등록 스크립트
HTML, XML, OAI-PMH 교육 콘텐츠를 백엔드에 등록합니다.
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
    print("❌ Admin user not found. Please create a superuser first.")
    exit(1)

print(f"✓ Admin user: {admin.username}")

# 상위 카테고리 생성
print("\n📁 Creating parent categories...")
parent_categories_data = [
    {"name": "웹페이지", "slug": "web-docs", "description": "웹 마크업 언어 학습", "order": 1},
    {"name": "검색프로토콜", "slug": "search-protocol", "description": "메타데이터 검색 프로토콜", "order": 2},
]

parent_categories = {}
for cat_data in parent_categories_data:
    category, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={
            'name': cat_data['name'],
            'description': cat_data['description'],
            'order': cat_data['order'],
            'parent': None,
        }
    )
    parent_categories[cat_data['name']] = category
    print(f"  {'✓ Created' if created else '○ Exists'} category: {category.name}")

# 하위 카테고리 생성
print("\n📁 Creating sub-categories...")
sub_categories_data = [
    {
        "name": "HTML",
        "slug": "html",
        "description": "HyperText Markup Language - 웹 페이지 구조",
        "parent": "웹페이지",
        "order": 1
    },
    {
        "name": "XML",
        "slug": "xml",
        "description": "eXtensible Markup Language - 데이터 저장 및 전송",
        "parent": "웹페이지",
        "order": 2
    },
    {
        "name": "OAI-PMH",
        "slug": "oai-pmh",
        "description": "메타데이터 하베스팅 프로토콜",
        "parent": "검색프로토콜",
        "order": 1
    },
]

sub_categories = {}
for cat_data in sub_categories_data:
    parent = parent_categories.get(cat_data['parent'])
    category, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={
            'name': cat_data['name'],
            'description': cat_data['description'],
            'parent': parent,
            'order': cat_data['order'],
        }
    )
    sub_categories[cat_data['name']] = category
    print(f"  {'✓ Created' if created else '○ Exists'} sub-category: {category.name} (under {parent.name})")

# 태그 생성
print("\n🏷️  Creating tags...")
tags_data = ["HTML", "XML", "마크업", "OAI-PMH", "메타데이터", "프로토콜", "웹표준"]

tags = {}
for tag_name in tags_data:
    tag, created = Tag.objects.get_or_create(
        slug=slugify(tag_name),
        defaults={'name': tag_name}
    )
    tags[tag_name] = tag
    print(f"  {'✓ Created' if created else '○ Exists'} tag: {tag.name}")

# 교육 콘텐츠 생성
print("\n📝 Creating education contents...")

contents_data = [
    {
        "title": "HTML 기초 학습",
        "summary": "HTML 태그를 직접 작성하고 결과를 확인하면서 웹 페이지의 기본 구조를 학습합니다.",
        "category": "HTML",
        "tags": ["HTML", "마크업", "웹표준"],
        "difficulty": "BEGINNER",
        "estimated_time": 45,
        "prerequisites": "없음",
        "learning_objectives": "HTML의 기본 구조와 주요 태그를 이해하고 간단한 웹 페이지를 작성할 수 있습니다.",
        "content": """
<h2>HTML이란?</h2>
<p><strong>HTML (HyperText Markup Language)</strong>은 웹 페이지를 만들기 위한 마크업 언어입니다.
웹 브라우저가 이해할 수 있는 형식으로 문서의 구조와 내용을 정의합니다.</p>

<h2>HTML 문서의 기본 구조</h2>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="ko"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;페이지 제목&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;안녕하세요!&lt;/h1&gt;
    &lt;p&gt;이것은 HTML 문서입니다.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>

<h2>주요 HTML 태그</h2>

<h3>문서 구조 태그</h3>
<ul>
    <li><code>&lt;!DOCTYPE html&gt;</code> - HTML5 문서 선언</li>
    <li><code>&lt;html&gt;</code> - HTML 문서의 루트 요소</li>
    <li><code>&lt;head&gt;</code> - 메타데이터 영역 (제목, 스타일, 스크립트 등)</li>
    <li><code>&lt;body&gt;</code> - 실제 표시되는 본문 내용</li>
</ul>

<h3>텍스트 관련 태그</h3>
<ul>
    <li><code>&lt;h1&gt; ~ &lt;h6&gt;</code> - 제목 (h1이 가장 큰 제목)</li>
    <li><code>&lt;p&gt;</code> - 단락 (paragraph)</li>
    <li><code>&lt;strong&gt;</code> - 굵은 글씨 (중요한 내용)</li>
    <li><code>&lt;em&gt;</code> - 기울임 글씨 (강조)</li>
    <li><code>&lt;br&gt;</code> - 줄 바꿈</li>
</ul>

<h3>목록 태그</h3>
<ul>
    <li><code>&lt;ul&gt;</code> - 순서 없는 목록 (Unordered List)</li>
    <li><code>&lt;ol&gt;</code> - 순서 있는 목록 (Ordered List)</li>
    <li><code>&lt;li&gt;</code> - 목록 항목 (List Item)</li>
</ul>

<h3>링크와 이미지</h3>
<ul>
    <li><code>&lt;a href="URL"&gt;</code> - 하이퍼링크</li>
    <li><code>&lt;img src="URL" alt="설명"&gt;</code> - 이미지</li>
</ul>

<h3>테이블 태그</h3>
<ul>
    <li><code>&lt;table&gt;</code> - 표</li>
    <li><code>&lt;tr&gt;</code> - 테이블 행 (Table Row)</li>
    <li><code>&lt;th&gt;</code> - 테이블 헤더 셀</li>
    <li><code>&lt;td&gt;</code> - 테이블 데이터 셀</li>
</ul>

<h2>실습 예제</h2>

<h3>1. 기본 웹 페이지</h3>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="ko"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;내 첫 웹페이지&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;환영합니다!&lt;/h1&gt;
    &lt;p&gt;이것은 내가 만든 첫 번째 웹 페이지입니다.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>

<h3>2. 목록이 있는 페이지</h3>
<pre><code>&lt;h2&gt;좋아하는 과일&lt;/h2&gt;
&lt;ul&gt;
    &lt;li&gt;사과&lt;/li&gt;
    &lt;li&gt;바나나&lt;/li&gt;
    &lt;li&gt;오렌지&lt;/li&gt;
&lt;/ul&gt;</code></pre>

<h3>3. 링크와 이미지</h3>
<pre><code>&lt;a href="https://www.w3schools.com/html/" target="_blank"&gt;
    HTML 튜토리얼 바로가기
&lt;/a&gt;

&lt;img src="https://via.placeholder.com/300x200"
     alt="예제 이미지"&gt;</code></pre>

<h2>학습 팁</h2>
<ul>
    <li>✓ 모든 태그는 열고 닫아야 합니다 (예: <code>&lt;p&gt;내용&lt;/p&gt;</code>)</li>
    <li>✓ 들여쓰기를 사용하여 코드를 읽기 쉽게 작성하세요</li>
    <li>✓ 브라우저의 개발자 도구를 활용하여 HTML 구조를 확인하세요</li>
    <li>✓ 직접 작성하고 결과를 확인하며 학습하세요</li>
</ul>

<h2>다음 단계</h2>
<p>HTML을 학습한 후에는 CSS로 스타일링을 배우고, JavaScript로 동적인 기능을 추가해보세요!</p>
"""
    },
    {
        "title": "XML 기초 학습",
        "summary": "XML의 기본 문법과 구조를 학습하고, HTML과의 차이점을 이해합니다.",
        "category": "XML",
        "tags": ["XML", "마크업"],
        "difficulty": "BEGINNER",
        "estimated_time": 45,
        "prerequisites": "HTML 기본 지식 권장",
        "learning_objectives": "XML의 기본 규칙과 구조를 이해하고, 간단한 XML 문서를 작성할 수 있습니다.",
        "content": """
<h2>XML이란?</h2>
<p><strong>XML (eXtensible Markup Language)</strong>은 데이터를 저장하고 전송하기 위한 마크업 언어입니다.
HTML과 달리 사용자가 직접 태그를 정의할 수 있으며, 데이터의 구조화와 교환에 주로 사용됩니다.</p>

<h2>HTML vs XML - 주요 차이점</h2>

<h3>HTML</h3>
<ul>
    <li>✓ 웹 페이지를 <strong>표시</strong>하기 위한 언어</li>
    <li>✓ 미리 정의된 태그만 사용 (h1, p, div 등)</li>
    <li>✓ 태그를 닫지 않아도 되는 경우 있음</li>
    <li>✓ 대소문자 구분 안 함</li>
    <li>✓ 주 목적: 데이터 표시 및 스타일링</li>
</ul>

<h3>XML</h3>
<ul>
    <li>✓ 데이터를 <strong>저장하고 전송</strong>하기 위한 언어</li>
    <li>✓ 사용자가 태그를 자유롭게 정의 가능</li>
    <li>✓ 모든 태그를 반드시 닫아야 함</li>
    <li>✓ 대소문자 엄격하게 구분</li>
    <li>✓ 주 목적: 데이터 구조화 및 교환</li>
</ul>

<h2>XML 작성 규칙</h2>

<h3>1. XML 선언</h3>
<p>문서 시작에 XML 버전과 인코딩을 선언합니다.</p>
<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;</code></pre>

<h3>2. 루트 요소</h3>
<p>반드시 하나의 루트 요소만 존재해야 합니다.</p>
<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;root&gt;
    &lt;!-- 모든 내용이 루트 요소 안에 --&gt;
&lt;/root&gt;</code></pre>

<h3>3. 닫는 태그 필수</h3>
<p>모든 태그는 반드시 닫아야 합니다.</p>
<pre><code>&lt;title&gt;제목&lt;/title&gt;
&lt;image src="img.jpg"/&gt;  &lt;!-- 자체 닫는 태그 --&gt;</code></pre>

<h3>4. 대소문자 구분</h3>
<p><code>&lt;Name&gt;</code>과 <code>&lt;name&gt;</code>은 다른 태그입니다.</p>

<h3>5. 속성값 따옴표</h3>
<p>속성값은 반드시 따옴표로 감싸야 합니다.</p>
<pre><code>&lt;person age="25" gender="male"&gt;홍길동&lt;/person&gt;</code></pre>

<h2>XML 문서 구조</h2>

<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;!-- 주석: 이것은 루트 요소입니다 --&gt;
&lt;bookstore&gt;
    &lt;book category="web"&gt;
        &lt;title lang="ko"&gt;XML 기초 학습&lt;/title&gt;
        &lt;author&gt;홍길동&lt;/author&gt;
        &lt;year&gt;2024&lt;/year&gt;
        &lt;price&gt;25000&lt;/price&gt;
    &lt;/book&gt;
    &lt;book category="programming"&gt;
        &lt;title lang="en"&gt;Learning Python&lt;/title&gt;
        &lt;author&gt;김철수&lt;/author&gt;
        &lt;year&gt;2023&lt;/year&gt;
        &lt;price&gt;30000&lt;/price&gt;
    &lt;/book&gt;
&lt;/bookstore&gt;</code></pre>

<h2>특수 문자 처리</h2>
<p>XML에서 특별한 의미를 가진 문자들은 엔티티로 표현해야 합니다.</p>

<table style="width:100%; border-collapse:collapse; border:1px solid #ddd;">
<thead style="background:#f5f5f5;">
    <tr>
        <th style="border:1px solid #ddd; padding:8px;">문자</th>
        <th style="border:1px solid #ddd; padding:8px;">엔티티</th>
        <th style="border:1px solid #ddd; padding:8px;">설명</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td style="border:1px solid #ddd; padding:8px;">&lt;</td>
        <td style="border:1px solid #ddd; padding:8px;">&amp;lt;</td>
        <td style="border:1px solid #ddd; padding:8px;">Less than</td>
    </tr>
    <tr>
        <td style="border:1px solid #ddd; padding:8px;">&gt;</td>
        <td style="border:1px solid #ddd; padding:8px;">&amp;gt;</td>
        <td style="border:1px solid #ddd; padding:8px;">Greater than</td>
    </tr>
    <tr>
        <td style="border:1px solid #ddd; padding:8px;">&amp;</td>
        <td style="border:1px solid #ddd; padding:8px;">&amp;amp;</td>
        <td style="border:1px solid #ddd; padding:8px;">Ampersand</td>
    </tr>
    <tr>
        <td style="border:1px solid #ddd; padding:8px;">"</td>
        <td style="border:1px solid #ddd; padding:8px;">&amp;quot;</td>
        <td style="border:1px solid #ddd; padding:8px;">Quote</td>
    </tr>
</tbody>
</table>

<h3>CDATA 섹션</h3>
<p>특수 문자가 많을 때는 CDATA 섹션을 사용합니다.</p>
<pre><code>&lt;code&gt;
    &lt;![CDATA[
    if (x < 10 && y > 5) {
        console.log("Hello!");
    }
    ]]&gt;
&lt;/code&gt;</code></pre>

<h2>XML 활용 분야</h2>

<h3>1. 웹 서비스</h3>
<ul>
    <li>SOAP 프로토콜</li>
    <li>RSS 피드</li>
    <li>Sitemap</li>
</ul>

<h3>2. 설정 파일</h3>
<ul>
    <li>Android 레이아웃</li>
    <li>Maven pom.xml</li>
    <li>Spring 설정</li>
</ul>

<h3>3. 문서 포맷</h3>
<ul>
    <li>Microsoft Office (docx, xlsx)</li>
    <li>SVG 이미지</li>
    <li>ePub 전자책</li>
</ul>

<h3>4. 데이터 교환</h3>
<ul>
    <li>B2B 데이터 교환</li>
    <li>금융 거래 (FpML)</li>
    <li>의료 정보 (HL7)</li>
</ul>

<h2>학습 팁</h2>
<ul>
    <li>✓ XML은 데이터의 의미를 태그 이름으로 표현합니다</li>
    <li>✓ 들여쓰기를 사용하여 계층 구조를 명확히 하세요</li>
    <li>✓ 속성보다는 요소로 데이터를 표현하는 것이 권장됩니다</li>
    <li>✓ XML 검증 도구를 사용하여 문법 오류를 확인하세요</li>
</ul>
"""
    },
    {
        "title": "OAI-PMH 프로토콜 학습",
        "summary": "디지털 저장소에서 메타데이터를 수집하기 위한 OAI-PMH 프로토콜의 개념과 사용법을 학습합니다.",
        "category": "OAI-PMH",
        "tags": ["OAI-PMH", "메타데이터", "프로토콜"],
        "difficulty": "BEGINNER",
        "estimated_time": 45,
        "prerequisites": "XML 기본 지식",
        "learning_objectives": "OAI-PMH 프로토콜의 개념을 이해하고, 6가지 기본 요청을 사용할 수 있습니다.",
        "content": """
<h2>OAI-PMH란?</h2>
<p><strong>OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting)</strong>는
디지털 저장소(리포지토리)에서 메타데이터를 수집(하베스팅)하기 위한 표준 프로토콜입니다.
2001년에 개발되어 현재 전 세계 도서관, 박물관, 학술 저장소에서 널리 사용되고 있습니다.</p>

<h2>주요 구성 요소</h2>

<h3>1. 데이터 제공자 (Data Provider)</h3>
<p>메타데이터를 보유하고 OAI-PMH를 통해 공개하는 저장소</p>
<ul>
    <li>예: 대학 도서관, 박물관, 학술 저장소</li>
</ul>

<h3>2. 서비스 제공자 (Service Provider)</h3>
<p>여러 저장소로부터 메타데이터를 수집하여 통합 검색 서비스 제공</p>
<ul>
    <li>예: 통합 검색 포털, 디지털 도서관 연합</li>
</ul>

<h3>3. HTTP 기반 프로토콜</h3>
<p>간단한 HTTP GET/POST 요청으로 메타데이터 교환하며, XML 형식으로 응답을 반환합니다.</p>

<h2>6가지 OAI-PMH Verb (요청)</h2>

<h3>1. Identify</h3>
<p><strong>설명:</strong> 저장소 정보 조회</p>
<p><strong>매개변수:</strong> 없음</p>
<p><strong>예시:</strong></p>
<pre><code>http://repository.org/oai?verb=Identify</code></pre>
<p><strong>응답:</strong> 저장소 이름, 관리자 이메일, 프로토콜 버전 등</p>

<h3>2. ListMetadataFormats</h3>
<p><strong>설명:</strong> 지원하는 메타데이터 형식 목록</p>
<p><strong>매개변수:</strong> identifier (선택)</p>
<p><strong>예시:</strong></p>
<pre><code>http://repository.org/oai?verb=ListMetadataFormats</code></pre>
<p><strong>응답:</strong> oai_dc, mods, marc21 등의 형식 목록</p>

<h3>3. ListSets</h3>
<p><strong>설명:</strong> 저장소의 세트(컬렉션) 목록</p>
<p><strong>매개변수:</strong> resumptionToken (선택)</p>
<p><strong>예시:</strong></p>
<pre><code>http://repository.org/oai?verb=ListSets</code></pre>
<p><strong>응답:</strong> 세트 이름과 설명 목록</p>

<h3>4. ListIdentifiers</h3>
<p><strong>설명:</strong> 레코드 식별자 목록만 조회</p>
<p><strong>매개변수:</strong> metadataPrefix (필수), from, until, set</p>
<p><strong>예시:</strong></p>
<pre><code>http://repository.org/oai?verb=ListIdentifiers&metadataPrefix=oai_dc</code></pre>
<p><strong>응답:</strong> 레코드 식별자와 타임스탬프 목록</p>

<h3>5. ListRecords</h3>
<p><strong>설명:</strong> 전체 메타데이터 레코드 조회</p>
<p><strong>매개변수:</strong> metadataPrefix (필수), from, until, set</p>
<p><strong>예시:</strong></p>
<pre><code>http://repository.org/oai?verb=ListRecords&metadataPrefix=oai_dc&from=2024-01-01</code></pre>
<p><strong>응답:</strong> 완전한 메타데이터 레코드 목록</p>

<h3>6. GetRecord</h3>
<p><strong>설명:</strong> 특정 레코드 하나만 조회</p>
<p><strong>매개변수:</strong> identifier (필수), metadataPrefix (필수)</p>
<p><strong>예시:</strong></p>
<pre><code>http://repository.org/oai?verb=GetRecord&identifier=oai:example:123&metadataPrefix=oai_dc</code></pre>
<p><strong>응답:</strong> 지정한 레코드의 완전한 메타데이터</p>

<h2>주요 메타데이터 형식</h2>

<h3>1. oai_dc (Dublin Core)</h3>
<ul>
    <li><strong>설명:</strong> OAI-PMH의 기본 메타데이터 형식</li>
    <li><strong>요소:</strong> title, creator, subject, description, publisher, date, type, format, identifier, language, rights</li>
    <li><strong>사용:</strong> 가장 보편적으로 사용되는 간단한 형식</li>
</ul>

<h3>2. mods (Metadata Object Description Schema)</h3>
<ul>
    <li><strong>설명:</strong> 더 상세한 서지 정보 표현</li>
    <li><strong>요소:</strong> titleInfo, name, typeOfResource, genre, originInfo, language, physicalDescription, abstract, subject 등</li>
    <li><strong>사용:</strong> 도서관, 박물관 등에서 상세한 메타데이터 필요 시</li>
</ul>

<h3>3. marc21</h3>
<ul>
    <li><strong>설명:</strong> 도서관 표준 서지 형식</li>
    <li><strong>요소:</strong> 숫자 태그 기반 (001-999)</li>
    <li><strong>사용:</strong> 전통적인 도서관 시스템과의 호환성</li>
</ul>

<h2>메타데이터 하베스팅 프로세스</h2>

<h3>1단계: 저장소 확인</h3>
<pre><code>GET http://repository.org/oai?verb=Identify</code></pre>

<h3>2단계: 지원 형식 확인</h3>
<pre><code>GET http://repository.org/oai?verb=ListMetadataFormats</code></pre>

<h3>3단계: 세트 확인 (선택)</h3>
<pre><code>GET http://repository.org/oai?verb=ListSets</code></pre>

<h3>4단계: 메타데이터 수집</h3>
<pre><code>GET http://repository.org/oai?verb=ListRecords&metadataPrefix=oai_dc&from=2024-01-01</code></pre>

<h3>5단계: 증분 수집</h3>
<p>응답에 resumptionToken이 있으면 계속해서 다음 페이지를 가져옵니다.</p>
<pre><code>GET http://repository.org/oai?verb=ListRecords&resumptionToken=xyz123</code></pre>

<h2>XML 응답 예시</h2>

<h3>Identify 응답</h3>
<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"&gt;
  &lt;responseDate&gt;2024-12-28T10:00:00Z&lt;/responseDate&gt;
  &lt;request verb="Identify"&gt;http://example.org/oai&lt;/request&gt;
  &lt;Identify&gt;
    &lt;repositoryName&gt;Example Digital Library&lt;/repositoryName&gt;
    &lt;baseURL&gt;http://example.org/oai&lt;/baseURL&gt;
    &lt;protocolVersion&gt;2.0&lt;/protocolVersion&gt;
    &lt;adminEmail&gt;admin@example.org&lt;/adminEmail&gt;
    &lt;earliestDatestamp&gt;2020-01-01&lt;/earliestDatestamp&gt;
  &lt;/Identify&gt;
&lt;/OAI-PMH&gt;</code></pre>

<h2>OAI-PMH 활용 사례</h2>

<h3>1. 학술 저장소 연합</h3>
<ul>
    <li>국내: RISS, NDSL</li>
    <li>해외: NDLTD, BASE</li>
    <li>여러 대학의 학위논문 저장소를 통합</li>
</ul>

<h3>2. 디지털 도서관</h3>
<ul>
    <li>국립중앙도서관</li>
    <li>지역 도서관 연합</li>
    <li>전자책, 고문서 통합 검색</li>
</ul>

<h3>3. 문화유산 포털</h3>
<ul>
    <li>Europeana (유럽)</li>
    <li>DPLA (미국)</li>
    <li>박물관, 미술관 소장품 정보 통합</li>
</ul>

<h3>4. 오픈 액세스 저장소</h3>
<ul>
    <li>arXiv (물리학, 수학)</li>
    <li>PubMed Central (의학)</li>
    <li>RePEc (경제학)</li>
</ul>

<h2>장점과 제약사항</h2>

<h3>장점</h3>
<ul>
    <li>✓ 간단한 HTTP 기반 프로토콜</li>
    <li>✓ 표준화된 메타데이터 형식</li>
    <li>✓ 증분 하베스팅 지원</li>
    <li>✓ 전 세계적으로 널리 사용</li>
    <li>✓ 낮은 진입 장벽</li>
</ul>

<h3>제약사항</h3>
<ul>
    <li>⚠ 메타데이터만 교환 (원문은 별도)</li>
    <li>⚠ 단방향 통신 (Pull 방식)</li>
    <li>⚠ 복잡한 검색 기능 없음</li>
    <li>⚠ 실시간 동기화 어려움</li>
</ul>

<h2>학습 팁</h2>
<ul>
    <li>✓ 실제 OAI-PMH 저장소에 요청을 보내보세요 (예: arXiv)</li>
    <li>✓ XML 응답 구조를 이해하는 것이 중요합니다</li>
    <li>✓ Dublin Core 메타데이터 요소를 먼저 학습하세요</li>
    <li>✓ resumptionToken의 개념을 이해하세요</li>
</ul>
"""
    },
]

for content_data in contents_data:
    category = sub_categories[content_data['category']]
    content_tags = [tags[tag_name] for tag_name in content_data['tags']]

    content, created = Content.objects.get_or_create(
        slug=slugify(content_data['title']),
        defaults={
            'title': content_data['title'],
            'summary': content_data['summary'],
            'category': category,
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

print("\n🎉 All education contents created successfully!")
print("\n📊 Summary:")
print(f"  - Parent Categories: {len(parent_categories)}")
print(f"  - Sub Categories: {len(sub_categories)}")
print(f"  - Tags: {len(tags)}")
print(f"  - Contents: {len(contents_data)}")
