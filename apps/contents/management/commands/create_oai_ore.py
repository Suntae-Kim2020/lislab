from django.core.management.base import BaseCommand
from apps.contents.models import Content, Category, Tag
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create OAI-ORE educational content'

    def handle(self, *args, **options):
        # 관리자 계정 가져오기
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR("관리자 계정을 찾을 수 없습니다."))
            return

        # 데이터 모델 카테고리 찾기
        data_model_category = Category.objects.filter(name="데이터 모델").first()
        if not data_model_category:
            self.stdout.write(self.style.ERROR("데이터 모델 카테고리를 찾을 수 없습니다."))
            return

        # 태그 생성 또는 가져오기
        tag_names = ['OAI-ORE', 'RDF', 'Vocabulary', 'Aggregation', 'ResourceMap', '복합객체', '디지털자원']
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': tag_name.lower().replace('-', '_')}
            )
            tags.append(tag)
            if created:
                self.stdout.write(self.style.SUCCESS(f"태그 '{tag_name}' 생성됨"))

        # OAI-ORE 콘텐츠 HTML
        content_html = """
<div class="prose max-w-none">
  <h1>OAI-ORE: 복합 디지털 객체를 위한 RDF 데이터 모델</h1>

  <div class="bg-blue-50 p-6 rounded-lg mb-8">
    <h2 class="text-2xl font-bold mb-4">🎯 학습 목표</h2>
    <ul class="list-disc pl-6 space-y-2">
      <li>OAI-ORE가 무엇인지, 정확한 분류가 무엇인지 이해합니다</li>
      <li>복합 디지털 객체(Compound Digital Objects)의 개념을 파악합니다</li>
      <li>OAI-ORE의 핵심 구성 요소(Aggregation, ResourceMap)를 학습합니다</li>
      <li>실제 데이터 구조를 직접 확인하고 이해합니다</li>
    </ul>
  </div>

  <h2>❓ OAI-ORE는 무엇인가요?</h2>

  <div class="bg-yellow-50 p-6 rounded-lg my-6">
    <h3 class="font-bold text-lg mb-3">🔍 정확한 분류</h3>
    <p class="mb-3"><strong>OAI-ORE</strong>는 다음과 같이 정의됩니다:</p>
    <div class="bg-white p-4 rounded-lg">
      <p class="font-semibold text-blue-800">
        "복합 디지털 객체의 집합과 관계를 표현하기 위해 정의된 <strong>RDF 기반의 경량 데이터 모델(Vocabulary)</strong>"
      </p>
    </div>
    <div class="mt-4 text-sm">
      <p><strong>OAI-ORE는:</strong></p>
      <ul class="list-disc pl-6 mt-2">
        <li>✅ RDF Vocabulary</li>
        <li>✅ 데이터 모델 명세</li>
        <li>✅ 경량 온톨로지적 성격</li>
        <li>❌ 프로토콜이 아님</li>
        <li>❌ 메타데이터 스키마가 아님</li>
        <li>❌ 완전한 도메인 온톨로지가 아님</li>
      </ul>
    </div>
  </div>

  <p><strong>OAI-ORE (Open Archives Initiative - Object Reuse and Exchange)</strong>는 디지털 자원들을 하나의 논리적 단위로 묶어서 설명하고 공유하기 위한 RDF 기반 데이터 모델입니다.</p>

  <div class="bg-gray-100 p-4 rounded-lg my-6">
    <p class="font-semibold">🎓 학생 눈높이로 설명하면...</p>
    <p>여러분이 과제를 제출할 때 워드 파일 1개만 내지 않죠? 보고서 본문 + 참고자료 PDF + 데이터 엑셀 + 발표 PPT를 함께 제출합니다. 이 여러 파일들을 "이것들은 모두 한 과제의 부분입니다"라고 명시적으로 연결해주는 것, 그것이 OAI-ORE의 역할입니다.</p>
  </div>

  <h2>🌟 왜 OAI-ORE가 필요한가요?</h2>

  <h3>1. 디지털 세상의 현실</h3>
  <p>예전에는 하나의 자료 = 하나의 파일이었습니다. 하지만 지금은:</p>

  <ul class="list-disc pl-6 space-y-2 my-4">
    <li><strong>연구 논문</strong>: 논문 PDF + 실험 데이터 + 분석 코드 + 그래프 이미지</li>
    <li><strong>온라인 전시</strong>: 작품 설명 + 고해상도 이미지 + 3D 모델 + 오디오 가이드</li>
    <li><strong>학습 자료</strong>: 강의 영상 + 슬라이드 + 읽기 자료 + 퀴즈</li>
  </ul>

  <p>이렇게 여러 파일이 하나의 "작품"을 이루는 경우가 많아졌습니다.</p>

  <h3>2. 문제: 어떻게 묶을까?</h3>

  <div class="bg-red-50 p-4 rounded-lg my-4">
    <p class="font-semibold mb-2">⚠️ 단순히 폴더에 넣으면?</p>
    <ul class="list-disc pl-6">
      <li>각 파일 간의 관계를 알 수 없음</li>
      <li>다른 시스템과 공유하기 어려움</li>
      <li>"이 이미지는 3페이지에 들어가는 그림" 같은 구조 정보 손실</li>
    </ul>
  </div>

  <h3>3. 해결책: OAI-ORE</h3>

  <p>OAI-ORE는 <strong>표준화된 방법</strong>으로 여러 파일의 관계를 기술합니다. 마치 "설명서"처럼요!</p>

  <h2>🔍 OAI-ORE의 핵심 개념 3가지</h2>

  <h3>1️⃣ Aggregation (집합)</h3>

  <div class="bg-blue-50 p-4 rounded-lg my-4">
    <p><strong>정의:</strong> 여러 자원을 하나로 묶은 논리적 단위</p>
    <p class="mt-2"><strong>비유:</strong> "2024학년도 1학기 데이터베이스 기말과제"라는 이름의 폴더</p>
    <p class="mt-2"><strong>특징:</strong> 실제 파일이 아니라 "개념적 묶음"</p>
  </div>

  <div class="bg-gray-50 p-4 rounded-lg my-4">
    <p class="font-semibold mb-2">📦 예시: 졸업논문 Aggregation</p>
    <ul class="list-disc pl-6">
      <li>논문 본문 (PDF)</li>
      <li>설문조사 원본 데이터 (Excel)</li>
      <li>통계 분석 결과 (CSV)</li>
      <li>그래프 이미지 (PNG 10개)</li>
    </ul>
    <p class="mt-2 text-sm text-gray-600">→ 이 모든 것이 "김철수 졸업논문"이라는 하나의 Aggregation</p>
  </div>

  <h3>2️⃣ Aggregated Resource (집합된 자원)</h3>

  <div class="bg-green-50 p-4 rounded-lg my-4">
    <p><strong>정의:</strong> Aggregation에 포함된 개별 자원</p>
    <p class="mt-2"><strong>비유:</strong> 폴더 안의 각 파일</p>
    <p class="mt-2"><strong>특징:</strong> 각각 고유한 주소(URI)를 가짐</p>
  </div>

  <h3>3️⃣ Resource Map (자원 지도)</h3>

  <div class="bg-purple-50 p-4 rounded-lg my-4">
    <p><strong>정의:</strong> Aggregation의 구조를 설명하는 메타데이터 문서</p>
    <p class="mt-2"><strong>비유:</strong> 폴더 안의 "README.txt" 파일</p>
    <p class="mt-2"><strong>내용:</strong> "어떤 파일들이 있고, 서로 어떤 관계인지" 설명</p>
    <p class="mt-2"><strong>형식:</strong> RDF (기계가 읽을 수 있는 형식)</p>
  </div>

  <h2>🏗️ OAI-ORE의 구조 (한눈에 보기)</h2>

  <div class="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg my-6">
<pre class="text-sm">
📋 Resource Map (자원 지도)
   ↓ describes (설명함)
📦 Aggregation (집합체)
   ├─ aggregates (포함함) → 📄 Resource 1 (논문.pdf)
   ├─ aggregates (포함함) → 📊 Resource 2 (데이터.xlsx)
   └─ aggregates (포함함) → 📈 Resource 3 (그래프.png)
</pre>
  </div>

  <h2>💻 실제 OAI-ORE 예제</h2>

  <p>대학생이 제출한 "기후변화 연구 과제"를 OAI-ORE로 표현하면:</p>

  <div class="code-block my-6">
<pre><code class="language-xml">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:ore="http://www.openarchives.org/ore/terms/"
         xmlns:dcterms="http://purl.org/dc/terms/"&gt;

  &lt;!-- 1. Resource Map: 이 문서는 "설명서"입니다 --&gt;
  &lt;rdf:Description rdf:about="http://university.edu/assignments/map-12345"&gt;
    &lt;rdf:type rdf:resource="http://www.openarchives.org/ore/terms/ResourceMap"/&gt;
    &lt;ore:describes rdf:resource="http://university.edu/assignments/12345"/&gt;
    &lt;dcterms:created&gt;2024-06-15T14:30:00Z&lt;/dcterms:created&gt;
    &lt;dcterms:creator&gt;시스템 자동 생성&lt;/dcterms:creator&gt;
  &lt;/rdf:Description&gt;

  &lt;!-- 2. Aggregation: "기후변화 연구 과제" 전체 --&gt;
  &lt;rdf:Description rdf:about="http://university.edu/assignments/12345"&gt;
    &lt;rdf:type rdf:resource="http://www.openarchives.org/ore/terms/Aggregation"/&gt;
    &lt;dcterms:title&gt;기후변화가 생물다양성에 미치는 영향 연구&lt;/dcterms:title&gt;
    &lt;dcterms:creator&gt;김학생&lt;/dcterms:creator&gt;
    &lt;dcterms:created&gt;2024-06-15&lt;/dcterms:created&gt;

    &lt;!-- 이 과제에 포함된 파일들 --&gt;
    &lt;ore:aggregates rdf:resource="http://university.edu/files/report.pdf"/&gt;
    &lt;ore:aggregates rdf:resource="http://university.edu/files/data.csv"/&gt;
    &lt;ore:aggregates rdf:resource="http://university.edu/files/presentation.pptx"/&gt;
  &lt;/rdf:Description&gt;

  &lt;!-- 3. Aggregated Resource들: 각 파일의 상세 정보 --&gt;

  &lt;!-- 파일 1: 보고서 본문 --&gt;
  &lt;rdf:Description rdf:about="http://university.edu/files/report.pdf"&gt;
    &lt;dcterms:format&gt;application/pdf&lt;/dcterms:format&gt;
    &lt;dcterms:title&gt;연구 보고서 본문&lt;/dcterms:title&gt;
    &lt;dcterms:extent&gt;1.8 MB&lt;/dcterms:extent&gt;
    &lt;dcterms:description&gt;15페이지 분량의 연구 결과 보고서&lt;/dcterms:description&gt;
  &lt;/rdf:Description&gt;

  &lt;!-- 파일 2: 실험 데이터 --&gt;
  &lt;rdf:Description rdf:about="http://university.edu/files/data.csv"&gt;
    &lt;dcterms:format&gt;text/csv&lt;/dcterms:format&gt;
    &lt;dcterms:title&gt;관측 데이터&lt;/dcterms:title&gt;
    &lt;dcterms:description&gt;2020-2024년 지역별 종 다양성 측정 데이터 500건&lt;/dcterms:description&gt;
  &lt;/rdf:Description&gt;

  &lt;!-- 파일 3: 발표 자료 --&gt;
  &lt;rdf:Description rdf:about="http://university.edu/files/presentation.pptx"&gt;
    &lt;dcterms:format&gt;application/vnd.openxmlformats-officedocument.presentationml.presentation&lt;/dcterms:format&gt;
    &lt;dcterms:title&gt;연구 결과 발표 슬라이드&lt;/dcterms:title&gt;
    &lt;dcterms:description&gt;20슬라이드 분량의 발표 자료&lt;/dcterms:description&gt;
  &lt;/rdf:Description&gt;

&lt;/rdf:RDF&gt;
</code></pre>
  </div>

  <div class="bg-blue-50 p-6 rounded-lg my-6">
    <h4 class="font-bold mb-2">📖 코드 해설</h4>
    <ul class="list-disc pl-6 space-y-2">
      <li><strong>Resource Map</strong>: 이 XML 문서 자체. "설명서" 역할</li>
      <li><strong>Aggregation</strong>: "기후변화 연구 과제"라는 논리적 묶음</li>
      <li><strong>ore:aggregates</strong>: 이 과제에 포함된 3개 파일을 나열</li>
      <li><strong>각 파일의 메타데이터</strong>: 파일 형식, 제목, 크기, 설명</li>
    </ul>
    <p class="mt-4 text-sm"><strong>핵심:</strong> 이 XML 파일만 보면 "어떤 파일들이 하나의 과제를 구성하는지" 정확히 알 수 있습니다!</p>
  </div>

  <h2>📊 분류표: OAI-ORE는 무엇인가?</h2>

  <div class="overflow-x-auto my-6">
    <table class="min-w-full border-collapse border border-gray-300">
      <thead class="bg-gray-100">
        <tr>
          <th class="border border-gray-300 px-4 py-2">구분</th>
          <th class="border border-gray-300 px-4 py-2">해당 여부</th>
          <th class="border border-gray-300 px-4 py-2">설명</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="border border-gray-300 px-4 py-2 font-semibold">메타데이터 요소 집합</td>
          <td class="border border-gray-300 px-4 py-2 text-center">✖</td>
          <td class="border border-gray-300 px-4 py-2">Dublin Core 같은 것이 아님</td>
        </tr>
        <tr class="bg-gray-50">
          <td class="border border-gray-300 px-4 py-2 font-semibold">프로토콜</td>
          <td class="border border-gray-300 px-4 py-2 text-center">✖</td>
          <td class="border border-gray-300 px-4 py-2">통신 규약이 아님 (OAI-PMH가 프로토콜)</td>
        </tr>
        <tr>
          <td class="border border-gray-300 px-4 py-2 font-semibold">데이터 모델</td>
          <td class="border border-gray-300 px-4 py-2 text-center text-green-600">✔</td>
          <td class="border border-gray-300 px-4 py-2">자원 간 관계를 표현하는 구조</td>
        </tr>
        <tr class="bg-gray-50">
          <td class="border border-gray-300 px-4 py-2 font-semibold">RDF Vocabulary</td>
          <td class="border border-gray-300 px-4 py-2 text-center text-green-600">✔</td>
          <td class="border border-gray-300 px-4 py-2">RDF로 표현된 용어 집합</td>
        </tr>
        <tr>
          <td class="border border-gray-300 px-4 py-2 font-semibold">경량 온톨로지적 성격</td>
          <td class="border border-gray-300 px-4 py-2 text-center text-green-600">✔</td>
          <td class="border border-gray-300 px-4 py-2">클래스·관계 정의, 추론은 제한적</td>
        </tr>
        <tr class="bg-gray-50">
          <td class="border border-gray-300 px-4 py-2 font-semibold">완전한 도메인 온톨로지</td>
          <td class="border border-gray-300 px-4 py-2 text-center">✖</td>
          <td class="border border-gray-300 px-4 py-2">FOAF, SKOS 같은 포괄적 온톨로지는 아님</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2>🆚 비교: 비슷해 보이는 것들과 어떻게 다른가요?</h2>

  <h3>1. OAI-PMH vs OAI-ORE</h3>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
    <div class="bg-blue-50 p-4 rounded-lg">
      <h4 class="font-bold mb-2">📡 OAI-PMH</h4>
      <ul class="list-disc pl-6 text-sm">
        <li><strong>종류:</strong> 프로토콜 (통신 규약)</li>
        <li><strong>목적:</strong> 메타데이터 수집</li>
        <li><strong>대상:</strong> 단일 자원</li>
        <li><strong>비유:</strong> "도서관 카탈로그 복사하기"</li>
      </ul>
    </div>

    <div class="bg-purple-50 p-4 rounded-lg">
      <h4 class="font-bold mb-2">📦 OAI-ORE</h4>
      <ul class="list-disc pl-6 text-sm">
        <li><strong>종류:</strong> 데이터 모델</li>
        <li><strong>목적:</strong> 복합 객체 구조 표현</li>
        <li><strong>대상:</strong> 여러 자원의 묶음</li>
        <li><strong>비유:</strong> "세트 상품 포장 설명서"</li>
      </ul>
    </div>
  </div>

  <h3>2. Dublin Core vs OAI-ORE</h3>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
    <div class="bg-green-50 p-4 rounded-lg">
      <h4 class="font-bold mb-2">🏷️ Dublin Core</h4>
      <ul class="list-disc pl-6 text-sm">
        <li><strong>종류:</strong> 메타데이터 요소 집합</li>
        <li><strong>내용:</strong> title, creator, date 등 15개 요소</li>
        <li><strong>목적:</strong> 자원의 속성 기술</li>
        <li><strong>비유:</strong> "책 날개의 기본 정보"</li>
      </ul>
    </div>

    <div class="bg-purple-50 p-4 rounded-lg">
      <h4 class="font-bold mb-2">📦 OAI-ORE</h4>
      <ul class="list-disc pl-6 text-sm">
        <li><strong>종류:</strong> RDF Vocabulary / 데이터 모델</li>
        <li><strong>내용:</strong> Aggregation, ResourceMap 등 관계 표현</li>
        <li><strong>목적:</strong> 자원 간 구조 기술</li>
        <li><strong>비유:</strong> "시리즈 전집의 구성 안내"</li>
      </ul>
    </div>
  </div>

  <h2>🌐 실제 활용 사례</h2>

  <h3>1. Europeana (유럽 디지털 도서관)</h3>
  <p>고서 한 권을 다음과 같이 표현:</p>
  <ul class="list-disc pl-6">
    <li>표지 이미지</li>
    <li>각 페이지 스캔 (200장)</li>
    <li>OCR 텍스트</li>
    <li>라틴어 → 영어 번역본</li>
    <li>해설 오디오</li>
  </ul>
  <p class="mt-2">→ 하나의 Aggregation으로 묶어서 제공</p>

  <h3>2. 대학 연구 데이터 저장소</h3>
  <p>박사논문 1편을:</p>
  <ul class="list-disc pl-6">
    <li>논문 PDF</li>
    <li>실험 원시 데이터 (10GB)</li>
    <li>분석 Python 코드</li>
    <li>시각화 Jupyter Notebook</li>
    <li>보충 자료 동영상</li>
  </ul>
  <p class="mt-2">→ 패키지로 묶어 장기 보존</p>

  <h3>3. 온라인 박물관 전시</h3>
  <p>"조선시대 도자기" 전시를:</p>
  <ul class="list-disc pl-6">
    <li>전시 소개 HTML</li>
    <li>유물 고해상도 사진 (각 유물당 20장)</li>
    <li>3D 회전 모델</li>
    <li>큐레이터 해설 MP3</li>
    <li>연표 인포그래픽</li>
  </ul>
  <p class="mt-2">→ 하나의 가상 전시로 통합</p>

  <h2>🎓 학습 확인 문제</h2>

  <div class="bg-yellow-50 p-6 rounded-lg my-6">
    <h4 class="font-bold mb-4">✏️ 다음 중 OAI-ORE에 대한 설명으로 <strong>틀린</strong> 것은?</h4>

    <ol class="list-decimal pl-6 space-y-2">
      <li>OAI-ORE는 메타데이터 수집을 위한 프로토콜이다. <strong>(❌)</strong></li>
      <li>OAI-ORE는 RDF 기반의 데이터 모델이다. <strong>(✅)</strong></li>
      <li>Aggregation은 여러 자원을 하나로 묶은 논리적 단위이다. <strong>(✅)</strong></li>
      <li>Resource Map은 Aggregation의 구조를 설명하는 문서이다. <strong>(✅)</strong></li>
    </ol>

    <p class="mt-4 p-3 bg-white rounded"><strong>정답: 1번</strong> - OAI-ORE는 프로토콜이 아니라 데이터 모델입니다. 메타데이터 수집 프로토콜은 OAI-PMH입니다.</p>
  </div>

  <div class="bg-yellow-50 p-6 rounded-lg my-6">
    <h4 class="font-bold mb-4">✏️ 실습 문제</h4>
    <p class="mb-2">여러분이 "한국 전통음악 아카이브" 웹사이트를 만든다면, 다음 자료를 OAI-ORE로 어떻게 구성할까요?</p>

    <div class="bg-white p-4 rounded my-3">
      <p class="font-semibold mb-2">자료: 판소리 "춘향가" 공연 기록</p>
      <ul class="list-disc pl-6">
        <li>공연 실황 동영상 (MP4, 2시간)</li>
        <li>소리 음원만 추출 (MP3, 120분)</li>
        <li>사설(가사) 전문 (PDF)</li>
        <li>공연 프로그램북 스캔 (PDF, 30페이지)</li>
        <li>명창 인터뷰 (MP3, 30분)</li>
        <li>무대 사진 (JPG, 50장)</li>
      </ul>
    </div>

    <p class="mt-4"><strong>해답:</strong></p>
    <ul class="list-disc pl-6 mt-2">
      <li><strong>Aggregation</strong>: "2024년 국립국악원 춘향가 공연"</li>
      <li><strong>Aggregated Resources</strong>: 위의 6종류 파일들</li>
      <li><strong>Resource Map</strong>: 이들의 관계를 설명하는 RDF XML 문서</li>
      <li><strong>관계 기술 예</strong>: "사설PDF는 동영상의 텍스트 버전", "사진들은 공연 중 촬영" 등</li>
    </ul>
  </div>

  <h2>📝 핵심 요약</h2>

  <div class="bg-purple-50 p-6 rounded-lg my-6">
    <ol class="list-decimal pl-6 space-y-3">
      <li><strong>OAI-ORE는 "RDF Vocabulary / 데이터 모델"</strong>이다. 프로토콜이나 메타데이터 스키마가 아니다.</li>
      <li><strong>목적:</strong> 복합 디지털 객체의 구조를 표준화된 방법으로 표현</li>
      <li><strong>핵심 3요소:</strong>
        <ul class="list-disc pl-6 mt-1">
          <li>Aggregation (여러 자원의 논리적 묶음)</li>
          <li>Aggregated Resource (묶음에 포함된 개별 자원)</li>
          <li>Resource Map (구조를 설명하는 RDF 문서)</li>
        </ul>
      </li>
      <li><strong>RDF 기반</strong>이므로 기계가 읽고 처리할 수 있음</li>
      <li><strong>온톨로지와의 관계:</strong> 경량 온톨로지적 성격은 있으나, 완전한 도메인 온톨로지는 아님</li>
      <li><strong>활용:</strong> 디지털 도서관, 연구 데이터 저장소, 온라인 전시 등</li>
    </ol>
  </div>

  <h2>🔑 시험에 나올 핵심 개념</h2>

  <div class="bg-gradient-to-r from-yellow-50 to-orange-50 p-6 rounded-lg my-6">
    <ul class="list-disc pl-6 space-y-2">
      <li><strong>OAI-ORE =</strong> RDF Vocabulary / 데이터 모델 명세</li>
      <li><strong>Aggregation =</strong> 논리적 묶음 (실제 파일 아님)</li>
      <li><strong>Resource Map =</strong> 구조 설명 문서 (RDF 형식)</li>
      <li><strong>OAI-PMH ≠ OAI-ORE</strong> (프로토콜 vs 데이터 모델)</li>
      <li><strong>Dublin Core ≠ OAI-ORE</strong> (메타데이터 요소 vs 구조 표현)</li>
    </ul>
  </div>

  <h2>🔗 더 공부하고 싶다면</h2>

  <ul class="list-disc pl-6 space-y-2">
    <li><a href="https://www.openarchives.org/ore/" target="_blank" class="text-blue-600 hover:underline">OAI-ORE 공식 사이트</a></li>
    <li><a href="https://www.openarchives.org/ore/1.0/primer" target="_blank" class="text-blue-600 hover:underline">OAI-ORE Primer (입문서)</a></li>
    <li><a href="https://www.openarchives.org/ore/1.0/vocabulary" target="_blank" class="text-blue-600 hover:underline">OAI-ORE Vocabulary 명세</a></li>
  </ul>

  <div class="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg mt-8">
    <p class="text-lg font-semibold">🎉 학습을 완료하셨습니다!</p>
    <p class="mt-2">OAI-ORE가 무엇인지, 어떻게 분류되는지, 그리고 복합 디지털 객체를 어떻게 표현하는지 배웠습니다. 시험에서 "OAI-ORE는 프로토콜이다" 같은 함정 문제가 나와도 이제 자신있게 대답할 수 있겠죠? 😊</p>
  </div>
</div>
"""


        # 콘텐츠 생성 또는 업데이트
        content, created = Content.objects.update_or_create(
            slug='oai-ore-introduction',
            defaults={
                'title': 'OAI-ORE: 복합 디지털 객체를 위한 RDF 데이터 모델',
                'summary': 'OAI-ORE는 프로토콜이 아닌 RDF 기반의 데이터 모델입니다. 여러 웹 리소스를 하나의 논리적 단위로 묶어 표현하는 Aggregation과 ResourceMap 개념을 학습합니다.',
                'content_html': content_html,
                'category': data_model_category,
                'author': admin_user,
                'status': Content.Status.PUBLISHED,
                'difficulty': 'INTERMEDIATE',
                'estimated_time': 30,
                'prerequisites': 'RDF와 메타데이터에 대한 기초 지식이 있으면 좋습니다.',
                'learning_objectives': 'OAI-ORE의 정확한 분류 이해, Aggregation과 ResourceMap 개념 파악, 실제 RDF 예제 분석',
                'version': '1.0'
            }
        )

        # 태그 추가
        content.tags.set(tags)

        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ OAI-ORE 콘텐츠가 생성되었습니다. (ID: {content.id})"))
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ OAI-ORE 콘텐츠가 업데이트되었습니다. (ID: {content.id})"))

        self.stdout.write(self.style.SUCCESS(f"제목: {content.title}"))
        self.stdout.write(self.style.SUCCESS(f"카테고리: {content.category.name}"))
        self.stdout.write(self.style.SUCCESS(f"태그: {', '.join([tag.name for tag in tags])}"))
        self.stdout.write(self.style.SUCCESS(f"난이도: {content.get_difficulty_display()}"))
        self.stdout.write(self.style.SUCCESS(f"예상 소요 시간: {content.estimated_time}분"))

        # 이메일 알림 발송
        self.stdout.write(self.style.WARNING("📧 이메일 알림 발송 중..."))
        from apps.accounts.email_utils import send_immediate_content_notification

        users = User.objects.filter(
            is_active=True,
            mailing_preference__enabled=True,
            mailing_preference__frequency='IMMEDIATE'
        ).select_related('mailing_preference')

        email_count = 0
        for user in users:
            try:
                pref = user.mailing_preference

                # 전체 카테고리 구독 또는 해당 카테고리 구독 확인
                if pref.all_categories:
                    should_send = True
                else:
                    selected_category_ids = list(pref.selected_categories.values_list('id', flat=True))
                    should_send = content.category_id in selected_category_ids

                if should_send:
                    send_immediate_content_notification(user, content)
                    email_count += 1
                    self.stdout.write(self.style.SUCCESS(f"  ✓ {user.username} ({user.email})"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ {user.username}: {str(e)}"))
                continue

        if email_count > 0:
            self.stdout.write(self.style.SUCCESS(f"📧 총 {email_count}명에게 이메일 발송 완료"))
        else:
            self.stdout.write(self.style.WARNING("📧 이메일을 받을 사용자가 없습니다"))
