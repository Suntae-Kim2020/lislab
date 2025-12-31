#!/usr/bin/env python
"""
Z39.50 학습 콘텐츠 추가 스크립트
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

def create_z3950_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 가져오기: 검색 프로토콜
    search_protocol_category = Category.objects.get(slug='search-protocol')
    print("✓ 상위 카테고리 확인: 검색 프로토콜")

    # 하위 카테고리 생성 또는 가져오기: Z39.50
    z3950_category, created = Category.objects.get_or_create(
        slug='z3950',
        defaults={
            'name': 'Z39.50',
            'description': 'Z39.50 도서관 검색 프로토콜',
            'parent': search_protocol_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: Z39.50")
    else:
        print("✓ 하위 카테고리 확인: Z39.50")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': 'Z39.50', 'slug': 'z3950'},
        {'name': 'NISO', 'slug': 'niso'},
        {'name': 'ISO 23950', 'slug': 'iso-23950'},
        {'name': '도서관 프로토콜', 'slug': 'library-protocol'},
        {'name': '검색 프로토콜', 'slug': 'search-protocol'},
        {'name': 'ASN.1', 'slug': 'asn1'},
        {'name': 'BER', 'slug': 'ber'},
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
        title="Z39.50: 도서관 검색의 시작",
        slug="z3950-library-search-protocol",
        summary="모든 도서관 검색 프로토콜의 할아버지 Z39.50! 1990년대부터 지금까지 도서관을 연결해온 이 프로토콜이 무엇인지, 왜 탄생했는지, 어떻게 작동하는지 배웁니다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>Z39.50이 왜 만들어졌는지 이해하기</li>
    <li>Z39.50의 기본 개념과 구조 파악하기</li>
    <li>Z39.50의 주요 작업(Operation) 이해하기</li>
    <li>Z39.50과 현대 프로토콜(SRU, SRW, REST API)의 차이점 알기</li>
    <li>Z39.50의 현재 위치와 미래 전망 이해하기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. Z39.50을 한 문장으로</h2>

  <div class="hero-definition">
    <h3>🔍 Z39.50이란?</h3>
    <p class="big-statement">
      <strong>Z39.50</strong>은 <strong>도서관끼리 서지 데이터를 검색하고 공유</strong>하기 위해<br>
      1990년대에 만들어진 <strong>국제 표준 통신 프로토콜</strong>입니다.
    </p>
  </div>

  <div class="origin-story">
    <h4>📖 탄생 배경</h4>
    <div class="story-box">
      <div class="problem-box">
        <h5>😫 1980년대 문제</h5>
        <p><strong>도서관마다 시스템이 제각각!</strong></p>
        <ul>
          <li>A 도서관: 자체 시스템으로 검색</li>
          <li>B 도서관: 다른 시스템으로 검색</li>
          <li>C 도서관: 또 다른 방식...</li>
        </ul>
        <p class="pain-point">💔 <strong>한 번에 여러 도서관을 검색할 수 없었습니다!</strong></p>
      </div>

      <div class="solution-arrow">⬇️ 해결책</div>

      <div class="solution-box">
        <h5>💡 Z39.50 솔루션 (1988~)</h5>
        <p><strong>"공통 언어를 만들자!"</strong></p>
        <ul>
          <li>✅ 표준 프로토콜로 통일</li>
          <li>✅ 한 번에 여러 도서관 검색</li>
          <li>✅ 서로 다른 시스템도 연결</li>
        </ul>
        <p class="success-point">💚 <strong>세계 도서관들이 하나로 연결!</strong></p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>2. Z39.50의 이름 뜻</h2>

  <div class="name-explanation">
    <div class="name-parts">
      <div class="name-part">
        <div class="letter">Z39</div>
        <div class="meaning">
          <strong>NISO 표준 시리즈</strong>
          <p>미국국가정보표준기구<br>(National Information Standards Organization)</p>
        </div>
      </div>

      <div class="name-separator">.</div>

      <div class="name-part">
        <div class="letter">50</div>
        <div class="meaning">
          <strong>번호</strong>
          <p>50번째 표준</p>
        </div>
      </div>
    </div>

    <div class="also-known">
      <h4>🌐 다른 이름</h4>
      <div class="aliases">
        <div class="alias-box">
          <strong>ISO 23950</strong>
          <p>국제 표준 버전</p>
        </div>
        <div class="alias-box">
          <strong>ANSI/NISO Z39.50</strong>
          <p>미국 표준 버전</p>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>3. Z39.50의 기본 구조</h2>

  <h3>🏗️ 클라이언트-서버 모델</h3>

  <div class="architecture-diagram">
    <div class="arch-row">
      <div class="arch-box client-box">
        <h4>클라이언트 (Origin)</h4>
        <p class="role">검색 요청하는 쪽</p>
        <div class="examples">
          <p><strong>예시:</strong></p>
          <ul>
            <li>도서관 사서의 검색 프로그램</li>
            <li>통합검색 시스템</li>
            <li>목록 작성 도구</li>
          </ul>
        </div>
      </div>

      <div class="connection-arrows">
        <div class="arrow-down">⬇️ 검색 요청</div>
        <div class="arrow-up">⬆️ 검색 결과</div>
      </div>

      <div class="arch-box server-box">
        <h4>서버 (Target)</h4>
        <p class="role">검색 처리하는 쪽</p>
        <div class="examples">
          <p><strong>예시:</strong></p>
          <ul>
            <li>도서관 목록 시스템</li>
            <li>서지 데이터베이스</li>
            <li>국가 도서관 서버</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <h3>🔧 기술 스택</h3>

  <div class="tech-stack-grid">
    <div class="tech-card">
      <div class="tech-icon">📡</div>
      <h4>전송 프로토콜</h4>
      <p><strong>TCP/IP</strong></p>
      <p class="tech-detail">인터넷 통신 기본 프로토콜</p>
      <p class="default-port">기본 포트: <code>210</code></p>
    </div>

    <div class="tech-card">
      <div class="tech-icon">📦</div>
      <h4>인코딩</h4>
      <p><strong>ASN.1 / BER</strong></p>
      <p class="tech-detail">데이터 구조 표현 언어<br>(Abstract Syntax Notation)</p>
      <p class="vs-modern">vs 현대: JSON, XML</p>
    </div>

    <div class="tech-card">
      <div class="tech-icon">📋</div>
      <h4>속성 집합</h4>
      <p><strong>Bib-1</strong></p>
      <p class="tech-detail">검색 가능한 필드 정의<br>(제목, 저자, ISBN 등)</p>
      <p class="most-common">가장 많이 사용됨</p>
    </div>
  </div>

  <div class="tech-note">
    <h4>💡 왜 이렇게 복잡할까?</h4>
    <p>Z39.50은 <strong>1980년대 후반에 설계</strong>되었습니다. 당시엔 XML도, JSON도 없었고, 웹도 막 시작하던 시기였어요. 그래서 당시 최고의 기술인 <strong>ASN.1/BER</strong>을 사용했습니다.</p>
    <div class="timeline-compare">
      <div class="year-box">
        <strong>1988</strong>
        <p>Z39.50 첫 버전</p>
      </div>
      <div class="vs-arrow">vs</div>
      <div class="year-box">
        <strong>1991</strong>
        <p>웹(WWW) 탄생</p>
      </div>
      <div class="vs-arrow">vs</div>
      <div class="year-box">
        <strong>1998</strong>
        <p>XML 표준화</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>4. Z39.50의 주요 작업(Operations)</h2>

  <div class="operations-intro">
    <p>Z39.50은 여러 가지 작업을 지원하지만, 가장 중요한 것은 <strong>3가지</strong>입니다:</p>
  </div>

  <div class="operations-grid">
    <div class="op-card search-op">
      <div class="op-number">1</div>
      <h4>Search</h4>
      <p class="op-name">검색 요청</p>

      <div class="op-detail">
        <p><strong>무엇을:</strong> 서버에 검색 쿼리 보내기</p>
        <p><strong>예시:</strong> "해리포터" 검색</p>

        <div class="op-flow">
          <div class="flow-item">
            <strong>클라이언트</strong>
            <p>"title=harry potter"</p>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-item">
            <strong>서버</strong>
            <p>"245건 찾았어요"</p>
          </div>
        </div>

        <div class="important-note">
          <p>⚠️ Search는 <strong>결과의 개수만</strong> 알려줍니다!<br>
          실제 데이터는 Present로 가져와야 해요.</p>
        </div>
      </div>
    </div>

    <div class="op-card present-op">
      <div class="op-number">2</div>
      <h4>Present</h4>
      <p class="op-name">결과 가져오기</p>

      <div class="op-detail">
        <p><strong>무엇을:</strong> 검색 결과 실제 데이터 요청</p>
        <p><strong>예시:</strong> "1번째부터 10개 주세요"</p>

        <div class="op-flow">
          <div class="flow-item">
            <strong>클라이언트</strong>
            <p>"1~10번 레코드 주세요"</p>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-item">
            <strong>서버</strong>
            <p>"여기 MARC 레코드 10개"</p>
          </div>
        </div>

        <div class="format-note">
          <p><strong>받을 수 있는 형식:</strong></p>
          <ul>
            <li>MARC21 (가장 일반적)</li>
            <li>Dublin Core</li>
            <li>SUTRS (간단한 텍스트)</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="op-card scan-op">
      <div class="op-number">3</div>
      <h4>Scan</h4>
      <p class="op-name">색인 탐색</p>

      <div class="op-detail">
        <p><strong>무엇을:</strong> 검색어 주변의 용어 목록 보기</p>
        <p><strong>예시:</strong> "har"로 시작하는 제목들</p>

        <div class="op-flow">
          <div class="flow-item">
            <strong>클라이언트</strong>
            <p>"title=har*"</p>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-item">
            <strong>서버</strong>
            <p>Harbor (15건)<br>
            Hardy (8건)<br>
            Harry Potter (245건)</p>
          </div>
        </div>

        <div class="use-case">
          <p><strong>언제 유용?</strong></p>
          <p>📚 사서가 정확한 표목을 찾을 때<br>
          🔍 브라우징하듯 탐색할 때</p>
        </div>
      </div>
    </div>
  </div>

  <div class="typical-session">
    <h4>🔄 일반적인 Z39.50 세션 흐름</h4>
    <div class="session-flow">
      <div class="session-step">
        <div class="step-num">1</div>
        <div class="step-content">
          <strong>Init</strong>
          <p>연결 초기화 및 설정</p>
        </div>
      </div>
      <div class="session-arrow">⬇️</div>
      <div class="session-step">
        <div class="step-num">2</div>
        <div class="step-content">
          <strong>Search</strong>
          <p>"해리포터" 검색 → "245건"</p>
        </div>
      </div>
      <div class="session-arrow">⬇️</div>
      <div class="session-step">
        <div class="step-num">3</div>
        <div class="step-content">
          <strong>Present</strong>
          <p>1~10번 레코드 가져오기</p>
        </div>
      </div>
      <div class="session-arrow">⬇️</div>
      <div class="session-step">
        <div class="step-num">4</div>
        <div class="step-content">
          <strong>Present</strong>
          <p>11~20번 레코드 가져오기</p>
        </div>
      </div>
      <div class="session-arrow">⬇️</div>
      <div class="session-step">
        <div class="step-num">5</div>
        <div class="step-content">
          <strong>Close</strong>
          <p>연결 종료</p>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>5. Z39.50 vs 현대 프로토콜</h2>

  <table class="protocol-comparison">
    <thead>
      <tr>
        <th>항목</th>
        <th>Z39.50</th>
        <th>SRU/SRW</th>
        <th>REST API</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>탄생 시기</strong></td>
        <td>1988년</td>
        <td>2002년</td>
        <td>2000년대~</td>
      </tr>
      <tr>
        <td><strong>기반 기술</strong></td>
        <td>TCP/IP 직접</td>
        <td>HTTP</td>
        <td>HTTP</td>
      </tr>
      <tr>
        <td><strong>데이터 형식</strong></td>
        <td>ASN.1/BER</td>
        <td>XML</td>
        <td>JSON (주로)</td>
      </tr>
      <tr>
        <td><strong>복잡도</strong></td>
        <td>⭐⭐⭐⭐⭐</td>
        <td>⭐⭐⭐</td>
        <td>⭐⭐</td>
      </tr>
      <tr>
        <td><strong>방화벽 통과</strong></td>
        <td>❌ 어려움 (포트 210)</td>
        <td>✅ 쉬움 (HTTP)</td>
        <td>✅ 쉬움 (HTTP)</td>
      </tr>
      <tr>
        <td><strong>브라우저 테스트</strong></td>
        <td>❌ 불가능</td>
        <td>✅ SRU는 가능</td>
        <td>✅ GET은 가능</td>
      </tr>
      <tr>
        <td><strong>개발 난이도</strong></td>
        <td>⭐⭐⭐⭐⭐ 매우 어려움</td>
        <td>⭐⭐⭐ 보통</td>
        <td>⭐⭐ 쉬움</td>
      </tr>
      <tr>
        <td><strong>기능 풍부도</strong></td>
        <td>⭐⭐⭐⭐⭐ 매우 많음</td>
        <td>⭐⭐⭐⭐ 많음</td>
        <td>⭐⭐⭐ 상황에 따라</td>
      </tr>
      <tr>
        <td><strong>도서관 전문성</strong></td>
        <td>⭐⭐⭐⭐⭐</td>
        <td>⭐⭐⭐⭐</td>
        <td>⭐⭐ 범용적</td>
      </tr>
      <tr>
        <td><strong>현재 사용</strong></td>
        <td>⚠️ 감소 중</td>
        <td>✅ 활발</td>
        <td>✅ 매우 활발</td>
      </tr>
    </tbody>
  </table>

  <div class="comparison-insight">
    <h4>🎯 핵심 차이</h4>
    <div class="insight-grid">
      <div class="insight-box z-box">
        <h5>Z39.50</h5>
        <p class="summary">강력하고 전문적이지만 복잡</p>
        <ul>
          <li>✅ 매우 풍부한 기능</li>
          <li>✅ 도서관에 특화</li>
          <li>❌ 개발이 어려움</li>
          <li>❌ 방화벽 문제</li>
          <li>❌ 웹 친화적이지 않음</li>
        </ul>
      </div>

      <div class="insight-box sru-box">
        <h5>SRU/SRW</h5>
        <p class="summary">Z39.50을 웹으로 현대화</p>
        <ul>
          <li>✅ HTTP 기반</li>
          <li>✅ 도서관에 특화</li>
          <li>✅ 방화벽 통과</li>
          <li>⚠️ Z39.50보다 기능 적음</li>
        </ul>
      </div>

      <div class="insight-box rest-box">
        <h5>REST API</h5>
        <p class="summary">간단하고 현대적이지만 표준 없음</p>
        <ul>
          <li>✅ 매우 간단</li>
          <li>✅ JSON으로 편리</li>
          <li>✅ 웹 친화적</li>
          <li>❌ 도서관 표준 없음</li>
          <li>❌ 각자 다르게 구현</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>6. Z39.50 사용 예시</h2>

  <div class="usage-examples">
    <h3>💻 Python으로 Z39.50 검색하기</h3>

    <div class="code-example">
      <h4>🔧 라이브러리 설치</h4>
      <pre class="code-block">
pip install PyZ3950
      </pre>
    </div>

    <div class="code-example">
      <h4>📝 기본 검색 코드</h4>
      <pre class="code-block">
from PyZ3950 import zoom

# Z39.50 연결 생성
conn = zoom.Connection('z3950.loc.gov', 7090)
conn.databaseName = 'VOYAGER'

# 검색 실행
query = zoom.Query('CCL', 'ti=python')
result = conn.search(query)

# 결과 출력
print(f'총 {len(result)}건 발견')

# 처음 5개 레코드 가져오기
for i in range(min(5, len(result))):
    record = result[i]
    print(f'\n레코드 {i+1}:')
    print(record.data)

# 연결 종료
conn.close()
      </pre>
    </div>

    <div class="example-explanation">
      <h4>📖 코드 설명</h4>
      <table class="code-table">
        <tr>
          <th>코드</th>
          <th>설명</th>
        </tr>
        <tr>
          <td><code>zoom.Connection</code></td>
          <td>Z39.50 서버에 연결</td>
        </tr>
        <tr>
          <td><code>z3950.loc.gov:7090</code></td>
          <td>미국 의회도서관 Z39.50 서버</td>
        </tr>
        <tr>
          <td><code>databaseName</code></td>
          <td>검색할 데이터베이스 지정</td>
        </tr>
        <tr>
          <td><code>CCL</code></td>
          <td>Common Command Language (검색 문법)</td>
        </tr>
        <tr>
          <td><code>ti=python</code></td>
          <td>제목(title)에 "python" 포함</td>
        </tr>
      </table>
    </div>
  </div>

  <div class="real-world-servers">
    <h4>🌐 실제 Z39.50 서버들</h4>
    <div class="servers-grid">
      <div class="server-card">
        <h5>🇺🇸 미국 의회도서관</h5>
        <div class="server-info">
          <p><strong>Host:</strong> <code>z3950.loc.gov</code></p>
          <p><strong>Port:</strong> <code>7090</code></p>
          <p><strong>Database:</strong> VOYAGER</p>
        </div>
      </div>

      <div class="server-card">
        <h5>🇰🇷 국립중앙도서관</h5>
        <div class="server-info">
          <p><strong>Host:</strong> <code>www.nl.go.kr</code></p>
          <p><strong>Port:</strong> <code>9909</code></p>
          <p><strong>Database:</strong> KOLIS</p>
        </div>
      </div>

      <div class="server-card">
        <h5>🇬🇧 영국 국립도서관</h5>
        <div class="server-info">
          <p><strong>Host:</strong> <code>z3950cat.bl.uk</code></p>
          <p><strong>Port:</strong> <code>9909</code></p>
          <p><strong>Database:</strong> BLAC</p>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>7. Z39.50의 장단점</h2>

  <div class="pros-cons-grid">
    <div class="pros-section">
      <h3>✅ 장점</h3>
      <div class="pros-list">
        <div class="pro-item">
          <div class="pro-icon">🌍</div>
          <div class="pro-content">
            <h4>국제 표준</h4>
            <p>전 세계 도서관들이 같은 방식으로 통신</p>
          </div>
        </div>

        <div class="pro-item">
          <div class="pro-icon">💪</div>
          <div class="pro-content">
            <h4>매우 강력한 기능</h4>
            <p>복잡한 검색, 정렬, 필터링 등 풍부한 기능</p>
          </div>
        </div>

        <div class="pro-item">
          <div class="pro-icon">📚</div>
          <div class="pro-content">
            <h4>도서관에 특화</h4>
            <p>서지 데이터 검색에 최적화된 설계</p>
          </div>
        </div>

        <div class="pro-item">
          <div class="pro-icon">🔄</div>
          <div class="pro-content">
            <h4>세션 유지</h4>
            <p>상태를 유지하며 복잡한 작업 가능</p>
          </div>
        </div>

        <div class="pro-item">
          <div class="pro-icon">📋</div>
          <div class="pro-content">
            <h4>MARC 지원</h4>
            <p>MARC21 레코드를 직접 주고받음</p>
          </div>
        </div>
      </div>
    </div>

    <div class="cons-section">
      <h3>❌ 단점</h3>
      <div class="cons-list">
        <div class="con-item">
          <div class="con-icon">😰</div>
          <div class="con-content">
            <h4>매우 복잡함</h4>
            <p>배우고 구현하기 어려운 프로토콜</p>
          </div>
        </div>

        <div class="con-item">
          <div class="con-icon">🧱</div>
          <div class="con-content">
            <h4>방화벽 문제</h4>
            <p>전용 포트(210) 사용으로 차단되기 쉬움</p>
          </div>
        </div>

        <div class="con-item">
          <div class="con-icon">🌐</div>
          <div class="con-content">
            <h4>웹 비친화적</h4>
            <p>HTTP가 아니라 웹 환경에 맞지 않음</p>
          </div>
        </div>

        <div class="con-item">
          <div class="con-icon">📱</div>
          <div class="con-content">
            <h4>모바일 부적합</h4>
            <p>모던 웹/모바일 앱과 통합 어려움</p>
          </div>
        </div>

        <div class="con-item">
          <div class="con-icon">⏰</div>
          <div class="con-content">
            <h4>오래된 기술</h4>
            <p>1980년대 기술 스택 사용</p>
          </div>
        </div>

        <div class="con-item">
          <div class="con-icon">👥</div>
          <div class="con-content">
            <h4>개발자 부족</h4>
            <p>젊은 개발자들이 배우지 않음</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>8. Z39.50의 현재와 미래</h2>

  <div class="current-status">
    <h3>📊 현재 상황</h3>

    <div class="status-grid">
      <div class="status-card still-used">
        <h4>✅ 여전히 사용 중</h4>
        <ul>
          <li><strong>대형 도서관:</strong> 국립도서관, 대학도서관</li>
          <li><strong>ILL (상호대차):</strong> 도서관 간 자료 공유</li>
          <li><strong>레거시 시스템:</strong> 오래된 도서관 시스템</li>
          <li><strong>목록 작성:</strong> 사서들의 MARC 레코드 복사</li>
        </ul>
      </div>

      <div class="status-card declining">
        <h4>📉 사용 감소 중</h4>
        <ul>
          <li>신규 프로젝트는 SRU/REST API 선택</li>
          <li>복잡도 때문에 유지보수 어려움</li>
          <li>웹 환경에 맞지 않음</li>
          <li>젊은 개발자들의 기피</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="evolution-path">
    <h4>📈 프로토콜 진화 과정</h4>
    <div class="evolution-timeline">
      <div class="evo-step z-step">
        <div class="evo-year">1988~2000년대</div>
        <div class="evo-tech">Z39.50</div>
        <div class="evo-role">도서관 검색의 유일한 표준</div>
        <div class="evo-status">👑 전성기</div>
      </div>

      <div class="evo-arrow">→</div>

      <div class="evo-step sru-step">
        <div class="evo-year">2002~현재</div>
        <div class="evo-tech">SRU/SRW</div>
        <div class="evo-role">Z39.50의 웹 버전</div>
        <div class="evo-status">📈 성장 중</div>
      </div>

      <div class="evo-arrow">→</div>

      <div class="evo-step rest-step">
        <div class="evo-year">2010년대~미래</div>
        <div class="evo-tech">REST API</div>
        <div class="evo-role">범용 웹 API</div>
        <div class="evo-status">🚀 주류</div>
      </div>
    </div>
  </div>

  <div class="future-outlook">
    <h4>🔮 앞으로는?</h4>
    <div class="outlook-content">
      <div class="scenario-box">
        <h5>예상 시나리오</h5>
        <ul>
          <li>✅ <strong>기존 시스템 유지:</strong> 당분간 계속 사용</li>
          <li>⚠️ <strong>신규 개발 없음:</strong> 새 프로젝트는 SRU/REST</li>
          <li>📉 <strong>점진적 감소:</strong> 시스템 교체하면서 줄어듦</li>
          <li>🔄 <strong>변환 계층:</strong> Z39.50 ↔ REST 브릿지 등장</li>
        </ul>
      </div>

      <div class="recommendation-box">
        <h5>💡 추천</h5>
        <table class="recommendation-table">
          <tr>
            <td><strong>사서/도서관 직원</strong></td>
            <td>개념만 알아두기 (실무에서 만날 수 있음)</td>
          </tr>
          <tr>
            <td><strong>신규 개발자</strong></td>
            <td>SRU/REST API 우선, Z39.50은 필요시만</td>
          </tr>
          <tr>
            <td><strong>레거시 유지보수</strong></td>
            <td>Z39.50 학습 필요</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>9. 요약: 한눈에 정리</h2>

  <div class="summary-grid">
    <div class="summary-main">
      <h3>🔍 Z39.50이란?</h3>
      <p class="definition">
        1988년에 만들어진 <strong>도서관 검색의 국제 표준 프로토콜</strong>
      </p>

      <div class="key-facts">
        <div class="fact">
          <strong>목적:</strong> 도서관끼리 서지 데이터 검색 및 공유
        </div>
        <div class="fact">
          <strong>기술:</strong> TCP/IP + ASN.1/BER
        </div>
        <div class="fact">
          <strong>주요 작업:</strong> Search, Present, Scan
        </div>
        <div class="fact">
          <strong>포트:</strong> 210 (기본)
        </div>
      </div>
    </div>

    <div class="summary-comparison">
      <h4>프로토콜 비교</h4>
      <table class="mini-compare">
        <tr>
          <td><strong>Z39.50</strong></td>
          <td>강력하지만 복잡, 웹 비친화적</td>
        </tr>
        <tr>
          <td><strong>SRU/SRW</strong></td>
          <td>Z39.50의 웹 버전, 더 간단</td>
        </tr>
        <tr>
          <td><strong>REST API</strong></td>
          <td>현대적이고 간단, 표준 없음</td>
        </tr>
      </table>
    </div>
  </div>

  <div class="final-message">
    <h3>🎯 핵심 메시지</h3>
    <div class="message-box">
      <p class="big-emphasis">
        <strong>Z39.50 = 도서관 검색의 할아버지</strong>
      </p>
      <p>
        1988년부터 도서관들을 연결해온 <strong>강력한 표준</strong>이지만,<br>
        웹 시대에 맞지 않아 <strong>SRU, SRW, REST API</strong>로 대체되고 있습니다.
      </p>
      <p class="learn-note">
        💡 <strong>개념과 역사는 알아두되, 신규 개발은 현대 프로토콜을 사용하세요!</strong>
      </p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>10. 학습 점검 퀴즈</h2>

  <div class="quiz-section">
    <div class="quiz-item">
      <p><strong>Q1.</strong> Z39.50이 만들어진 이유는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ 1980년대에 각 도서관마다 시스템이 달라서 <strong>한 번에 여러 도서관을 검색할 수 없었던 문제</strong>를 해결하기 위해 만들어진 <strong>공통 표준 프로토콜</strong>입니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> Z39.50의 3가지 주요 작업은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>Search (검색 요청)</strong>, <strong>Present (결과 가져오기)</strong>, <strong>Scan (색인 탐색)</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> Search와 Present를 왜 분리했을까요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>Search</strong>는 검색 조건이 맞는 레코드가 <strong>몇 개인지만</strong> 알려주고, <strong>Present</strong>로 원하는 범위(예: 1~10번)의 실제 데이터를 가져옵니다. 이렇게 하면 <strong>필요한 만큼만 전송</strong>할 수 있어 효율적입니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> Z39.50이 웹 환경에 맞지 않는 이유는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>HTTP가 아닌 TCP/IP를 직접 사용</strong>하고, <strong>전용 포트(210)</strong>를 쓰며, <strong>ASN.1/BER</strong>이라는 오래된 인코딩 방식을 사용해서 <strong>방화벽 통과가 어렵고</strong> 브라우저에서 직접 테스트할 수 없습니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> SRU/SRW는 Z39.50과 어떤 관계인가요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ SRU/SRW는 <strong>Z39.50의 기능을 HTTP/웹 환경으로 옮긴</strong> 프로토콜입니다. Z39.50보다 간단하고 웹 친화적이지만, 일부 고급 기능은 빠져있습니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q6.</strong> 지금도 Z39.50을 사용하나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>예</strong>, 여전히 많은 대형 도서관과 레거시 시스템에서 사용 중입니다. 특히 <strong>상호대차(ILL)</strong>와 <strong>목록 작성</strong>에서 많이 씁니다. 하지만 신규 프로젝트는 SRU나 REST API를 선택하는 추세입니다.</p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 더 알아보기</h2>
  <ul>
    <li><strong>Z39.50 공식 사이트</strong> - Library of Congress Z39.50 문서</li>
    <li><strong>ISO 23950</strong> - 국제 표준 버전</li>
    <li><strong>PyZ3950</strong> - Python Z39.50 클라이언트 라이브러리</li>
    <li><strong>YAZ</strong> - 오픈소스 Z39.50 툴킷</li>
    <li><strong>Index Data</strong> - Z39.50 소프트웨어 개발사</li>
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

.story-box {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  margin: 1.5rem 0;
}

.problem-box {
  background: #ffebee;
  border: 3px solid #f44336;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.problem-box h5 {
  color: #c62828;
  margin-bottom: 1rem;
}

.pain-point {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-weight: bold;
  color: #c62828;
}

.solution-arrow {
  text-align: center;
  font-size: 2rem;
  color: #4caf50;
  margin: 1rem 0;
  font-weight: bold;
}

.solution-box {
  background: #e8f5e9;
  border: 3px solid #4caf50;
  border-radius: 8px;
  padding: 1.5rem;
}

.solution-box h5 {
  color: #2e7d32;
  margin-bottom: 1rem;
}

.success-point {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-weight: bold;
  color: #2e7d32;
}

.name-explanation {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.name-parts {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 2rem 0;
}

.name-part {
  text-align: center;
}

.letter {
  font-size: 3rem;
  font-weight: bold;
  color: #1976d2;
  background: #e3f2fd;
  padding: 1rem 2rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.name-separator {
  font-size: 3rem;
  font-weight: bold;
  color: #666;
}

.meaning {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
}

.also-known {
  margin-top: 2rem;
}

.aliases {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-top: 1rem;
}

.alias-box {
  background: #fff3e0;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  border: 2px solid #ff9800;
}

.alias-box strong {
  color: #e65100;
  font-size: 1.2rem;
}

.architecture-diagram {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.arch-row {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 2rem;
  align-items: center;
}

.arch-box {
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
}

.client-box {
  background: #e3f2fd;
  border: 3px solid #2196f3;
}

.server-box {
  background: #e8f5e9;
  border: 3px solid #4caf50;
}

.arch-box h4 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.role {
  font-weight: bold;
  color: #666;
  margin: 0.5rem 0 1rem 0;
}

.examples {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  text-align: left;
  margin-top: 1rem;
}

.connection-arrows {
  text-align: center;
  font-weight: bold;
}

.arrow-down,
.arrow-up {
  font-size: 1.2rem;
  margin: 0.5rem 0;
  color: #1976d2;
}

.tech-stack-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin: 2rem 0;
}

.tech-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  border: 2px solid #ddd;
}

.tech-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.tech-card h4 {
  color: #1976d2;
  margin: 1rem 0;
}

.tech-detail {
  color: #666;
  font-size: 0.9rem;
  margin: 0.5rem 0;
  line-height: 1.6;
}

.default-port,
.vs-modern,
.most-common {
  background: #f5f5f5;
  padding: 0.5rem;
  border-radius: 4px;
  margin-top: 0.75rem;
  font-size: 0.85rem;
}

.tech-note {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.timeline-compare {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.year-box {
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  text-align: center;
  border: 2px solid #ff9800;
}

.year-box strong {
  color: #e65100;
  font-size: 1.2rem;
}

.vs-arrow {
  font-size: 1.5rem;
  font-weight: bold;
  color: #666;
}

.operations-intro {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
  text-align: center;
  font-size: 1.1rem;
}

.operations-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin: 2rem 0;
}

.op-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  position: relative;
  border: 3px solid #ddd;
}

.search-op {
  border-color: #2196f3;
}

.present-op {
  border-color: #4caf50;
}

.scan-op {
  border-color: #ff9800;
}

.op-number {
  position: absolute;
  top: -15px;
  left: 15px;
  width: 40px;
  height: 40px;
  background: #1976d2;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
}

.op-card h4 {
  color: #1976d2;
  margin: 1rem 0 0.5rem 0;
  font-size: 1.4rem;
}

.op-name {
  font-weight: bold;
  color: #666;
  margin-bottom: 1rem;
}

.op-detail {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.op-flow {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1rem 0;
  justify-content: center;
}

.flow-item {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  flex: 1;
}

.flow-arrow {
  font-size: 1.5rem;
  color: #4caf50;
}

.important-note {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 4px;
}

.format-note,
.use-case {
  background: #e8f5e9;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 4px;
}

.typical-session {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.session-flow {
  margin-top: 1.5rem;
}

.session-step {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 0.75rem 0;
  border-left: 4px solid #2196f3;
}

.step-num {
  width: 40px;
  height: 40px;
  background: #2196f3;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.step-content strong {
  color: #1976d2;
  font-size: 1.1rem;
}

.session-arrow {
  text-align: center;
  font-size: 1.5rem;
  color: #4caf50;
  margin: 0.25rem 0;
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

.protocol-comparison tr:nth-child(even) {
  background: #f5f5f5;
}

.comparison-insight {
  margin: 2rem 0;
}

.insight-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 1.5rem;
}

.insight-box {
  padding: 1.5rem;
  border-radius: 8px;
}

.z-box {
  background: #e3f2fd;
  border: 3px solid #2196f3;
}

.sru-box {
  background: #e8f5e9;
  border: 3px solid #4caf50;
}

.rest-box {
  background: #fff3e0;
  border: 3px solid #ff9800;
}

.insight-box h5 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.summary {
  font-weight: bold;
  color: #666;
  margin-bottom: 1rem;
}

.usage-examples {
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

.code-block {
  background: #1e272e;
  color: #aed581;
  padding: 1.5rem;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  line-height: 1.6;
  margin: 0;
}

.example-explanation {
  background: #e3f2fd;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.code-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background: white;
}

.code-table th,
.code-table td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.code-table th {
  background: #f5f5f5;
  font-weight: bold;
}

.code-table code {
  background: #263238;
  color: #aed581;
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
}

.real-world-servers {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.servers-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.server-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #ddd;
}

.server-card h5 {
  color: #1976d2;
  margin-bottom: 1rem;
  text-align: center;
}

.server-info {
  font-size: 0.9rem;
}

.server-info code {
  background: #263238;
  color: #aed581;
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
}

.pros-cons-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.pros-section {
  background: #e8f5e9;
  padding: 2rem;
  border-radius: 8px;
  border: 3px solid #4caf50;
}

.cons-section {
  background: #ffebee;
  padding: 2rem;
  border-radius: 8px;
  border: 3px solid #f44336;
}

.pros-section h3 {
  color: #2e7d32;
}

.cons-section h3 {
  color: #c62828;
}

.pros-list,
.cons-list {
  margin-top: 1.5rem;
}

.pro-item,
.con-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: white;
  padding: 1rem;
  border-radius: 4px;
  margin: 0.75rem 0;
}

.pro-icon,
.con-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.pro-content h4,
.con-content h4 {
  color: #1976d2;
  margin-bottom: 0.25rem;
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

.status-card.still-used {
  background: #e8f5e9;
  border: 3px solid #4caf50;
}

.status-card.declining {
  background: #fff3e0;
  border: 3px solid #ff9800;
}

.evolution-path {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.evolution-timeline {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.evo-step {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  min-width: 200px;
  border: 3px solid #ddd;
}

.z-step {
  border-color: #2196f3;
  background: #e3f2fd;
}

.sru-step {
  border-color: #4caf50;
  background: #e8f5e9;
}

.rest-step {
  border-color: #ff9800;
  background: #fff3e0;
}

.evo-year {
  font-size: 0.85rem;
  color: #666;
}

.evo-tech {
  font-weight: bold;
  color: #1976d2;
  font-size: 1.3rem;
  margin: 0.5rem 0;
}

.evo-role {
  font-size: 0.9rem;
  color: #666;
  margin: 0.5rem 0;
}

.evo-status {
  font-size: 1.1rem;
  margin-top: 0.5rem;
}

.evo-arrow {
  font-size: 2rem;
  color: #4caf50;
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

.scenario-box {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1.5rem 0;
}

.recommendation-box {
  background: #fff3e0;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1.5rem 0;
}

.recommendation-table {
  width: 100%;
  margin-top: 1rem;
  border-collapse: collapse;
}

.recommendation-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #ddd;
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
  border: 3px solid #2196f3;
  border-radius: 8px;
}

.definition {
  font-size: 1.1rem;
  color: #333;
  margin: 1rem 0;
}

.key-facts {
  display: grid;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.fact {
  background: #f5f5f5;
  padding: 0.75rem;
  border-radius: 4px;
}

.summary-comparison {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
}

.mini-compare {
  width: 100%;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.mini-compare td {
  padding: 0.75rem;
  border-bottom: 1px solid #ddd;
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

.learn-note {
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

@media (max-width: 1024px) {
  .tech-stack-grid,
  .operations-grid,
  .insight-grid,
  .servers-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .name-parts,
  .aliases,
  .arch-row,
  .pros-cons-grid,
  .status-grid,
  .summary-grid,
  .tech-stack-grid,
  .operations-grid,
  .insight-grid,
  .servers-grid {
    grid-template-columns: 1fr;
  }

  .evolution-timeline,
  .timeline-compare {
    flex-direction: column;
  }

  .evo-arrow,
  .vs-arrow {
    transform: rotate(90deg);
  }
}
</style>
        """,
        category=z3950_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=40,
        prerequisites="네트워크 기본 이해, 도서관 시스템 기초 지식",
        learning_objectives="Z39.50의 탄생 배경과 역사적 의의 이해하기, Z39.50의 구조와 주요 작업(Search, Present, Scan) 파악하기, Z39.50과 현대 프로토콜(SRU, SRW, REST)의 차이점 명확히 알기, Z39.50의 장단점과 현재 위치 이해하기, 언제 Z39.50을 사용하고 언제 다른 프로토콜을 선택해야 하는지 판단하기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {z3950_category.name} (상위: {search_protocol_category.name})")
    print(f"  - 난이도: 중급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=search-protocol")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_z3950_content()
