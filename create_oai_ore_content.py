import os
import django
import sys

# Django 설정
sys.path.append('/Users/kimsuntae/LIS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content, Category
from django.contrib.auth import get_user_model

User = get_user_model()

# 관리자 계정 가져오기
admin_user = User.objects.filter(is_staff=True).first()
if not admin_user:
    print("관리자 계정을 찾을 수 없습니다.")
    sys.exit(1)

# 메타데이터 카테고리 찾기
metadata_category = Category.objects.filter(name="메타데이터").first()
if not metadata_category:
    print("메타데이터 카테고리를 찾을 수 없습니다.")
    sys.exit(1)

# OAI-ORE 콘텐츠 생성
content_html = """
<div class="prose max-w-none">
  <h1>OAI-ORE: 객체 재사용과 교환 프로토콜</h1>

  <div class="bg-blue-50 p-6 rounded-lg mb-8">
    <h2 class="text-2xl font-bold mb-4">🎯 학습 목표</h2>
    <ul class="list-disc pl-6 space-y-2">
      <li>OAI-ORE 프로토콜의 탄생 배경과 목적을 이해합니다</li>
      <li>복합 디지털 객체(Compound Digital Objects)의 개념을 파악합니다</li>
      <li>OAI-PMH와 OAI-ORE의 차이점을 명확히 구분합니다</li>
      <li>실제 ORE 데이터 구조를 직접 확인하고 이해합니다</li>
    </ul>
  </div>

  <h2>📚 OAI-ORE란?</h2>

  <p><strong>OAI-ORE (Open Archives Initiative - Object Reuse and Exchange)</strong>는 디지털 자원들을 하나의 논리적 단위로 묶어서 설명하고 공유하기 위한 표준 프레임워크입니다.</p>

  <div class="bg-gray-100 p-4 rounded-lg my-6">
    <p class="font-semibold">쉽게 말하면...</p>
    <p>책 한 권이 본문, 삽화, 주석, 참고문헌 등 여러 부분으로 구성되어 있듯이, 디지털 세계에서도 하나의 작품이 여러 파일(텍스트, 이미지, 동영상 등)로 이루어져 있습니다. OAI-ORE는 이런 흩어진 파일들을 "이것들은 모두 한 작품의 부분입니다"라고 명시적으로 묶어주는 방법입니다.</p>
  </div>

  <h2>🌟 생성 배경</h2>

  <h3>1. 디지털 자원의 복잡성 증가</h3>
  <p>초기 디지털 아카이브는 주로 단일 파일(논문 PDF, 이미지 파일 등)을 다뤘습니다. 하지만 시간이 지나면서:</p>

  <ul class="list-disc pl-6 space-y-2 my-4">
    <li><strong>멀티미디어 자료 증가</strong>: 하나의 연구 결과물이 논문 + 데이터셋 + 시각화 + 코드로 구성</li>
    <li><strong>웹 자원의 다양화</strong>: 웹페이지 하나가 HTML + CSS + JavaScript + 이미지 등 수십 개 파일로 구성</li>
    <li><strong>디지털 전시물</strong>: 박물관 전시가 텍스트 설명 + 3D 스캔 + 오디오 가이드 + 고해상도 이미지 등으로 구성</li>
  </ul>

  <div class="bg-yellow-50 p-6 rounded-lg my-6">
    <h4 class="font-bold mb-2">💡 실제 사례</h4>
    <p>하버드 대학의 어느 고고학 연구 프로젝트를 생각해봅시다:</p>
    <ul class="list-disc pl-6 mt-2">
      <li>연구 논문 PDF (1개)</li>
      <li>발굴 현장 사진 (200개)</li>
      <li>유물 3D 스캔 데이터 (50개)</li>
      <li>연대 측정 데이터 엑셀 파일 (10개)</li>
      <li>인터뷰 오디오 파일 (20개)</li>
    </ul>
    <p class="mt-2">이 281개의 파일을 어떻게 "하나의 연구 프로젝트"로 관리하고 공유할까요? 이것이 OAI-ORE가 해결하려는 문제입니다.</p>
  </div>

  <h3>2. OAI-PMH의 한계</h3>
  <p>기존의 <strong>OAI-PMH</strong>는 훌륭한 메타데이터 수확(harvesting) 프로토콜이었지만:</p>

  <ul class="list-disc pl-6 space-y-2 my-4">
    <li>하나의 레코드 = 하나의 자원을 가정</li>
    <li>자원 간의 관계를 표현하기 어려움</li>
    <li>복합 객체를 표현하는 표준 방법 부재</li>
  </ul>

  <h2>🎯 OAI-ORE의 목적</h2>

  <ol class="list-decimal pl-6 space-y-3 my-4">
    <li><strong>복합 객체의 구조화된 표현</strong>
      <p class="ml-4 mt-1">여러 자원이 모여 하나의 논리적 객체를 구성함을 명시적으로 표현</p>
    </li>

    <li><strong>자원 간 관계 정의</strong>
      <p class="ml-4 mt-1">"이 이미지는 본문의 3페이지에 해당", "이 데이터는 논문의 실험 결과" 같은 관계 표현</p>
    </li>

    <li><strong>재사용성 향상</strong>
      <p class="ml-4 mt-1">다른 시스템이 복합 객체를 정확히 이해하고 재사용할 수 있도록</p>
    </li>

    <li><strong>상호운용성</strong>
      <p class="ml-4 mt-1">기관 간, 시스템 간 복합 객체를 일관된 방식으로 교환</p>
    </li>
  </ol>

  <h2>🔍 핵심 개념</h2>

  <h3>1. Aggregation (집합)</h3>
  <p>여러 자원을 하나로 묶은 논리적 단위입니다. "이 자원들은 함께 하나의 의미 있는 단위를 구성합니다"라는 선언입니다.</p>

  <div class="bg-gray-50 p-4 rounded-lg my-4">
    <p class="font-semibold mb-2">예시: 학술 논문 Aggregation</p>
    <ul class="list-disc pl-6">
      <li>논문 본문 PDF</li>
      <li>보충 자료 Excel</li>
      <li>데이터셋 CSV</li>
      <li>저자 사진</li>
    </ul>
  </div>

  <h3>2. Aggregated Resource (집합된 자원)</h3>
  <p>Aggregation에 포함된 개별 자원입니다. 각각은 고유한 URI를 가집니다.</p>

  <h3>3. Resource Map (자원 지도)</h3>
  <p>Aggregation의 구조를 기술하는 메타데이터 문서입니다. "지도"처럼 어떤 자원들이 있고, 어떻게 연결되어 있는지 보여줍니다.</p>

  <h2>📊 OAI-PMH vs OAI-ORE</h2>

  <div class="overflow-x-auto my-6">
    <table class="min-w-full border-collapse border border-gray-300">
      <thead class="bg-gray-100">
        <tr>
          <th class="border border-gray-300 px-4 py-2">구분</th>
          <th class="border border-gray-300 px-4 py-2">OAI-PMH</th>
          <th class="border border-gray-300 px-4 py-2">OAI-ORE</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="border border-gray-300 px-4 py-2 font-semibold">주요 목적</td>
          <td class="border border-gray-300 px-4 py-2">메타데이터 수확(harvesting)</td>
          <td class="border border-gray-300 px-4 py-2">복합 객체 표현 및 교환</td>
        </tr>
        <tr class="bg-gray-50">
          <td class="border border-gray-300 px-4 py-2 font-semibold">대상</td>
          <td class="border border-gray-300 px-4 py-2">단일 자원</td>
          <td class="border border-gray-300 px-4 py-2">복합 자원 (여러 개 묶음)</td>
        </tr>
        <tr>
          <td class="border border-gray-300 px-4 py-2 font-semibold">관계 표현</td>
          <td class="border border-gray-300 px-4 py-2">제한적</td>
          <td class="border border-gray-300 px-4 py-2">풍부한 관계 표현 가능</td>
        </tr>
        <tr class="bg-gray-50">
          <td class="border border-gray-300 px-4 py-2 font-semibold">데이터 모델</td>
          <td class="border border-gray-300 px-4 py-2">XML 기반</td>
          <td class="border border-gray-300 px-4 py-2">RDF 기반 (Linked Data)</td>
        </tr>
        <tr>
          <td class="border border-gray-300 px-4 py-2 font-semibold">프로토콜</td>
          <td class="border border-gray-300 px-4 py-2">HTTP + XML</td>
          <td class="border border-gray-300 px-4 py-2">RESTful + RDF</td>
        </tr>
        <tr class="bg-gray-50">
          <td class="border border-gray-300 px-4 py-2 font-semibold">사용 시나리오</td>
          <td class="border border-gray-300 px-4 py-2">도서관 카탈로그 수집</td>
          <td class="border border-gray-300 px-4 py-2">디지털 전시, 연구 데이터 패키지</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="bg-green-50 p-6 rounded-lg my-6">
    <h4 class="font-bold mb-2">🤝 상호 보완적 관계</h4>
    <p>OAI-PMH와 OAI-ORE는 경쟁 관계가 아닙니다!</p>
    <ul class="list-disc pl-6 mt-2">
      <li><strong>OAI-PMH</strong>: "어디에 무엇이 있는지" 알려줌 (메타데이터 공유)</li>
      <li><strong>OAI-ORE</strong>: "무엇이 무엇과 연결되어 있는지" 설명 (구조 공유)</li>
    </ul>
    <p class="mt-2">많은 시스템이 두 프로토콜을 함께 사용합니다.</p>
  </div>

  <h2>💻 실제 OAI-ORE 예제</h2>

  <p>논문 한 편이 본문 PDF와 데이터셋 CSV로 구성된 경우, OAI-ORE Resource Map은 다음과 같이 표현됩니다:</p>

  <div class="code-block my-6">
<pre><code class="language-xml">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:ore="http://www.openarchives.org/ore/terms/"
         xmlns:dcterms="http://purl.org/dc/terms/"&gt;

  &lt;!-- Resource Map 자체 --&gt;
  &lt;rdf:Description rdf:about="http://example.org/rem/1"&gt;
    &lt;rdf:type rdf:resource="http://www.openarchives.org/ore/terms/ResourceMap"/&gt;
    &lt;ore:describes rdf:resource="http://example.org/aggregation/1"/&gt;
    &lt;dcterms:created&gt;2024-01-15T10:30:00Z&lt;/dcterms:created&gt;
  &lt;/rdf:Description&gt;

  &lt;!-- Aggregation: 논문 전체 --&gt;
  &lt;rdf:Description rdf:about="http://example.org/aggregation/1"&gt;
    &lt;rdf:type rdf:resource="http://www.openarchives.org/ore/terms/Aggregation"/&gt;
    &lt;dcterms:title&gt;기후변화가 생물다양성에 미치는 영향 연구&lt;/dcterms:title&gt;
    &lt;dcterms:creator&gt;김연구&lt;/dcterms:creator&gt;

    &lt;!-- 집합된 자원들 --&gt;
    &lt;ore:aggregates rdf:resource="http://example.org/paper.pdf"/&gt;
    &lt;ore:aggregates rdf:resource="http://example.org/dataset.csv"/&gt;
    &lt;ore:aggregates rdf:resource="http://example.org/figures/fig1.png"/&gt;
  &lt;/rdf:Description&gt;

  &lt;!-- Aggregated Resource 1: 논문 본문 --&gt;
  &lt;rdf:Description rdf:about="http://example.org/paper.pdf"&gt;
    &lt;dcterms:format&gt;application/pdf&lt;/dcterms:format&gt;
    &lt;dcterms:title&gt;논문 본문&lt;/dcterms:title&gt;
    &lt;dcterms:extent&gt;2.5 MB&lt;/dcterms:extent&gt;
  &lt;/rdf:Description&gt;

  &lt;!-- Aggregated Resource 2: 데이터셋 --&gt;
  &lt;rdf:Description rdf:about="http://example.org/dataset.csv"&gt;
    &lt;dcterms:format&gt;text/csv&lt;/dcterms:format&gt;
    &lt;dcterms:title&gt;관측 데이터&lt;/dcterms:title&gt;
    &lt;dcterms:description&gt;2020-2023년 종 다양성 측정 데이터&lt;/dcterms:description&gt;
  &lt;/rdf:Description&gt;

  &lt;!-- Aggregated Resource 3: 그림 --&gt;
  &lt;rdf:Description rdf:about="http://example.org/figures/fig1.png"&gt;
    &lt;dcterms:format&gt;image/png&lt;/dcterms:format&gt;
    &lt;dcterms:title&gt;Figure 1: 연도별 종 다양성 변화&lt;/dcterms:title&gt;
  &lt;/rdf:Description&gt;

&lt;/rdf:RDF&gt;
</code></pre>
  </div>

  <div class="bg-blue-50 p-6 rounded-lg my-6">
    <h4 class="font-bold mb-2">📖 코드 해설</h4>
    <ul class="list-disc pl-6 space-y-2">
      <li><strong>&lt;ore:ResourceMap&gt;</strong>: 이 문서가 자원 지도임을 선언</li>
      <li><strong>&lt;ore:Aggregation&gt;</strong>: 논문 전체를 하나의 집합으로 정의</li>
      <li><strong>&lt;ore:aggregates&gt;</strong>: 이 집합에 포함된 자원들을 나열</li>
      <li><strong>각 자원의 메타데이터</strong>: 포맷, 제목, 설명 등 상세 정보</li>
    </ul>
  </div>

  <h2>🌐 실제 활용 사례</h2>

  <h3>1. 유럽 디지털 도서관 (Europeana)</h3>
  <p>수백만 건의 디지털 문화유산을 OAI-ORE로 구조화하여 제공합니다. 한 권의 고서가 표지, 본문 페이지, 주석, 번역본 등으로 구성된 복합 객체로 표현됩니다.</p>

  <h3>2. 연구 데이터 저장소</h3>
  <p>과학 연구 결과를 논문 + 원시 데이터 + 분석 코드 + 시각화 패키지로 묶어 공유합니다.</p>

  <h3>3. 디지털 전시</h3>
  <p>박물관의 온라인 전시를 전시 설명 + 유물 이미지 + 3D 모델 + 오디오 가이드의 복합체로 구성합니다.</p>

  <h2>🎓 실습: OAI-ORE 구조 이해하기</h2>

  <div class="bg-yellow-50 p-6 rounded-lg my-6">
    <h4 class="font-bold mb-4">✏️ 연습 문제</h4>
    <p class="mb-2">다음 시나리오를 OAI-ORE로 표현한다면 어떤 자원들이 포함될까요?</p>

    <div class="bg-white p-4 rounded my-3">
      <p class="font-semibold mb-2">시나리오: 대학 강의 녹화 콘텐츠</p>
      <ul class="list-disc pl-6">
        <li>강의 동영상 (MP4, 1.2GB)</li>
        <li>강의 슬라이드 (PDF, 5MB)</li>
        <li>강의 노트 (DOCX, 500KB)</li>
        <li>참고문헌 목록 (PDF, 200KB)</li>
        <li>퀴즈 파일 (HTML, 50KB)</li>
      </ul>
    </div>

    <p class="mt-4"><strong>해답:</strong></p>
    <ul class="list-disc pl-6 mt-2">
      <li><strong>Aggregation</strong>: "데이터베이스개론 3주차 강의"</li>
      <li><strong>Aggregated Resources</strong>: 위의 5개 파일 각각</li>
      <li><strong>Resource Map</strong>: 이들의 관계를 설명하는 RDF 문서</li>
    </ul>
    <p class="mt-2">각 자원에는 고유 URI가 부여되고, 역할(강의 본체, 보충 자료 등)이 명시됩니다.</p>
  </div>

  <h2>🔮 미래 전망</h2>

  <p>OAI-ORE는 다음 영역에서 더욱 중요해지고 있습니다:</p>

  <ul class="list-disc pl-6 space-y-2 my-4">
    <li><strong>연구 데이터 관리</strong>: FAIR 원칙(Findable, Accessible, Interoperable, Reusable)을 준수하는 데이터 공유</li>
    <li><strong>디지털 인문학</strong>: 복잡한 문화유산 자원의 구조화된 표현</li>
    <li><strong>교육 자원</strong>: 멀티미디어 학습 객체의 패키징</li>
    <li><strong>Linked Data</strong>: 시맨틱 웹의 핵심 구성 요소</li>
  </ul>

  <h2>📝 핵심 요약</h2>

  <div class="bg-purple-50 p-6 rounded-lg my-6">
    <ol class="list-decimal pl-6 space-y-2">
      <li><strong>OAI-ORE는 복합 디지털 객체를 표현하고 교환하기 위한 표준</strong>입니다.</li>
      <li><strong>디지털 자원의 복잡성 증가</strong>와 <strong>OAI-PMH의 한계</strong>가 탄생 배경입니다.</li>
      <li><strong>Aggregation, Aggregated Resource, Resource Map</strong>이 핵심 개념입니다.</li>
      <li><strong>OAI-PMH는 메타데이터 수확, OAI-ORE는 구조 표현</strong>이 주 목적입니다.</li>
      <li><strong>RDF 기반</strong>으로 풍부한 관계 표현이 가능합니다.</li>
      <li>연구 데이터, 디지털 전시, 교육 콘텐츠 등 <strong>다양한 분야에서 활용</strong>됩니다.</li>
    </ol>
  </div>

  <h2>🔗 참고 자료</h2>

  <ul class="list-disc pl-6 space-y-2">
    <li><a href="https://www.openarchives.org/ore/" target="_blank" class="text-blue-600 hover:underline">OAI-ORE 공식 사이트</a></li>
    <li><a href="https://www.openarchives.org/ore/1.0/primer" target="_blank" class="text-blue-600 hover:underline">OAI-ORE Primer</a></li>
    <li><a href="https://www.openarchives.org/ore/1.0/datamodel" target="_blank" class="text-blue-600 hover:underline">OAI-ORE Data Model</a></li>
  </ul>

  <div class="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg mt-8">
    <p class="text-lg font-semibold">🎉 학습을 완료하셨습니다!</p>
    <p class="mt-2">OAI-ORE를 통해 복잡한 디지털 자원을 체계적으로 관리하고 공유하는 방법을 배웠습니다. 실제 프로젝트에서 여러 파일을 하나의 논리적 단위로 묶어야 할 때 OAI-ORE를 떠올려보세요!</p>
  </div>
</div>
"""

# 콘텐츠 생성
from datetime import datetime

content = Content.objects.create(
    category=metadata_category,
    title="OAI-ORE: 복합 디지털 객체의 구조화된 표현",
    slug="oai-ore-protocol",
    summary="OAI-ORE(Object Reuse and Exchange) 프로토콜의 개념, 탄생 배경, 핵심 구성 요소, 그리고 OAI-PMH와의 차이점을 실제 예제를 통해 학습합니다. 복합 디지털 객체를 어떻게 표현하고 공유하는지 이해할 수 있습니다.",
    content_html=content_html,
    author=admin_user,
    status="PUBLISHED",
    difficulty="INTERMEDIATE",
    estimated_time=30,
    view_count=0,
    published_at=datetime.now()
)

print(f"✅ OAI-ORE 콘텐츠가 생성되었습니다!")
print(f"   - ID: {content.id}")
print(f"   - 제목: {content.title}")
print(f"   - 카테고리: {content.category.name}")
print(f"   - 난이도: {content.difficulty}")
print(f"   - 예상 시간: {content.estimated_time}분")
print(f"   - 상태: {content.status}")
print(f"   - Slug: {content.slug}")
print(f"   - URL: http://localhost:8000/api/contents/by-slug/{content.slug}/")
