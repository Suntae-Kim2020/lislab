#!/usr/bin/env python
"""
SRU 학습 콘텐츠 추가 스크립트
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

def create_sru_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 가져오기 및 이름 업데이트: 검색 프로토콜 (스페이스 추가)
    search_protocol_category = Category.objects.get(slug='search-protocol')
    if search_protocol_category.name == '검색프로토콜':
        search_protocol_category.name = '검색 프로토콜'
        search_protocol_category.save()
        print("✓ 상위 카테고리 이름 업데이트: 검색 프로토콜")
    else:
        print("✓ 상위 카테고리 확인: 검색 프로토콜")

    # 하위 카테고리 생성 또는 가져오기: SRU
    sru_category, created = Category.objects.get_or_create(
        slug='sru',
        defaults={
            'name': 'SRU',
            'description': 'SRU (Search/Retrieval via URL)',
            'parent': search_protocol_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: SRU")
    else:
        print("✓ 하위 카테고리 확인: SRU")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': 'SRU', 'slug': 'sru'},
        {'name': '검색 프로토콜', 'slug': 'search-protocol'},
        {'name': 'CQL', 'slug': 'cql'},
        {'name': 'HTTP', 'slug': 'http'},
        {'name': 'XML', 'slug': 'xml'},
        {'name': '정보검색', 'slug': 'information-retrieval'},
        {'name': '도서관 시스템', 'slug': 'library-system'},
        {'name': 'Z39.50', 'slug': 'z3950'}
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
        title="SRU: URL로 검색하는 도서관 프로토콜",
        slug="sru-search-protocol",
        summary="웹 브라우저로 도서관을 검색하는 SRU! Z39.50보다 쉽고, REST보다 표준적인 SRU 프로토콜을 배우고 실제로 작동하는 것을 확인해봅니다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>SRU가 무엇인지, 왜 필요한지 이해하기</li>
    <li>SRU 요청 구조와 CQL 쿼리 익히기</li>
    <li>OAI-PMH, Z39.50, REST API와의 차이점 알기</li>
    <li>실제 도서관 SRU를 브라우저에서 사용해보기</li>
    <li>SRU를 언제 사용해야 하는지 판단하기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. SRU를 한 문장으로</h2>

  <div class="hero-box">
    <h3>🔍 SRU란?</h3>
    <p class="big-definition">
      <strong>SRU (Search/Retrieval via URL)</strong>는<br>
      URL만으로 도서관 검색을 할 수 있는 <strong>표준 검색 프로토콜</strong>입니다.
    </p>
  </div>

  <div class="simple-demo">
    <h4>🌐 이런 식으로 작동합니다</h4>
    <div class="url-example">
      <p class="url-label">SRU 검색 URL:</p>
      <code class="url-box">
        http://example.org/sru?<br>
        &nbsp;&nbsp;operation=searchRetrieve<br>
        &nbsp;&nbsp;&query=dc.title=해리포터<br>
        &nbsp;&nbsp;&version=1.1
      </code>
      <p class="url-desc">→ "해리포터"를 제목으로 검색하고 결과를 XML로 받음</p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>2. 왜 SRU가 필요한가?</h2>

  <div class="problem-solution">
    <div class="problem-box">
      <h4>😰 전통적인 문제</h4>
      <ul>
        <li><strong>Z39.50</strong>: 너무 복잡함, 전용 클라이언트 필요</li>
        <li><strong>각자의 API</strong>: 도서관마다 다른 방식</li>
        <li><strong>통합 검색 어려움</strong>: 여러 도서관 검색 힘듦</li>
      </ul>
    </div>

    <div class="arrow-right">→</div>

    <div class="solution-box">
      <h4>✅ SRU의 해결</h4>
      <ul>
        <li><strong>웹 기반</strong>: 브라우저로 바로 사용 가능</li>
        <li><strong>표준화</strong>: 모든 SRU 서버가 같은 방식</li>
        <li><strong>쉬운 통합</strong>: 여러 도서관을 하나의 방식으로</li>
      </ul>
    </div>
  </div>

  <div class="key-features">
    <h4>🌟 SRU의 특징</h4>
    <div class="features-grid">
      <div class="feature">
        <div class="feature-icon">🌐</div>
        <h5>HTTP 기반</h5>
        <p>일반 웹 요청 사용</p>
      </div>
      <div class="feature">
        <div class="feature-icon">📝</div>
        <h5>CQL 쿼리</h5>
        <p>표준 검색 언어</p>
      </div>
      <div class="feature">
        <div class="feature-icon">📄</div>
        <h5>XML 응답</h5>
        <p>구조화된 데이터</p>
      </div>
      <div class="feature">
        <div class="feature-icon">🔧</div>
        <h5>RESTful 스타일</h5>
        <p>간단한 구조</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>3. SRU 요청 구조</h2>

  <h3>📋 기본 파라미터</h3>

  <table class="param-table">
    <thead>
      <tr>
        <th>파라미터</th>
        <th>필수</th>
        <th>설명</th>
        <th>예시</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>operation</strong></td>
        <td>✅</td>
        <td>수행할 작업</td>
        <td>searchRetrieve, explain, scan</td>
      </tr>
      <tr>
        <td><strong>version</strong></td>
        <td>✅</td>
        <td>SRU 버전</td>
        <td>1.1, 1.2, 2.0</td>
      </tr>
      <tr>
        <td><strong>query</strong></td>
        <td>✅</td>
        <td>CQL 검색 쿼리</td>
        <td>dc.title=해리포터</td>
      </tr>
      <tr>
        <td><strong>startRecord</strong></td>
        <td></td>
        <td>시작 레코드 번호</td>
        <td>1 (기본값)</td>
      </tr>
      <tr>
        <td><strong>maximumRecords</strong></td>
        <td></td>
        <td>최대 결과 수</td>
        <td>10 (기본값)</td>
      </tr>
      <tr>
        <td><strong>recordSchema</strong></td>
        <td></td>
        <td>결과 스키마</td>
        <td>marcxml, dc, mods</td>
      </tr>
    </tbody>
  </table>

  <h3>🔍 세 가지 작업(Operation)</h3>

  <div class="operations-grid">
    <div class="operation-card">
      <h4>1️⃣ searchRetrieve</h4>
      <p class="op-desc">검색하고 결과 가져오기</p>
      <div class="op-example">
        <strong>용도:</strong> 책 검색, 자료 찾기<br>
        <strong>가장 많이 사용</strong>
      </div>
    </div>

    <div class="operation-card">
      <h4>2️⃣ explain</h4>
      <p class="op-desc">서버 정보 확인</p>
      <div class="op-example">
        <strong>용도:</strong> 지원 필드, 스키마 확인<br>
        서버가 뭘 할 수 있는지 알려줌
      </div>
    </div>

    <div class="operation-card">
      <h4>3️⃣ scan</h4>
      <p class="op-desc">색인 브라우징</p>
      <div class="op-example">
        <strong>용도:</strong> 가능한 값 목록 보기<br>
        예: "ㄱ"으로 시작하는 저자
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>4. CQL (Contextual Query Language)</h2>

  <p>SRU는 <strong>CQL</strong>이라는 표준 검색 언어를 사용합니다.</p>

  <div class="cql-basics">
    <h4>📝 기본 문법</h4>

    <table class="cql-table">
      <thead>
        <tr>
          <th>유형</th>
          <th>문법</th>
          <th>예시</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>단순 검색</strong></td>
          <td>필드=값</td>
          <td>dc.title=해리포터</td>
        </tr>
        <tr>
          <td><strong>AND 검색</strong></td>
          <td>쿼리1 and 쿼리2</td>
          <td>dc.title=해리 and dc.creator=롤링</td>
        </tr>
        <tr>
          <td><strong>OR 검색</strong></td>
          <td>쿼리1 or 쿼리2</td>
          <td>dc.title=해리포터 or dc.title=반지의제왕</td>
        </tr>
        <tr>
          <td><strong>NOT 검색</strong></td>
          <td>쿼리1 not 쿼리2</td>
          <td>dc.title=해리 not dc.title=포터</td>
        </tr>
        <tr>
          <td><strong>와일드카드</strong></td>
          <td>* (여러 문자), ? (한 문자)</td>
          <td>dc.title=해리*</td>
        </tr>
        <tr>
          <td><strong>구문 검색</strong></td>
          <td>"여러 단어"</td>
          <td>dc.title="해리 포터"</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="cql-examples">
    <h4>💡 실전 예제</h4>

    <div class="example-item">
      <p class="example-query"><strong>제목에 "도서관"이 포함된 책 찾기</strong></p>
      <code>dc.title=도서관</code>
    </div>

    <div class="example-item">
      <p class="example-query"><strong>저자가 "조남주"인 책 찾기</strong></p>
      <code>dc.creator=조남주</code>
    </div>

    <div class="example-item">
      <p class="example-query"><strong>2020년 이후 출판된 책 찾기</strong></p>
      <code>dc.date >= 2020</code>
    </div>

    <div class="example-item">
      <p class="example-query"><strong>제목에 "해리"가 있고 저자가 "롤링"인 책</strong></p>
      <code>dc.title=해리 and dc.creator=롤링</code>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>5. 실제 작동 예제 🚀</h2>

  <div class="live-demo">
    <h3>🌍 실제 도서관 SRU 사용해보기</h3>

    <div class="demo-box">
      <h4>미국 의회도서관 (Library of Congress)</h4>
      <p class="demo-desc">세계 최대 도서관의 SRU를 직접 사용해봅시다!</p>

      <div class="demo-step">
        <p class="step-title"><strong>예제 1: "Harry Potter" 검색</strong></p>
        <div class="url-display">
          <a href="https://lx2.loc.gov:210/lcdb?operation=searchRetrieve&version=1.1&query=dc.title=harry%20potter&maximumRecords=5" target="_blank" class="live-url">
            https://lx2.loc.gov:210/lcdb?operation=searchRetrieve&version=1.1&query=dc.title=harry%20potter&maximumRecords=5
          </a>
        </div>
        <p class="click-instruction">👆 클릭하면 실제 검색 결과(XML)를 볼 수 있습니다!</p>
      </div>

      <div class="demo-step">
        <p class="step-title"><strong>예제 2: 서버 정보 확인 (explain)</strong></p>
        <div class="url-display">
          <a href="https://lx2.loc.gov:210/lcdb?operation=explain&version=1.1" target="_blank" class="live-url">
            https://lx2.loc.gov:210/lcdb?operation=explain&version=1.1
          </a>
        </div>
        <p class="click-instruction">👆 이 서버가 지원하는 기능들을 확인할 수 있습니다!</p>
      </div>
    </div>

    <div class="demo-box">
      <h4>OCLC WorldCat</h4>
      <p class="demo-desc">전 세계 도서관 통합 검색</p>

      <div class="demo-step">
        <p class="step-title"><strong>예제 3: "Einstein" 저자 검색</strong></p>
        <div class="url-display">
          <a href="http://www.worldcat.org/webservices/catalog/search/sru?query=srw.au=einstein&maximumRecords=3" target="_blank" class="live-url">
            http://www.worldcat.org/webservices/catalog/search/sru?query=srw.au=einstein&maximumRecords=3
          </a>
        </div>
        <p class="click-instruction">👆 아인슈타인이 쓴 책을 검색합니다!</p>
      </div>
    </div>

    <div class="how-to-read">
      <h4>📖 결과 읽는 법</h4>
      <ul>
        <li><strong>&lt;numberOfRecords&gt;</strong>: 총 검색 결과 수</li>
        <li><strong>&lt;records&gt;</strong>: 실제 레코드 목록</li>
        <li><strong>&lt;recordData&gt;</strong>: 각 레코드의 메타데이터</li>
        <li>브라우저에서 XML이 보기 어려우면 "페이지 소스 보기" 사용</li>
      </ul>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>6. 다른 프로토콜과 비교</h2>

  <h3>📊 SRU vs 다른 프로토콜</h3>

  <table class="protocol-comparison">
    <thead>
      <tr>
        <th>프로토콜</th>
        <th>목적</th>
        <th>기술</th>
        <th>쿼리</th>
        <th>복잡도</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Z39.50</strong></td>
        <td>도서관 검색</td>
        <td>전용 프로토콜</td>
        <td>Type-1 query</td>
        <td>⭐⭐⭐⭐⭐ 매우 복잡</td>
      </tr>
      <tr class="highlight-row">
        <td><strong>SRU</strong></td>
        <td>도서관 검색</td>
        <td>HTTP GET</td>
        <td>CQL</td>
        <td>⭐⭐ 쉬움</td>
      </tr>
      <tr>
        <td><strong>SRW</strong></td>
        <td>도서관 검색</td>
        <td>SOAP/XML</td>
        <td>CQL</td>
        <td>⭐⭐⭐ 중간</td>
      </tr>
      <tr>
        <td><strong>OAI-PMH</strong></td>
        <td>메타데이터 수확</td>
        <td>HTTP GET</td>
        <td>없음 (ListRecords)</td>
        <td>⭐ 매우 쉬움</td>
      </tr>
      <tr>
        <td><strong>REST API</strong></td>
        <td>다양</td>
        <td>HTTP</td>
        <td>비표준 (각자)</td>
        <td>⭐ ~ ⭐⭐⭐ 다양</td>
      </tr>
    </tbody>
  </table>

  <div class="detailed-comparison">
    <h4>🔍 상세 비교</h4>

    <div class="vs-grid">
      <div class="vs-card">
        <h5>SRU vs Z39.50</h5>
        <table class="mini-table">
          <tr>
            <th>Z39.50</th>
            <th>SRU</th>
          </tr>
          <tr>
            <td>전용 클라이언트 필요</td>
            <td>웹 브라우저로 가능</td>
          </tr>
          <tr>
            <td>복잡한 프로토콜</td>
            <td>간단한 URL</td>
          </tr>
          <tr>
            <td>1990년대 표준</td>
            <td>2000년대 표준</td>
          </tr>
        </table>
        <p class="summary"><strong>SRU = 현대화된 Z39.50</strong></p>
      </div>

      <div class="vs-card">
        <h5>SRU vs OAI-PMH</h5>
        <table class="mini-table">
          <tr>
            <th>SRU</th>
            <th>OAI-PMH</th>
          </tr>
          <tr>
            <td>검색 (Search)</td>
            <td>수확 (Harvest)</td>
          </tr>
          <tr>
            <td>복잡한 쿼리 가능</td>
            <td>쿼리 없음</td>
          </tr>
          <tr>
            <td>실시간 검색</td>
            <td>대량 수집</td>
          </tr>
        </table>
        <p class="summary"><strong>용도가 완전히 다름</strong></p>
      </div>

      <div class="vs-card">
        <h5>SRU vs REST API</h5>
        <table class="mini-table">
          <tr>
            <th>SRU</th>
            <th>REST API</th>
          </tr>
          <tr>
            <td>표준화됨</td>
            <td>비표준 (각자)</td>
          </tr>
          <tr>
            <td>도서관 전용</td>
            <td>범용</td>
          </tr>
          <tr>
            <td>XML 응답</td>
            <td>JSON/XML 등</td>
          </tr>
        </table>
        <p class="summary"><strong>SRU = 도서관 특화 REST</strong></p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>7. 언제 SRU를 사용하나요?</h2>

  <div class="use-cases">
    <div class="usecase-box yes">
      <h4>✅ SRU가 적합한 경우</h4>
      <ul>
        <li><strong>통합 검색</strong>: 여러 도서관을 하나로 검색</li>
        <li><strong>메타 검색</strong>: 다양한 소스 동시 검색</li>
        <li><strong>프로그래밍</strong>: 자동화된 검색 시스템</li>
        <li><strong>웹 서비스</strong>: 도서관 검색 API 제공</li>
        <li><strong>Z39.50 대체</strong>: 복잡한 Z39.50 대신</li>
      </ul>
    </div>

    <div class="usecase-box no">
      <h4>❌ SRU가 부적합한 경우</h4>
      <ul>
        <li><strong>대량 수집</strong>: OAI-PMH 사용</li>
        <li><strong>단일 도서관 내부</strong>: REST API로 충분</li>
        <li><strong>복잡한 워크플로</strong>: 전용 시스템 필요</li>
        <li><strong>실시간 업데이트 필요</strong>: WebSocket 등</li>
      </ul>
    </div>
  </div>

  <div class="real-usage">
    <h4>🌍 실제 사용 사례</h4>
    <div class="usage-grid">
      <div class="usage-item">
        <h5>📚 대학 도서관 통합검색</h5>
        <p>여러 대학의 SRU를 연결하여 한 번에 검색</p>
      </div>
      <div class="usage-item">
        <h5>🔍 메타 검색 엔진</h5>
        <p>국내외 도서관 동시 검색 서비스</p>
      </div>
      <div class="usage-item">
        <h5>📖 디지털 도서관</h5>
        <p>다양한 컬렉션 통합 인터페이스</p>
      </div>
      <div class="usage-item">
        <h5>🤖 자동화 시스템</h5>
        <p>수서, 목록 자동화에 활용</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>8. SRU 구현하기</h2>

  <div class="implementation">
    <h4>🔧 SRU 서버 구축</h4>
    <p>도서관이 SRU 서버를 제공하려면:</p>

    <div class="impl-steps">
      <div class="impl-step">
        <div class="step-num">1</div>
        <div class="step-content">
          <h5>SRU 서버 소프트웨어 선택</h5>
          <ul>
            <li>IndexData의 YAZ (오픈소스)</li>
            <li>상용 ILS에 내장된 SRU</li>
            <li>직접 구현 (SRU 스펙 따라)</li>
          </ul>
        </div>
      </div>

      <div class="impl-step">
        <div class="step-num">2</div>
        <div class="step-content">
          <h5>데이터베이스 연결</h5>
          <ul>
            <li>MARC 레코드 DB</li>
            <li>검색 인덱스 생성</li>
          </ul>
        </div>
      </div>

      <div class="impl-step">
        <div class="step-num">3</div>
        <div class="step-content">
          <h5>CQL 쿼리 처리기 설정</h5>
          <ul>
            <li>지원 필드 정의 (dc.title, dc.creator 등)</li>
            <li>CQL → SQL 변환</li>
          </ul>
        </div>
      </div>

      <div class="impl-step">
        <div class="step-num">4</div>
        <div class="step-content">
          <h5>응답 포맷 설정</h5>
          <ul>
            <li>MARCXML, Dublin Core, MODS 등</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <div class="client-code">
    <h4>💻 클라이언트 코드 예제 (Python)</h4>
    <pre class="code-block">
import requests
import xml.etree.ElementTree as ET

# SRU 검색 함수
def sru_search(base_url, query, max_records=10):
    params = {
        'operation': 'searchRetrieve',
        'version': '1.1',
        'query': query,
        'maximumRecords': max_records
    }

    response = requests.get(base_url, params=params)
    return response.text

# 사용 예제
base_url = 'https://lx2.loc.gov:210/lcdb'
query = 'dc.title=python'
results = sru_search(base_url, query)

print(results)
    </pre>
  </div>
</div>

<div class="content-section">
  <h2>9. 요약: 한눈에 정리</h2>

  <div class="summary-grid">
    <div class="summary-main">
      <h3>🔍 SRU란?</h3>
      <p class="definition">URL로 도서관을 검색하는 표준 프로토콜</p>

      <div class="key-points">
        <div class="point">
          <strong>기술:</strong> HTTP GET + CQL 쿼리
        </div>
        <div class="point">
          <strong>응답:</strong> XML (MARCXML, DC, MODS 등)
        </div>
        <div class="point">
          <strong>장점:</strong> 표준화, 쉬움, 웹 기반
        </div>
      </div>
    </div>

    <div class="summary-operations">
      <h4>3가지 작업</h4>
      <ol>
        <li><strong>searchRetrieve</strong> - 검색</li>
        <li><strong>explain</strong> - 서버 정보</li>
        <li><strong>scan</strong> - 색인 브라우징</li>
      </ol>
    </div>
  </div>

  <div class="final-takeaway">
    <h3>🎯 핵심 메시지</h3>
    <div class="takeaway-content">
      <p class="big-text">
        <strong>SRU = Z39.50의 현대판</strong>
      </p>
      <p>복잡한 Z39.50 대신, <strong>웹 브라우저로 바로</strong> 사용할 수 있는<br>
      표준화된 도서관 검색 프로토콜입니다.</p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>10. 학습 점검 퀴즈</h2>

  <div class="quiz-section">
    <div class="quiz-item">
      <p><strong>Q1.</strong> SRU를 한 문장으로 설명하면?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>URL만으로 도서관 검색을 할 수 있는 표준 검색 프로토콜</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> SRU에서 사용하는 쿼리 언어는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>CQL (Contextual Query Language)</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> SRU의 3가지 작업(operation)은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>searchRetrieve (검색), explain (서버 정보), scan (색인 브라우징)</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> SRU와 Z39.50의 가장 큰 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ SRU는 <strong>웹 기반(HTTP)</strong>으로 브라우저로 바로 사용 가능하지만, Z39.50은 <strong>전용 클라이언트</strong>가 필요함</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> SRU와 OAI-PMH의 주요 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ SRU는 <strong>검색(Search)</strong> 용도, OAI-PMH는 <strong>메타데이터 수확(Harvest)</strong> 용도</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q6.</strong> "제목에 해리가 있고 저자가 롤링인 책"을 찾는 CQL은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>dc.title=해리 and dc.creator=롤링</strong></p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 더 알아보기</h2>
  <ul>
    <li><strong>SRU 공식 사이트</strong> - Library of Congress SRU/SRW 문서</li>
    <li><strong>CQL 스펙</strong> - Contextual Query Language 상세 가이드</li>
    <li><strong>SRU Implementations</strong> - 다양한 SRU 서버 소프트웨어</li>
    <li><strong>YAZ Toolkit</strong> - IndexData의 오픈소스 Z39.50/SRU 도구</li>
    <li><strong>WorldCat SRU</strong> - OCLC WorldCat SRU API 문서</li>
  </ul>
</div>

<style>
.content-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.hero-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2.5rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
}

.hero-box h3,
.hero-box p {
  color: white;
}

.big-definition {
  font-size: 1.4rem;
  line-height: 1.8;
  margin: 1rem 0;
}

.simple-demo {
  background: #e8f5e9;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.url-example {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.url-label {
  font-weight: bold;
  color: #1976d2;
  margin-bottom: 0.75rem;
}

.url-box {
  display: block;
  background: #263238;
  color: #aed581;
  padding: 1rem;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.9rem;
  margin: 0.75rem 0;
  overflow-x: auto;
}

.url-desc {
  color: #666;
  font-size: 0.95rem;
  margin-top: 0.75rem;
}

.problem-solution {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1.5rem;
  align-items: center;
  margin: 2rem 0;
}

.problem-box {
  background: #ffebee;
  border: 2px solid #f44336;
  padding: 1.5rem;
  border-radius: 8px;
}

.solution-box {
  background: #e8f5e9;
  border: 2px solid #4caf50;
  padding: 1.5rem;
  border-radius: 8px;
}

.arrow-right {
  font-size: 2rem;
  color: #4caf50;
  font-weight: bold;
}

.key-features {
  background: #e3f2fd;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.feature {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  border: 2px solid #ddd;
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.feature h5 {
  color: #1976d2;
  margin: 0.5rem 0;
}

.param-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  background: white;
}

.param-table th,
.param-table td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.param-table th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.param-table tr:nth-child(even) {
  background: #f5f5f5;
}

.operations-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

.operation-card {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
}

.operation-card h4 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.op-desc {
  font-weight: bold;
  color: #333;
  margin: 0.5rem 0;
}

.op-example {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.cql-basics {
  margin: 2rem 0;
}

.cql-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.cql-table th,
.cql-table td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.cql-table th {
  background: #4caf50;
  color: white;
  font-weight: bold;
}

.cql-table td code {
  background: #263238;
  color: #aed581;
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  font-family: monospace;
}

.cql-examples {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.example-item {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
  border-left: 4px solid #ff9800;
}

.example-query {
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
}

.example-item code {
  display: block;
  background: #263238;
  color: #aed581;
  padding: 0.75rem;
  border-radius: 4px;
  font-family: monospace;
  margin-top: 0.5rem;
}

.live-demo {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.live-demo h3,
.live-demo h4,
.live-demo p {
  color: white;
}

.demo-box {
  background: rgba(255,255,255,0.1);
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1.5rem 0;
}

.demo-desc {
  font-size: 0.95rem;
  margin: 0.5rem 0 1rem 0;
}

.demo-step {
  background: white;
  color: #333;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.step-title {
  font-weight: bold;
  color: #1976d2;
  margin-bottom: 0.75rem;
}

.url-display {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin: 0.5rem 0;
  overflow-x: auto;
}

.live-url {
  color: #1976d2;
  text-decoration: underline;
  word-break: break-all;
  font-family: monospace;
  font-size: 0.9rem;
}

.live-url:hover {
  color: #0d47a1;
}

.click-instruction {
  color: #666;
  font-size: 0.9rem;
  font-style: italic;
  margin-top: 0.5rem;
}

.how-to-read {
  background: white;
  color: #333;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1.5rem;
}

.how-to-read h4 {
  color: #1976d2;
}

.protocol-comparison {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  background: white;
}

.protocol-comparison th,
.protocol-comparison td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.protocol-comparison th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.highlight-row {
  background: #fff3e0;
  font-weight: bold;
}

.detailed-comparison {
  margin: 2rem 0;
}

.vs-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.vs-card {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
}

.vs-card h5 {
  color: #1976d2;
  text-align: center;
  margin-bottom: 1rem;
}

.mini-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.mini-table th,
.mini-table td {
  border: 1px solid #ddd;
  padding: 0.75rem;
  text-align: center;
}

.mini-table th {
  background: #f5f5f5;
  font-weight: bold;
}

.summary {
  text-align: center;
  font-weight: bold;
  color: #ff9800;
  margin-top: 1rem;
  padding: 0.75rem;
  background: #fff3e0;
  border-radius: 4px;
}

.use-cases {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.usecase-box {
  padding: 1.5rem;
  border-radius: 8px;
}

.usecase-box.yes {
  background: #e8f5e9;
  border: 3px solid #4caf50;
}

.usecase-box.no {
  background: #ffebee;
  border: 3px solid #f44336;
}

.real-usage {
  background: #e3f2fd;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.usage-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.usage-item {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
}

.usage-item h5 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.implementation {
  margin: 2rem 0;
}

.impl-steps {
  margin-top: 1.5rem;
}

.impl-step {
  display: flex;
  gap: 1.5rem;
  align-items: start;
  margin: 1rem 0;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #2196f3;
}

.step-num {
  width: 50px;
  height: 50px;
  background: #2196f3;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h5 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.client-code {
  background: #263238;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.client-code h4 {
  color: #aed581;
  margin-bottom: 1rem;
}

.code-block {
  background: transparent;
  color: #aed581;
  padding: 0;
  border-radius: 0;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
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
  border: 3px solid #1976d2;
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

.summary-operations {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
}

.summary-operations ol {
  margin-top: 1rem;
}

.final-takeaway {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
}

.final-takeaway h3,
.final-takeaway p {
  color: white;
}

.takeaway-content {
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

@media (max-width: 1024px) {
  .features-grid,
  .operations-grid,
  .vs-grid,
  .usage-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .problem-solution,
  .features-grid,
  .operations-grid,
  .use-cases,
  .summary-grid,
  .vs-grid,
  .usage-grid {
    grid-template-columns: 1fr;
  }

  .arrow-right {
    transform: rotate(90deg);
  }
}
</style>
        """,
        category=sru_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=35,
        prerequisites="HTTP 기본 이해, XML 기초 지식",
        learning_objectives="SRU 프로토콜의 목적과 구조 이해하기, CQL 쿼리 작성법 익히기, SRU와 다른 프로토콜의 차이점 파악하기, 실제 도서관 SRU를 사용하여 검색해보기, SRU의 적절한 사용처 판단하기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {sru_category.name} (상위: {search_protocol_category.name})")
    print(f"  - 난이도: 중급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=search-protocol")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_sru_content()
