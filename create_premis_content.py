import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content, Category, Tag
from apps.accounts.models import User

# 관리자 사용자 가져오기
admin_user = User.objects.filter(role='ADMIN').first()
if not admin_user:
    print("관리자 사용자를 찾을 수 없습니다.")
    exit()

# 메타데이터 카테고리 가져오기
try:
    metadata_category = Category.objects.get(slug='metadata')
except Category.DoesNotExist:
    print("메타데이터 카테고리를 찾을 수 없습니다.")
    exit()

# 태그 생성 또는 가져오기
tags_data = [
    ('PREMIS', 'premis'),
    ('디지털보존', 'digital-preservation'),
    ('메타데이터표준', 'metadata-standard'),
    ('보존메타데이터', 'preservation-metadata'),
    ('디지털아카이빙', 'digital-archiving'),
]

tags = []
for tag_name, tag_slug in tags_data:
    tag, created = Tag.objects.get_or_create(
        slug=tag_slug,
        defaults={'name': tag_name}
    )
    tags.append(tag)
    if created:
        print(f"태그 생성됨: {tag_name}")

# PREMIS 콘텐츠 HTML 작성
content_html = """
<div class="premis-tutorial">
  <h1>PREMIS: 디지털 보존을 위한 메타데이터 표준</h1>

  <div class="intro-section">
    <h2>📚 학습 목표</h2>
    <ul>
      <li>PREMIS가 무엇인지, 왜 필요한지 이해하기</li>
      <li>PREMIS 데이터 모델의 핵심 구성 요소 파악하기</li>
      <li>실제 PREMIS 메타데이터 예시를 통해 적용 방법 학습하기</li>
      <li>도서관 및 아카이브에서의 실무 활용 방안 이해하기</li>
    </ul>
  </div>

  <div class="section">
    <h2>1️⃣ PREMIS란 무엇인가요?</h2>

    <div class="explanation-box">
      <h3>💡 쉽게 이해하기</h3>
      <p>
        여러분이 중요한 디지털 사진을 가지고 있다고 상상해보세요. 10년 후에도 그 사진을 볼 수 있을까요?
        파일 형식이 바뀌거나, 하드웨어가 오래되거나, 소프트웨어가 업데이트되면 어떻게 될까요?
      </p>
      <p>
        <strong>PREMIS(PREservation Metadata: Implementation Strategies)</strong>는 바로 이런 문제를 해결하기 위한
        <strong>디지털 보존 메타데이터 표준</strong>입니다.
      </p>
    </div>

    <div class="definition-box">
      <h3>📖 정의</h3>
      <p>
        PREMIS는 디지털 자료를 <strong>장기적으로 보존하고 관리</strong>하기 위해 필요한 메타데이터를
        체계적으로 기술하는 국제 표준입니다.
      </p>
    </div>

    <div class="history-box">
      <h3>🕰️ PREMIS의 역사</h3>
      <ul>
        <li><strong>2003년:</strong> OCLC와 RLG가 공동 작업 그룹 구성</li>
        <li><strong>2005년:</strong> PREMIS 데이터 사전 1.0 발표</li>
        <li><strong>2008년:</strong> 버전 2.0 발표 (XML 스키마 포함)</li>
        <li><strong>2015년:</strong> 버전 3.0 발표 (현재 버전)</li>
        <li><strong>현재:</strong> 국제도서관협회연맹(IFLA)과 미국의회도서관이 공동 관리</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>2️⃣ 왜 PREMIS가 필요한가요?</h2>

    <div class="problem-box">
      <h3>🤔 디지털 보존의 어려움</h3>

      <div class="challenge">
        <h4>문제 1: 기술적 진부화</h4>
        <p>
          <strong>예시:</strong> 1990년대에 만든 HWP 파일, 지금도 열 수 있나요?
          플로피 디스크에 저장된 자료는요?
        </p>
        <p class="solution">
          <strong>PREMIS 해결책:</strong> 파일 형식, 생성 소프트웨어, 의존성 정보를 기록하여
          향후 마이그레이션이나 에뮬레이션에 활용
        </p>
      </div>

      <div class="challenge">
        <h4>문제 2: 진본성 입증</h4>
        <p>
          <strong>예시:</strong> 이 디지털 문서가 정말 원본인지, 누가 언제 수정했는지 어떻게 증명하나요?
        </p>
        <p class="solution">
          <strong>PREMIS 해결책:</strong> 모든 변경 이력(Event)과 책임자(Agent) 정보를 기록하여
          신뢰성과 진본성 보장
        </p>
      </div>

      <div class="challenge">
        <h4>문제 3: 법적 권리 관리</h4>
        <p>
          <strong>예시:</strong> 이 디지털 자료를 누가 열람할 수 있나요? 복제는? 재배포는?
        </p>
        <p class="solution">
          <strong>PREMIS 해결책:</strong> 저작권, 접근 권한, 이용 조건을 명확히 기록
        </p>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>3️⃣ PREMIS 데이터 모델</h2>

    <div class="model-overview">
      <h3>🏗️ 4가지 핵심 엔티티</h3>
      <p>PREMIS는 4개의 상호 연결된 엔티티로 구성됩니다:</p>
    </div>

    <div class="entity-grid">
      <div class="entity-card">
        <h4>1. Object (객체)</h4>
        <p class="entity-desc">보존 대상이 되는 디지털 자료</p>
        <p class="example">예: PDF 파일, 이미지, 웹사이트</p>
        <div class="entity-types">
          <strong>하위 유형:</strong>
          <ul>
            <li><strong>파일(File):</strong> 컴퓨터 파일 시스템의 개별 파일</li>
            <li><strong>비트스트림(Bitstream):</strong> 파일 내의 데이터 스트림</li>
            <li><strong>지적 개체(Intellectual Entity):</strong> 논리적 단위 (예: 전자책)</li>
            <li><strong>표현형(Representation):</strong> 지적 개체의 특정 형태</li>
          </ul>
        </div>
      </div>

      <div class="entity-card">
        <h4>2. Event (이벤트)</h4>
        <p class="entity-desc">객체에 발생한 모든 행위</p>
        <p class="example">예: 생성, 수정, 마이그레이션, 바이러스 검사</p>
        <div class="entity-info">
          <strong>포함 정보:</strong>
          <ul>
            <li>이벤트 유형 (생성, 검증, 마이그레이션 등)</li>
            <li>발생 일시</li>
            <li>결과 (성공/실패)</li>
            <li>세부 정보</li>
          </ul>
        </div>
      </div>

      <div class="entity-card">
        <h4>3. Agent (에이전트)</h4>
        <p class="entity-desc">이벤트 수행 주체</p>
        <p class="example">예: 사람, 조직, 소프트웨어</p>
        <div class="entity-info">
          <strong>포함 정보:</strong>
          <ul>
            <li>에이전트 식별자</li>
            <li>에이전트 이름</li>
            <li>에이전트 유형 (사람/조직/소프트웨어)</li>
          </ul>
        </div>
      </div>

      <div class="entity-card">
        <h4>4. Rights (권리)</h4>
        <p class="entity-desc">객체와 관련된 법적 권리</p>
        <p class="example">예: 저작권, 접근 권한, 이용 허가</p>
        <div class="entity-info">
          <strong>포함 정보:</strong>
          <ul>
            <li>권리 유형 (저작권, 라이선스 등)</li>
            <li>권리 보유자</li>
            <li>권리 범위</li>
            <li>권리 기간</li>
          </ul>
        </div>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>4️⃣ 실제 예시로 배우는 PREMIS</h2>

    <div class="scenario">
      <h3>📖 시나리오</h3>
      <p>
        전북대학교 도서관이 <strong>"2024년 졸업 논문 모음집.pdf"</strong> 파일을
        기관 리포지터리에 보존하려고 합니다.
      </p>
    </div>

    <div class="example-section">
      <h3>예시 1: Object 메타데이터</h3>

      <div class="code-explanation">
        <p><strong>👉 이 부분이 중요한 이유:</strong></p>
        <p>
          Object 메타데이터는 파일의 "신분증"과 같습니다.
          파일이 무엇인지, 어떤 형식인지, 크기가 얼마인지 등 기본 정보를 담고 있습니다.
        </p>
      </div>

      <pre><code class="language-xml">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;premis:object xsi:type="premis:file"&gt;

  &lt;!-- 객체 식별자: 이 파일의 고유 ID --&gt;
  &lt;premis:objectIdentifier&gt;
    &lt;premis:objectIdentifierType&gt;UUID&lt;/premis:objectIdentifierType&gt;
    &lt;premis:objectIdentifierValue&gt;
      550e8400-e29b-41d4-a716-446655440000
    &lt;/premis:objectIdentifierValue&gt;
  &lt;/premis:objectIdentifier&gt;

  &lt;!-- 객체 카테고리: 파일 유형 --&gt;
  &lt;premis:objectCategory&gt;file&lt;/premis:objectCategory&gt;

  &lt;!-- 파일 특성 정보 --&gt;
  &lt;premis:objectCharacteristics&gt;

    &lt;!-- 파일 크기 (바이트) --&gt;
    &lt;premis:size&gt;2458624&lt;/premis:size&gt;
    &lt;!-- 👆 약 2.4MB입니다 --&gt;

    &lt;!-- 파일 형식 정보 --&gt;
    &lt;premis:format&gt;
      &lt;premis:formatDesignation&gt;
        &lt;premis:formatName&gt;PDF&lt;/premis:formatName&gt;
        &lt;premis:formatVersion&gt;1.7&lt;/premis:formatVersion&gt;
        &lt;!-- 👆 PDF 버전 1.7 (Adobe PDF 1.7 = ISO 32000-1) --&gt;
      &lt;/premis:formatDesignation&gt;

      &lt;premis:formatRegistry&gt;
        &lt;premis:formatRegistryName&gt;PRONOM&lt;/premis:formatRegistryName&gt;
        &lt;premis:formatRegistryKey&gt;fmt/276&lt;/premis:formatRegistryKey&gt;
        &lt;!-- 👆 PRONOM은 영국 국립기록원의 파일 형식 레지스트리입니다 --&gt;
      &lt;/premis:formatRegistry&gt;
    &lt;/premis:format&gt;

    &lt;!-- 체크섬: 파일 무결성 검증용 --&gt;
    &lt;premis:fixity&gt;
      &lt;premis:messageDigestAlgorithm&gt;SHA-256&lt;/premis:messageDigestAlgorithm&gt;
      &lt;premis:messageDigest&gt;
        7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730
      &lt;/premis:messageDigest&gt;
      &lt;!-- 👆 이 값이 바뀌면 파일이 손상되었거나 변조되었다는 뜻입니다 --&gt;
      &lt;premis:messageDigestOriginator&gt;repository_system&lt;/premis:messageDigestOriginator&gt;
    &lt;/premis:fixity&gt;

    &lt;!-- 생성 애플리케이션 정보 --&gt;
    &lt;premis:creatingApplication&gt;
      &lt;premis:creatingApplicationName&gt;
        Adobe Acrobat Pro DC
      &lt;/premis:creatingApplicationName&gt;
      &lt;premis:creatingApplicationVersion&gt;2024.001.20643&lt;/premis:creatingApplicationVersion&gt;
      &lt;premis:dateCreatedByApplication&gt;2024-12-15&lt;/premis:dateCreatedByApplication&gt;
    &lt;/premis:creatingApplication&gt;
  &lt;/premis:objectCharacteristics&gt;

  &lt;!-- 원본 파일명 --&gt;
  &lt;premis:originalName&gt;2024년_졸업논문_모음집.pdf&lt;/premis:originalName&gt;

  &lt;!-- 저장 위치 --&gt;
  &lt;premis:storage&gt;
    &lt;premis:storageMedium&gt;online storage&lt;/premis:storageMedium&gt;
    &lt;premis:contentLocation&gt;
      &lt;premis:contentLocationType&gt;URL&lt;/premis:contentLocationType&gt;
      &lt;premis:contentLocationValue&gt;
        https://repository.jbnu.ac.kr/files/2024/thesis_collection.pdf
      &lt;/premis:contentLocationValue&gt;
    &lt;/premis:contentLocation&gt;
  &lt;/premis:storage&gt;

&lt;/premis:object&gt;</code></pre>

      <div class="explanation-callout">
        <h4>🔍 왜 이런 정보가 필요한가요?</h4>
        <ul>
          <li><strong>UUID:</strong> 파일이 여러 곳에 복제되어도 동일한 것임을 식별</li>
          <li><strong>체크섬:</strong> 파일이 손상되지 않았는지 주기적으로 검증</li>
          <li><strong>형식 정보:</strong> 10년 후에도 이 파일을 열 수 있는 소프트웨어 찾기</li>
          <li><strong>생성 애플리케이션:</strong> 파일 재현 문제 발생 시 참고</li>
        </ul>
      </div>
    </div>

    <div class="example-section">
      <h3>예시 2: Event 메타데이터</h3>

      <div class="code-explanation">
        <p><strong>👉 이 부분이 중요한 이유:</strong></p>
        <p>
          Event 메타데이터는 파일의 "일지"입니다.
          파일에 무슨 일이 일어났는지, 누가 했는지, 언제 했는지 모두 기록합니다.
        </p>
      </div>

      <h4>이벤트 1: 파일 수집 (Ingestion)</h4>
      <pre><code class="language-xml">&lt;premis:event&gt;

  &lt;!-- 이벤트 식별자 --&gt;
  &lt;premis:eventIdentifier&gt;
    &lt;premis:eventIdentifierType&gt;UUID&lt;/premis:eventIdentifierType&gt;
    &lt;premis:eventIdentifierValue&gt;
      evt-2024-12-15-001
    &lt;/premis:eventIdentifierValue&gt;
  &lt;/premis:eventIdentifier&gt;

  &lt;!-- 이벤트 유형 --&gt;
  &lt;premis:eventType&gt;ingestion&lt;/premis:eventType&gt;
  &lt;!-- 👆 "수집" - 파일이 저장소에 처음 들어온 것 --&gt;

  &lt;!-- 이벤트 발생 시간 --&gt;
  &lt;premis:eventDateTime&gt;2024-12-15T14:23:05+09:00&lt;/premis:eventDateTime&gt;
  &lt;!-- 👆 2024년 12월 15일 오후 2시 23분 5초 (한국 시간) --&gt;

  &lt;!-- 이벤트 상세 설명 --&gt;
  &lt;premis:eventDetailInformation&gt;
    &lt;premis:eventDetail&gt;
      전북대학교 기관 리포지터리 시스템에 2024년 졸업논문 모음집 파일을
      업로드하고 초기 검증을 완료함
    &lt;/premis:eventDetail&gt;
  &lt;/premis:eventDetailInformation&gt;

  &lt;!-- 이벤트 결과 --&gt;
  &lt;premis:eventOutcomeInformation&gt;
    &lt;premis:eventOutcome&gt;success&lt;/premis:eventOutcome&gt;
    &lt;!-- 👆 성공! --&gt;
    &lt;premis:eventOutcomeDetail&gt;
      &lt;premis:eventOutcomeDetailNote&gt;
        파일 무결성 검증 완료. 바이러스 검사 통과.
      &lt;/premis:eventOutcomeDetailNote&gt;
    &lt;/premis:eventOutcomeDetail&gt;
  &lt;/premis:eventOutcomeInformation&gt;

  &lt;!-- 이벤트 수행자 연결 --&gt;
  &lt;premis:linkingAgentIdentifier&gt;
    &lt;premis:linkingAgentIdentifierType&gt;staff_id&lt;/premis:linkingAgentIdentifierType&gt;
    &lt;premis:linkingAgentIdentifierValue&gt;
      librarian_kim_suntae
    &lt;/premis:linkingAgentIdentifierValue&gt;
    &lt;!-- 👆 김선태 사서가 수행했습니다 --&gt;
  &lt;/premis:linkingAgentIdentifier&gt;

  &lt;!-- 대상 객체 연결 --&gt;
  &lt;premis:linkingObjectIdentifier&gt;
    &lt;premis:linkingObjectIdentifierType&gt;UUID&lt;/premis:linkingObjectIdentifierType&gt;
    &lt;premis:linkingObjectIdentifierValue&gt;
      550e8400-e29b-41d4-a716-446655440000
    &lt;/premis:linkingObjectIdentifierValue&gt;
    &lt;!-- 👆 위에서 본 그 파일입니다 --&gt;
  &lt;/premis:linkingObjectIdentifier&gt;

&lt;/premis:event&gt;</code></pre>

      <h4>이벤트 2: 바이러스 검사 (Virus Check)</h4>
      <pre><code class="language-xml">&lt;premis:event&gt;
  &lt;premis:eventIdentifier&gt;
    &lt;premis:eventIdentifierType&gt;UUID&lt;/premis:eventIdentifierType&gt;
    &lt;premis:eventIdentifierValue&gt;evt-2024-12-15-002&lt;/premis:eventIdentifierValue&gt;
  &lt;/premis:eventIdentifier&gt;

  &lt;premis:eventType&gt;virus check&lt;/premis:eventType&gt;
  &lt;!-- 👆 바이러스 검사 --&gt;

  &lt;premis:eventDateTime&gt;2024-12-15T14:23:15+09:00&lt;/premis:eventDateTime&gt;

  &lt;premis:eventDetailInformation&gt;
    &lt;premis:eventDetail&gt;
      ClamAV 안티바이러스 엔진을 사용하여 악성코드 검사 수행
    &lt;/premis:eventDetail&gt;
  &lt;/premis:eventDetailInformation&gt;

  &lt;premis:eventOutcomeInformation&gt;
    &lt;premis:eventOutcome&gt;success&lt;/premis:eventOutcome&gt;
    &lt;premis:eventOutcomeDetail&gt;
      &lt;premis:eventOutcomeDetailNote&gt;
        악성코드 미발견. 안전한 파일로 확인됨.
      &lt;/premis:eventOutcomeDetailNote&gt;
    &lt;/premis:eventOutcomeDetail&gt;
  &lt;/premis:eventOutcomeInformation&gt;

  &lt;!-- 소프트웨어가 수행 --&gt;
  &lt;premis:linkingAgentIdentifier&gt;
    &lt;premis:linkingAgentIdentifierType&gt;software&lt;/premis:linkingAgentIdentifierType&gt;
    &lt;premis:linkingAgentIdentifierValue&gt;
      clamav_v1.3.0
    &lt;/premis:linkingAgentIdentifierValue&gt;
  &lt;/premis:linkingAgentIdentifier&gt;

  &lt;premis:linkingObjectIdentifier&gt;
    &lt;premis:linkingObjectIdentifierType&gt;UUID&lt;/premis:linkingObjectIdentifierType&gt;
    &lt;premis:linkingObjectIdentifierValue&gt;
      550e8400-e29b-41d4-a716-446655440000
    &lt;/premis:linkingObjectIdentifierValue&gt;
  &lt;/premis:linkingObjectIdentifier&gt;
&lt;/premis:event&gt;</code></pre>

      <div class="explanation-callout">
        <h4>🔍 이벤트 기록의 중요성</h4>
        <ul>
          <li><strong>진본성 입증:</strong> "이 파일은 2024년 12월 15일에 김선태 사서가 업로드했고, 그 이후 수정되지 않았습니다"</li>
          <li><strong>문제 추적:</strong> 파일이 손상되었다면, 언제부터인지 이벤트 로그로 확인 가능</li>
          <li><strong>법적 증거:</strong> 법정에서 디지털 증거물로 사용 시 이력 증명</li>
        </ul>
      </div>
    </div>

    <div class="example-section">
      <h3>예시 3: Agent 메타데이터</h3>

      <div class="code-explanation">
        <p><strong>👉 이 부분이 중요한 이유:</strong></p>
        <p>
          누가 파일을 다뤘는지 명확히 기록해야 책임 소재가 분명해집니다.
        </p>
      </div>

      <h4>에이전트 1: 사람 (김선태 사서)</h4>
      <pre><code class="language-xml">&lt;premis:agent&gt;

  &lt;premis:agentIdentifier&gt;
    &lt;premis:agentIdentifierType&gt;staff_id&lt;/premis:agentIdentifierType&gt;
    &lt;premis:agentIdentifierValue&gt;
      librarian_kim_suntae
    &lt;/premis:agentIdentifierValue&gt;
  &lt;/premis:agentIdentifier&gt;

  &lt;premis:agentName&gt;김선태&lt;/premis:agentName&gt;

  &lt;premis:agentType&gt;person&lt;/premis:agentType&gt;
  &lt;!-- 👆 사람입니다 --&gt;

  &lt;premis:agentNote&gt;
    전북대학교 문헌정보학과 교수 / 기관 리포지터리 관리자
  &lt;/premis:agentNote&gt;

&lt;/premis:agent&gt;</code></pre>

      <h4>에이전트 2: 소프트웨어 (ClamAV)</h4>
      <pre><code class="language-xml">&lt;premis:agent&gt;

  &lt;premis:agentIdentifier&gt;
    &lt;premis:agentIdentifierType&gt;software&lt;/premis:agentIdentifierType&gt;
    &lt;premis:agentIdentifierValue&gt;clamav_v1.3.0&lt;/premis:agentIdentifierValue&gt;
  &lt;/premis:agentIdentifier&gt;

  &lt;premis:agentName&gt;ClamAV&lt;/premis:agentName&gt;

  &lt;premis:agentType&gt;software&lt;/premis:agentType&gt;
  &lt;!-- 👆 소프트웨어입니다 --&gt;

  &lt;premis:agentVersion&gt;1.3.0&lt;/premis:agentVersion&gt;

  &lt;premis:agentNote&gt;
    오픈소스 안티바이러스 엔진
  &lt;/premis:agentNote&gt;

&lt;/premis:agent&gt;</code></pre>

      <h4>에이전트 3: 조직 (전북대학교)</h4>
      <pre><code class="language-xml">&lt;premis:agent&gt;

  &lt;premis:agentIdentifier&gt;
    &lt;premis:agentIdentifierType&gt;organization_code&lt;/premis:agentIdentifierType&gt;
    &lt;premis:agentIdentifierValue&gt;JBNU&lt;/premis:agentIdentifierValue&gt;
  &lt;/premis:agentIdentifier&gt;

  &lt;premis:agentName&gt;전북대학교&lt;/premis:agentName&gt;

  &lt;premis:agentType&gt;organization&lt;/premis:agentType&gt;
  &lt;!-- 👆 조직입니다 --&gt;

  &lt;premis:agentNote&gt;
    Jeonbuk National University - 대한민국 국립대학교
  &lt;/premis:agentNote&gt;

&lt;/premis:agent&gt;</code></pre>
    </div>

    <div class="example-section">
      <h3>예시 4: Rights 메타데이터</h3>

      <div class="code-explanation">
        <p><strong>👉 이 부분이 중요한 이유:</strong></p>
        <p>
          디지털 자료를 누가 어떻게 사용할 수 있는지 법적으로 명확히 해야 합니다.
        </p>
      </div>

      <pre><code class="language-xml">&lt;premis:rights&gt;

  &lt;!-- 권리 구문 --&gt;
  &lt;premis:rightsStatement&gt;

    &lt;premis:rightsStatementIdentifier&gt;
      &lt;premis:rightsStatementIdentifierType&gt;
        local
      &lt;/premis:rightsStatementIdentifierType&gt;
      &lt;premis:rightsStatementIdentifierValue&gt;
        rights-001
      &lt;/premis:rightsStatementIdentifierValue&gt;
    &lt;/premis:rightsStatementIdentifier&gt;

    &lt;!-- 저작권 정보 --&gt;
    &lt;premis:copyrightInformation&gt;

      &lt;premis:copyrightStatus&gt;copyrighted&lt;/premis:copyrightStatus&gt;
      &lt;!-- 👆 저작권 보호를 받는 저작물입니다 --&gt;

      &lt;premis:copyrightJurisdiction&gt;kr&lt;/premis:copyrightJurisdiction&gt;
      &lt;!-- 👆 대한민국 저작권법 적용 --&gt;

      &lt;premis:copyrightStatusDeterminationDate&gt;
        2024-12-15
      &lt;/premis:copyrightStatusDeterminationDate&gt;

      &lt;premis:copyrightNote&gt;
        본 졸업논문 모음집의 저작권은 각 논문 저자에게 있으며,
        전북대학교는 교육 및 연구 목적의 배포 권한을 보유함
      &lt;/premis:copyrightNote&gt;

    &lt;/premis:copyrightInformation&gt;

    &lt;!-- 접근 권한 정보 --&gt;
    &lt;premis:rightsGranted&gt;

      &lt;premis:act&gt;disseminate&lt;/premis:act&gt;
      &lt;!-- 👆 "배포" 행위에 대한 권한 --&gt;

      &lt;premis:restriction&gt;
        &lt;premis:restrictionType&gt;access&lt;/premis:restrictionType&gt;
        &lt;premis:restrictionValue&gt;
          전북대학교 구성원 (학생, 교직원)에게만 접근 허용
        &lt;/premis:restrictionValue&gt;
      &lt;/premis:restriction&gt;

      &lt;premis:termOfGrant&gt;
        &lt;premis:startDate&gt;2024-12-15&lt;/premis:startDate&gt;
        &lt;premis:endDate&gt;2029-12-31&lt;/premis:endDate&gt;
        &lt;!-- 👆 5년간 유효 --&gt;
      &lt;/premis:termOfGrant&gt;

    &lt;/premis:rightsGranted&gt;

    &lt;!-- 복제 권한 정보 --&gt;
    &lt;premis:rightsGranted&gt;

      &lt;premis:act&gt;replicate&lt;/premis:act&gt;
      &lt;!-- 👆 "복제" 행위에 대한 권한 --&gt;

      &lt;premis:restriction&gt;
        &lt;premis:restrictionType&gt;permission&lt;/premis:restrictionType&gt;
        &lt;premis:restrictionValue&gt;
          보존 목적의 복제는 허용됨. 상업적 복제는 금지.
        &lt;/premis:restrictionValue&gt;
      &lt;/premis:restriction&gt;

      &lt;premis:rightsGrantedNote&gt;
        도서관은 디지털 보존을 위해 필요한 만큼 복제본을 생성할 수 있음
      &lt;/premis:rightsGrantedNote&gt;

    &lt;/premis:rightsGranted&gt;

  &lt;/premis:rightsStatement&gt;

  &lt;!-- 권리 보유자 연결 --&gt;
  &lt;premis:linkingAgentIdentifier&gt;
    &lt;premis:linkingAgentIdentifierType&gt;
      organization_code
    &lt;/premis:linkingAgentIdentifierType&gt;
    &lt;premis:linkingAgentIdentifierValue&gt;
      JBNU
    &lt;/premis:linkingAgentIdentifierValue&gt;
  &lt;/premis:linkingAgentIdentifier&gt;

&lt;/premis:rights&gt;</code></pre>

      <div class="explanation-callout">
        <h4>🔍 권리 정보의 실무적 활용</h4>
        <ul>
          <li><strong>접근 통제:</strong> 시스템이 이 정보를 읽고 자동으로 접근 권한 확인</li>
          <li><strong>보존 정책:</strong> 복제 권한에 따라 백업 정책 결정</li>
          <li><strong>만료 관리:</strong> 권리 기간 만료 전에 갱신 여부 검토</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>5️⃣ PREMIS 엔티티 간의 관계</h2>

    <div class="relationship-diagram">
      <h3>🔗 어떻게 연결되나요?</h3>

      <div class="diagram-explanation">
        <p>위의 예시들이 실제로 어떻게 연결되는지 보겠습니다:</p>

        <pre><code>
📄 Object (2024년_졸업논문_모음집.pdf)
    │
    ├─── 🎬 Event 1: ingestion (수집)
    │       ├─── 수행자: 👤 Agent (김선태 사서)
    │       └─── 결과: 성공
    │
    ├─── 🎬 Event 2: virus check (바이러스 검사)
    │       ├─── 수행자: 💻 Agent (ClamAV 소프트웨어)
    │       └─── 결과: 안전
    │
    └─── ⚖️ Rights (권리)
            ├─── 보유자: 🏛️ Agent (전북대학교)
            ├─── 접근: 구성원만 가능
            └─── 기간: 2024~2029
        </code></pre>
      </div>

      <div class="linking-explanation">
        <h4>🔍 링크 식별자의 역할</h4>
        <p>
          각 엔티티는 <code>linkingObjectIdentifier</code>, <code>linkingAgentIdentifier</code> 등을
          사용하여 서로 연결됩니다. 이것이 PREMIS의 핵심 강점입니다!
        </p>
        <ul>
          <li>Event는 어떤 Object에 발생했는지 <code>linkingObjectIdentifier</code>로 연결</li>
          <li>Event는 누가 수행했는지 <code>linkingAgentIdentifier</code>로 연결</li>
          <li>Rights는 어떤 Object와 Agent에 관련되는지 링크로 연결</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>6️⃣ 실무에서의 PREMIS 활용</h2>

    <div class="use-case">
      <h3>📚 사례 1: 국립중앙도서관의 웹 아카이빙</h3>
      <div class="case-detail">
        <p><strong>상황:</strong> 대한민국 정부 웹사이트를 수집하여 영구 보존</p>
        <p><strong>PREMIS 활용:</strong></p>
        <ul>
          <li><strong>Object:</strong> 웹페이지 WARC 파일</li>
          <li><strong>Event:</strong> 수집(harvesting), 변환(migration), 품질검사</li>
          <li><strong>Agent:</strong> Heritrix 웹크롤러, 담당 아키비스트</li>
          <li><strong>Rights:</strong> 공공저작물 자유이용허락</li>
        </ul>
        <p><strong>결과:</strong> 10년 전 웹사이트도 완벽하게 재현 가능</p>
      </div>
    </div>

    <div class="use-case">
      <h3>🎓 사례 2: 대학 기관 리포지터리</h3>
      <div class="case-detail">
        <p><strong>상황:</strong> 학위논문 PDF를 장기 보존</p>
        <p><strong>PREMIS 활용:</strong></p>
        <ul>
          <li><strong>Object:</strong> PDF/A 형식의 논문 파일</li>
          <li><strong>Event:</strong> 형식 검증, PDF/A 변환, 정기 체크섬 확인</li>
          <li><strong>Agent:</strong> DSpace 시스템, 도서관 직원</li>
          <li><strong>Rights:</strong> Creative Commons 라이선스 정보</li>
        </ul>
        <p><strong>결과:</strong> 저자가 졸업 후에도 논문의 진본성 보장</p>
      </div>
    </div>

    <div class="use-case">
      <h3>🏛️ 사례 3: 국가기록원의 행정문서 보존</h3>
      <div class="case-detail">
        <p><strong>상황:</strong> 전자정부 시스템의 행정문서 영구보존</p>
        <p><strong>PREMIS 활용:</strong></p>
        <ul>
          <li><strong>Object:</strong> 한글(HWP), PDF, XML 문서</li>
          <li><strong>Event:</strong> 이관(transfer), 포맷 마이그레이션, 암호화</li>
          <li><strong>Agent:</strong> 생산 부처, 기록관리시스템</li>
          <li><strong>Rights:</strong> 공개/비공개 등급, 열람 권한</li>
        </ul>
        <p><strong>결과:</strong> 법적 효력을 가진 증거자료로 활용 가능</p>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>7️⃣ PREMIS 구현 도구 및 시스템</h2>

    <div class="tools-grid">

      <div class="tool-card">
        <h4>🛠️ Archivematica</h4>
        <p class="tool-desc">오픈소스 디지털 보존 시스템</p>
        <ul>
          <li>자동으로 PREMIS 메타데이터 생성</li>
          <li>웹 기반 인터페이스</li>
          <li>전 세계 500개 이상 기관 사용</li>
        </ul>
        <p class="tool-link">🔗 https://www.archivematica.org</p>
      </div>

      <div class="tool-card">
        <h4>🛠️ DSpace</h4>
        <p class="tool-desc">기관 리포지터리 소프트웨어</p>
        <ul>
          <li>PREMIS 메타데이터 통합 지원</li>
          <li>대학도서관에서 널리 사용</li>
          <li>학위논문, 연구자료 보존에 최적화</li>
        </ul>
        <p class="tool-link">🔗 https://dspace.lyrasis.org</p>
      </div>

      <div class="tool-card">
        <h4>🛠️ Rosetta</h4>
        <p class="tool-desc">Ex Libris의 상용 보존 시스템</p>
        <ul>
          <li>엔터프라이즈급 디지털 보존</li>
          <li>완전한 PREMIS 구현</li>
          <li>대형 국가도서관 및 아카이브 사용</li>
        </ul>
        <p class="tool-link">🔗 https://exlibrisgroup.com/products/rosetta</p>
      </div>

      <div class="tool-card">
        <h4>🛠️ JHOVE</h4>
        <p class="tool-desc">파일 형식 검증 도구</p>
        <ul>
          <li>파일 형식 식별 및 검증</li>
          <li>PREMIS Object 메타데이터 생성</li>
          <li>하버드 대학교 개발</li>
        </ul>
        <p class="tool-link">🔗 http://jhove.openpreservation.org</p>
      </div>

    </div>
  </div>

  <div class="section">
    <h2>8️⃣ PREMIS 데이터 사전 핵심 요소</h2>

    <div class="data-dictionary">
      <h3>📖 자주 사용되는 PREMIS 요소</h3>

      <table class="premis-elements-table">
        <thead>
          <tr>
            <th>엔티티</th>
            <th>요소명</th>
            <th>설명</th>
            <th>필수?</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td rowspan="6"><strong>Object</strong></td>
            <td>objectIdentifier</td>
            <td>객체의 고유 식별자 (UUID 등)</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td>objectCategory</td>
            <td>file, bitstream, representation 등</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td>size</td>
            <td>파일 크기 (바이트)</td>
            <td>권장</td>
          </tr>
          <tr>
            <td>format</td>
            <td>파일 형식 정보</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td>fixity</td>
            <td>체크섬 (무결성 검증용)</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td>creatingApplication</td>
            <td>파일 생성 애플리케이션</td>
            <td>권장</td>
          </tr>
          <tr>
            <td rowspan="4"><strong>Event</strong></td>
            <td>eventIdentifier</td>
            <td>이벤트 고유 식별자</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td>eventType</td>
            <td>ingestion, migration, validation 등</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td>eventDateTime</td>
            <td>이벤트 발생 일시</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td>eventOutcome</td>
            <td>이벤트 결과 (success/failure)</td>
            <td>권장</td>
          </tr>
          <tr>
            <td rowspan="3"><strong>Agent</strong></td>
            <td>agentIdentifier</td>
            <td>에이전트 고유 식별자</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td>agentName</td>
            <td>에이전트 이름</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td>agentType</td>
            <td>person, organization, software</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td rowspan="2"><strong>Rights</strong></td>
            <td>rightsStatement</td>
            <td>권리 진술</td>
            <td>✅ 필수</td>
          </tr>
          <tr>
            <td>rightsGranted</td>
            <td>부여된 권리 (접근, 복제 등)</td>
            <td>권장</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <h2>9️⃣ 실습: PREMIS 메타데이터 직접 작성해보기</h2>

    <div class="exercise">
      <h3>✏️ 연습문제</h3>
      <div class="exercise-scenario">
        <p><strong>시나리오:</strong></p>
        <p>
          여러분은 대학 도서관 사서입니다.
          교수님이 작성한 <strong>"디지털도서관론.pptx"</strong> 강의 자료를
          기관 리포지터리에 보존하려고 합니다.
        </p>
        <p><strong>파일 정보:</strong></p>
        <ul>
          <li>파일명: 디지털도서관론.pptx</li>
          <li>형식: Microsoft PowerPoint (PPTX)</li>
          <li>크기: 5,242,880 바이트 (5MB)</li>
          <li>생성일: 2024년 12월 20일</li>
          <li>작성자: 김선태 교수</li>
          <li>라이선스: CC BY-NC (저작자표시-비영리)</li>
        </ul>
      </div>

      <div class="exercise-task">
        <h4>과제: 다음 PREMIS 메타데이터를 작성하세요</h4>
        <ol>
          <li><strong>Object 메타데이터:</strong> 파일 기본 정보 및 체크섬</li>
          <li><strong>Event 메타데이터:</strong> "수집(ingestion)" 이벤트</li>
          <li><strong>Agent 메타데이터:</strong> 김선태 교수</li>
          <li><strong>Rights 메타데이터:</strong> CC BY-NC 라이선스</li>
        </ol>
      </div>

      <div class="exercise-hint">
        <h4>💡 힌트</h4>
        <ul>
          <li>위의 예시들을 참고하여 작성하세요</li>
          <li>UUID는 온라인 생성기를 사용하거나 임의로 만들어도 됩니다</li>
          <li>체크섬은 실제로는 도구로 생성하지만, 연습이므로 임의의 값 사용 가능</li>
          <li>PPTX의 PRONOM ID는 fmt/215입니다</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>🔟 학습 자료 및 참고 문헌</h2>

    <div class="resources">
      <h3>📚 공식 문서</h3>
      <ul>
        <li>
          <strong>PREMIS 공식 웹사이트:</strong>
          <a href="https://www.loc.gov/standards/premis/" target="_blank">
            https://www.loc.gov/standards/premis/
          </a>
        </li>
        <li>
          <strong>PREMIS 데이터 사전 v3.0 (한국어 번역):</strong>
          국립중앙도서관 디지털도서관연구소
        </li>
        <li>
          <strong>PREMIS XML 스키마:</strong>
          <a href="https://www.loc.gov/standards/premis/premis.xsd" target="_blank">
            https://www.loc.gov/standards/premis/premis.xsd
          </a>
        </li>
      </ul>

      <h3>📖 추천 도서</h3>
      <ul>
        <li>
          <strong>"디지털 보존 메타데이터"</strong> - 한국국가기록연구원 (2018)
        </li>
        <li>
          <strong>"Understanding PREMIS"</strong> - Jenn Riley (2017)
        </li>
      </ul>

      <h3>🎓 온라인 강좌</h3>
      <ul>
        <li>
          <strong>Digital Preservation Essentials</strong> - DPC (Digital Preservation Coalition)
        </li>
        <li>
          <strong>PREMIS Tutorial</strong> - Library of Congress
        </li>
      </ul>

      <h3>🛠️ 유용한 도구</h3>
      <ul>
        <li>
          <strong>JHOVE (파일 검증):</strong>
          <a href="https://jhove.openpreservation.org/" target="_blank">
            https://jhove.openpreservation.org/
          </a>
        </li>
        <li>
          <strong>DROID (파일 식별):</strong>
          <a href="https://www.nationalarchives.gov.uk/information-management/manage-information/preserving-digital-records/droid/" target="_blank">
            National Archives UK
          </a>
        </li>
        <li>
          <strong>Siegfried (파일 식별):</strong>
          <a href="https://www.itforarchivists.com/siegfried" target="_blank">
            https://www.itforarchivists.com/siegfried
          </a>
        </li>
      </ul>
    </div>
  </div>

  <div class="summary-section">
    <h2>✨ 핵심 요약</h2>

    <div class="key-points">
      <div class="point">
        <h3>1️⃣ PREMIS는 디지털 보존을 위한 메타데이터 표준</h3>
        <p>장기적으로 디지털 자료를 보존하고 관리하기 위한 국제 표준입니다.</p>
      </div>

      <div class="point">
        <h3>2️⃣ 4가지 핵심 엔티티</h3>
        <ul>
          <li><strong>Object:</strong> 보존 대상 (파일, 비트스트림 등)</li>
          <li><strong>Event:</strong> 객체에 발생한 행위</li>
          <li><strong>Agent:</strong> 행위 수행 주체</li>
          <li><strong>Rights:</strong> 법적 권리 정보</li>
        </ul>
      </div>

      <div class="point">
        <h3>3️⃣ 실무 활용 분야</h3>
        <ul>
          <li>국가 아카이브의 행정문서 보존</li>
          <li>대학 기관 리포지터리의 학위논문 관리</li>
          <li>국립도서관의 웹 아카이빙</li>
          <li>박물관의 디지털 컬렉션 보존</li>
        </ul>
      </div>

      <div class="point">
        <h3>4️⃣ PREMIS의 핵심 가치</h3>
        <ul>
          <li><strong>상호운용성:</strong> 서로 다른 시스템 간 메타데이터 교환</li>
          <li><strong>지속가능성:</strong> 장기적 보존 전략 수립 가능</li>
          <li><strong>진본성:</strong> 디지털 자료의 신뢰성 보장</li>
          <li><strong>책임성:</strong> 모든 행위의 추적 가능</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="conclusion">
    <h2>🎯 마치며</h2>
    <p>
      PREMIS는 처음에는 복잡해 보이지만, 실제로는 매우 <strong>논리적이고 체계적</strong>인 구조를 가지고 있습니다.
      디지털 자료가 점점 늘어나는 현대 사회에서, PREMIS는 우리의 디지털 유산을 미래 세대에게
      온전히 전달하기 위한 <strong>필수적인 도구</strong>입니다.
    </p>
    <p>
      여러분이 도서관, 아카이브, 박물관 등에서 디지털 자료를 다루게 된다면,
      PREMIS는 반드시 알아야 할 핵심 표준입니다.
      이 학습 자료가 PREMIS를 이해하고 실무에 적용하는 데 도움이 되기를 바랍니다!
    </p>
  </div>

</div>

<style>
.premis-tutorial {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.8;
  color: #333;
}

.section {
  margin: 3rem 0;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.intro-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.intro-section h2 {
  color: white;
  margin-top: 0;
}

.explanation-box,
.definition-box,
.history-box {
  background: white;
  padding: 1.5rem;
  margin: 1.5rem 0;
  border-left: 4px solid #667eea;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.problem-box {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
}

.challenge {
  background: #fff3cd;
  padding: 1.5rem;
  margin: 1rem 0;
  border-radius: 8px;
  border-left: 4px solid #ffc107;
}

.challenge h4 {
  color: #856404;
  margin-top: 0;
}

.solution {
  background: #d4edda;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 4px;
  color: #155724;
}

.entity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.entity-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border-top: 4px solid #667eea;
}

.entity-card h4 {
  color: #667eea;
  margin-top: 0;
}

.entity-desc {
  font-style: italic;
  color: #666;
}

.example {
  background: #e7f3ff;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  margin: 0.5rem 0;
  font-size: 0.9em;
}

.entity-types,
.entity-info {
  margin-top: 1rem;
}

.entity-types ul,
.entity-info ul {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.scenario {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.scenario h3 {
  color: white;
  margin-top: 0;
}

.example-section {
  background: white;
  padding: 2rem;
  margin: 2rem 0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.example-section h3 {
  color: #667eea;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.code-explanation {
  background: #fff3e0;
  padding: 1rem;
  border-left: 4px solid #ff9800;
  margin: 1rem 0;
  border-radius: 4px;
}

pre {
  background: #2d2d2d;
  color: #f8f8f2;
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
  margin: 1.5rem 0;
  line-height: 1.6;
}

code {
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 0.9em;
}

.explanation-callout {
  background: #e8f5e9;
  padding: 1.5rem;
  border-left: 4px solid #4caf50;
  margin: 1.5rem 0;
  border-radius: 4px;
}

.explanation-callout h4 {
  color: #2e7d32;
  margin-top: 0;
}

.relationship-diagram {
  background: white;
  padding: 2rem;
  border-radius: 8px;
}

.diagram-explanation pre {
  background: #f5f5f5;
  color: #333;
  border: 2px solid #ddd;
}

.linking-explanation {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1.5rem;
}

.linking-explanation code {
  background: #bbdefb;
  color: #0d47a1;
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
}

.use-case {
  background: white;
  padding: 1.5rem;
  margin: 1.5rem 0;
  border-radius: 8px;
  border-left: 4px solid #9c27b0;
}

.use-case h3 {
  color: #9c27b0;
  margin-top: 0;
}

.case-detail {
  padding-left: 1rem;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.tool-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border-top: 4px solid #00bcd4;
}

.tool-card h4 {
  color: #00bcd4;
  margin-top: 0;
}

.tool-desc {
  font-weight: bold;
  color: #666;
}

.tool-link {
  color: #00bcd4;
  font-size: 0.9em;
  margin-top: 1rem;
}

.premis-elements-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.premis-elements-table th,
.premis-elements-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.premis-elements-table th {
  background: #667eea;
  color: white;
  font-weight: bold;
}

.premis-elements-table tr:hover {
  background: #f5f5f5;
}

.exercise {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  border: 2px solid #ff5722;
}

.exercise-scenario {
  background: #fff3e0;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.exercise-task {
  background: #e1f5fe;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.exercise-hint {
  background: #f3e5f5;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.resources {
  background: white;
  padding: 2rem;
  border-radius: 8px;
}

.resources h3 {
  color: #667eea;
  margin-top: 2rem;
}

.resources h3:first-child {
  margin-top: 0;
}

.resources a {
  color: #667eea;
  text-decoration: none;
  border-bottom: 1px dashed #667eea;
}

.resources a:hover {
  border-bottom: 1px solid #667eea;
}

.summary-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 3rem 0;
}

.summary-section h2 {
  color: white;
}

.key-points {
  display: grid;
  gap: 1.5rem;
  margin-top: 2rem;
}

.point {
  background: rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid white;
}

.point h3 {
  color: white;
  margin-top: 0;
}

.conclusion {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  border-top: 4px solid #667eea;
  margin: 2rem 0;
}

.conclusion h2 {
  color: #667eea;
}

.conclusion p {
  font-size: 1.1em;
  line-height: 2;
}

@media (max-width: 768px) {
  .entity-grid,
  .tools-grid {
    grid-template-columns: 1fr;
  }

  .section {
    padding: 1rem;
  }
}
</style>
"""

# PREMIS 콘텐츠 생성
content = Content.objects.create(
    title="PREMIS: 디지털 보존을 위한 메타데이터 표준",
    slug="premis-digital-preservation-metadata",
    summary="디지털 자료를 장기적으로 보존하기 위한 국제 표준 PREMIS를 실제 예시와 함께 학습합니다. 4가지 핵심 엔티티(Object, Event, Agent, Rights)의 구조와 활용법을 친절하고 상세하게 설명합니다.",
    content_html=content_html,
    category=metadata_category,
    author=admin_user,
    status='PUBLISHED',
    difficulty='INTERMEDIATE',
    estimated_time=30,
    meta_description="PREMIS 디지털 보존 메타데이터 표준을 실제 예시와 함께 배우는 종합 가이드. Object, Event, Agent, Rights 엔티티의 구조와 실무 활용법을 상세히 설명합니다.",
    meta_keywords="PREMIS, 디지털보존, 보존메타데이터, 메타데이터표준, 디지털아카이빙, 기관리포지터리, 장기보존",
    prerequisites="메타데이터 기초 개념, XML 기본 구조에 대한 이해",
    learning_objectives="PREMIS의 목적과 필요성 이해, 4가지 핵심 엔티티의 구조와 역할 파악, 실제 PREMIS 메타데이터 작성 능력 함양, 디지털 보존 실무에서의 활용 방법 습득"
)

# 태그 추가
content.tags.set(tags)

print(f"✅ PREMIS 콘텐츠가 성공적으로 생성되었습니다!")
print(f"   제목: {content.title}")
print(f"   카테고리: {content.category.name}")
print(f"   난이도: {content.get_difficulty_display()}")
print(f"   예상 시간: {content.estimated_time}분")
print(f"   상태: {content.get_status_display()}")
print(f"   태그: {', '.join([tag.name for tag in tags])}")
print(f"   URL: /contents/{content.slug}")
