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

  <section class="mb-8">
    <h2 class="text-3xl font-bold mb-4">1. OAI-ORE란 무엇인가?</h2>

    <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
      <p class="font-semibold">⚠️ 중요한 분류 이해</p>
      <p class="mt-2">OAI-ORE는 <strong>프로토콜이 아닙니다</strong>. 이것은 RDF 기반의 <strong>데이터 모델</strong>이자 <strong>어휘(Vocabulary)</strong>입니다.</p>
    </div>

    <h3 class="text-2xl font-semibold mb-3">OAI-ORE의 정확한 분류</h3>
    <ul class="list-disc pl-6 space-y-2 mb-6">
      <li><strong>RDF Vocabulary (어휘)</strong>: 복합 디지털 객체를 표현하기 위한 용어와 개념을 정의</li>
      <li><strong>Data Model (데이터 모델)</strong>: 여러 웹 리소스를 하나의 집합으로 표현하는 구조적 프레임워크</li>
      <li><strong>NOT a Protocol (프로토콜이 아님)</strong>: OAI-PMH와 달리 통신 규약이 아닙니다</li>
      <li><strong>NOT an Ontology (온톨로지가 아님)</strong>: 개념 간의 복잡한 관계보다는 구조적 표현에 집중</li>
    </ul>

    <h3 class="text-2xl font-semibold mb-3">OAI-ORE의 탄생 배경</h3>
    <p class="mb-4">
      현대 웹에서는 하나의 학술 자료가 여러 파일로 구성되는 경우가 많습니다:
    </p>
    <ul class="list-disc pl-6 space-y-2 mb-6">
      <li>논문 PDF 본문</li>
      <li>보충 데이터셋 (CSV, Excel)</li>
      <li>관련 이미지와 그래프</li>
      <li>영상 자료나 발표 슬라이드</li>
      <li>메타데이터 파일</li>
    </ul>

    <p class="mb-4">
      이러한 여러 리소스를 <strong>"하나의 논리적 객체"</strong>로 묶어서 표현하고 관리하기 위해 OAI-ORE가 개발되었습니다.
    </p>
  </section>

  <section class="mb-8">
    <h2 class="text-3xl font-bold mb-4">2. 핵심 개념: Aggregation과 ResourceMap</h2>

    <div class="grid md:grid-cols-2 gap-6 mb-6">
      <div class="bg-green-50 p-6 rounded-lg">
        <h3 class="text-xl font-bold mb-3">📦 Aggregation (집합)</h3>
        <p class="mb-3">
          여러 웹 리소스를 하나로 묶은 논리적 집합입니다.
        </p>
        <p class="text-sm italic">
          예: "2024년 AI 연구 논문"이라는 Aggregation은 PDF, 데이터셋, 이미지를 포함할 수 있습니다.
        </p>
      </div>

      <div class="bg-purple-50 p-6 rounded-lg">
        <h3 class="text-xl font-bold mb-3">🗺️ ResourceMap (리소스 맵)</h3>
        <p class="mb-3">
          Aggregation을 RDF 형식으로 기술한 메타데이터 문서입니다.
        </p>
        <p class="text-sm italic">
          ResourceMap은 "어떤 리소스들이 포함되어 있고, 어떤 관계인지"를 명시합니다.
        </p>
      </div>
    </div>

    <h3 class="text-2xl font-semibold mb-3">관계 다이어그램</h3>
    <pre class="bg-gray-100 p-4 rounded-lg overflow-x-auto mb-6">
ResourceMap (RDF 문서)
    │
    ├── describes → Aggregation
    │                  │
    │                  ├── aggregates → Resource 1 (PDF)
    │                  ├── aggregates → Resource 2 (Dataset)
    │                  └── aggregates → Resource 3 (Image)
    </pre>
  </section>

  <section class="mb-8">
    <h2 class="text-3xl font-bold mb-4">3. 실제 RDF 예제</h2>

    <p class="mb-4">
      다음은 논문 하나를 Aggregation으로 표현한 ResourceMap 예제입니다:
    </p>

    <pre class="bg-gray-900 text-green-400 p-6 rounded-lg overflow-x-auto mb-6"><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:ore="http://www.openarchives.org/ore/terms/"
         xmlns:dcterms="http://purl.org/dc/terms/"&gt;

  &lt;!-- ResourceMap 자체 --&gt;
  &lt;rdf:Description rdf:about="http://example.org/rem/1"&gt;
    &lt;rdf:type rdf:resource="http://www.openarchives.org/ore/terms/ResourceMap"/&gt;
    &lt;ore:describes rdf:resource="http://example.org/aggregation/1"/&gt;
    &lt;dcterms:created&gt;2024-01-15T10:30:00Z&lt;/dcterms:created&gt;
  &lt;/rdf:Description&gt;

  &lt;!-- Aggregation --&gt;
  &lt;rdf:Description rdf:about="http://example.org/aggregation/1"&gt;
    &lt;rdf:type rdf:resource="http://www.openarchives.org/ore/terms/Aggregation"/&gt;
    &lt;dcterms:title&gt;AI 윤리에 관한 연구&lt;/dcterms:title&gt;
    &lt;dcterms:creator&gt;홍길동&lt;/dcterms:creator&gt;

    &lt;!-- 포함된 리소스들 --&gt;
    &lt;ore:aggregates rdf:resource="http://example.org/paper.pdf"/&gt;
    &lt;ore:aggregates rdf:resource="http://example.org/dataset.csv"/&gt;
    &lt;ore:aggregates rdf:resource="http://example.org/figure1.png"/&gt;
  &lt;/rdf:Description&gt;

  &lt;!-- 각 리소스에 대한 상세 정보 --&gt;
  &lt;rdf:Description rdf:about="http://example.org/paper.pdf"&gt;
    &lt;dcterms:format&gt;application/pdf&lt;/dcterms:format&gt;
    &lt;dcterms:extent&gt;2.5 MB&lt;/dcterms:extent&gt;
  &lt;/rdf:Description&gt;

  &lt;rdf:Description rdf:about="http://example.org/dataset.csv"&gt;
    &lt;dcterms:format&gt;text/csv&lt;/dcterms:format&gt;
    &lt;dcterms:description&gt;실험 데이터셋&lt;/dcterms:description&gt;
  &lt;/rdf:Description&gt;

&lt;/rdf:RDF&gt;</code></pre>

    <div class="bg-blue-50 p-4 rounded-lg">
      <h4 class="font-semibold mb-2">📖 코드 설명</h4>
      <ul class="list-disc pl-6 space-y-1 text-sm">
        <li><code>ore:ResourceMap</code>: 메타데이터 문서 자체</li>
        <li><code>ore:describes</code>: ResourceMap이 어떤 Aggregation을 설명하는지 표시</li>
        <li><code>ore:Aggregation</code>: 논리적으로 묶인 리소스 집합</li>
        <li><code>ore:aggregates</code>: Aggregation에 포함된 개별 리소스</li>
      </ul>
    </div>
  </section>

  <section class="mb-8">
    <h2 class="text-3xl font-bold mb-4">4. OAI-ORE의 실제 활용 사례</h2>

    <div class="space-y-4">
      <div class="border-l-4 border-blue-500 pl-4">
        <h3 class="font-bold">학술 리포지터리</h3>
        <p class="text-sm">논문 본문, 데이터셋, 보충 자료를 하나의 Aggregation으로 관리</p>
      </div>

      <div class="border-l-4 border-green-500 pl-4">
        <h3 class="font-bold">디지털 도서관</h3>
        <p class="text-sm">고서의 이미지 스캔, 텍스트 전사본, 주석을 통합 관리</p>
      </div>

      <div class="border-l-4 border-purple-500 pl-4">
        <h3 class="font-bold">멀티미디어 아카이브</h3>
        <p class="text-sm">영상, 자막, 메타데이터, 섬네일을 하나의 객체로 표현</p>
      </div>

      <div class="border-l-4 border-red-500 pl-4">
        <h3 class="font-bold">연구 데이터 관리</h3>
        <p class="text-sm">실험 데이터, 분석 스크립트, 결과 그래프를 연결</p>
      </div>
    </div>
  </section>

  <section class="mb-8">
    <h2 class="text-3xl font-bold mb-4">5. OAI-PMH와의 차이점</h2>

    <div class="overflow-x-auto">
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
            <td class="border border-gray-300 px-4 py-2 font-semibold">분류</td>
            <td class="border border-gray-300 px-4 py-2">프로토콜 (Protocol)</td>
            <td class="border border-gray-300 px-4 py-2">데이터 모델 / RDF 어휘</td>
          </tr>
          <tr>
            <td class="border border-gray-300 px-4 py-2 font-semibold">목적</td>
            <td class="border border-gray-300 px-4 py-2">메타데이터 수집 (Harvesting)</td>
            <td class="border border-gray-300 px-4 py-2">복합 객체 표현 (Aggregation)</td>
          </tr>
          <tr>
            <td class="border border-gray-300 px-4 py-2 font-semibold">기술 형식</td>
            <td class="border border-gray-300 px-4 py-2">XML (Dublin Core 등)</td>
            <td class="border border-gray-300 px-4 py-2">RDF (Turtle, RDF/XML, JSON-LD)</td>
          </tr>
          <tr>
            <td class="border border-gray-300 px-4 py-2 font-semibold">주요 용도</td>
            <td class="border border-gray-300 px-4 py-2">리포지터리 간 메타데이터 동기화</td>
            <td class="border border-gray-300 px-4 py-2">여러 리소스를 논리적 단위로 묶기</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="mb-8">
    <h2 class="text-3xl font-bold mb-4">6. 학습 정리 및 핵심 요점</h2>

    <div class="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg">
      <h3 class="text-xl font-bold mb-4">✅ 핵심 요약</h3>
      <ul class="space-y-3">
        <li class="flex items-start">
          <span class="text-2xl mr-3">1️⃣</span>
          <div>
            <strong>OAI-ORE는 프로토콜이 아닌 RDF 기반 데이터 모델입니다</strong>
            <p class="text-sm text-gray-600">복합 디지털 객체를 표현하기 위한 어휘와 구조를 제공합니다</p>
          </div>
        </li>
        <li class="flex items-start">
          <span class="text-2xl mr-3">2️⃣</span>
          <div>
            <strong>Aggregation은 여러 웹 리소스를 하나로 묶는 논리적 집합입니다</strong>
            <p class="text-sm text-gray-600">논문, 데이터, 이미지 등을 하나의 단위로 관리할 수 있습니다</p>
          </div>
        </li>
        <li class="flex items-start">
          <span class="text-2xl mr-3">3️⃣</span>
          <div>
            <strong>ResourceMap은 Aggregation을 RDF로 기술한 메타데이터입니다</strong>
            <p class="text-sm text-gray-600">기계가 읽을 수 있는 형식으로 구조와 관계를 명시합니다</p>
          </div>
        </li>
        <li class="flex items-start">
          <span class="text-2xl mr-3">4️⃣</span>
          <div>
            <strong>Linked Data와 Semantic Web 기술을 활용합니다</strong>
            <p class="text-sm text-gray-600">웹 표준을 따르며 상호운용성이 높습니다</p>
          </div>
        </li>
      </ul>
    </div>
  </section>

  <section class="mb-8">
    <h2 class="text-3xl font-bold mb-4">7. 더 알아보기</h2>

    <div class="bg-gray-50 p-6 rounded-lg">
      <h3 class="font-bold mb-3">📚 참고 자료</h3>
      <ul class="space-y-2">
        <li>
          <a href="https://www.openarchives.org/ore/1.0/primer" class="text-blue-600 hover:underline" target="_blank">
            OAI-ORE Primer (공식 문서)
          </a>
        </li>
        <li>
          <a href="https://www.openarchives.org/ore/1.0/vocabulary" class="text-blue-600 hover:underline" target="_blank">
            OAI-ORE Vocabulary Specification
          </a>
        </li>
        <li>
          <a href="http://www.openarchives.org/ore/1.0/datamodel" class="text-blue-600 hover:underline" target="_blank">
            OAI-ORE Data Model
          </a>
        </li>
      </ul>
    </div>
  </section>

  <div class="bg-yellow-50 border-l-4 border-yellow-400 p-6 mt-8">
    <h3 class="font-bold text-lg mb-2">💡 실습 과제</h3>
    <ol class="list-decimal pl-6 space-y-2">
      <li>자신의 연구 자료나 프로젝트를 OAI-ORE Aggregation으로 설계해보세요</li>
      <li>위 예제를 참고하여 간단한 ResourceMap RDF 문서를 작성해보세요</li>
      <li>OAI-PMH와 OAI-ORE가 함께 사용될 수 있는 시나리오를 생각해보세요</li>
    </ol>
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
