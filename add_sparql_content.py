#!/usr/bin/env python3
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.contents.models import Content, Category, Tag

User = get_user_model()

# 관리자 사용자 가져오기
admin = User.objects.filter(is_superuser=True).first()
if not admin:
    print("관리자 사용자를 찾을 수 없습니다.")
    sys.exit(1)

# 온톨로지 카테고리 찾기
ontology_category = Category.objects.filter(slug='ontology').first()
if not ontology_category:
    print("온톨로지 카테고리를 찾을 수 없습니다.")
    sys.exit(1)

# SPARQL 하위 카테고리 생성 또는 가져오기
sparql_category, created = Category.objects.get_or_create(
    slug='sparql',
    defaults={
        'name': 'SPARQL',
        'description': 'SPARQL 쿼리 언어',
        'parent': ontology_category
    }
)

if created:
    print(f"✓ SPARQL 카테고리 생성됨: {sparql_category.name}")
else:
    print(f"✓ 기존 SPARQL 카테고리 사용: {sparql_category.name}")

# 태그 데이터
tag_data = [
    {'name': 'SPARQL', 'slug': 'sparql'},
    {'name': '쿼리 언어', 'slug': 'query-language'},
    {'name': 'RDF', 'slug': 'rdf'},
    {'name': '시맨틱 웹', 'slug': 'semantic-web'},
    {'name': '온톨로지', 'slug': 'ontology'},
    {'name': '링크드 데이터', 'slug': 'linked-data'},
    {'name': '데이터베이스', 'slug': 'database'},
]

# 태그 생성
tags = []
for tag_info in tag_data:
    try:
        tag = Tag.objects.get(slug=tag_info['slug'])
        print(f"✓ 기존 태그 사용: {tag.name}")
    except Tag.DoesNotExist:
        try:
            tag = Tag.objects.get(name=tag_info['name'])
            print(f"✓ 기존 태그 사용 (name으로): {tag.name}")
        except Tag.DoesNotExist:
            tag = Tag.objects.create(name=tag_info['name'], slug=tag_info['slug'])
            print(f"✓ 태그 생성됨: {tag.name}")
    tags.append(tag)

# SPARQL 콘텐츠 생성 또는 업데이트
content, created = Content.objects.update_or_create(
    slug="sparql-query-language",
    defaults={
        'title': "SPARQL: RDF 데이터 검색의 표준 언어",
        'category': sparql_category,
        'author': admin,
        'difficulty': 'ADVANCED',
        'estimated_time': 50,
        'status': Content.Status.PUBLISHED,
        'summary': "SPARQL 쿼리 언어의 핵심 개념과 문법을 학습하고, 도서관 데이터를 직접 검색하는 실습을 통해 실무 활용 능력을 기릅니다.",
        'prerequisites': "RDF 기초, Turtle 문법, RDFS/OWL 기본 이해",
        'learning_objectives': "SPARQL의 기본 문법(SELECT, WHERE, FILTER) 이해하기, 트리플 패턴을 사용한 데이터 검색 방법 익히기, OPTIONAL, UNION 등 고급 쿼리 작성하기, 도서관 데이터를 실제로 검색하고 결과 분석하기, SPARQL 쿼리 오류를 이해하고 수정하기",
        'content_html': """
<div style="font-family: 'Noto Sans KR', sans-serif; line-height: 1.8; max-width: 1200px; margin: 0 auto; padding: 20px;">
    <h1 style="color: #1a1a1a; border-bottom: 3px solid #2563eb; padding-bottom: 10px; margin-bottom: 30px;">
        🔍 SPARQL: RDF 데이터 검색의 표준 언어
    </h1>

    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; margin-bottom: 30px;">
        <h2 style="color: white; margin-top: 0;">SPARQL이란 무엇인가?</h2>
        <p style="font-size: 16px; margin: 0;">
            <strong>SPARQL</strong>(SPARQL Protocol and RDF Query Language)은 <strong>RDF 데이터를 검색하는 표준 쿼리 언어</strong>입니다.
            SQL이 관계형 데이터베이스를 위한 언어라면, SPARQL은 시맨틱 웹과 링크드 데이터를 위한 언어입니다.
            도서관, 박물관, 정부 기관 등에서 대규모 지식 그래프를 검색하고 활용하는 데 사용됩니다.
        </p>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        📚 실습용 도서관 데이터
    </h2>

    <p>먼저 실습에 사용할 도서관 데이터를 살펴보겠습니다. 20권의 책과 저자, 주제 정보가 포함되어 있습니다.</p>

    <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <h3 style="color: #1e40af; margin: 0;">샘플 데이터 (Turtle 형식)</h3>
            <button onclick="toggleData()" style="background-color: #3b82f6; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px;">
                데이터 보기/숨기기
            </button>
        </div>
        <div id="sampleData" style="display: none;">
            <pre style="background-color: #1e293b; color: #e2e8f0; padding: 20px; border-radius: 6px; overflow-x: auto; font-size: 13px; line-height: 1.6; max-height: 500px; overflow-y: auto;">@prefix : &lt;http://library.example.org/&gt; .
@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .
@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .
@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .
@prefix dcterms: &lt;http://purl.org/dc/terms/&gt; .

# 책 데이터
:book1 a :Book ;
    dc:title "해리포터와 마법사의 돌" ;
    dc:creator :author1 ;
    dc:subject "판타지", "소설" ;
    :resourceType :PhysicalBook ;
    dcterms:issued "1997" ;
    :isbn "978-89-8392-476-1" .

:book2 a :Book ;
    dc:title "해리포터와 비밀의 방" ;
    dc:creator :author1 ;
    dc:subject "판타지", "소설" ;
    :resourceType :EBook ;
    dcterms:issued "1998" .

:book3 a :Book ;
    dc:title "클린 코드" ;
    dc:creator :author2 ;
    dc:subject "프로그래밍", "소프트웨어 공학" ;
    :resourceType :EBook ;
    dcterms:issued "2008" .

:book4 a :Book ;
    dc:title "리팩토링" ;
    dc:creator :author3 ;
    dc:subject "프로그래밍", "소프트웨어 공학" ;
    :resourceType :PhysicalBook ;
    dcterms:issued "1999" .

:book5 a :Book ;
    dc:title "소년이 온다" ;
    dc:creator :author4 ;
    dc:subject "문학", "한국소설" ;
    :resourceType :PhysicalBook ;
    dcterms:issued "2014" .

:book6 a :Book ;
    dc:title "채식주의자" ;
    dc:creator :author4 ;
    dc:subject "문학", "한국소설" ;
    :resourceType :EBook ;
    dcterms:issued "2007" .

:book7 a :Book ;
    dc:title "데이터베이스 시스템" ;
    dc:creator :author5 ;
    dc:subject "데이터베이스", "컴퓨터과학" ;
    :resourceType :PhysicalBook ;
    dcterms:issued "2011" .

:book8 a :Book ;
    dc:title "시맨틱 웹 입문" ;
    dc:creator :author6 ;
    dc:subject "시맨틱 웹", "온톨로지" ;
    :resourceType :EBook ;
    dcterms:issued "2015" .

:book9 a :Book ;
    dc:title "RDF와 SPARQL" ;
    dc:creator :author6 ;
    dc:subject "RDF", "SPARQL", "링크드 데이터" ;
    :resourceType :EBook ;
    dcterms:issued "2018" .

:book10 a :Book ;
    dc:title "도서관 정보학 개론" ;
    dc:creator :author7 ;
    dc:subject "도서관학", "정보학" ;
    :resourceType :PhysicalBook ;
    dcterms:issued "2010" .

:book11 a :Book ;
    dc:title "메타데이터의 이해" ;
    dc:creator :author7 ;
    dc:subject "메타데이터", "정보조직" ;
    :resourceType :EBook ;
    dcterms:issued "2016" .

:book12 a :Book ;
    dc:title "1984" ;
    dc:creator :author8 ;
    dc:subject "디스토피아", "소설" ;
    :resourceType :PhysicalBook ;
    dcterms:issued "1949" .

:book13 a :Book ;
    dc:title "동물농장" ;
    dc:creator :author8 ;
    dc:subject "우화", "소설" ;
    :resourceType :EBook ;
    dcterms:issued "1945" .

:book14 a :Book ;
    dc:title "코스모스" ;
    dc:creator :author9 ;
    dc:subject "천문학", "과학" ;
    :resourceType :PhysicalBook ;
    dcterms:issued "1980" .

:book15 a :Book ;
    dc:title "총, 균, 쇠" ;
    dc:creator :author10 ;
    dc:subject "역사", "인류학" ;
    :resourceType :EBook ;
    dcterms:issued "1997" .

:book16 a :Book ;
    dc:title "사피엔스" ;
    dc:creator :author11 ;
    dc:subject "역사", "인류학" ;
    :resourceType :PhysicalBook ;
    dcterms:issued "2011" .

:book17 a :Book ;
    dc:title "호모 데우스" ;
    dc:creator :author11 ;
    dc:subject "미래학", "기술" ;
    :resourceType :EBook ;
    dcterms:issued "2015" .

:book18 a :Book ;
    dc:title "파이썬으로 배우는 머신러닝" ;
    dc:creator :author12 ;
    dc:subject "머신러닝", "프로그래밍" ;
    :resourceType :EBook ;
    dcterms:issued "2019" .

:book19 a :Book ;
    dc:title "딥러닝의 정석" ;
    dc:creator :author12 ;
    dc:subject "딥러닝", "인공지능" ;
    :resourceType :EBook ;
    dcterms:issued "2020" .

:book20 a :Book ;
    dc:title "온톨로지 설계와 활용" ;
    dc:creator :author13 ;
    dc:subject "온톨로지", "지식표현" ;
    :resourceType :PhysicalBook ;
    dcterms:issued "2017" .

# 저자 데이터
:author1 a :Person ;
    rdfs:label "J.K. 롤링" ;
    :nationality "영국" .

:author2 a :Person ;
    rdfs:label "로버트 C. 마틴" ;
    :nationality "미국" .

:author3 a :Person ;
    rdfs:label "마틴 파울러" ;
    :nationality "영국" .

:author4 a :Person ;
    rdfs:label "한강" ;
    :nationality "한국" .

:author5 a :Person ;
    rdfs:label "엘마스리" ;
    :nationality "미국" .

:author6 a :Person ;
    rdfs:label "김승연" ;
    :nationality "한국" .

:author7 a :Person ;
    rdfs:label "이명희" ;
    :nationality "한국" .

:author8 a :Person ;
    rdfs:label "조지 오웰" ;
    :nationality "영국" .

:author9 a :Person ;
    rdfs:label "칼 세이건" ;
    :nationality "미국" .

:author10 a :Person ;
    rdfs:label "재레드 다이아몬드" ;
    :nationality "미국" .

:author11 a :Person ;
    rdfs:label "유발 하라리" ;
    :nationality "이스라엘" .

:author12 a :Person ;
    rdfs:label "박해선" ;
    :nationality "한국" .

:author13 a :Person ;
    rdfs:label "최윤수" ;
    :nationality "한국" .</pre>
        </div>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        💻 SPARQL 쿼리 실습
    </h2>

    <p>아래에서 직접 SPARQL 쿼리를 작성하고 실행해보세요!</p>

    <div style="background-color: #f0f9ff; padding: 25px; border-radius: 10px; margin: 20px 0; border: 2px solid #3b82f6;">
        <h3 style="color: #1e40af; margin-top: 0;">쿼리 입력</h3>

        <div style="margin-bottom: 15px;">
            <label style="display: block; margin-bottom: 8px; font-weight: bold; color: #1e40af;">예제 쿼리 선택:</label>
            <select id="exampleSelect" onchange="loadExample()" style="width: 100%; padding: 10px; border: 2px solid #3b82f6; border-radius: 6px; font-size: 14px;">
                <option value="">-- 예제를 선택하세요 --</option>
                <option value="all_books">1. 모든 책 조회</option>
                <option value="ebooks">2. 전자책만 조회</option>
                <option value="korean_authors">3. 한국 저자의 책</option>
                <option value="programming_books">4. 프로그래밍 관련 책</option>
                <option value="fantasy_novels">5. 판타지 소설</option>
                <option value="books_with_authors">6. 책과 저자 정보</option>
                <option value="recent_books">7. 2010년 이후 출간된 책</option>
                <option value="jk_rowling_books">8. J.K. 롤링의 책</option>
                <option value="subject_count">9. 주제별 책 수</option>
                <option value="optional_isbn">10. ISBN이 있으면 표시</option>
            </select>
        </div>

        <textarea id="queryInput" rows="10" style="width: 100%; padding: 15px; border: 2px solid #3b82f6; border-radius: 6px; font-family: monospace; font-size: 14px; resize: vertical;" placeholder="여기에 SPARQL 쿼리를 입력하세요...

예:
SELECT ?title ?author
WHERE {
  ?book dc:title ?title .
  ?book dc:creator ?creator .
  ?creator rdfs:label ?author .
}"></textarea>

        <div style="display: flex; gap: 10px; margin-top: 15px;">
            <button onclick="executeQuery()" style="background-color: #3b82f6; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold;">
                🔍 쿼리 실행
            </button>
            <button onclick="clearQuery()" style="background-color: #6b7280; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 16px;">
                🗑️ 초기화
            </button>
        </div>
    </div>

    <div id="queryExplanation" style="display: none; background-color: #ecfdf5; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #10b981;">
        <h3 style="color: #065f46; margin-top: 0;">📖 쿼리 설명</h3>
        <div id="explanationContent"></div>
    </div>

    <div id="errorMessage" style="display: none; background-color: #fef2f2; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ef4444;">
        <h3 style="color: #991b1b; margin-top: 0;">❌ 오류 발생</h3>
        <div id="errorContent"></div>
    </div>

    <div id="results" style="display: none; background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #1e40af; margin-top: 0;">✅ 검색 결과</h3>
        <div id="resultsContent"></div>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        📘 SPARQL 기본 문법
    </h2>

    <div style="background-color: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #1e40af; margin-top: 0;">기본 구조</h3>
        <pre style="background-color: #1e293b; color: #e2e8f0; padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 14px;">PREFIX prefix: &lt;URI&gt;

SELECT 변수들
WHERE {
  트리플 패턴들
}
LIMIT 숫자</pre>

        <div style="background-color: white; padding: 15px; border-radius: 6px; margin-top: 15px;">
            <h4 style="color: #1e40af; margin-top: 0;">구성 요소 설명</h4>
            <ul style="line-height: 2;">
                <li><strong>PREFIX</strong>: URI 축약을 위한 접두사 정의</li>
                <li><strong>SELECT</strong>: 결과로 반환할 변수 지정 (변수는 ? 또는 $로 시작)</li>
                <li><strong>WHERE</strong>: 검색 조건 (트리플 패턴)</li>
                <li><strong>LIMIT</strong>: 결과 개수 제한 (선택사항)</li>
            </ul>
        </div>
    </div>

    <h3 style="color: #1e40af; margin-top: 30px;">트리플 패턴</h3>

    <div style="background-color: #fff; padding: 20px; border-radius: 8px; margin: 15px 0; border: 2px solid #3b82f6;">
        <p style="margin-top: 0;">RDF는 <strong>주어-술어-목적어</strong> 형태의 트리플로 구성됩니다.</p>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
            <div style="background-color: #dbeafe; padding: 15px; border-radius: 6px;">
                <h4 style="color: #1e40af; margin: 0 0 10px 0;">RDF 데이터</h4>
                <code style="background-color: #1e293b; color: #22c55e; padding: 8px; display: block; border-radius: 4px; font-size: 13px;">
                    :book1 dc:title "해리포터" .
                </code>
                <p style="margin: 10px 0 0 0; font-size: 13px;">
                    주어: :book1<br>
                    술어: dc:title<br>
                    목적어: "해리포터"
                </p>
            </div>

            <div style="background-color: #dcfce7; padding: 15px; border-radius: 6px;">
                <h4 style="color: #166534; margin: 0 0 10px 0;">SPARQL 패턴</h4>
                <code style="background-color: #1e293b; color: #22c55e; padding: 8px; display: block; border-radius: 4px; font-size: 13px;">
                    ?book dc:title ?title .
                </code>
                <p style="margin: 10px 0 0 0; font-size: 13px;">
                    주어: ?book (변수)<br>
                    술어: dc:title<br>
                    목적어: ?title (변수)
                </p>
            </div>
        </div>

        <div style="background-color: #fef3c7; padding: 15px; border-radius: 6px;">
            <p style="margin: 0; font-size: 14px;">
                <strong>💡 핵심:</strong> 변수(?book, ?title)는 RDF 데이터에서 매칭되는 값을 찾습니다.
                위 패턴은 "어떤 책이든 그 제목을 모두 찾아라"는 의미입니다.
            </p>
        </div>
    </div>

    <h2 style="color: #2563eb; margin-top: 40px; border-left: 4px solid #2563eb; padding-left: 12px;">
        🎓 학습 가이드
    </h2>

    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0;">
        <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); color: white; padding: 20px; border-radius: 10px;">
            <h3 style="color: white; margin-top: 0;">1단계: 기본 조회</h3>
            <p style="font-size: 14px; margin: 0;">예제 1, 2, 3을 실행하며 SELECT와 WHERE의 기본을 익히세요.</p>
        </div>

        <div style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); color: white; padding: 20px; border-radius: 10px;">
            <h3 style="color: white; margin-top: 0;">2단계: 조건 검색</h3>
            <p style="font-size: 14px; margin: 0;">예제 4, 5, 7을 통해 FILTER 사용법을 배우세요.</p>
        </div>

        <div style="background: linear-gradient(135deg, #ec4899 0%, #db2777 100%); color: white; padding: 20px; border-radius: 10px;">
            <h3 style="color: white; margin-top: 0;">3단계: 고급 쿼리</h3>
            <p style="font-size: 14px; margin: 0;">예제 9, 10으로 OPTIONAL, GROUP BY를 마스터하세요.</p>
        </div>
    </div>

</div>

<script>
// 샘플 데이터를 JavaScript 객체로 변환 (중복 실행 방지)
if (!window.libraryData) {
    window.libraryData = {
        books: [
            {id: 'book1', title: '해리포터와 마법사의 돌', creator: 'author1', subject: ['판타지', '소설'], resourceType: 'PhysicalBook', issued: '1997', isbn: '978-89-8392-476-1'},
            {id: 'book2', title: '해리포터와 비밀의 방', creator: 'author1', subject: ['판타지', '소설'], resourceType: 'EBook', issued: '1998'},
            {id: 'book3', title: '클린 코드', creator: 'author2', subject: ['프로그래밍', '소프트웨어 공학'], resourceType: 'EBook', issued: '2008'},
            {id: 'book4', title: '리팩토링', creator: 'author3', subject: ['프로그래밍', '소프트웨어 공학'], resourceType: 'PhysicalBook', issued: '1999'},
            {id: 'book5', title: '소년이 온다', creator: 'author4', subject: ['문학', '한국소설'], resourceType: 'PhysicalBook', issued: '2014'},
            {id: 'book6', title: '채식주의자', creator: 'author4', subject: ['문학', '한국소설'], resourceType: 'EBook', issued: '2007'},
            {id: 'book7', title: '데이터베이스 시스템', creator: 'author5', subject: ['데이터베이스', '컴퓨터과학'], resourceType: 'PhysicalBook', issued: '2011'},
            {id: 'book8', title: '시맨틱 웹 입문', creator: 'author6', subject: ['시맨틱 웹', '온톨로지'], resourceType: 'EBook', issued: '2015'},
            {id: 'book9', title: 'RDF와 SPARQL', creator: 'author6', subject: ['RDF', 'SPARQL', '링크드 데이터'], resourceType: 'EBook', issued: '2018'},
            {id: 'book10', title: '도서관 정보학 개론', creator: 'author7', subject: ['도서관학', '정보학'], resourceType: 'PhysicalBook', issued: '2010'},
            {id: 'book11', title: '메타데이터의 이해', creator: 'author7', subject: ['메타데이터', '정보조직'], resourceType: 'EBook', issued: '2016'},
            {id: 'book12', title: '1984', creator: 'author8', subject: ['디스토피아', '소설'], resourceType: 'PhysicalBook', issued: '1949'},
            {id: 'book13', title: '동물농장', creator: 'author8', subject: ['우화', '소설'], resourceType: 'EBook', issued: '1945'},
            {id: 'book14', title: '코스모스', creator: 'author9', subject: ['천문학', '과학'], resourceType: 'PhysicalBook', issued: '1980'},
            {id: 'book15', title: '총, 균, 쇠', creator: 'author10', subject: ['역사', '인류학'], resourceType: 'EBook', issued: '1997'},
            {id: 'book16', title: '사피엔스', creator: 'author11', subject: ['역사', '인류학'], resourceType: 'PhysicalBook', issued: '2011'},
            {id: 'book17', title: '호모 데우스', creator: 'author11', subject: ['미래학', '기술'], resourceType: 'EBook', issued: '2015'},
            {id: 'book18', title: '파이썬으로 배우는 머신러닝', creator: 'author12', subject: ['머신러닝', '프로그래밍'], resourceType: 'EBook', issued: '2019'},
            {id: 'book19', title: '딥러닝의 정석', creator: 'author12', subject: ['딥러닝', '인공지능'], resourceType: 'EBook', issued: '2020'},
            {id: 'book20', title: '온톨로지 설계와 활용', creator: 'author13', subject: ['온톨로지', '지식표현'], resourceType: 'PhysicalBook', issued: '2017'}
        ],
        authors: [
            {id: 'author1', label: 'J.K. 롤링', nationality: '영국'},
            {id: 'author2', label: '로버트 C. 마틴', nationality: '미국'},
            {id: 'author3', label: '마틴 파울러', nationality: '영국'},
            {id: 'author4', label: '한강', nationality: '한국'},
            {id: 'author5', label: '엘마스리', nationality: '미국'},
            {id: 'author6', label: '김승연', nationality: '한국'},
            {id: 'author7', label: '이명희', nationality: '한국'},
            {id: 'author8', label: '조지 오웰', nationality: '영국'},
            {id: 'author9', label: '칼 세이건', nationality: '미국'},
            {id: 'author10', label: '재레드 다이아몬드', nationality: '미국'},
            {id: 'author11', label: '유발 하라리', nationality: '이스라엘'},
            {id: 'author12', label: '박해선', nationality: '한국'},
            {id: 'author13', label: '최윤수', nationality: '한국'}
        ]
    };
}
const libraryData = window.libraryData;

if (!window.sparqlExamples) {
    window.sparqlExamples = {
    all_books: {
        query: `PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://library.example.org/>

SELECT ?title
WHERE {
  ?book dc:title ?title .
}`,
        explanation: `<h4>모든 책의 제목 조회</h4>
<p>이 쿼리는 데이터베이스에 있는 모든 책의 제목을 검색합니다.</p>
<h5>쿼리 분석:</h5>
<ul>
  <li><strong>PREFIX</strong>: dc와 : 접두사를 정의합니다.</li>
  <li><strong>SELECT ?title</strong>: 책 제목을 결과로 반환합니다.</li>
  <li><strong>?book dc:title ?title</strong>: "어떤 책이든 그 제목을 찾아라"는 패턴입니다.</li>
</ul>
<p>💡 <strong>변수 ?book</strong>은 결과에 표시되지 않지만, 제목을 가진 모든 책을 찾는 데 사용됩니다.</p>`
    },
    ebooks: {
        query: `PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://library.example.org/>

SELECT ?title
WHERE {
  ?book dc:title ?title .
  ?book :resourceType :EBook .
}`,
        explanation: `<h4>전자책만 조회</h4>
<p>두 개의 트리플 패턴을 사용하여 전자책만 필터링합니다.</p>
<h5>쿼리 분석:</h5>
<ul>
  <li><strong>첫 번째 패턴</strong>: ?book dc:title ?title - 책 제목 찾기</li>
  <li><strong>두 번째 패턴</strong>: ?book :resourceType :EBook - 같은 책이 전자책인지 확인</li>
</ul>
<p>💡 두 패턴의 <strong>?book 변수가 같은 값</strong>을 가져야 하므로, 전자책인 것만 결과에 포함됩니다.</p>`
    },
    korean_authors: {
        query: `PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://library.example.org/>

SELECT ?title ?author
WHERE {
  ?book dc:title ?title .
  ?book dc:creator ?creator .
  ?creator rdfs:label ?author .
  ?creator :nationality "한국" .
}`,
        explanation: `<h4>한국 저자의 책 조회</h4>
<p>여러 트리플을 연결하여 책, 저자, 국적 정보를 함께 검색합니다.</p>
<h5>쿼리 분석:</h5>
<ul>
  <li><strong>?book dc:title ?title</strong>: 책 제목</li>
  <li><strong>?book dc:creator ?creator</strong>: 책의 저자 (ID)</li>
  <li><strong>?creator rdfs:label ?author</strong>: 저자 이름</li>
  <li><strong>?creator :nationality "한국"</strong>: 국적이 한국인 저자만</li>
</ul>
<p>💡 네 개의 패턴이 모두 만족되는 경우만 결과에 포함됩니다. 이를 <strong>그래프 패턴 매칭</strong>이라고 합니다.</p>`
    },
    programming_books: {
        query: `PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://library.example.org/>

SELECT ?title ?subject
WHERE {
  ?book dc:title ?title .
  ?book dc:subject ?subject .
  FILTER(CONTAINS(LCASE(?subject), "프로그래밍"))
}`,
        explanation: `<h4>프로그래밍 관련 책 조회</h4>
<p>FILTER를 사용하여 주제에 "프로그래밍"이 포함된 책을 검색합니다.</p>
<h5>쿼리 분석:</h5>
<ul>
  <li><strong>FILTER</strong>: 조건을 만족하는 결과만 필터링</li>
  <li><strong>CONTAINS()</strong>: 문자열 포함 여부 확인</li>
  <li><strong>LCASE()</strong>: 소문자로 변환 (대소문자 무시)</li>
</ul>
<p>💡 FILTER는 WHERE 블록 내 어디든 위치할 수 있으며, 이미 매칭된 결과를 추가로 거릅니다.</p>`
    },
    fantasy_novels: {
        query: `PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://library.example.org/>

SELECT ?title
WHERE {
  ?book dc:title ?title .
  ?book dc:subject "판타지" .
}`,
        explanation: `<h4>판타지 소설 조회</h4>
<p>주제가 정확히 "판타지"인 책을 검색합니다.</p>
<h5>쿼리 분석:</h5>
<ul>
  <li><strong>dc:subject "판타지"</strong>: 주제가 정확히 "판타지"인 경우만</li>
  <li>변수 대신 <strong>리터럴 값</strong>("판타지")을 사용하여 정확한 매칭</li>
</ul>
<p>💡 한 책이 여러 주제를 가질 수 있으므로, 여러 dc:subject 트리플이 있을 수 있습니다.</p>`
    },
    books_with_authors: {
        query: `PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://library.example.org/>

SELECT ?title ?author ?nationality
WHERE {
  ?book dc:title ?title .
  ?book dc:creator ?creator .
  ?creator rdfs:label ?author .
  ?creator :nationality ?nationality .
}
LIMIT 10`,
        explanation: `<h4>책과 저자 정보 함께 조회</h4>
<p>책 제목, 저자 이름, 저자 국적을 한 번에 검색합니다.</p>
<h5>쿼리 분석:</h5>
<ul>
  <li>여러 변수를 SELECT에 나열하여 <strong>조인 결과</strong> 생성</li>
  <li><strong>LIMIT 10</strong>: 결과를 10개로 제한</li>
</ul>
<p>💡 이는 SQL의 JOIN과 유사하지만, SPARQL에서는 공통 변수로 자동 조인됩니다.</p>`
    },
    recent_books: {
        query: `PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX : <http://library.example.org/>

SELECT ?title ?year
WHERE {
  ?book dc:title ?title .
  ?book dcterms:issued ?year .
  FILTER(?year >= "2010")
}
ORDER BY DESC(?year)`,
        explanation: `<h4>2010년 이후 출간된 책 조회</h4>
<p>출판 연도를 기준으로 필터링하고 정렬합니다.</p>
<h5>쿼리 분석:</h5>
<ul>
  <li><strong>FILTER(?year >= "2010")</strong>: 2010년 이후 출간</li>
  <li><strong>ORDER BY DESC(?year)</strong>: 출판 연도 내림차순 정렬</li>
</ul>
<p>💡 숫자나 날짜 비교를 위해 FILTER에서 비교 연산자(>=, <=, =, !=)를 사용할 수 있습니다.</p>`
    },
    jk_rowling_books: {
        query: `PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX : <http://library.example.org/>

SELECT ?title
WHERE {
  ?book dc:title ?title .
  ?book dc:creator ?creator .
  ?creator rdfs:label "J.K. 롤링" .
}`,
        explanation: `<h4>특정 저자(J.K. 롤링)의 책 조회</h4>
<p>저자 이름으로 직접 필터링합니다.</p>
<h5>쿼리 분석:</h5>
<ul>
  <li><strong>rdfs:label "J.K. 롤링"</strong>: 저자 이름이 정확히 일치하는 경우만</li>
  <li>변수를 사용하지 않고 <strong>리터럴 값으로 직접 매칭</strong></li>
</ul>
<p>💡 이 방법은 정확한 이름을 알 때 유용합니다. 부분 검색은 FILTER(CONTAINS())를 사용하세요.</p>`
    },
    subject_count: {
        query: `PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://library.example.org/>

SELECT ?subject (COUNT(?book) AS ?count)
WHERE {
  ?book dc:subject ?subject .
}
GROUP BY ?subject
ORDER BY DESC(?count)`,
        explanation: `<h4>주제별 책 수 집계</h4>
<p>GROUP BY와 집계 함수를 사용하여 통계를 생성합니다.</p>
<h5>쿼리 분석:</h5>
<ul>
  <li><strong>COUNT(?book)</strong>: 각 주제별 책 개수 세기</li>
  <li><strong>AS ?count</strong>: 집계 결과를 ?count 변수에 저장</li>
  <li><strong>GROUP BY ?subject</strong>: 주제별로 그룹화</li>
  <li><strong>ORDER BY DESC(?count)</strong>: 책 수가 많은 순으로 정렬</li>
</ul>
<p>💡 집계 함수: COUNT, SUM, AVG, MIN, MAX를 사용할 수 있습니다.</p>`
    },
    optional_isbn: {
        query: `PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://library.example.org/>

SELECT ?title ?isbn
WHERE {
  ?book dc:title ?title .
  OPTIONAL { ?book :isbn ?isbn . }
}`,
        explanation: `<h4>ISBN이 있으면 표시 (OPTIONAL)</h4>
<p>OPTIONAL을 사용하여 선택적 정보를 조회합니다.</p>
<h5>쿼리 분석:</h5>
<ul>
  <li><strong>OPTIONAL { ... }</strong>: 이 패턴은 선택사항</li>
  <li>ISBN이 있으면 표시하고, 없어도 책 제목은 결과에 포함</li>
  <li>ISBN이 없는 경우 ?isbn 값은 NULL(또는 빈 값)이 됩니다</li>
</ul>
<p>💡 OPTIONAL 없이 ?book :isbn ?isbn을 사용하면, ISBN이 없는 책은 결과에서 제외됩니다.</p>`
    }
    };
}
const examples = window.sparqlExamples;

function toggleData() {
    const dataDiv = document.getElementById('sampleData');
    dataDiv.style.display = dataDiv.style.display === 'none' ? 'block' : 'none';
}

function loadExample() {
    const select = document.getElementById('exampleSelect');
    const exampleKey = select.value;

    if (exampleKey && examples[exampleKey]) {
        document.getElementById('queryInput').value = examples[exampleKey].query;

        // Show explanation
        const explDiv = document.getElementById('queryExplanation');
        const explContent = document.getElementById('explanationContent');
        explContent.innerHTML = examples[exampleKey].explanation;
        explDiv.style.display = 'block';

        // Hide error and results
        document.getElementById('errorMessage').style.display = 'none';
        document.getElementById('results').style.display = 'none';
    }
}

function clearQuery() {
    document.getElementById('queryInput').value = '';
    document.getElementById('exampleSelect').value = '';
    document.getElementById('queryExplanation').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('results').style.display = 'none';
}

function executeQuery() {
    const queryInput = document.getElementById('queryInput');

    if (!queryInput) {
        showError('쿼리 입력창을 찾을 수 없습니다.', '페이지를 새로고침하고 다시 시도해주세요.');
        return;
    }

    const query = queryInput.value.trim();
    console.log('Query input value:', query);

    if (!query) {
        showError('쿼리를 입력해주세요.', '위의 텍스트 영역에 SPARQL 쿼리를 입력하거나 예제를 선택하세요.');
        return;
    }

    try {
        const results = parseAndExecuteSPARQL(query);
        displayResults(results);
    } catch (error) {
        console.error('Query execution error:', error);
        showError(error.message, error.details);
    }
}

function showError(message, details = '') {
    const errorDiv = document.getElementById('errorMessage');
    const errorContent = document.getElementById('errorContent');

    let html = `<p style="font-size: 16px; margin: 0 0 10px 0;"><strong>${message}</strong></p>`;

    if (details) {
        html += `<div style="background-color: white; padding: 15px; border-radius: 6px; margin-top: 10px;">
            <h4 style="color: #991b1b; margin-top: 0;">상세 정보:</h4>
            <p style="margin: 0;">${details}</p>
        </div>`;
    }

    errorContent.innerHTML = html;
    errorDiv.style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');

    if (results.length === 0) {
        resultsContent.innerHTML = '<p style="color: #6b7280;">검색 결과가 없습니다.</p>';
    } else {
        const columns = Object.keys(results[0]);

        let html = `<p style="margin: 0 0 15px 0;"><strong>${results.length}개의 결과를 찾았습니다.</strong></p>`;
        html += '<div style="overflow-x: auto;"><table style="width: 100%; border-collapse: collapse; background-color: white;">';

        // Header
        html += '<thead><tr style="background-color: #3b82f6; color: white;">';
        columns.forEach(col => {
            html += `<th style="padding: 12px; text-align: left; border: 1px solid #ddd;">${col}</th>`;
        });
        html += '</tr></thead>';

        // Body
        html += '<tbody>';
        results.forEach((row, idx) => {
            const bgColor = idx % 2 === 0 ? '#f8fafc' : 'white';
            html += `<tr style="background-color: ${bgColor};">`;
            columns.forEach(col => {
                const value = row[col] !== undefined && row[col] !== null ? row[col] : '-';
                html += `<td style="padding: 10px; border: 1px solid #ddd;">${value}</td>`;
            });
            html += '</tr>';
        });
        html += '</tbody></table></div>';

        resultsContent.innerHTML = html;
    }

    resultsDiv.style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';
}

function parseAndExecuteSPARQL(query) {
    // Simple SPARQL parser and executor
    const selectMatch = query.match(/SELECT\s+(.*?)\s+WHERE/is);
    if (!selectMatch) {
        throw {
            message: 'SELECT 절을 찾을 수 없습니다.',
            details: 'SPARQL 쿼리는 SELECT 키워드와 WHERE 키워드를 포함해야 합니다. 예: SELECT ?title WHERE { ... }'
        };
    }

    const selectClause = selectMatch[1].trim();

    // Parse SELECT variables
    const selectVars = [];
    const varMatches = selectClause.matchAll(/\?(\w+)|\(COUNT\(\?(\w+)\)\s+AS\s+\?(\w+)\)/g);
    let hasAggregation = false;
    let aggregationVar = null;

    for (const match of varMatches) {
        if (match[1]) {
            selectVars.push(match[1]);
        } else if (match[2] && match[3]) {
            hasAggregation = true;
            aggregationVar = match[3];
            if (!selectVars.includes(match[2])) {
                selectVars.push(match[2]);
            }
        }
    }

    if (selectVars.length === 0) {
        throw {
            message: 'SELECT 절에 변수가 없습니다.',
            details: '변수는 ?로 시작해야 합니다. 예: SELECT ?title ?author'
        };
    }

    // Parse WHERE clause
    const whereMatch = query.match(/WHERE\s*\{(.*)\}/is);
    if (!whereMatch) {
        throw {
            message: 'WHERE 절을 찾을 수 없습니다.',
            details: 'WHERE { ... } 형식으로 작성해야 합니다. 중괄호를 확인하세요.'
        };
    }

    const whereClause = whereMatch[1];

    // Parse triple patterns
    const patterns = [];
    const optionalPatterns = [];
    const filters = [];

    // Extract OPTIONAL blocks
    const optionalMatch = whereClause.match(/OPTIONAL\s*\{([^}]*)\}/i);
    let mainWhere = whereClause;
    if (optionalMatch) {
        mainWhere = whereClause.replace(optionalMatch[0], '');
        const optTriples = optionalMatch[1].split('.').map(t => t.trim()).filter(t => t);
        optTriples.forEach(triple => {
            const parsed = parseTriple(triple);
            if (parsed) optionalPatterns.push(parsed);
        });
    }

    // Extract FILTER
    const filterMatches = mainWhere.matchAll(/FILTER\s*\((.*?)\)/gi);
    for (const match of filterMatches) {
        filters.push(match[1]);
        mainWhere = mainWhere.replace(match[0], '');
    }

    // Parse main triples
    const triples = mainWhere.split('.').map(t => t.trim()).filter(t => t && !t.match(/^\s*$/));
    triples.forEach(triple => {
        const parsed = parseTriple(triple);
        if (parsed) patterns.push(parsed);
    });

    // Execute query
    let results = executePatterns(patterns, filters);

    // Apply OPTIONAL patterns
    if (optionalPatterns.length > 0) {
        results = results.map(binding => {
            const optResults = executePatterns(optionalPatterns, [], binding);
            if (optResults.length > 0) {
                return {...binding, ...optResults[0]};
            }
            return binding;
        });
    }

    // Apply GROUP BY if aggregation
    if (hasAggregation) {
        const groupByMatch = query.match(/GROUP\s+BY\s+\?(\w+)/i);
        if (groupByMatch) {
            const groupVar = groupByMatch[1];
            const grouped = {};

            results.forEach(row => {
                const key = row[groupVar];
                if (!grouped[key]) {
                    grouped[key] = [];
                }
                grouped[key].push(row);
            });

            results = Object.entries(grouped).map(([key, rows]) => {
                const result = {};
                result[groupVar] = key;
                result[aggregationVar] = rows.length;
                return result;
            });
        }
    }

    // Apply ORDER BY
    const orderMatch = query.match(/ORDER\s+BY\s+(DESC\s*\()?\?(\w+)\)?/i);
    if (orderMatch) {
        const orderVar = orderMatch[2];
        const isDesc = orderMatch[1] !== undefined;
        results.sort((a, b) => {
            const aVal = a[orderVar];
            const bVal = b[orderVar];
            if (aVal < bVal) return isDesc ? 1 : -1;
            if (aVal > bVal) return isDesc ? -1 : 1;
            return 0;
        });
    }

    // Apply LIMIT
    const limitMatch = query.match(/LIMIT\s+(\d+)/i);
    if (limitMatch) {
        results = results.slice(0, parseInt(limitMatch[1]));
    }

    // Project only selected variables
    const finalVars = hasAggregation ?
        [...selectVars.filter(v => v !== selectVars[selectVars.length - 1]), aggregationVar] :
        selectVars;

    results = results.map(row => {
        const projected = {};
        finalVars.forEach(v => {
            projected[v] = row[v];
        });
        return projected;
    });

    return results;
}

function parseTriple(triple) {
    const parts = triple.trim().split(/\s+/);
    if (parts.length < 3) return null;

    return {
        subject: parts[0],
        predicate: parts[1],
        object: parts.slice(2).join(' ').replace(/\s*\.$/, '')
    };
}

function executePatterns(patterns, filters, initialBinding = {}) {
    let bindings = [initialBinding];

    patterns.forEach(pattern => {
        const newBindings = [];

        bindings.forEach(binding => {
            const matches = matchPattern(pattern, binding);
            newBindings.push(...matches);
        });

        bindings = newBindings;
    });

    // Apply filters
    filters.forEach(filter => {
        bindings = bindings.filter(binding => evaluateFilter(filter, binding));
    });

    return bindings;
}

function matchPattern(pattern, binding) {
    const results = [];

    // Match against books
    libraryData.books.forEach(book => {
        const match = matchTripleToBook(pattern, book, binding);
        if (match) {
            results.push(match);
        }
    });

    // Match against authors
    libraryData.authors.forEach(author => {
        const match = matchTripleToAuthor(pattern, author, binding);
        if (match) {
            results.push(match);
        }
    });

    return results;
}

function matchTripleToBook(pattern, book, binding) {
    const newBinding = {...binding};
    const {subject, predicate, object} = pattern;

    // Subject matching
    if (subject.startsWith('?')) {
        if (binding[subject.substring(1)] && binding[subject.substring(1)] !== book.id) {
            return null;
        }
        newBinding[subject.substring(1)] = book.id;
    } else if (subject !== ':' + book.id) {
        return null;
    }

    // Predicate and object matching
    const pred = predicate.replace(/^(dc:|dcterms:|:|rdfs:)/, '');

    if (pred === 'title') {
        return matchObjectValue(object, book.title, newBinding);
    } else if (pred === 'creator') {
        return matchObjectValue(object, book.creator, newBinding);
    } else if (pred === 'subject') {
        // subjects is array
        for (const subj of book.subject) {
            const match = matchObjectValue(object, subj, newBinding);
            if (match) return match;
        }
        return null;
    } else if (pred === 'resourceType') {
        return matchObjectValue(object, book.resourceType, newBinding);
    } else if (pred === 'issued') {
        return matchObjectValue(object, book.issued, newBinding);
    } else if (pred === 'isbn') {
        if (book.isbn) {
            return matchObjectValue(object, book.isbn, newBinding);
        }
        return null;
    }

    return null;
}

function matchTripleToAuthor(pattern, author, binding) {
    const newBinding = {...binding};
    const {subject, predicate, object} = pattern;

    // Subject matching
    if (subject.startsWith('?')) {
        if (binding[subject.substring(1)] && binding[subject.substring(1)] !== author.id) {
            return null;
        }
        newBinding[subject.substring(1)] = author.id;
    } else if (subject !== ':' + author.id) {
        return null;
    }

    // Predicate and object matching
    const pred = predicate.replace(/^(rdfs:|:)/, '');

    if (pred === 'label') {
        return matchObjectValue(object, author.label, newBinding);
    } else if (pred === 'nationality') {
        return matchObjectValue(object, author.nationality, newBinding);
    }

    return null;
}

function matchObjectValue(objectPattern, value, binding) {
    if (objectPattern.startsWith('?')) {
        const varName = objectPattern.substring(1);
        if (binding[varName] && binding[varName] !== value) {
            return null;
        }
        binding[varName] = value;
        return binding;
    } else {
        // Literal value
        const cleanPattern = objectPattern.replace(/^["']|["']$/g, '').replace(/^:/, '');
        const cleanValue = value.replace(/^:/, '');
        if (cleanPattern === cleanValue) {
            return binding;
        }
        return null;
    }
}

function evaluateFilter(filter, binding) {
    // Simple filter evaluation

    // CONTAINS filter
    const containsMatch = filter.match(/CONTAINS\s*\(\s*LCASE\s*\(\s*\?(\w+)\s*\)\s*,\s*"([^"]+)"\s*\)/i);
    if (containsMatch) {
        const varName = containsMatch[1];
        const searchTerm = containsMatch[2].toLowerCase();
        const value = binding[varName];
        if (value) {
            return value.toLowerCase().includes(searchTerm);
        }
        return false;
    }

    // Comparison filters
    const compMatch = filter.match(/\?(\w+)\s*(>=|<=|=|!=|>|<)\s*"([^"]+)"/);
    if (compMatch) {
        const varName = compMatch[1];
        const operator = compMatch[2];
        const compareValue = compMatch[3];
        const value = binding[varName];

        if (value === undefined) return false;

        switch (operator) {
            case '>=': return value >= compareValue;
            case '<=': return value <= compareValue;
            case '>': return value > compareValue;
            case '<': return value < compareValue;
            case '=': return value === compareValue;
            case '!=': return value !== compareValue;
        }
    }

    return true;
}

// 페이지 로드 시 첫 번째 예제 자동 선택
if (!window.sparqlInitialized) {
    window.sparqlInitialized = true;

    // DOM이 준비되면 실행
    setTimeout(() => {
        const exampleSelect = document.getElementById('exampleSelect');
        if (exampleSelect && !exampleSelect.value) {
            exampleSelect.value = 'all_books';
            loadExample();
        }
    }, 100);
}
</script>

<style>
button:hover {
    opacity: 0.9;
}

select {
    cursor: pointer;
}

table {
    border-radius: 8px;
    overflow: hidden;
}

@media (max-width: 768px) {
    .grid {
        grid-template-columns: 1fr !important;
    }
}
</style>
"""
    }
)

# 태그 연결
content.tags.set(tags)

if created:
    print("\n✓ SPARQL 콘텐츠 생성 완료!")
else:
    print("\n✓ SPARQL 콘텐츠 업데이트 완료!")

print(f"  - 제목: {content.title}")
print(f"  - 카테고리: {content.category.name}")
print(f"  - 난이도: {content.difficulty}")
print(f"  - 예상 학습시간: {content.estimated_time}분")
print(f"  - 태그: {', '.join([tag.name for tag in content.tags.all()])}")
print(f"\n콘텐츠가 성공적으로 {'추가' if created else '업데이트'}되었습니다!")
