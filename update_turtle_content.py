#!/usr/bin/env python
"""Turtle 교육자료 업데이트 스크립트"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content

# Turtle 교육 콘텐츠
turtle_content_html = """
<div class="space-y-8">
    <section>
        <h2 class="text-2xl font-bold mb-4">Turtle이란 무엇인가요? 🐢</h2>
        <div class="prose prose-lg">
            <p>
                <strong>Turtle (Terse RDF Triple Language)</strong>은 RDF 데이터를 사람이 읽고 쓰기 쉽게 표현하는 텍스트 형식입니다.
            </p>
            <p>
                XML/RDF의 복잡한 태그 대신, 간결하고 직관적인 문법으로 RDF 트리플을 표현합니다.
            </p>

            <div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-4">
                <p class="font-semibold">💡 왜 Turtle을 배워야 할까요?</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>XML/RDF보다 훨씬 읽고 쓰기 쉽습니다</li>
                    <li>RDF 데이터를 직접 작성하고 편집할 수 있습니다</li>
                    <li>SPARQL 쿼리와 문법이 유사합니다</li>
                    <li>W3C 표준 형식입니다</li>
                    <li>도서관, 박물관 등에서 메타데이터 작성에 활용됩니다</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">Turtle의 기본 문법 📝</h2>
        <div class="prose prose-lg">
            <h3 class="text-xl font-semibold mb-3">1. 트리플 (Triple) 기본 구조</h3>
            <p>Turtle의 가장 기본 단위는 <strong>주어-술어-목적어</strong> 형태의 트리플입니다.</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">&lt;http://example.org/person/kim&gt; &lt;http://xmlns.com/foaf/0.1/name&gt; "김철수" .
&lt;http://example.org/person/kim&gt; &lt;http://xmlns.com/foaf/0.1/age&gt; "25" .
&lt;http://example.org/person/kim&gt; &lt;http://xmlns.com/foaf/0.1/mbox&gt; &lt;mailto:kim@example.org&gt; .</code></pre>
            </div>

            <p>위 예제의 구조:</p>
            <ul class="list-disc pl-6 space-y-2">
                <li><code style="color: #1f2937;">&lt;http://example.org/person/kim&gt;</code> - <strong>주어 (Subject)</strong>: URI로 표현된 자원</li>
                <li><code style="color: #1f2937;">&lt;http://xmlns.com/foaf/0.1/name&gt;</code> - <strong>술어 (Predicate)</strong>: 속성</li>
                <li><code style="color: #1f2937;">"김철수"</code> - <strong>목적어 (Object)</strong>: 리터럴 값</li>
                <li><code style="color: #1f2937;">.</code> - <strong>마침표</strong>: 트리플의 끝</li>
            </ul>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">Prefix로 간결하게 쓰기 🎯</h2>
        <div class="prose prose-lg">
            <p>긴 URI를 매번 쓰는 것은 불편합니다. <strong>Prefix</strong>를 사용하면 간결하게 표현할 수 있습니다.</p>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
                <div>
                    <p class="text-sm font-semibold text-red-600 mb-2">❌ Prefix 사용 전</p>
                    <div class="bg-red-50 p-3 rounded">
                        <pre class="text-sm"><code style="color: #1f2937;">&lt;http://example.org/person/kim&gt;
  &lt;http://xmlns.com/foaf/0.1/name&gt;
  "김철수" .</code></pre>
                    </div>
                </div>

                <div>
                    <p class="text-sm font-semibold text-green-600 mb-2">✅ Prefix 사용 후</p>
                    <div class="bg-green-50 p-3 rounded">
                        <pre class="text-sm"><code style="color: #1f2937;">@prefix ex: &lt;http://example.org/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .

ex:person/kim foaf:name "김철수" .</code></pre>
                    </div>
                </div>
            </div>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">💡 자주 사용되는 Prefix</p>
                <div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
                    <pre style="margin: 0;"><code style="color: #1f2937;">@prefix rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt; .
@prefix rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt; .
@prefix owl: &lt;http://www.w3.org/2002/07/owl#&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .
@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .
@prefix dcterms: &lt;http://purl.org/dc/terms/&gt; .</code></pre>
                </div>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">같은 주어 반복 줄이기 📌</h2>
        <div class="prose prose-lg">
            <p>같은 주어에 대해 여러 속성을 표현할 때, <strong>세미콜론(;)</strong>을 사용하면 주어를 반복하지 않아도 됩니다.</p>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
                <div>
                    <p class="text-sm font-semibold mb-2">반복적인 방법</p>
                    <div style="background-color: #fef2f2; padding: 0.75rem; border-radius: 0.375rem;">
                        <pre class="text-sm"><code style="color: #1f2937;">ex:kim foaf:name "김철수" .
ex:kim foaf:age "25" .
ex:kim foaf:knows ex:lee .</code></pre>
                    </div>
                </div>

                <div>
                    <p class="text-sm font-semibold text-green-600 mb-2">✅ 세미콜론 사용</p>
                    <div style="background-color: #f0fdf4; padding: 0.75rem; border-radius: 0.375rem;">
                        <pre class="text-sm"><code style="color: #1f2937;">ex:kim foaf:name "김철수" ;
       foaf:age "25" ;
       foaf:knows ex:lee .</code></pre>
                    </div>
                </div>
            </div>

            <p class="mt-4">같은 주어와 술어에 여러 목적어가 있을 때는 <strong>쉼표(,)</strong>를 사용합니다.</p>

            <div style="background-color: #f0fdf4; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
                <pre style="margin: 0;"><code style="color: #1f2937;">ex:kim foaf:interest ex:reading ,
                   ex:programming ,
                   ex:music .</code></pre>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">데이터 타입과 언어 태그 🏷️</h2>
        <div class="prose prose-lg">
            <h3 class="text-xl font-semibold mb-3">데이터 타입 지정</h3>
            <p>숫자, 날짜 등의 데이터 타입을 명시적으로 지정할 수 있습니다.</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .

ex:book ex:price "25000"^^xsd:integer ;
        ex:published "2023-01-15"^^xsd:date ;
        ex:rating "4.5"^^xsd:decimal ;
        ex:inStock "true"^^xsd:boolean .</code></pre>
            </div>

            <h3 class="text-xl font-semibold mb-3 mt-6">언어 태그</h3>
            <p>다국어 텍스트를 표현할 때 언어 태그를 사용합니다.</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">ex:book dc:title "어린왕자"@ko ;
        dc:title "The Little Prince"@en ;
        dc:title "Le Petit Prince"@fr .</code></pre>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">실전 예제: 도서관 장서 정보 📚</h2>
        <div class="prose prose-lg">
            <p>실제 도서관에서 사용할 수 있는 Turtle 문서 예제입니다.</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">@prefix ex: &lt;http://example.org/library/&gt; .
@prefix dc: &lt;http://purl.org/dc/elements/1.1/&gt; .
@prefix dcterms: &lt;http://purl.org/dc/terms/&gt; .
@prefix bibo: &lt;http://purl.org/ontology/bibo/&gt; .
@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .

ex:book001
    a bibo:Book ;
    dc:title "어린왕자"@ko ;
    dc:title "The Little Prince"@en ;
    dc:creator "생텍쥐페리" ;
    dc:publisher "민음사" ;
    dcterms:issued "2015"^^xsd:gYear ;
    bibo:isbn "978-8937460449" ;
    ex:location "제1자료실" ;
    ex:callNumber "863-생63ㅇ" ;
    ex:available "true"^^xsd:boolean ;
    ex:copies "3"^^xsd:integer .

ex:book002
    a bibo:Book ;
    dc:title "데미안"@ko ;
    dc:creator "헤르만 헤세" ;
    dc:publisher "민음사" ;
    dcterms:issued "2018"^^xsd:gYear ;
    bibo:isbn "978-8932917221" ;
    ex:location "제2자료실" ;
    ex:callNumber "853-헤53ㄷ" ;
    ex:available "false"^^xsd:boolean ;
    ex:copies "2"^^xsd:integer .</code></pre>
            </div>

            <div class="bg-green-50 border-l-4 border-green-500 p-4 my-4">
                <p class="font-semibold">💡 이 예제의 특징</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li><code style="color: #1f2937;">a</code>는 <code style="color: #1f2937;">rdf:type</code>의 축약형</li>
                    <li>다국어 제목을 언어 태그로 구분</li>
                    <li>날짜, 숫자, 불린 등 데이터 타입 명시</li>
                    <li>세미콜론으로 속성을 나열하여 가독성 향상</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">Blank Node (익명 노드) 🔹</h2>
        <div class="prose prose-lg">
            <p>URI가 필요 없는 중간 노드를 표현할 때 Blank Node를 사용합니다.</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">ex:kim foaf:name "김철수" ;
       foaf:address [
           ex:street "세종대로 110" ;
           ex:city "서울" ;
           ex:postalCode "03172"
       ] .</code></pre>
            </div>

            <p>또는 명시적으로 Blank Node 식별자를 사용할 수 있습니다:</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">_:addr1 ex:street "세종대로 110" ;
        ex:city "서울" ;
        ex:postalCode "03172" .

ex:kim foaf:address _:addr1 .</code></pre>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">Collection (컬렉션) 📦</h2>
        <div class="prose prose-lg">
            <p>순서가 있는 목록을 표현할 때 괄호 <code style="color: #1f2937;">()</code>를 사용합니다.</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">ex:course ex:topics ( "RDF 기초" "SPARQL 쿼리" "온톨로지 설계" ) .</code></pre>
            </div>

            <p>이것은 다음과 동일합니다:</p>

            <div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0;"><code style="color: #1f2937;">ex:course ex:topics _:b1 .
_:b1 rdf:first "RDF 기초" ;
     rdf:rest _:b2 .
_:b2 rdf:first "SPARQL 쿼리" ;
     rdf:rest _:b3 .
_:b3 rdf:first "온톨로지 설계" ;
     rdf:rest rdf:nil .</code></pre>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">주석 달기 💬</h2>
        <div class="prose prose-lg">
            <p>Turtle에서는 <code style="color: #1f2937;">#</code>을 사용하여 주석을 답니다.</p>

            <div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0;"><code style="color: #1f2937;"># 이것은 주석입니다
@prefix ex: &lt;http://example.org/&gt; .

# 저자 정보
ex:author001
    foaf:name "홍길동" ;  # 한글 이름
    foaf:age "30" .       # 나이</code></pre>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">정리하며 📚</h2>
        <div class="prose prose-lg">
            <div class="bg-blue-50 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">핵심 개념 정리</h3>
                <ul class="space-y-3">
                    <li>
                        <strong>Turtle은 사람이 읽기 쉬운 RDF 형식</strong>입니다
                        <br><small class="text-gray-600">XML/RDF보다 훨씬 간결하고 직관적</small>
                    </li>
                    <li>
                        <strong>@prefix로 URI를 간결하게</strong> 표현합니다
                        <br><small class="text-gray-600">긴 URI를 짧은 접두어로 대체</small>
                    </li>
                    <li>
                        <strong>세미콜론(;)으로 같은 주어 반복 제거</strong>
                        <br><small class="text-gray-600">쉼표(,)로 같은 술어에 여러 목적어 나열</small>
                    </li>
                    <li>
                        <strong>^^로 데이터 타입, @로 언어 태그 지정</strong>
                        <br><small class="text-gray-600">타입 안전성과 다국어 지원</small>
                    </li>
                    <li>
                        <strong>[]로 Blank Node, ()로 Collection 표현</strong>
                        <br><small class="text-gray-600">복잡한 구조도 간결하게 표현 가능</small>
                    </li>
                </ul>
            </div>

            <div class="mt-6 bg-green-50 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">다음 단계</h3>
                <p>
                    Turtle을 배웠다면, 다음으로 <strong>SPARQL</strong>로 Turtle 데이터를 쿼리하고,
                    <strong>RDF Schema</strong>나 <strong>OWL</strong>로 온톨로지를 설계해보세요!
                </p>
            </div>
        </div>
    </section>
</div>
"""

def update_turtle_content():
    """Turtle 콘텐츠 업데이트"""
    try:
        content = Content.objects.get(slug='turtle-rdf-serialization')

        content.content_html = turtle_content_html
        content.save()

        print("✓ Turtle 교육자료가 업데이트되었습니다!")
        print(f"  - 제목: {content.title}")
        print(f"  - URL: /contents/turtle-rdf-serialization")

    except Content.DoesNotExist:
        print("✗ Turtle 콘텐츠를 찾을 수 없습니다.")
    except Exception as e:
        print(f"✗ 오류 발생: {e}")

if __name__ == '__main__':
    update_turtle_content()
