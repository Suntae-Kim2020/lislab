#!/usr/bin/env python
"""
SRW 학습 콘텐츠 추가 스크립트
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

def create_srw_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 가져오기: 검색 프로토콜
    search_protocol_category = Category.objects.get(slug='search-protocol')
    print("✓ 상위 카테고리 확인: 검색 프로토콜")

    # 하위 카테고리 생성 또는 가져오기: SRW
    srw_category, created = Category.objects.get_or_create(
        slug='srw',
        defaults={
            'name': 'SRW',
            'description': 'SRW (Search/Retrieval Web service)',
            'parent': search_protocol_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: SRW")
    else:
        print("✓ 하위 카테고리 확인: SRW")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': 'SRW', 'slug': 'srw'},
        {'name': 'SOAP', 'slug': 'soap'},
        {'name': 'WSDL', 'slug': 'wsdl'},
        {'name': '웹서비스', 'slug': 'web-service'},
        {'name': '검색 프로토콜', 'slug': 'search-protocol'},
        {'name': 'CQL', 'slug': 'cql'},
        {'name': 'XML', 'slug': 'xml'},
        {'name': '정보검색', 'slug': 'information-retrieval'}
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
        title="SRW: SOAP 기반 도서관 웹서비스",
        slug="srw-web-service-protocol",
        summary="SRU의 SOAP 버전 SRW! 웹서비스(SOAP, WSDL, UDDI)의 개념을 이해하고, SRW가 왜 필요한지, SRU와 무엇이 다른지 배웁니다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>웹서비스(SOAP, WSDL, UDDI)의 기본 개념 이해하기</li>
    <li>SRW가 무엇인지, SRU와 어떻게 다른지 알기</li>
    <li>SRW 요청/응답 구조 파악하기</li>
    <li>SRW, SRU, Z39.50, OAI-PMH, REST API 차이점 이해하기</li>
    <li>언제 SRW를 사용하고 언제 SRU를 사용해야 하는지 판단하기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. 웹서비스(Web Services)란?</h2>

  <div class="ws-intro">
    <h3>🌐 웹서비스 기초</h3>
    <p>SRW를 이해하려면 먼저 <strong>웹서비스</strong>를 알아야 합니다!</p>

    <div class="ws-definition">
      <p class="definition-text">
        <strong>웹서비스</strong>는 서로 다른 시스템이 인터넷을 통해<br>
        자동으로 데이터를 주고받을 수 있게 하는 <strong>표준 기술</strong>입니다.
      </p>
    </div>

    <div class="ws-analogy">
      <h4>📮 쉬운 비유</h4>
      <div class="analogy-boxes">
        <div class="analogy-box">
          <strong>웹사이트</strong>
          <p>= 사람이 보는 우편물</p>
          <p class="small">HTML로 예쁘게 디자인</p>
        </div>
        <div class="vs-arrow">vs</div>
        <div class="analogy-box">
          <strong>웹서비스</strong>
          <p>= 컴퓨터가 읽는 우편물</p>
          <p class="small">XML로 정확하게 구조화</p>
        </div>
      </div>
    </div>
  </div>

  <h3>🔧 웹서비스의 3대 요소</h3>

  <div class="ws-components">
    <div class="component-card soap-card">
      <div class="component-number">1</div>
      <h4>SOAP</h4>
      <p class="component-name">Simple Object Access Protocol</p>
      <p class="component-role">메시지 형식</p>
      <div class="component-detail">
        <p><strong>무엇을:</strong> 데이터를 XML로 포장하는 방법</p>
        <p><strong>비유:</strong> 택배 상자 규격</p>
        <div class="example-mini">
          <code>&lt;soap:Envelope&gt;<br>&nbsp;&nbsp;&lt;soap:Body&gt;<br>&nbsp;&nbsp;&nbsp;&nbsp;데이터...<br>&nbsp;&nbsp;&lt;/soap:Body&gt;<br>&lt;/soap:Envelope&gt;</code>
        </div>
      </div>
    </div>

    <div class="component-card wsdl-card">
      <div class="component-number">2</div>
      <h4>WSDL</h4>
      <p class="component-name">Web Services Description Language</p>
      <p class="component-role">서비스 설명서</p>
      <div class="component-detail">
        <p><strong>무엇을:</strong> 웹서비스가 뭘 할 수 있는지 설명</p>
        <p><strong>비유:</strong> 식당 메뉴판</p>
        <div class="example-mini">
          "이 서비스는 searchRetrieve,<br>
          explain, scan을 할 수 있어요"
        </div>
      </div>
    </div>

    <div class="component-card uddi-card">
      <div class="component-number">3</div>
      <h4>UDDI</h4>
      <p class="component-name">Universal Description, Discovery and Integration</p>
      <p class="component-role">서비스 디렉토리</p>
      <div class="component-detail">
        <p><strong>무엇을:</strong> 웹서비스를 찾을 수 있는 전화번호부</p>
        <p><strong>비유:</strong> 식당 검색 앱</p>
        <div class="example-mini">
          "도서관 검색 서비스를<br>
          어디서 찾을 수 있나?"
        </div>
      </div>
    </div>
  </div>

  <div class="ws-flow">
    <h4>🔄 웹서비스 작동 흐름</h4>
    <div class="flow-diagram">
      <div class="flow-step">
        <div class="step-box">1. UDDI에서 서비스 찾기</div>
        <p class="step-desc">"도서관 검색 서비스 어디 있나?"</p>
      </div>
      <div class="flow-arrow">⬇️</div>
      <div class="flow-step">
        <div class="step-box">2. WSDL 읽기</div>
        <p class="step-desc">"이 서비스가 뭘 할 수 있는지 확인"</p>
      </div>
      <div class="flow-arrow">⬇️</div>
      <div class="flow-step">
        <div class="step-box">3. SOAP 메시지 보내기</div>
        <p class="step-desc">"검색 요청을 XML로 포장해서 전송"</p>
      </div>
      <div class="flow-arrow">⬇️</div>
      <div class="flow-step">
        <div class="step-box">4. SOAP 응답 받기</div>
        <p class="step-desc">"검색 결과를 XML로 받음"</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>2. SRW를 한 문장으로</h2>

  <div class="hero-definition">
    <h3>🔍 SRW란?</h3>
    <p class="big-statement">
      <strong>SRW (Search/Retrieval Web service)</strong>는<br>
      <strong>SOAP</strong>을 사용하여 도서관을 검색하는 <strong>웹서비스 프로토콜</strong>입니다.
    </p>
  </div>

  <div class="sru-vs-srw">
    <h4>🤔 SRU와 SRW의 관계</h4>
    <div class="relationship-grid">
      <div class="protocol-box sru-box">
        <h5>SRU</h5>
        <p class="tech-stack">HTTP GET</p>
        <p class="desc">URL 파라미터로 검색</p>
        <div class="pros">
          ✅ 간단함<br>
          ✅ 브라우저로 가능
        </div>
      </div>

      <div class="same-core">
        <p>같은 핵심 기능</p>
        <ul>
          <li>CQL 쿼리</li>
          <li>같은 작업</li>
          <li>같은 결과</li>
        </ul>
      </div>

      <div class="protocol-box srw-box">
        <h5>SRW</h5>
        <p class="tech-stack">HTTP POST + SOAP</p>
        <p class="desc">SOAP 메시지로 검색</p>
        <div class="pros">
          ✅ 표준적<br>
          ✅ 확장 가능
        </div>
      </div>
    </div>

    <div class="key-insight">
      <p><strong>💡 핵심:</strong> SRU와 SRW는 <strong>같은 기능을 다른 방식</strong>으로 제공합니다!</p>
      <p>SRU = 간단한 URL 방식 | SRW = 표준 웹서비스 방식</p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>3. SRW 요청 구조</h2>

  <h3>📨 SOAP 요청 예제</h3>

  <div class="soap-example">
    <p class="example-title"><strong>searchRetrieve 요청 (해리포터 검색)</strong></p>
    <pre class="code-block">
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:srw="http://www.loc.gov/zing/srw/"&gt;

  &lt;soap:Body&gt;
    &lt;srw:searchRetrieveRequest&gt;
      &lt;srw:version&gt;1.1&lt;/srw:version&gt;
      &lt;srw:query&gt;dc.title=harry potter&lt;/srw:query&gt;
      &lt;srw:startRecord&gt;1&lt;/srw:startRecord&gt;
      &lt;srw:maximumRecords&gt;10&lt;/srw:maximumRecords&gt;
      &lt;srw:recordSchema&gt;dc&lt;/srw:recordSchema&gt;
    &lt;/srw:searchRetrieveRequest&gt;
  &lt;/soap:Body&gt;

&lt;/soap:Envelope&gt;
    </pre>
  </div>

  <div class="structure-explanation">
    <h4>🔍 구조 설명</h4>
    <table class="structure-table">
      <tr>
        <th>요소</th>
        <th>설명</th>
      </tr>
      <tr>
        <td><code>&lt;soap:Envelope&gt;</code></td>
        <td>SOAP 메시지의 외부 포장</td>
      </tr>
      <tr>
        <td><code>&lt;soap:Body&gt;</code></td>
        <td>실제 요청 내용</td>
      </tr>
      <tr>
        <td><code>&lt;srw:searchRetrieveRequest&gt;</code></td>
        <td>SRW 검색 요청</td>
      </tr>
      <tr>
        <td><code>&lt;srw:query&gt;</code></td>
        <td>CQL 쿼리 (SRU와 동일)</td>
      </tr>
    </table>
  </div>

  <h3>📬 SOAP 응답 예제</h3>

  <div class="soap-example">
    <p class="example-title"><strong>searchRetrieve 응답 (일부)</strong></p>
    <pre class="code-block">
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:srw="http://www.loc.gov/zing/srw/"&gt;

  &lt;soap:Body&gt;
    &lt;srw:searchRetrieveResponse&gt;
      &lt;srw:version&gt;1.1&lt;/srw:version&gt;
      &lt;srw:numberOfRecords&gt;245&lt;/srw:numberOfRecords&gt;

      &lt;srw:records&gt;
        &lt;srw:record&gt;
          &lt;srw:recordSchema&gt;dc&lt;/srw:recordSchema&gt;
          &lt;srw:recordData&gt;
            &lt;dc:title&gt;Harry Potter and the Philosopher's Stone&lt;/dc:title&gt;
            &lt;dc:creator&gt;Rowling, J. K.&lt;/dc:creator&gt;
            &lt;dc:date&gt;1997&lt;/dc:date&gt;
          &lt;/srw:recordData&gt;
        &lt;/srw:record&gt;
        &lt;!-- 더 많은 레코드... --&gt;
      &lt;/srw:records&gt;

    &lt;/srw:searchRetrieveResponse&gt;
  &lt;/soap:Body&gt;

&lt;/soap:Envelope&gt;
    </pre>
  </div>
</div>

<div class="content-section">
  <h2>4. WSDL로 서비스 확인하기</h2>

  <div class="wsdl-section">
    <h3>📋 WSDL이란?</h3>
    <p>WSDL은 웹서비스가 제공하는 기능을 XML로 설명한 <strong>서비스 설명서</strong>입니다.</p>

    <div class="wsdl-demo">
      <h4>🌐 실제 WSDL 확인하기</h4>

      <div class="demo-box">
        <p class="demo-title"><strong>미국 의회도서관 SRW WSDL</strong></p>
        <div class="url-display">
          <a href="http://www.loc.gov/standards/sru/srw/wsdl/SRW.wsdl" target="_blank" class="wsdl-link">
            http://www.loc.gov/standards/sru/srw/wsdl/SRW.wsdl
          </a>
        </div>
        <p class="instruction">👆 클릭하면 SRW 표준 WSDL을 볼 수 있습니다!</p>
      </div>
    </div>

    <div class="wsdl-content">
      <h4>📖 WSDL에서 알 수 있는 것</h4>
      <ul>
        <li><strong>Operations</strong>: 사용 가능한 작업 (searchRetrieve, explain, scan)</li>
        <li><strong>Input/Output</strong>: 입력/출력 메시지 형식</li>
        <li><strong>Binding</strong>: SOAP 사용 방법</li>
        <li><strong>Service</strong>: 실제 서비스 주소 (endpoint)</li>
      </ul>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>5. SRU vs SRW 상세 비교</h2>

  <table class="detailed-comparison">
    <thead>
      <tr>
        <th>비교 항목</th>
        <th>SRU</th>
        <th>SRW</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>전송 방식</strong></td>
        <td>HTTP GET</td>
        <td>HTTP POST</td>
      </tr>
      <tr>
        <td><strong>요청 형식</strong></td>
        <td>URL 파라미터</td>
        <td>SOAP XML</td>
      </tr>
      <tr>
        <td><strong>응답 형식</strong></td>
        <td>SRU XML</td>
        <td>SOAP + SRU XML</td>
      </tr>
      <tr>
        <td><strong>쿼리 언어</strong></td>
        <td>CQL</td>
        <td>CQL (동일)</td>
      </tr>
      <tr>
        <td><strong>작업</strong></td>
        <td>searchRetrieve, explain, scan</td>
        <td>searchRetrieve, explain, scan (동일)</td>
      </tr>
      <tr>
        <td><strong>복잡도</strong></td>
        <td>⭐⭐ 쉬움</td>
        <td>⭐⭐⭐⭐ 복잡</td>
      </tr>
      <tr>
        <td><strong>브라우저 테스트</strong></td>
        <td>✅ 가능</td>
        <td>❌ 불가능 (도구 필요)</td>
      </tr>
      <tr>
        <td><strong>표준 웹서비스</strong></td>
        <td>❌ 아님</td>
        <td>✅ SOAP 표준</td>
      </tr>
      <tr>
        <td><strong>확장성</strong></td>
        <td>제한적</td>
        <td>높음</td>
      </tr>
    </tbody>
  </table>

  <div class="comparison-summary">
    <h4>🎯 언제 뭘 쓸까?</h4>
    <div class="when-to-use">
      <div class="use-card sru-use">
        <h5>SRU를 쓰세요</h5>
        <ul>
          <li>간단한 검색만 필요</li>
          <li>빠른 개발 원함</li>
          <li>브라우저 테스트 필요</li>
          <li>REST 스타일 선호</li>
        </ul>
      </div>

      <div class="use-card srw-use">
        <h5>SRW를 쓰세요</h5>
        <ul>
          <li>표준 웹서비스 필요</li>
          <li>기존 SOAP 인프라 있음</li>
          <li>복잡한 확장 필요</li>
          <li>엔터프라이즈 환경</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>6. 다른 프로토콜과의 비교</h2>

  <table class="protocol-master-comparison">
    <thead>
      <tr>
        <th>프로토콜</th>
        <th>기술</th>
        <th>복잡도</th>
        <th>주 용도</th>
        <th>브라우저 테스트</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Z39.50</strong></td>
        <td>전용 프로토콜</td>
        <td>⭐⭐⭐⭐⭐</td>
        <td>도서관 검색</td>
        <td>❌</td>
      </tr>
      <tr>
        <td><strong>SRU</strong></td>
        <td>HTTP GET</td>
        <td>⭐⭐</td>
        <td>도서관 검색</td>
        <td>✅</td>
      </tr>
      <tr class="highlight-row">
        <td><strong>SRW</strong></td>
        <td>SOAP/HTTP POST</td>
        <td>⭐⭐⭐⭐</td>
        <td>도서관 검색</td>
        <td>❌</td>
      </tr>
      <tr>
        <td><strong>OAI-PMH</strong></td>
        <td>HTTP GET</td>
        <td>⭐</td>
        <td>메타데이터 수확</td>
        <td>✅</td>
      </tr>
      <tr>
        <td><strong>REST API</strong></td>
        <td>HTTP (다양)</td>
        <td>⭐⭐</td>
        <td>범용</td>
        <td>✅ (GET만)</td>
      </tr>
    </tbody>
  </table>

  <div class="evolution-timeline">
    <h4>📈 프로토콜 진화 과정</h4>
    <div class="timeline">
      <div class="timeline-item">
        <div class="year">1990년대</div>
        <div class="tech">Z39.50</div>
        <div class="desc">복잡한 전용 프로토콜</div>
      </div>
      <div class="timeline-arrow">→</div>
      <div class="timeline-item">
        <div class="year">2000년대 초</div>
        <div class="tech">SRW</div>
        <div class="desc">SOAP 웹서비스로 현대화</div>
      </div>
      <div class="timeline-arrow">→</div>
      <div class="timeline-item">
        <div class="year">2000년대 중</div>
        <div class="tech">SRU</div>
        <div class="desc">더 간단한 RESTful 스타일</div>
      </div>
      <div class="timeline-arrow">→</div>
      <div class="timeline-item current">
        <div class="year">현재</div>
        <div class="tech">REST API</div>
        <div class="desc">표준 없이 각자 구현</div>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>7. SRW 사용하기</h2>

  <div class="usage-guide">
    <h3>🔧 SRW 클라이언트 개발</h3>

    <div class="code-example">
      <h4>💻 Python 예제 (suds-py3 라이브러리 사용)</h4>
      <pre class="code-block">
from suds.client import Client

# WSDL URL
wsdl_url = 'http://example.org/srw?wsdl'

# SOAP 클라이언트 생성
client = Client(wsdl_url)

# searchRetrieve 호출
result = client.service.searchRetrieve(
    version='1.1',
    query='dc.title=python',
    startRecord=1,
    maximumRecords=10,
    recordSchema='dc'
)

# 결과 출력
print(f"총 {result.numberOfRecords}건 발견")
for record in result.records:
    print(record.recordData)
      </pre>
    </div>

    <div class="code-example">
      <h4>🧪 Postman으로 테스트하기</h4>
      <ol>
        <li><strong>Postman 열기</strong></li>
        <li><strong>New Request</strong> → POST 선택</li>
        <li><strong>URL</strong>: SRW 서비스 endpoint 입력</li>
        <li><strong>Body</strong> → raw → XML 선택</li>
        <li><strong>SOAP 요청 XML</strong> 붙여넣기</li>
        <li><strong>Send</strong> 클릭</li>
      </ol>
    </div>
  </div>

  <div class="testing-tools">
    <h4>🛠️ SRW 테스트 도구</h4>
    <div class="tools-grid">
      <div class="tool-card">
        <h5>SoapUI</h5>
        <p>SOAP 전용 테스트 도구</p>
        <p class="tool-feature">✅ WSDL 자동 분석<br>✅ 요청 자동 생성</p>
      </div>
      <div class="tool-card">
        <h5>Postman</h5>
        <p>범용 API 테스트 도구</p>
        <p class="tool-feature">✅ 사용 간편<br>✅ SOAP 지원</p>
      </div>
      <div class="tool-card">
        <h5>cURL</h5>
        <p>명령줄 도구</p>
        <p class="tool-feature">✅ 스크립트 가능<br>✅ 서버에서 사용</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>8. SRW의 현재와 미래</h2>

  <div class="current-status">
    <h3>📊 현재 상황</h3>

    <div class="status-grid">
      <div class="status-card declining">
        <h4>📉 SRW 사용 감소</h4>
        <ul>
          <li>SOAP의 인기 하락</li>
          <li>REST API 선호 증가</li>
          <li>SRU가 더 간단</li>
          <li>새 프로젝트는 SRU 선택</li>
        </ul>
      </div>

      <div class="status-card still-used">
        <h4>✅ 여전히 사용 중</h4>
        <ul>
          <li>기존 시스템 유지</li>
          <li>엔터프라이즈 환경</li>
          <li>표준 준수 필요</li>
          <li>레거시 통합</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="future-outlook">
    <h4>🔮 앞으로는?</h4>
    <div class="outlook-content">
      <p><strong>SRW는 점진적으로 SRU와 REST API로 대체되고 있습니다.</strong></p>
      <ul>
        <li>✅ <strong>SRU</strong>: 간단한 검색에 적합</li>
        <li>✅ <strong>REST API</strong>: 현대적, JSON 지원</li>
        <li>⚠️ <strong>SRW</strong>: 기존 시스템 유지만</li>
      </ul>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>9. 요약: 한눈에 정리</h2>

  <div class="summary-boxes">
    <div class="summary-main">
      <h3>🔍 SRW란?</h3>
      <p class="definition">SOAP을 사용하여 도서관을 검색하는 웹서비스 프로토콜</p>

      <div class="key-points">
        <div class="point">
          <strong>기술:</strong> HTTP POST + SOAP + CQL
        </div>
        <div class="point">
          <strong>표준:</strong> WSDL로 정의된 웹서비스
        </div>
        <div class="point">
          <strong>관계:</strong> SRU의 SOAP 버전
        </div>
      </div>
    </div>

    <div class="summary-comparison">
      <h4>SRU vs SRW</h4>
      <table class="mini-comparison">
        <tr>
          <td><strong>SRU</strong></td>
          <td>간단, GET, 브라우저 OK</td>
        </tr>
        <tr>
          <td><strong>SRW</strong></td>
          <td>표준, POST+SOAP, 도구 필요</td>
        </tr>
      </table>
    </div>
  </div>

  <div class="web-services-recap">
    <h4>📚 웹서비스 복습</h4>
    <div class="recap-grid">
      <div class="recap-item">
        <strong>SOAP</strong>
        <p>XML 메시지 포장 방법</p>
      </div>
      <div class="recap-item">
        <strong>WSDL</strong>
        <p>서비스 설명서 (메뉴판)</p>
      </div>
      <div class="recap-item">
        <strong>UDDI</strong>
        <p>서비스 디렉토리 (전화번호부)</p>
      </div>
    </div>
  </div>

  <div class="final-message">
    <h3>🎯 핵심 메시지</h3>
    <div class="message-box">
      <p class="big-emphasis">
        <strong>SRW = 표준 웹서비스 방식의 SRU</strong>
      </p>
      <p>같은 기능이지만, <strong>SRU는 간단</strong>하고 <strong>SRW는 표준</strong>적입니다.<br>
      현재는 <strong>SRU가 더 많이 사용</strong>되고, SRW는 <strong>기존 시스템 유지</strong>에 주로 쓰입니다.</p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>10. 학습 점검 퀴즈</h2>

  <div class="quiz-section">
    <div class="quiz-item">
      <p><strong>Q1.</strong> 웹서비스의 3대 요소는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>SOAP (메시지 형식), WSDL (서비스 설명), UDDI (서비스 디렉토리)</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> SRU와 SRW의 가장 큰 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>SRU는 HTTP GET + URL 파라미터</strong>, <strong>SRW는 HTTP POST + SOAP</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> WSDL의 역할은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>웹서비스가 제공하는 기능을 설명하는 서비스 설명서</strong> (메뉴판 같은 역할)</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> SRW는 브라우저에서 직접 테스트할 수 있나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>불가능</strong>합니다. HTTP POST와 SOAP을 사용하므로 Postman, SoapUI 같은 도구가 필요합니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> 언제 SRW 대신 SRU를 사용하나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>간단한 검색</strong>, <strong>빠른 개발</strong>, <strong>브라우저 테스트</strong>가 필요할 때, <strong>REST 스타일</strong>을 선호할 때</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q6.</strong> SRW와 SRU는 쿼리 언어가 다른가요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>아니요</strong>. 둘 다 <strong>CQL (Contextual Query Language)</strong>을 사용합니다.</p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 더 알아보기</h2>
  <ul>
    <li><strong>SRW 공식 사이트</strong> - Library of Congress SRW 문서</li>
    <li><strong>SOAP 스펙</strong> - W3C SOAP 표준</li>
    <li><strong>WSDL 가이드</strong> - W3C WSDL 문서</li>
    <li><strong>SoapUI</strong> - SOAP 테스트 도구</li>
    <li><strong>SRW WSDL 예제</strong> - 실제 서비스 WSDL</li>
  </ul>
</div>

<style>
.content-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.ws-intro {
  margin: 2rem 0;
}

.ws-definition {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  margin: 1.5rem 0;
}

.definition-text {
  font-size: 1.3rem;
  line-height: 1.8;
  color: white;
}

.ws-analogy {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.analogy-boxes {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  margin-top: 1.5rem;
}

.analogy-box {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  border: 2px solid #ff9800;
  flex: 1;
}

.vs-arrow {
  font-size: 2rem;
  font-weight: bold;
  color: #666;
}

.small {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
}

.ws-components {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin: 2rem 0;
}

.component-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  position: relative;
  border: 3px solid #ddd;
}

.soap-card {
  border-color: #2196f3;
}

.wsdl-card {
  border-color: #4caf50;
}

.uddi-card {
  border-color: #ff9800;
}

.component-number {
  position: absolute;
  top: -15px;
  left: 15px;
  width: 35px;
  height: 35px;
  background: #1976d2;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1rem;
}

.component-card h4 {
  color: #1976d2;
  margin: 1rem 0 0.5rem 0;
  font-size: 1.3rem;
}

.component-name {
  font-size: 0.85rem;
  color: #666;
  font-style: italic;
}

.component-role {
  font-weight: bold;
  color: #333;
  margin: 0.75rem 0;
}

.component-detail {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.example-mini {
  background: #263238;
  color: #aed581;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 0.75rem;
  font-family: monospace;
  font-size: 0.85rem;
  line-height: 1.5;
}

.ws-flow {
  background: #e3f2fd;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.flow-diagram {
  margin-top: 1.5rem;
}

.flow-step {
  margin: 1rem 0;
  text-align: center;
}

.step-box {
  background: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  display: inline-block;
  font-weight: bold;
  color: #1976d2;
  border: 2px solid #2196f3;
}

.step-desc {
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.flow-arrow {
  font-size: 2rem;
  color: #4caf50;
  margin: 0.5rem 0;
}

.hero-definition {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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

.sru-vs-srw {
  margin: 2rem 0;
}

.relationship-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 2rem;
  align-items: center;
  margin: 2rem 0;
}

.protocol-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
}

.sru-box {
  border: 3px solid #4caf50;
}

.srw-box {
  border: 3px solid #2196f3;
}

.protocol-box h5 {
  font-size: 1.5rem;
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.tech-stack {
  font-weight: bold;
  color: #666;
  margin: 0.5rem 0;
}

.desc {
  margin: 1rem 0;
}

.pros {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-size: 0.9rem;
  line-height: 1.6;
}

.same-core {
  background: #fff3e0;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.same-core p {
  font-weight: bold;
  color: #ff9800;
  margin-bottom: 0.75rem;
}

.key-insight {
  background: #e8f5e9;
  border-left: 4px solid #4caf50;
  padding: 1.5rem;
  border-radius: 4px;
  margin: 2rem 0;
}

.soap-example {
  background: white;
  border: 2px solid #2196f3;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 2rem 0;
}

.example-title {
  font-weight: bold;
  color: #1976d2;
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
  margin: 0;
}

.structure-explanation {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.structure-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin-top: 1rem;
}

.structure-table th,
.structure-table td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.structure-table th {
  background: #f5f5f5;
  font-weight: bold;
}

.structure-table code {
  background: #263238;
  color: #aed581;
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
}

.wsdl-section {
  margin: 2rem 0;
}

.wsdl-demo {
  background: #e8f5e9;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.demo-box {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #4caf50;
}

.demo-title {
  font-weight: bold;
  color: #2e7d32;
  margin-bottom: 1rem;
}

.url-display {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
  overflow-x: auto;
}

.wsdl-link {
  color: #1976d2;
  text-decoration: underline;
  word-break: break-all;
  font-family: monospace;
}

.wsdl-link:hover {
  color: #0d47a1;
}

.instruction {
  color: #666;
  font-size: 0.9rem;
  font-style: italic;
  margin-top: 0.5rem;
}

.wsdl-content {
  background: #fff3e0;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.detailed-comparison {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  background: white;
}

.detailed-comparison th,
.detailed-comparison td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.detailed-comparison th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.detailed-comparison tr:nth-child(even) {
  background: #f5f5f5;
}

.comparison-summary {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.when-to-use {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 1.5rem;
}

.use-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
}

.sru-use {
  border: 3px solid #4caf50;
}

.srw-use {
  border: 3px solid #2196f3;
}

.use-card h5 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.protocol-master-comparison {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  background: white;
}

.protocol-master-comparison th,
.protocol-master-comparison td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.protocol-master-comparison th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.highlight-row {
  background: #e3f2fd;
  font-weight: bold;
}

.evolution-timeline {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.timeline {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.timeline-item {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  min-width: 150px;
  border: 2px solid #ddd;
}

.timeline-item.current {
  border: 3px solid #4caf50;
  background: #e8f5e9;
}

.year {
  font-size: 0.85rem;
  color: #666;
}

.tech {
  font-weight: bold;
  color: #1976d2;
  font-size: 1.1rem;
  margin: 0.5rem 0;
}

.timeline .desc {
  font-size: 0.85rem;
  color: #666;
}

.timeline-arrow {
  font-size: 2rem;
  color: #4caf50;
}

.usage-guide {
  margin: 2rem 0;
}

.code-example {
  background: #263238;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.code-example h4 {
  color: #aed581;
  margin-bottom: 1rem;
}

.code-example ol {
  color: #aed581;
}

.testing-tools {
  background: #e3f2fd;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.tool-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  border: 2px solid #ddd;
}

.tool-card h5 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.tool-feature {
  background: #f5f5f5;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 0.75rem;
  font-size: 0.85rem;
}

.current-status {
  margin: 2rem 0;
}

.status-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-top: 1.5rem;
}

.status-card {
  padding: 1.5rem;
  border-radius: 8px;
}

.status-card.declining {
  background: #ffebee;
  border: 3px solid #f44336;
}

.status-card.still-used {
  background: #e8f5e9;
  border: 3px solid #4caf50;
}

.future-outlook {
  background: #e3f2fd;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.outlook-content {
  margin-top: 1rem;
}

.summary-boxes {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.summary-main {
  background: white;
  padding: 2rem;
  border: 3px solid #2196f3;
  border-radius: 8px;
}

.definition {
  font-size: 1.1rem;
  color: #333;
  margin: 1rem 0;
}

.key-points {
  display: grid;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.point {
  background: #f5f5f5;
  padding: 0.75rem;
  border-radius: 4px;
}

.summary-comparison {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
}

.mini-comparison {
  width: 100%;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.mini-comparison td {
  padding: 0.75rem;
}

.web-services-recap {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.recap-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.recap-item {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
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

.big-emphasis {
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

@media (max-width: 1024px) {
  .ws-components,
  .tools-grid,
  .recap-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .analogy-boxes,
  .relationship-grid,
  .when-to-use,
  .status-grid,
  .summary-boxes,
  .ws-components,
  .tools-grid,
  .recap-grid {
    grid-template-columns: 1fr;
  }

  .timeline {
    flex-direction: column;
  }

  .timeline-arrow {
    transform: rotate(90deg);
  }
}
</style>
        """,
        category=srw_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=35,
        prerequisites="HTTP 기본 이해, XML 기초 지식, SRU 개념",
        learning_objectives="웹서비스(SOAP, WSDL, UDDI) 개념 이해하기, SRW 프로토콜의 구조와 작동 방식 파악하기, SRW와 SRU의 차이점 명확히 알기, SRW와 다른 프로토콜들의 비교를 통한 특징 이해하기, SRW 사용 여부를 판단할 수 있는 능력 기르기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {srw_category.name} (상위: {search_protocol_category.name})")
    print(f"  - 난이도: 중급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=search-protocol")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_srw_content()
