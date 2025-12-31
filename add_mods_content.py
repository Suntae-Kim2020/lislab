#!/usr/bin/env python
"""
MODS 학습 콘텐츠 추가 스크립트
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

def create_mods_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 가져오기: 메타데이터
    metadata_category = Category.objects.get(slug='metadata')
    print("✓ 상위 카테고리 확인: 메타데이터")

    # 하위 카테고리 생성 또는 가져오기: MODS
    mods_category, created = Category.objects.get_or_create(
        slug='mods',
        defaults={
            'name': 'MODS',
            'description': 'MODS (Metadata Object Description Schema)',
            'parent': metadata_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: MODS")
    else:
        print("✓ 하위 카테고리 확인: MODS")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': 'MODS', 'slug': 'mods'},
        {'name': 'XML', 'slug': 'xml'},
        {'name': '메타데이터 스키마', 'slug': 'metadata-schema'},
        {'name': '디지털 라이브러리', 'slug': 'digital-library'},
        {'name': 'MARC', 'slug': 'marc'},
        {'name': '인코딩', 'slug': 'encoding'},
        {'name': '아카이브', 'slug': 'archive'}
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
        title="MODS: 사람이 읽을 수 있는 XML 메타데이터",
        slug="mods-metadata-schema",
        summary="MARC에서 필요한 것만 뽑아 XML로 표현한 MODS! MARC와 BIBFRAME 사이에서 MODS의 위치를 이해하고, 실전 예제로 세 가지 포맷을 비교해봅니다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>MODS가 무엇인지, 왜 필요한지 이해하기</li>
    <li>MARC, MODS, BIBFRAME의 위치 관계 파악하기</li>
    <li>MODS XML 구조와 주요 요소 익히기</li>
    <li>같은 책을 MARC/MODS/BIBFRAME으로 비교하며 차이점 알기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. MODS를 한 문장으로</h2>

  <div class="definition-box">
    <h3>📖 MODS란?</h3>
    <p class="big-definition">
      <strong>MODS (Metadata Object Description Schema)</strong>는<br>
      MARC에서 필요한 핵심만 뽑아, <strong>XML로 표현한 서지 메타데이터 스키마</strong>입니다.
    </p>
  </div>

  <div class="feature-grid">
    <div class="feature-item">
      <h4>✅ MARC처럼</h4>
      <p>도서관 서지 메타데이터를 표현</p>
    </div>
    <div class="feature-item">
      <h4>👀 하지만 더 쉽게</h4>
      <p>사람이 읽기 쉬운 XML 형식</p>
    </div>
    <div class="feature-item">
      <h4>🌐 디지털 시대에</h4>
      <p>디지털 라이브러리와 아카이브에 최적화</p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>2. MODS는 무엇이고, 무엇은 아닌가</h2>

  <div class="is-isnot-grid">
    <div class="is-box">
      <h3>✔️ MODS는</h3>
      <ul>
        <li>✔ <strong>메타데이터 스키마</strong></li>
        <li>✔ <strong>XML 인코딩 포맷</strong></li>
        <li>✔ <strong>MARC → XML 변환용</strong> 중간/대안 포맷</li>
        <li>✔ 디지털 컬렉션, 리포지터리에서 많이 사용</li>
        <li>✔ 미국 의회도서관(LC)이 개발·유지</li>
      </ul>
    </div>

    <div class="isnot-box">
      <h3>❌ MODS는 아님</h3>
      <ul>
        <li>❌ 개념 모델 (FRBR/LRM 아님)</li>
        <li>❌ 콘텐츠 규칙 (RDA 아님)</li>
        <li>❌ Linked Data 데이터 모델 (RDF/BIBFRAME 아님)</li>
        <li>❌ 목록 작성 규칙</li>
        <li>❌ 차세대 웹 표준</li>
      </ul>
    </div>
  </div>

  <div class="key-insight">
    <h4>💡 핵심 포인트</h4>
    <p>MODS는 <strong>표현 방식(인코딩)</strong>일 뿐, <strong>규칙이나 개념 모델이 아닙니다</strong>!</p>
  </div>
</div>

<div class="content-section">
  <h2>3. 한눈에 보는 위치 관계</h2>

  <p>MODS를 정확히 위치시켜 보면:</p>

  <div class="architecture-full">
    <div class="arch-layer layer-1">
      <div class="layer-left">
        <div class="layer-num">1층</div>
        <div class="layer-name">개념 모델</div>
      </div>
      <div class="layer-right">
        <div class="tech-name">FRBR → LRM</div>
        <div class="tech-desc">"책이란 무엇인가?" 철학적 틀</div>
      </div>
    </div>

    <div class="arch-layer layer-2">
      <div class="layer-left">
        <div class="layer-num">2층</div>
        <div class="layer-name">콘텐츠 표준</div>
      </div>
      <div class="layer-right">
        <div class="tech-name">RDA</div>
        <div class="tech-desc">"무엇을 어떻게 기술할까?" 규칙</div>
      </div>
    </div>

    <div class="arch-layer layer-3 highlighted">
      <div class="layer-left">
        <div class="layer-num">3층</div>
        <div class="layer-name">데이터 모델<br>/ 표현 방식</div>
      </div>
      <div class="layer-right">
        <div class="tech-split">
          <div class="tech-option">
            <strong>RDF 기반:</strong> BIBFRAME
          </div>
          <div class="tech-option mods-highlight">
            <strong>XML 기반: ⭐ MODS ⭐</strong>
          </div>
        </div>
        <div class="tech-desc">"데이터를 어떻게 표현할까?"</div>
      </div>
    </div>

    <div class="arch-layer layer-4">
      <div class="layer-left">
        <div class="layer-num">4층</div>
        <div class="layer-name">레코드 포맷<br>/ 인코딩</div>
      </div>
      <div class="layer-right">
        <div class="tech-split">
          <div class="tech-option">MARC 21 (ISO 2709)</div>
          <div class="tech-option">MODS (XML)</div>
        </div>
        <div class="tech-desc">"파일로 어떻게 담아 보낼까?"</div>
      </div>
    </div>
  </div>

  <div class="position-summary">
    <h4>🎯 MODS의 위치</h4>
    <p>MODS는 <strong>3층(표현 방식)</strong>과 <strong>4층(인코딩)</strong> 사이에 걸쳐있어요!</p>
    <ul>
      <li><strong>BIBFRAME의 XML 쪽 사촌</strong>이라고 생각하면 됩니다</li>
      <li>MARC보다는 현대적이지만, BIBFRAME보다는 전통적</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>4. MODS vs 다른 표준들</h2>

  <h3>📊 MODS vs MARC</h3>
  <table class="comparison-table">
    <thead>
      <tr>
        <th>항목</th>
        <th>MARC</th>
        <th>MODS</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>목적</strong></td>
        <td>전통 도서관 교환</td>
        <td>디지털 라이브러리/아카이브</td>
      </tr>
      <tr>
        <td><strong>가독성</strong></td>
        <td>낮음 (태그 기반)</td>
        <td>높음 (의미 중심)</td>
      </tr>
      <tr>
        <td><strong>기술 방식</strong></td>
        <td>숫자 태그 (245, 100...)</td>
        <td>의미 요소 (&lt;titleInfo&gt;)</td>
      </tr>
      <tr>
        <td><strong>형식</strong></td>
        <td>바이너리/ISO 2709</td>
        <td>XML</td>
      </tr>
      <tr>
        <td><strong>학습 난이도</strong></td>
        <td>어려움</td>
        <td>상대적으로 쉬움</td>
      </tr>
    </tbody>
  </table>

  <div class="summary-line">
    <p>💡 <strong>MODS = "사람이 읽을 수 있는 MARC"</strong></p>
  </div>

  <h3>📊 MODS vs RDA</h3>
  <div class="vs-box">
    <div class="vs-item">
      <h4>RDA</h4>
      <p class="vs-role">규칙/지침</p>
      <p><em>무엇을 기록할 것인가</em></p>
      <p class="example">"저자명은 성, 이름 순으로"</p>
    </div>
    <div class="vs-arrow">→</div>
    <div class="vs-item">
      <h4>MODS</h4>
      <p class="vs-role">스키마/포맷</p>
      <p><em>그 기록을 XML로 어떻게 담을 것인가</em></p>
      <p class="example">&lt;name&gt;&lt;namePart&gt;조남주&lt;/namePart&gt;&lt;/name&gt;</p>
    </div>
  </div>

  <h3>📊 MODS vs BIBFRAME</h3>
  <table class="comparison-table">
    <thead>
      <tr>
        <th>항목</th>
        <th>MODS</th>
        <th>BIBFRAME</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>기술 기반</strong></td>
        <td>XML</td>
        <td>RDF/Linked Data</td>
      </tr>
      <tr>
        <td><strong>모델 성격</strong></td>
        <td>평면적 요소 집합</td>
        <td>엔티티-관계 모델</td>
      </tr>
      <tr>
        <td><strong>웹 친화성</strong></td>
        <td>중간</td>
        <td>매우 높음</td>
      </tr>
      <tr>
        <td><strong>주 용도</strong></td>
        <td>디지털 라이브러리</td>
        <td>차세대 목록/웹</td>
      </tr>
      <tr>
        <td><strong>세대</strong></td>
        <td>웹 이전 세대 (XML 중심)</td>
        <td>웹 네이티브 (Linked Data)</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="content-section">
  <h2>5. 아주 직관적인 비유</h2>

  <div class="analogy-container">
    <div class="analogy-card">
      <div class="analogy-icon">🏗️</div>
      <div class="analogy-title">FRBR/LRM</div>
      <div class="analogy-desc">설계 철학 / 세계관</div>
    </div>

    <div class="analogy-card">
      <div class="analogy-icon">📋</div>
      <div class="analogy-title">RDA</div>
      <div class="analogy-desc">"무엇을 어떻게 적을지" 규칙책</div>
    </div>

    <div class="analogy-card">
      <div class="analogy-icon">📄</div>
      <div class="analogy-title">MARC</div>
      <div class="analogy-desc">오래된 전용 양식지<br>(숫자 코드로 가득)</div>
    </div>

    <div class="analogy-card highlighted">
      <div class="analogy-icon">📝</div>
      <div class="analogy-title">MODS</div>
      <div class="analogy-desc">정리 잘 된 <strong>XML 양식지</strong><br>(읽기 쉬운 라벨)</div>
    </div>

    <div class="analogy-card">
      <div class="analogy-icon">🌐</div>
      <div class="analogy-title">BIBFRAME</div>
      <div class="analogy-desc">웹에서 바로 쓰는<br>Linked Data 언어</div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>6. MODS XML 구조 이해하기</h2>

  <h3>🔍 주요 요소</h3>

  <div class="elements-grid">
    <div class="element-card">
      <h4>&lt;titleInfo&gt;</h4>
      <p>표제 정보</p>
      <div class="element-example">
        &lt;title&gt;82년생 김지영&lt;/title&gt;
      </div>
    </div>

    <div class="element-card">
      <h4>&lt;name&gt;</h4>
      <p>저자, 기여자 정보</p>
      <div class="element-example">
        &lt;namePart&gt;조남주&lt;/namePart&gt;<br>
        &lt;role&gt;&lt;roleTerm&gt;author&lt;/roleTerm&gt;&lt;/role&gt;
      </div>
    </div>

    <div class="element-card">
      <h4>&lt;originInfo&gt;</h4>
      <p>출판 정보</p>
      <div class="element-example">
        &lt;publisher&gt;민음사&lt;/publisher&gt;<br>
        &lt;dateIssued&gt;2016&lt;/dateIssued&gt;
      </div>
    </div>

    <div class="element-card">
      <h4>&lt;physicalDescription&gt;</h4>
      <p>형태 정보</p>
      <div class="element-example">
        &lt;extent&gt;192 p.&lt;/extent&gt;
      </div>
    </div>

    <div class="element-card">
      <h4>&lt;subject&gt;</h4>
      <p>주제 정보</p>
      <div class="element-example">
        &lt;topic&gt;한국소설&lt;/topic&gt;
      </div>
    </div>

    <div class="element-card">
      <h4>&lt;identifier&gt;</h4>
      <p>식별자 (ISBN 등)</p>
      <div class="element-example">
        &lt;identifier type="isbn"&gt;978-89-546-5050-4&lt;/identifier&gt;
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>7. 실전 예제: 같은 책, 세 가지 표현</h2>

  <div class="book-example">
    <h3>📕 예제 도서: "82년생 김지영"</h3>
    <ul>
      <li>저자: 조남주</li>
      <li>출판사: 민음사</li>
      <li>출판연도: 2016</li>
      <li>ISBN: 978-89-546-5050-4</li>
      <li>면수: 192쪽</li>
    </ul>
  </div>

  <h3>방식 1️⃣: MARC 21</h3>
  <div class="format-example marc-format">
    <pre class="code-block">
100 1_ $a 조남주
245 10 $a 82년생 김지영 / $c 조남주 지음.
260 __ $a 서울 : $b 민음사, $c 2016.
300 __ $a 192 p.
020 __ $a 9788954650504
650 _0 $a 한국소설
    </pre>
    <div class="format-pros-cons">
      <p>✅ <strong>장점</strong>: 전 세계 도서관이 사용, 검증됨</p>
      <p>❌ <strong>단점</strong>: 숫자 코드 어려움, 가독성 낮음</p>
    </div>
  </div>

  <h3>방식 2️⃣: MODS (XML)</h3>
  <div class="format-example mods-format">
    <pre class="code-block">
&lt;mods xmlns="http://www.loc.gov/mods/v3"&gt;
  &lt;titleInfo&gt;
    &lt;title&gt;82년생 김지영&lt;/title&gt;
  &lt;/titleInfo&gt;

  &lt;name type="personal"&gt;
    &lt;namePart&gt;조남주&lt;/namePart&gt;
    &lt;role&gt;
      &lt;roleTerm type="text"&gt;author&lt;/roleTerm&gt;
    &lt;/role&gt;
  &lt;/name&gt;

  &lt;originInfo&gt;
    &lt;place&gt;
      &lt;placeTerm type="text"&gt;서울&lt;/placeTerm&gt;
    &lt;/place&gt;
    &lt;publisher&gt;민음사&lt;/publisher&gt;
    &lt;dateIssued&gt;2016&lt;/dateIssued&gt;
  &lt;/originInfo&gt;

  &lt;physicalDescription&gt;
    &lt;extent&gt;192 p.&lt;/extent&gt;
  &lt;/physicalDescription&gt;

  &lt;identifier type="isbn"&gt;9788954650504&lt;/identifier&gt;

  &lt;subject&gt;
    &lt;topic&gt;한국소설&lt;/topic&gt;
  &lt;/subject&gt;
&lt;/mods&gt;
    </pre>
    <div class="format-pros-cons">
      <p>✅ <strong>장점</strong>: 읽기 쉬움, 의미 명확, XML 도구 활용 가능</p>
      <p>❌ <strong>단점</strong>: MARC보다 덜 보편적, 평면적 구조</p>
    </div>
  </div>

  <h3>방식 3️⃣: BIBFRAME (RDF)</h3>
  <div class="format-example bibframe-format">
    <pre class="code-block">
&lt;bf:Work rdf:about="http://example.org/work/82년생김지영"&gt;
  &lt;bf:title&gt;
    &lt;bf:Title&gt;
      &lt;bf:mainTitle&gt;82년생 김지영&lt;/bf:mainTitle&gt;
    &lt;/bf:Title&gt;
  &lt;/bf:title&gt;

  &lt;bf:contribution&gt;
    &lt;bf:Contribution&gt;
      &lt;bf:agent&gt;
        &lt;bf:Person rdf:about="http://example.org/person/조남주"&gt;
          &lt;rdfs:label&gt;조남주&lt;/rdfs:label&gt;
        &lt;/bf:Person&gt;
      &lt;/bf:agent&gt;
      &lt;bf:role&gt;
        &lt;bf:Role&gt;&lt;rdfs:label&gt;author&lt;/rdfs:label&gt;&lt;/bf:Role&gt;
      &lt;/bf:role&gt;
    &lt;/bf:Contribution&gt;
  &lt;/bf:contribution&gt;
&lt;/bf:Work&gt;

&lt;bf:Instance rdf:about="http://example.org/instance/82년생김지영-2016"&gt;
  &lt;bf:instanceOf rdf:resource="http://example.org/work/82년생김지영"/&gt;
  &lt;bf:provisionActivity&gt;
    &lt;bf:Publication&gt;
      &lt;bf:agent&gt;
        &lt;bf:Organization rdf:about="http://example.org/org/민음사"&gt;
          &lt;rdfs:label&gt;민음사&lt;/rdfs:label&gt;
        &lt;/bf:Organization&gt;
      &lt;/bf:agent&gt;
      &lt;bf:date&gt;2016&lt;/bf:date&gt;
    &lt;/bf:Publication&gt;
  &lt;/bf:provisionActivity&gt;
  &lt;bf:identifiedBy&gt;
    &lt;bf:Isbn&gt;
      &lt;rdf:value&gt;9788954650504&lt;/rdf:value&gt;
    &lt;/bf:Isbn&gt;
  &lt;/bf:identifiedBy&gt;
&lt;/bf:Instance&gt;
    </pre>
    <div class="format-pros-cons">
      <p>✅ <strong>장점</strong>: 웹 연결 가능, 의미 관계 명확, 확장성 높음</p>
      <p>❌ <strong>단점</strong>: 복잡함, 전환 시간 필요</p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>8. 변환 흐름도</h2>

  <div class="conversion-flow">
    <div class="flow-step">
      <div class="flow-box marc-bg">
        <h4>MARC 21</h4>
        <p>기존 도서관 레코드</p>
      </div>
      <div class="flow-label">↓ MARC → MODS 변환<br>(LOC 제공 XSLT)</div>
    </div>

    <div class="flow-step">
      <div class="flow-box mods-bg">
        <h4>MODS</h4>
        <p>XML 기반 메타데이터</p>
      </div>
      <div class="flow-options">
        <div class="flow-label">↓ 디지털 라이브러리에서 사용</div>
        <div class="flow-label">→ MODS → BIBFRAME 변환 가능</div>
      </div>
    </div>

    <div class="flow-step">
      <div class="flow-box bibframe-bg">
        <h4>BIBFRAME</h4>
        <p>Linked Data 기반</p>
      </div>
      <div class="flow-label">↓ 웹에서 연결·공유</div>
    </div>
  </div>

  <div class="conversion-note">
    <h4>💡 실무 팁</h4>
    <ul>
      <li>미국 의회도서관(LC)이 <strong>MARC → MODS 변환 도구(XSLT)</strong> 무료 제공</li>
      <li>많은 디지털 리포지터리 시스템이 MODS 지원 (DSpace, Fedora 등)</li>
      <li>MODS는 중간 포맷으로 활용 가능 (MARC → MODS → 다른 포맷)</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>9. 언제 MODS를 사용하나요?</h2>

  <div class="usecase-grid">
    <div class="usecase-card">
      <h4>✅ MODS가 적합한 경우</h4>
      <ul>
        <li>디지털 아카이브 구축</li>
        <li>디지털 컬렉션 관리</li>
        <li>MARC 레코드를 XML로 변환</li>
        <li>웹 서비스에서 메타데이터 교환</li>
        <li>기관 리포지터리 운영</li>
        <li>XML 기반 시스템 통합</li>
      </ul>
    </div>

    <div class="usecase-card">
      <h4>❌ MODS가 부적합한 경우</h4>
      <ul>
        <li>전통적 도서관 목록 교환 → MARC 사용</li>
        <li>차세대 웹 목록 구축 → BIBFRAME 사용</li>
        <li>Linked Data 필요 → RDF/BIBFRAME 사용</li>
        <li>대규모 도서관 컨소시엄 → MARC 사용</li>
      </ul>
    </div>
  </div>

  <div class="realworld-examples">
    <h4>🌍 실제 사용 사례</h4>
    <ul>
      <li><strong>미국 의회도서관 디지털 컬렉션</strong>: MODS로 메타데이터 관리</li>
      <li><strong>DSpace</strong>: 기관 리포지터리 소프트웨어, MODS 지원</li>
      <li><strong>Fedora Commons</strong>: 디지털 자산 관리 시스템, MODS 사용</li>
      <li><strong>Internet Archive</strong>: 일부 컬렉션에서 MODS 활용</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>10. 요약: 한눈에 정리</h2>

  <div class="final-summary">
    <table class="summary-table">
      <thead>
        <tr>
          <th>특성</th>
          <th>설명</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>정체</strong></td>
          <td>XML 기반 서지 메타데이터 스키마</td>
        </tr>
        <tr>
          <td><strong>목적</strong></td>
          <td>MARC를 읽기 쉬운 XML로 표현</td>
        </tr>
        <tr>
          <td><strong>위치</strong></td>
          <td>3층(표현 방식) ~ 4층(인코딩) 사이</td>
        </tr>
        <tr>
          <td><strong>개발</strong></td>
          <td>미국 의회도서관(LC)</td>
        </tr>
        <tr>
          <td><strong>주 사용처</strong></td>
          <td>디지털 라이브러리, 아카이브, 리포지터리</td>
        </tr>
        <tr>
          <td><strong>장점</strong></td>
          <td>가독성 높음, XML 도구 활용, MARC 호환</td>
        </tr>
        <tr>
          <td><strong>단점</strong></td>
          <td>Linked Data 아님, MARC보다 덜 보편적</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="one-liner-summary">
    <h3>🎯 한 문장 정리</h3>
    <p class="big-text">
      <strong>MODS는 MARC에서 출발한, XML 기반의 서지 메타데이터 스키마이며,<br>
      개념 모델은 아니고, RDA 내용을 담을 수 있는 표현(인코딩) 포맷이다.</strong>
    </p>
  </div>

  <div class="comparison-summary">
    <h4>📊 핵심 비교</h4>
    <div class="compare-boxes">
      <div class="compare-item">
        <strong>MARC</strong><br>
        전통 도서관<br>
        (숫자 태그)
      </div>
      <div class="arrow">→</div>
      <div class="compare-item highlight">
        <strong>MODS</strong><br>
        디지털 시대<br>
        (XML)
      </div>
      <div class="arrow">→</div>
      <div class="compare-item">
        <strong>BIBFRAME</strong><br>
        웹 시대<br>
        (Linked Data)
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>11. 학습 점검 퀴즈</h2>

  <div class="quiz-section">
    <div class="quiz-item">
      <p><strong>Q1.</strong> MODS를 한 문장으로 설명하면?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>MARC에서 필요한 핵심만 뽑아, XML로 표현한 서지 메타데이터 스키마</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> MODS는 개념 모델인가요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>아니요</strong>. MODS는 표현 방식(인코딩 포맷)이지, 개념 모델(FRBR/LRM)이 아닙니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> MODS와 MARC의 가장 큰 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>가독성</strong>. MARC는 숫자 태그 기반이고, MODS는 의미 있는 XML 요소 기반</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> MODS가 주로 사용되는 곳은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>디지털 라이브러리, 아카이브, 기관 리포지터리</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> MODS와 BIBFRAME의 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ MODS는 <strong>XML 기반</strong> (웹 이전 세대), BIBFRAME은 <strong>RDF/Linked Data 기반</strong> (웹 네이티브)</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q6.</strong> MARC 레코드를 MODS로 변환할 수 있나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>가능</strong>합니다. 미국 의회도서관이 MARC → MODS 변환 도구(XSLT)를 무료로 제공합니다.</p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 더 알아보기</h2>
  <ul>
    <li><strong>MODS 공식 사이트</strong> - Library of Congress MODS 문서</li>
    <li><strong>MODS Schema (XSD)</strong> - XML 스키마 정의</li>
    <li><strong>MARC to MODS Conversion</strong> - 변환 도구 및 가이드</li>
    <li><strong>DSpace Documentation</strong> - MODS 활용 예시</li>
    <li><strong>Fedora Commons</strong> - 디지털 자산 관리에서의 MODS</li>
  </ul>
</div>

<style>
.content-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.definition-box {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
}

.definition-box h3,
.definition-box p {
  color: white;
}

.big-definition {
  font-size: 1.3rem;
  line-height: 1.8;
  margin: 1rem 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

.feature-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  border: 2px solid #ddd;
}

.feature-item h4 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.is-isnot-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.is-box {
  background: #e8f5e9;
  border: 3px solid #4caf50;
  padding: 1.5rem;
  border-radius: 8px;
}

.isnot-box {
  background: #ffebee;
  border: 3px solid #f44336;
  padding: 1.5rem;
  border-radius: 8px;
}

.is-box h3 {
  color: #2e7d32;
}

.isnot-box h3 {
  color: #c62828;
}

.key-insight {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.architecture-full {
  margin: 2rem 0;
}

.arch-layer {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 1rem;
  margin: 1rem 0;
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.arch-layer.highlighted {
  border: 3px solid #ff9800;
  box-shadow: 0 4px 8px rgba(255,152,0,0.3);
}

.layer-left {
  background: #f5f5f5;
  padding: 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.layer-num {
  font-size: 1.5rem;
  font-weight: bold;
  color: #666;
}

.layer-name {
  font-size: 0.9rem;
  color: #888;
  margin-top: 0.5rem;
}

.layer-right {
  padding: 1.5rem;
}

.tech-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.tech-desc {
  color: #666;
  font-size: 0.95rem;
}

.tech-split {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.tech-option {
  flex: 1;
  padding: 0.75rem;
  background: #f5f5f5;
  border-radius: 4px;
  font-size: 0.95rem;
}

.mods-highlight {
  background: #fff3e0;
  border: 2px solid #ff9800;
  font-weight: bold;
}

.position-summary {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
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

.comparison-table tr:nth-child(even) {
  background: #f5f5f5;
}

.summary-line {
  background: #fff3e0;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
  margin: 1rem 0;
  border-left: 4px solid #ff9800;
}

.vs-box {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 1.5rem;
  align-items: center;
  margin: 2rem 0;
}

.vs-item {
  background: white;
  padding: 1.5rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  text-align: center;
}

.vs-role {
  font-weight: bold;
  color: #1976d2;
  margin: 0.5rem 0;
}

.vs-arrow {
  font-size: 2rem;
  color: #4caf50;
}

.example {
  background: #f5f5f5;
  padding: 0.75rem;
  margin-top: 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-family: monospace;
}

.analogy-container {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1rem;
  margin: 2rem 0;
}

.analogy-card {
  background: white;
  padding: 1.5rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  text-align: center;
}

.analogy-card.highlighted {
  border: 3px solid #ff9800;
  background: #fff3e0;
}

.analogy-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.analogy-title {
  font-weight: bold;
  color: #1976d2;
  margin: 0.5rem 0;
}

.analogy-desc {
  font-size: 0.85rem;
  color: #666;
  line-height: 1.4;
}

.elements-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

.element-card {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 1rem;
}

.element-card h4 {
  color: #1976d2;
  font-family: monospace;
  margin-bottom: 0.5rem;
}

.element-example {
  background: #263238;
  color: #aed581;
  padding: 0.75rem;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.85rem;
  margin-top: 0.75rem;
  line-height: 1.4;
}

.book-example {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
  padding: 1rem;
  margin: 1.5rem 0;
  border-radius: 4px;
}

.format-example {
  margin: 2rem 0;
  border-radius: 8px;
  overflow: hidden;
}

.marc-format {
  border: 3px solid #ff9800;
}

.mods-format {
  border: 3px solid #4caf50;
}

.bibframe-format {
  border: 3px solid #2196f3;
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

.format-pros-cons {
  background: white;
  padding: 1rem;
  font-size: 0.95rem;
}

.conversion-flow {
  margin: 2rem 0;
}

.flow-step {
  margin: 1.5rem 0;
  text-align: center;
}

.flow-box {
  display: inline-block;
  padding: 2rem 3rem;
  border-radius: 8px;
  color: white;
  margin-bottom: 1rem;
}

.marc-bg {
  background: #ff9800;
}

.mods-bg {
  background: #4caf50;
}

.bibframe-bg {
  background: #2196f3;
}

.flow-label {
  color: #666;
  font-size: 0.95rem;
  margin: 0.5rem 0;
}

.flow-options {
  display: flex;
  gap: 2rem;
  justify-content: center;
}

.conversion-note {
  background: #e8f5e9;
  border-left: 4px solid #4caf50;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.usecase-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.usecase-card {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
}

.realworld-examples {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.final-summary {
  margin: 2rem 0;
}

.summary-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.summary-table th,
.summary-table td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.summary-table th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.summary-table tr:nth-child(even) {
  background: #f5f5f5;
}

.one-liner-summary {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
}

.one-liner-summary h3,
.one-liner-summary p {
  color: white;
}

.big-text {
  font-size: 1.2rem;
  line-height: 1.8;
}

.comparison-summary {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.compare-boxes {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.compare-item {
  background: white;
  padding: 1.5rem 2rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  text-align: center;
  min-width: 150px;
}

.compare-item.highlight {
  border: 3px solid #ff9800;
  background: #fff3e0;
  font-weight: bold;
}

.arrow {
  font-size: 2rem;
  color: #4caf50;
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
  .feature-grid,
  .elements-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .analogy-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .is-isnot-grid,
  .usecase-grid,
  .feature-grid,
  .elements-grid {
    grid-template-columns: 1fr;
  }

  .analogy-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .arch-layer {
    grid-template-columns: 1fr;
  }

  .compare-boxes {
    flex-direction: column;
  }
}
</style>
        """,
        category=mods_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=47,
        prerequisites="MARC21 기본 이해, XML 기초 지식",
        learning_objectives="MODS의 정체와 목적 이해하기, MARC/MODS/BIBFRAME의 위치 관계 파악하기, MODS XML 구조와 주요 요소 익히기, 실전 예제로 세 가지 포맷 비교하기, MODS의 적절한 사용처 판단하기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {mods_category.name} (상위: {metadata_category.name})")
    print(f"  - 난이도: 중급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=metadata")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_mods_content()
