#!/usr/bin/env python
"""
METS 학습 콘텐츠 추가 스크립트
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

def create_mets_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 가져오기: 메타데이터
    metadata_category = Category.objects.get(slug='metadata')
    print("✓ 상위 카테고리 확인: 메타데이터")

    # 하위 카테고리 생성 또는 가져오기: METS
    mets_category, created = Category.objects.get_or_create(
        slug='mets',
        defaults={
            'name': 'METS',
            'description': 'METS (Metadata Encoding and Transmission Standard)',
            'parent': metadata_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: METS")
    else:
        print("✓ 하위 카테고리 확인: METS")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': 'METS', 'slug': 'mets'},
        {'name': 'XML', 'slug': 'xml'},
        {'name': '디지털 보존', 'slug': 'digital-preservation'},
        {'name': '메타데이터 패키징', 'slug': 'metadata-packaging'},
        {'name': '구조 메타데이터', 'slug': 'structural-metadata'},
        {'name': '디지털 객체', 'slug': 'digital-object'},
        {'name': '메타데이터 스키마', 'slug': 'metadata-schema'},
        {'name': '디지털 아카이브', 'slug': 'digital-archive'}
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
        title="METS: 디지털 객체를 묶는 컨테이너",
        slug="mets-metadata-standard",
        summary="디지털 책, 사진, 영상을 하나로 묶어주는 METS! 메타데이터의 포장 전문가 METS를 이해하고, MODS/MARC와의 차이점을 명확히 배웁니다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>METS가 무엇인지, 왜 필요한지 이해하기</li>
    <li>METS의 7가지 섹션 구조 파악하기</li>
    <li>MODS/MARC/BIBFRAME과 METS의 차이점 알기</li>
    <li>실전 예제로 디지털 책 패키징 방법 익히기</li>
    <li>METS를 언제 사용해야 하는지 판단하기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. METS를 한 문장으로</h2>

  <div class="hero-definition">
    <h3>📦 METS란?</h3>
    <p class="big-statement">
      <strong>METS (Metadata Encoding and Transmission Standard)</strong>는<br>
      디지털 객체와 그 메타데이터를 <strong>하나로 묶어 포장하는 XML 표준</strong>입니다.
    </p>
  </div>

  <div class="simple-analogy">
    <h4>🎁 쉬운 비유</h4>
    <div class="analogy-visual">
      <div class="analogy-item">
        <div class="icon">📚</div>
        <p>디지털 책 파일<br>(PDF, 이미지 등)</p>
      </div>
      <div class="plus">+</div>
      <div class="analogy-item">
        <div class="icon">📋</div>
        <p>메타데이터<br>(제목, 저자, 목차 등)</p>
      </div>
      <div class="arrow">→</div>
      <div class="analogy-item highlight">
        <div class="icon">📦</div>
        <p><strong>METS로 포장</strong><br>완전한 디지털 패키지</p>
      </div>
    </div>
    <p class="analogy-text">택배 상자에 물건과 송장을 함께 넣듯이, METS는 디지털 파일과 메타데이터를 하나로 묶습니다!</p>
  </div>
</div>

<div class="content-section">
  <h2>2. 다른 메타데이터 표준과 뭐가 다른가?</h2>

  <div class="comparison-grid">
    <div class="standard-card marc-card">
      <h4>📄 MARC</h4>
      <p class="role">서지 레코드 교환</p>
      <p class="purpose">"책 정보를 다른 도서관과 주고받자"</p>
      <div class="scope">범위: <strong>서지정보만</strong></div>
    </div>

    <div class="standard-card mods-card">
      <h4>📝 MODS</h4>
      <p class="role">서지 메타데이터</p>
      <p class="purpose">"책 정보를 XML로 표현하자"</p>
      <div class="scope">범위: <strong>서지정보만</strong></div>
    </div>

    <div class="standard-card bibframe-card">
      <h4>🌐 BIBFRAME</h4>
      <p class="role">Linked Data 모델</p>
      <p class="purpose">"책 정보를 웹에서 연결하자"</p>
      <div class="scope">범위: <strong>서지정보만</strong></div>
    </div>

    <div class="standard-card mets-card highlighted">
      <h4>📦 METS</h4>
      <p class="role">디지털 객체 패키징</p>
      <p class="purpose">"디지털 파일과 메타데이터를 묶자"</p>
      <div class="scope">범위: <strong>모든 메타데이터 + 파일</strong></div>
    </div>
  </div>

  <div class="key-difference">
    <h4>🔑 핵심 차이점</h4>
    <table class="diff-table">
      <thead>
        <tr>
          <th>표준</th>
          <th>주요 목적</th>
          <th>포함 내용</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>MARC/MODS/BIBFRAME</strong></td>
          <td>서지정보 기술</td>
          <td>제목, 저자, 출판사 등 <strong>메타데이터만</strong></td>
        </tr>
        <tr class="highlight-row">
          <td><strong>METS</strong></td>
          <td>디지털 객체 포장</td>
          <td>메타데이터 + <strong>파일 자체</strong> + <strong>구조 정보</strong></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="content-section">
  <h2>3. METS의 역할 이해하기</h2>

  <div class="role-explanation">
    <h3>💡 METS는 "포장지"다!</h3>

    <div class="wrapper-concept">
      <div class="inner-content">
        <p><strong>내용물 (MODS 사용 가능)</strong></p>
        <ul>
          <li>서지 메타데이터 (MODS XML)</li>
          <li>관리 메타데이터 (저작권, 보존 정보)</li>
          <li>구조 정보 (페이지 순서, 목차)</li>
          <li>실제 파일들 (PDF, 이미지, 텍스트)</li>
        </ul>
      </div>
      <div class="wrapper-label">
        ← METS로 전체를 감싸서 하나의 패키지로!
      </div>
    </div>
  </div>

  <div class="mets-vs-others">
    <h4>📊 다른 표준들과의 관계</h4>

    <table class="relation-table">
      <thead>
        <tr>
          <th>표준</th>
          <th>METS와의 관계</th>
          <th>비유</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>MODS</strong></td>
          <td>METS <strong>안에 들어갈 수 있음</strong></td>
          <td>상자(METS) 안의 품목 명세서</td>
        </tr>
        <tr>
          <td><strong>Dublin Core</strong></td>
          <td>METS <strong>안에 들어갈 수 있음</strong></td>
          <td>상자 안의 간단한 라벨</td>
        </tr>
        <tr>
          <td><strong>PREMIS</strong></td>
          <td>METS <strong>안에 들어갈 수 있음</strong> (보존 메타데이터)</td>
          <td>상자 안의 보관 지침서</td>
        </tr>
        <tr>
          <td><strong>MARC</strong></td>
          <td>METS와 <strong>별개</strong> (다른 용도)</td>
          <td>다른 포장 시스템</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<div class="content-section">
  <h2>4. METS의 7가지 섹션</h2>

  <p>METS는 7개의 섹션으로 구성됩니다:</p>

  <div class="sections-grid">
    <div class="section-card">
      <div class="section-number">1</div>
      <h4>&lt;metsHdr&gt;</h4>
      <p class="section-name">METS 헤더</p>
      <p class="section-desc">이 패키지 자체에 대한 정보<br>(작성자, 작성일)</p>
      <div class="example-mini">
        누가, 언제 만들었는지
      </div>
    </div>

    <div class="section-card">
      <div class="section-number">2</div>
      <h4>&lt;dmdSec&gt;</h4>
      <p class="section-name">기술 메타데이터</p>
      <p class="section-desc">내용에 대한 설명<br>(제목, 저자 등)</p>
      <div class="example-mini">
        MODS, Dublin Core 등 사용
      </div>
    </div>

    <div class="section-card">
      <div class="section-number">3</div>
      <h4>&lt;amdSec&gt;</h4>
      <p class="section-name">관리 메타데이터</p>
      <p class="section-desc">관리 정보<br>(저작권, 보존 이력)</p>
      <div class="example-mini">
        PREMIS 등 사용
      </div>
    </div>

    <div class="section-card">
      <div class="section-number">4</div>
      <h4>&lt;fileSec&gt;</h4>
      <p class="section-name">파일 섹션</p>
      <p class="section-desc">포함된 모든 파일 목록<br>(PDF, 이미지 등)</p>
      <div class="example-mini">
        파일명, 크기, 형식
      </div>
    </div>

    <div class="section-card highlight">
      <div class="section-number">5</div>
      <h4>&lt;structMap&gt;</h4>
      <p class="section-name">구조 맵 ⭐</p>
      <p class="section-desc">파일들의 계층 구조<br>(목차, 페이지 순서)</p>
      <div class="example-mini">
        <strong>METS만의 핵심 기능!</strong>
      </div>
    </div>

    <div class="section-card">
      <div class="section-number">6</div>
      <h4>&lt;structLink&gt;</h4>
      <p class="section-name">구조 링크</p>
      <p class="section-desc">구조 간 하이퍼링크<br>(주석 연결 등)</p>
      <div class="example-mini">
        선택사항
      </div>
    </div>

    <div class="section-card">
      <div class="section-number">7</div>
      <h4>&lt;behaviorSec&gt;</h4>
      <p class="section-name">행위 섹션</p>
      <p class="section-desc">실행 가능한 동작<br>(뷰어 지정 등)</p>
      <div class="example-mini">
        선택사항
      </div>
    </div>
  </div>

  <div class="structure-highlight">
    <h4>💡 핵심은 structMap!</h4>
    <p><strong>&lt;structMap&gt;</strong>이 METS를 특별하게 만듭니다!</p>
    <p>다른 메타데이터 표준에는 없는, <strong>파일들의 계층 구조</strong>를 표현합니다.</p>
    <div class="example-box">
      <p><strong>예시:</strong></p>
      <ul>
        <li>책 → 1장 → 1절 → 1.1절 → 페이지 1, 2, 3...</li>
        <li>각 페이지가 어떤 이미지 파일인지 연결</li>
      </ul>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>5. 실전 예제: 디지털 책 패키징</h2>

  <div class="digital-book">
    <h3>📕 예제: "82년생 김지영" 디지털판</h3>
    <div class="book-structure">
      <p><strong>구성:</strong></p>
      <ul>
        <li>표지 이미지 (cover.jpg)</li>
        <li>1장 PDF (chapter1.pdf)</li>
        <li>2장 PDF (chapter2.pdf)</li>
        <li>전문 텍스트 (fulltext.txt)</li>
      </ul>
    </div>
  </div>

  <h4>METS 문서 구조</h4>

  <div class="code-example">
    <pre class="code-block">
&lt;mets xmlns="http://www.loc.gov/METS/"&gt;

  &lt;!-- 1. METS 헤더 --&gt;
  &lt;metsHdr CREATEDATE="2025-01-15"&gt;
    &lt;agent ROLE="CREATOR"&gt;
      &lt;name&gt;국립중앙도서관&lt;/name&gt;
    &lt;/agent&gt;
  &lt;/metsHdr&gt;

  &lt;!-- 2. 기술 메타데이터 (MODS 사용) --&gt;
  &lt;dmdSec ID="DMD1"&gt;
    &lt;mdWrap MDTYPE="MODS"&gt;
      &lt;xmlData&gt;
        &lt;mods&gt;
          &lt;titleInfo&gt;
            &lt;title&gt;82년생 김지영&lt;/title&gt;
          &lt;/titleInfo&gt;
          &lt;name&gt;
            &lt;namePart&gt;조남주&lt;/namePart&gt;
            &lt;role&gt;&lt;roleTerm&gt;author&lt;/roleTerm&gt;&lt;/role&gt;
          &lt;/name&gt;
        &lt;/mods&gt;
      &lt;/xmlData&gt;
    &lt;/mdWrap&gt;
  &lt;/dmdSec&gt;

  &lt;!-- 3. 관리 메타데이터 --&gt;
  &lt;amdSec&gt;
    &lt;rightsMD ID="RIGHTS1"&gt;
      &lt;mdWrap MDTYPE="OTHER"&gt;
        &lt;xmlData&gt;
          &lt;copyright&gt;저작권자: 조남주&lt;/copyright&gt;
          &lt;license&gt;출판사 허가 필요&lt;/license&gt;
        &lt;/xmlData&gt;
      &lt;/mdWrap&gt;
    &lt;/rightsMD&gt;
  &lt;/amdSec&gt;

  &lt;!-- 4. 파일 섹션 --&gt;
  &lt;fileSec&gt;
    &lt;fileGrp USE="Images"&gt;
      &lt;file ID="FILE001" MIMETYPE="image/jpeg"&gt;
        &lt;FLocat LOCTYPE="URL" xlink:href="cover.jpg"/&gt;
      &lt;/file&gt;
    &lt;/fileGrp&gt;
    &lt;fileGrp USE="PDFs"&gt;
      &lt;file ID="FILE002" MIMETYPE="application/pdf"&gt;
        &lt;FLocat LOCTYPE="URL" xlink:href="chapter1.pdf"/&gt;
      &lt;/file&gt;
      &lt;file ID="FILE003" MIMETYPE="application/pdf"&gt;
        &lt;FLocat LOCTYPE="URL" xlink:href="chapter2.pdf"/&gt;
      &lt;/file&gt;
    &lt;/fileGrp&gt;
    &lt;fileGrp USE="Text"&gt;
      &lt;file ID="FILE004" MIMETYPE="text/plain"&gt;
        &lt;FLocat LOCTYPE="URL" xlink:href="fulltext.txt"/&gt;
      &lt;/file&gt;
    &lt;/fileGrp&gt;
  &lt;/fileSec&gt;

  &lt;!-- 5. 구조 맵 (핵심!) --&gt;
  &lt;structMap TYPE="logical"&gt;
    &lt;div TYPE="book" LABEL="82년생 김지영" DMDID="DMD1"&gt;
      &lt;div TYPE="cover" LABEL="표지"&gt;
        &lt;fptr FILEID="FILE001"/&gt;
      &lt;/div&gt;
      &lt;div TYPE="chapter" LABEL="1장" ORDER="1"&gt;
        &lt;fptr FILEID="FILE002"/&gt;
      &lt;/div&gt;
      &lt;div TYPE="chapter" LABEL="2장" ORDER="2"&gt;
        &lt;fptr FILEID="FILE003"/&gt;
      &lt;/div&gt;
      &lt;div TYPE="fulltext" LABEL="전문"&gt;
        &lt;fptr FILEID="FILE004"/&gt;
      &lt;/div&gt;
    &lt;/div&gt;
  &lt;/structMap&gt;

&lt;/mets&gt;
    </pre>
  </div>

  <div class="explanation-box">
    <h4>🔍 코드 이해하기</h4>
    <ul>
      <li><strong>dmdSec</strong>: MODS로 책 정보 기술</li>
      <li><strong>fileSec</strong>: 4개 파일 목록 (표지, 1장, 2장, 전문)</li>
      <li><strong>structMap</strong>: 책 → 표지, 1장, 2장, 전문 계층 구조</li>
      <li><strong>fptr</strong>: 각 구조가 어떤 파일을 가리키는지 연결</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>6. 언제 METS를 사용하나요?</h2>

  <div class="usecases">
    <div class="usecase-card yes">
      <h4>✅ METS가 필요한 경우</h4>
      <ul>
        <li><strong>디지털 아카이브</strong>: 역사 자료, 고문서 디지털화</li>
        <li><strong>디지털 도서관</strong>: 전자책, 학위논문 저장</li>
        <li><strong>리포지터리</strong>: 기관의 디지털 자산 관리</li>
        <li><strong>복잡한 구조</strong>: 다중 파일, 계층 구조 필요</li>
        <li><strong>장기 보존</strong>: 모든 정보를 하나로 패키징</li>
      </ul>
    </div>

    <div class="usecase-card no">
      <h4>❌ METS가 불필요한 경우</h4>
      <ul>
        <li><strong>단순 서지 정보만</strong>: MODS나 MARC 사용</li>
        <li><strong>웹 목록 구축</strong>: BIBFRAME 사용</li>
        <li><strong>단일 파일</strong>: 복잡한 패키징 불필요</li>
        <li><strong>실시간 검색</strong>: 검색 엔진에 부적합</li>
      </ul>
    </div>
  </div>

  <div class="practical-examples">
    <h4>🌍 실제 사용 사례</h4>
    <div class="examples-grid">
      <div class="example-item">
        <h5>📚 DSpace</h5>
        <p>기관 리포지터리 소프트웨어<br>METS로 논문 패키징</p>
      </div>
      <div class="example-item">
        <h5>🏛️ 미국 의회도서관</h5>
        <p>디지털 컬렉션<br>역사 자료 보존</p>
      </div>
      <div class="example-item">
        <h5>📖 Internet Archive</h5>
        <p>대규모 디지털 도서관<br>책 스캔 패키징</p>
      </div>
      <div class="example-item">
        <h5>🎓 대학 도서관</h5>
        <p>학위논문 저장소<br>ETD (전자학위논문)</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>7. METS와 다른 표준 종합 비교</h2>

  <table class="master-comparison">
    <thead>
      <tr>
        <th>표준</th>
        <th>주요 목적</th>
        <th>포함 내용</th>
        <th>기술 기반</th>
        <th>사용처</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>MARC</strong></td>
        <td>서지 레코드 교환</td>
        <td>서지정보</td>
        <td>ISO 2709</td>
        <td>전통 도서관</td>
      </tr>
      <tr>
        <td><strong>MODS</strong></td>
        <td>서지 기술</td>
        <td>서지정보</td>
        <td>XML</td>
        <td>디지털 라이브러리</td>
      </tr>
      <tr>
        <td><strong>BIBFRAME</strong></td>
        <td>Linked Data 목록</td>
        <td>서지정보</td>
        <td>RDF</td>
        <td>차세대 웹 목록</td>
      </tr>
      <tr>
        <td><strong>Dublin Core</strong></td>
        <td>간단한 메타데이터</td>
        <td>기본 서지정보</td>
        <td>XML/RDF</td>
        <td>웹 자원</td>
      </tr>
      <tr class="highlight-row">
        <td><strong>METS</strong></td>
        <td><strong>디지털 객체 패키징</strong></td>
        <td><strong>모든 메타데이터<br>+ 파일 + 구조</strong></td>
        <td>XML</td>
        <td><strong>디지털 아카이브<br>보존 시스템</strong></td>
      </tr>
    </tbody>
  </table>

  <div class="summary-insight">
    <h4>🎯 핵심 정리</h4>
    <div class="insight-grid">
      <div class="insight-item">
        <strong>MARC/MODS/BIBFRAME</strong>
        <p>"무엇"에 대한 정보<br>(서지 메타데이터만)</p>
      </div>
      <div class="arrow-big">→</div>
      <div class="insight-item highlight">
        <strong>METS</strong>
        <p>"무엇" + "파일" + "구조"<br>(완전한 디지털 패키지)</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>8. METS 작업 흐름</h2>

  <div class="workflow">
    <h4>📋 디지털화 프로젝트에서 METS 사용하기</h4>

    <div class="workflow-steps">
      <div class="workflow-step">
        <div class="step-num">1</div>
        <div class="step-content">
          <h5>자료 디지털화</h5>
          <p>책, 문서를 스캔하여 이미지/PDF 파일 생성</p>
        </div>
      </div>

      <div class="workflow-arrow">⬇️</div>

      <div class="workflow-step">
        <div class="step-num">2</div>
        <div class="step-content">
          <h5>메타데이터 작성</h5>
          <p>MODS로 서지정보 작성, PREMIS로 보존 정보 작성</p>
        </div>
      </div>

      <div class="workflow-arrow">⬇️</div>

      <div class="workflow-step">
        <div class="step-num">3</div>
        <div class="step-content">
          <h5>구조 정의</h5>
          <p>페이지 순서, 목차 구조 정의</p>
        </div>
      </div>

      <div class="workflow-arrow">⬇️</div>

      <div class="workflow-step highlighted">
        <div class="step-num">4</div>
        <div class="step-content">
          <h5>METS로 패키징</h5>
          <p>파일 + 메타데이터 + 구조를 하나의 METS XML로</p>
        </div>
      </div>

      <div class="workflow-arrow">⬇️</div>

      <div class="workflow-step">
        <div class="step-num">5</div>
        <div class="step-content">
          <h5>저장소에 저장</h5>
          <p>DSpace, Fedora 등 리포지터리 시스템에 업로드</p>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>9. 요약: 한눈에 정리</h2>

  <div class="final-summary">
    <div class="summary-card main">
      <h3>📦 METS란?</h3>
      <p class="definition">디지털 객체와 메타데이터를 하나로 묶는 XML 포장 표준</p>

      <div class="features">
        <div class="feature">
          <strong>개발:</strong> 미국 의회도서관 + DLF
        </div>
        <div class="feature">
          <strong>형식:</strong> XML
        </div>
        <div class="feature">
          <strong>용도:</strong> 디지털 아카이브, 보존
        </div>
      </div>
    </div>

    <div class="summary-sections">
      <h4>7가지 섹션</h4>
      <ol>
        <li>metsHdr - 패키지 정보</li>
        <li>dmdSec - 기술 메타데이터</li>
        <li>amdSec - 관리 메타데이터</li>
        <li>fileSec - 파일 목록</li>
        <li><strong>structMap - 구조 (핵심!)</strong></li>
        <li>structLink - 구조 링크</li>
        <li>behaviorSec - 행위</li>
      </ol>
    </div>
  </div>

  <div class="key-takeaway">
    <h3>🎯 가장 중요한 것!</h3>
    <div class="takeaway-box">
      <p class="big-emphasis">
        <strong>METS = 메타데이터의 "컨테이너"</strong>
      </p>
      <p>다른 표준들(MODS, MARC 등)은 <em>내용</em>을 기술하지만,<br>
      METS는 그 내용들과 파일을 <strong>하나로 묶어 포장</strong>합니다.</p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>10. 학습 점검 퀴즈</h2>

  <div class="quiz-section">
    <div class="quiz-item">
      <p><strong>Q1.</strong> METS를 한 문장으로 설명하면?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>디지털 객체와 그 메타데이터를 하나로 묶어 포장하는 XML 표준</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> MODS와 METS의 가장 큰 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>MODS는 서지정보만</strong> 기술하고, <strong>METS는 파일과 구조까지 포함</strong>하여 패키징</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> METS의 7가지 섹션 중 핵심은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>&lt;structMap&gt; (구조 맵)</strong> - 파일들의 계층 구조를 표현하는 METS만의 핵심 기능</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> MODS와 METS를 함께 사용할 수 있나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>가능</strong>합니다! METS의 dmdSec 섹션 안에 MODS를 넣을 수 있습니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> METS가 주로 사용되는 곳은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>디지털 아카이브, 디지털 도서관, 기관 리포지터리, 장기 보존 시스템</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q6.</strong> 단순히 책 제목과 저자만 기록하려면 METS가 필요한가요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>불필요</strong>합니다. 단순 서지정보만 필요하면 MODS나 MARC를 사용하세요.</p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 더 알아보기</h2>
  <ul>
    <li><strong>METS 공식 사이트</strong> - Library of Congress METS 문서</li>
    <li><strong>METS Schema</strong> - XML 스키마 정의 및 가이드</li>
    <li><strong>METS Profiles</strong> - 분야별 METS 사용 지침</li>
    <li><strong>DSpace METS Implementation</strong> - 실전 활용 예시</li>
    <li><strong>PREMIS</strong> - 보존 메타데이터 (METS와 함께 사용)</li>
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
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.analogy-visual {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 2rem 0;
  flex-wrap: wrap;
}

.analogy-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  min-width: 150px;
  border: 2px solid #ddd;
}

.analogy-item.highlight {
  border: 3px solid #ff9800;
  background: #fffbf0;
  font-weight: bold;
}

.icon {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.plus, .arrow {
  font-size: 2rem;
  color: #4caf50;
  font-weight: bold;
}

.analogy-text {
  text-align: center;
  font-size: 1.1rem;
  color: #666;
  margin-top: 1rem;
}

.comparison-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

.standard-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #ddd;
  text-align: center;
}

.standard-card.highlighted {
  border: 3px solid #ff9800;
  box-shadow: 0 4px 8px rgba(255,152,0,0.3);
}

.standard-card h4 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.role {
  font-weight: bold;
  color: #1976d2;
  margin: 0.5rem 0;
}

.purpose {
  font-size: 0.95rem;
  color: #666;
  margin: 0.75rem 0;
  font-style: italic;
}

.scope {
  background: #f5f5f5;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.key-difference {
  background: #e8f5e9;
  border-left: 4px solid #4caf50;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.diff-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  background: white;
}

.diff-table th,
.diff-table td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.diff-table th {
  background: #4caf50;
  color: white;
  font-weight: bold;
}

.highlight-row {
  background: #fff3e0;
  font-weight: bold;
}

.role-explanation {
  margin: 2rem 0;
}

.wrapper-concept {
  background: white;
  border: 3px solid #ff9800;
  border-radius: 8px;
  padding: 2rem;
  margin: 1.5rem 0;
  position: relative;
}

.inner-content {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 4px;
}

.wrapper-label {
  position: absolute;
  right: -200px;
  top: 50%;
  transform: translateY(-50%);
  background: #ff9800;
  color: white;
  padding: 1rem;
  border-radius: 4px;
  font-weight: bold;
  white-space: nowrap;
}

.mets-vs-others {
  margin: 2rem 0;
}

.relation-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin-top: 1rem;
}

.relation-table th,
.relation-table td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.relation-table th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.relation-table tr:nth-child(even) {
  background: #f5f5f5;
}

.sections-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

.section-card {
  background: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  position: relative;
}

.section-card.highlight {
  border: 3px solid #ff9800;
  background: #fff3e0;
}

.section-number {
  position: absolute;
  top: -15px;
  left: 15px;
  background: #1976d2;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.section-card h4 {
  color: #1976d2;
  font-family: monospace;
  margin: 1rem 0 0.5rem 0;
}

.section-name {
  font-weight: bold;
  color: #333;
  margin: 0.5rem 0;
}

.section-desc {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
}

.example-mini {
  background: #f5f5f5;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.85rem;
  margin-top: 0.75rem;
  text-align: center;
}

.structure-highlight {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.example-box {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.digital-book {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.book-structure {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.code-example {
  margin: 2rem 0;
}

.code-block {
  background: #263238;
  color: #aed581;
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  line-height: 1.6;
}

.explanation-box {
  background: #f1f8e9;
  border-left: 4px solid #8bc34a;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.usecases {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.usecase-card {
  padding: 1.5rem;
  border-radius: 8px;
}

.usecase-card.yes {
  background: #e8f5e9;
  border: 3px solid #4caf50;
}

.usecase-card.no {
  background: #ffebee;
  border: 3px solid #f44336;
}

.usecase-card h4 {
  margin-bottom: 1rem;
}

.practical-examples {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 4px;
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.example-item {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
}

.example-item h5 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.master-comparison {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  background: white;
}

.master-comparison th,
.master-comparison td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.master-comparison th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.master-comparison tr:nth-child(even) {
  background: #f5f5f5;
}

.summary-insight {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.insight-grid {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  margin-top: 1.5rem;
}

.insight-item {
  background: white;
  padding: 2rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  text-align: center;
  flex: 1;
}

.insight-item.highlight {
  border: 3px solid #ff9800;
  background: #fffbf0;
}

.arrow-big {
  font-size: 3rem;
  color: #4caf50;
}

.workflow {
  margin: 2rem 0;
}

.workflow-steps {
  margin-top: 1.5rem;
}

.workflow-step {
  display: flex;
  gap: 1.5rem;
  align-items: start;
  margin: 1rem 0;
}

.workflow-step.highlighted {
  background: #fff3e0;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #ff9800;
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

.workflow-step.highlighted .step-num {
  background: #ff9800;
}

.step-content {
  flex: 1;
}

.step-content h5 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.workflow-arrow {
  text-align: center;
  font-size: 2rem;
  color: #4caf50;
  margin: 0.5rem 0;
}

.final-summary {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.summary-card {
  background: white;
  padding: 2rem;
  border: 2px solid #ddd;
  border-radius: 8px;
}

.summary-card.main {
  border: 3px solid #ff9800;
}

.definition {
  font-size: 1.1rem;
  color: #333;
  margin: 1rem 0;
  line-height: 1.6;
}

.features {
  display: grid;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.feature {
  background: #f5f5f5;
  padding: 0.75rem;
  border-radius: 4px;
}

.summary-sections {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
}

.summary-sections ol {
  margin-top: 1rem;
}

.summary-sections li {
  margin: 0.5rem 0;
}

.key-takeaway {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
}

.key-takeaway h3,
.key-takeaway p {
  color: white;
}

.takeaway-box {
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
  .comparison-grid,
  .sections-grid,
  .examples-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .wrapper-label {
    position: static;
    transform: none;
    margin-top: 1rem;
  }
}

@media (max-width: 768px) {
  .comparison-grid,
  .usecases,
  .final-summary,
  .sections-grid,
  .examples-grid {
    grid-template-columns: 1fr;
  }

  .analogy-visual {
    flex-direction: column;
  }

  .insight-grid {
    flex-direction: column;
  }
}
</style>
        """,
        category=mets_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=35,
        prerequisites="MODS 기본 이해, XML 기초 지식",
        learning_objectives="METS의 목적과 역할 이해하기, METS와 MODS/MARC/BIBFRAME의 차이점 파악하기, METS의 7가지 섹션 구조 익히기, 디지털 객체 패키징 방법 배우기, METS의 적절한 사용처 판단하기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {mets_category.name} (상위: {metadata_category.name})")
    print(f"  - 난이도: 중급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=metadata")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_mets_content()
