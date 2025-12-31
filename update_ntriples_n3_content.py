#!/usr/bin/env python
"""N-Triples/N3 교육자료 업데이트 스크립트"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content

# N-Triples/N3 교육 콘텐츠
ntriples_n3_content_html = """
<div class="space-y-8">
    <section>
        <h2 class="text-2xl font-bold mb-4">N-Triples와 N3 소개 📋</h2>
        <div class="prose prose-lg">
            <p>
                <strong>N-Triples</strong>와 <strong>N3 (Notation3)</strong>는 두 가지 RDF 직렬화 형식입니다.
                N-Triples는 가장 단순하고, N3는 가장 강력한 형식입니다.
            </p>

            <div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-4">
                <p class="font-semibold">💡 두 형식의 관계</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li><strong>N-Triples</strong>: 가장 단순한 형식, 한 줄에 하나의 트리플</li>
                    <li><strong>N3</strong>: Turtle의 전신, 변수와 추론 규칙 지원</li>
                    <li>N-Triples ⊂ Turtle ⊂ N3 (포함 관계)</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">N-Triples: 단순함의 극치 🔹</h2>
        <div class="prose prose-lg">
            <h3 class="text-xl font-semibold mb-3">특징</h3>
            <ul class="list-disc pl-6 space-y-2">
                <li>한 줄에 정확히 하나의 트리플</li>
                <li>축약 문법 없음 (prefix, 세미콜론 등 사용 불가)</li>
                <li>파싱이 매우 빠르고 단순</li>
                <li>스트리밍 처리에 최적화</li>
                <li>대용량 데이터 처리에 적합</li>
            </ul>

            <h3 class="text-xl font-semibold mb-3 mt-6">기본 문법</h3>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">&lt;http://example.org/person/kim&gt; &lt;http://xmlns.com/foaf/0.1/name&gt; "김철수" .
&lt;http://example.org/person/kim&gt; &lt;http://xmlns.com/foaf/0.1/age&gt; "25"^^&lt;http://www.w3.org/2001/XMLSchema#integer&gt; .
&lt;http://example.org/person/kim&gt; &lt;http://xmlns.com/foaf/0.1/knows&gt; &lt;http://example.org/person/lee&gt; .</code></pre>
            </div>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">⚠️ 주의사항</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>모든 URI는 &lt;&gt;로 감싸야 합니다</li>
                    <li>문자열은 ""로 감싸야 합니다</li>
                    <li>각 트리플은 . (마침표)로 끝나야 합니다</li>
                    <li>주석은 # 로 시작합니다</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">N-Triples 예제 📝</h2>
        <div class="prose prose-lg">
            <h3 class="text-xl font-semibold mb-3">도서 정보 표현</h3>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;"># 도서 정보
&lt;http://example.org/book/001&gt; &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#type&gt; &lt;http://purl.org/ontology/bibo/Book&gt; .
&lt;http://example.org/book/001&gt; &lt;http://purl.org/dc/elements/1.1/title&gt; "어린왕자"@ko .
&lt;http://example.org/book/001&gt; &lt;http://purl.org/dc/elements/1.1/title&gt; "The Little Prince"@en .
&lt;http://example.org/book/001&gt; &lt;http://purl.org/dc/elements/1.1/creator&gt; "생텍쥐페리" .
&lt;http://example.org/book/001&gt; &lt;http://purl.org/dc/elements/1.1/publisher&gt; "민음사" .
&lt;http://example.org/book/001&gt; &lt;http://purl.org/ontology/bibo/isbn&gt; "978-8937460449" .</code></pre>
            </div>

            <div class="bg-green-50 border-l-4 border-green-500 p-4 my-4">
                <p class="font-semibold">✅ N-Triples의 장점</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>파싱 로직이 매우 단순 (정규식으로 충분)</li>
                    <li>줄 단위 처리로 메모리 효율적</li>
                    <li>병렬 처리 가능</li>
                    <li>오류 발생 시 해당 줄만 건너뛰면 됨</li>
                    <li>대규모 데이터 덤프에 적합</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">N-Quads: N-Triples + 그래프 🔷</h2>
        <div class="prose prose-lg">
            <p><strong>N-Quads</strong>는 N-Triples에 네 번째 요소(그래프 이름)를 추가한 형식입니다.</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;"># 주어 술어 목적어 그래프
&lt;http://example.org/person/kim&gt; &lt;http://xmlns.com/foaf/0.1/name&gt; "김철수" &lt;http://example.org/graph/users&gt; .
&lt;http://example.org/person/lee&gt; &lt;http://xmlns.com/foaf/0.1/name&gt; "이영희" &lt;http://example.org/graph/users&gt; .
&lt;http://example.org/book/001&gt; &lt;http://purl.org/dc/elements/1.1/title&gt; "어린왕자" &lt;http://example.org/graph/books&gt; .</code></pre>
            </div>

            <p class="mt-4">네 번째 요소로 데이터 출처나 컨텍스트를 구분할 수 있습니다.</p>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">N3: 강력함의 극치 💪</h2>
        <div class="prose prose-lg">
            <h3 class="text-xl font-semibold mb-3">N3의 특징</h3>
            <ul class="list-disc pl-6 space-y-2">
                <li>Turtle의 모든 기능 포함</li>
                <li><strong>변수</strong> 사용 가능 (<code style="color: #1f2937;">?변수명</code>)</li>
                <li><strong>추론 규칙</strong> 표현 가능 (<code style="color: #1f2937;">=&gt;</code>)</li>
                <li><strong>부정</strong> 표현 가능</li>
                <li><strong>경로 표현식</strong> 지원</li>
                <li>Tim Berners-Lee가 고안</li>
            </ul>

            <h3 class="text-xl font-semibold mb-3 mt-6">기본 문법 (Turtle과 동일)</h3>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">@prefix ex: &lt;http://example.org/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .

ex:kim a foaf:Person ;
    foaf:name "김철수" ;
    foaf:age 25 ;
    foaf:knows ex:lee .</code></pre>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">N3의 고급 기능: 추론 규칙 🧠</h2>
        <div class="prose prose-lg">
            <p>N3의 가장 강력한 기능은 <strong>추론 규칙</strong>을 표현할 수 있다는 것입니다.</p>

            <h3 class="text-xl font-semibold mb-3 mt-4">1. 변수 사용</h3>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">@prefix ex: &lt;http://example.org/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .

# 규칙: X가 Y를 알면, Y도 X를 안다
{ ?X foaf:knows ?Y } =&gt; { ?Y foaf:knows ?X } .</code></pre>
            </div>

            <h3 class="text-xl font-semibold mb-3 mt-6">2. 복잡한 추론 예제</h3>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">@prefix ex: &lt;http://example.org/&gt; .
@prefix foaf: &lt;http://xmlns.com/foaf/0.1/&gt; .

# 데이터
ex:kim foaf:knows ex:lee .
ex:lee foaf:knows ex:park .

# 규칙 1: 친구의 친구는 지인이다
{ ?X foaf:knows ?Y . ?Y foaf:knows ?Z }
=&gt;
{ ?X ex:acquaintance ?Z } .

# 규칙 2: 20세 이상은 성인이다
{ ?X foaf:age ?age . ?age &gt;= 20 }
=&gt;
{ ?X a ex:Adult } .</code></pre>
            </div>

            <div class="bg-purple-50 border-l-4 border-purple-500 p-4 my-4">
                <p class="font-semibold">🧠 추론 엔진</p>
                <p class="mt-2">N3 규칙을 처리하려면 특별한 추론 엔진이 필요합니다:</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li><strong>cwm</strong> (Closed World Machine) - Python</li>
                    <li><strong>EYE</strong> (Euler Yet another proof Engine) - Prolog</li>
                    <li><strong>Jena Rules</strong> - Java</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">N3 실전 예제: 도서관 규칙 📚</h2>
        <div class="prose prose-lg">
            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">@prefix ex: &lt;http://example.org/library/&gt; .
@prefix bibo: &lt;http://purl.org/ontology/bibo/&gt; .
@prefix xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt; .

# 데이터
ex:member001 ex:age "15"^^xsd:integer .
ex:member002 ex:age "25"^^xsd:integer .
ex:book001 ex:ageRating "18"^^xsd:integer .

# 규칙 1: 나이가 도서 등급 이상이면 대출 가능
{ ?member ex:age ?memberAge .
  ?book ex:ageRating ?bookRating .
  ?memberAge &gt;= ?bookRating }
=&gt;
{ ?member ex:canBorrow ?book } .

# 규칙 2: 3권 이상 대출 중이면 대출 불가
{ ?member ex:borrowed ?count .
  ?count &gt;= 3 }
=&gt;
{ ?member ex:borrowingBlocked "true"^^xsd:boolean } .

# 규칙 3: 연체 중이면 대출 불가
{ ?member ex:hasOverdueBook "true"^^xsd:boolean }
=&gt;
{ ?member ex:borrowingBlocked "true"^^xsd:boolean } .</code></pre>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">형식 비교 ⚖️</h2>
        <div class="prose prose-lg">
            <div class="bg-gradient-to-r from-blue-50 to-blue-100 border-2 border-blue-300 rounded-lg p-6 mb-6">
                <h3 class="font-bold text-xl mb-4">📊 N-Triples vs Turtle vs N3</h3>

                <table class="w-full border-collapse">
                    <thead>
                        <tr class="bg-blue-200">
                            <th class="border border-blue-300 p-2">기능</th>
                            <th class="border border-blue-300 p-2">N-Triples</th>
                            <th class="border border-blue-300 p-2">Turtle</th>
                            <th class="border border-blue-300 p-2">N3</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="border border-blue-300 p-2 font-semibold">Prefix</td>
                            <td class="border border-blue-300 p-2">✗</td>
                            <td class="border border-blue-300 p-2">✓</td>
                            <td class="border border-blue-300 p-2">✓</td>
                        </tr>
                        <tr class="bg-blue-50">
                            <td class="border border-blue-300 p-2 font-semibold">세미콜론 축약</td>
                            <td class="border border-blue-300 p-2">✗</td>
                            <td class="border border-blue-300 p-2">✓</td>
                            <td class="border border-blue-300 p-2">✓</td>
                        </tr>
                        <tr>
                            <td class="border border-blue-300 p-2 font-semibold">Blank Node</td>
                            <td class="border border-blue-300 p-2">_:label</td>
                            <td class="border border-blue-300 p-2">_:label, []</td>
                            <td class="border border-blue-300 p-2">_:label, []</td>
                        </tr>
                        <tr class="bg-blue-50">
                            <td class="border border-blue-300 p-2 font-semibold">Collection</td>
                            <td class="border border-blue-300 p-2">✗</td>
                            <td class="border border-blue-300 p-2">✓ ()</td>
                            <td class="border border-blue-300 p-2">✓ ()</td>
                        </tr>
                        <tr>
                            <td class="border border-blue-300 p-2 font-semibold">변수</td>
                            <td class="border border-blue-300 p-2">✗</td>
                            <td class="border border-blue-300 p-2">✗</td>
                            <td class="border border-blue-300 p-2">✓ ?var</td>
                        </tr>
                        <tr class="bg-blue-50">
                            <td class="border border-blue-300 p-2 font-semibold">추론 규칙</td>
                            <td class="border border-blue-300 p-2">✗</td>
                            <td class="border border-blue-300 p-2">✗</td>
                            <td class="border border-blue-300 p-2">✓ =&gt;</td>
                        </tr>
                        <tr>
                            <td class="border border-blue-300 p-2 font-semibold">파싱 속도</td>
                            <td class="border border-blue-300 p-2">매우 빠름</td>
                            <td class="border border-blue-300 p-2">보통</td>
                            <td class="border border-blue-300 p-2">느림</td>
                        </tr>
                        <tr class="bg-blue-50">
                            <td class="border border-blue-300 p-2 font-semibold">사용 난이도</td>
                            <td class="border border-blue-300 p-2">매우 쉬움</td>
                            <td class="border border-blue-300 p-2">쉬움</td>
                            <td class="border border-blue-300 p-2">어려움</td>
                        </tr>
                        <tr>
                            <td class="border border-blue-300 p-2 font-semibold">주요 용도</td>
                            <td class="border border-blue-300 p-2">대용량 데이터</td>
                            <td class="border border-blue-300 p-2">일반 RDF</td>
                            <td class="border border-blue-300 p-2">추론, 규칙</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">언제 어떤 형식을 쓸까? 🤔</h2>
        <div class="prose prose-lg">
            <div class="space-y-4">
                <div class="border-2 border-green-300 rounded-lg p-4 bg-green-50">
                    <h3 class="font-bold text-lg mb-2 text-green-700">N-Triples를 사용하세요</h3>
                    <ul class="list-disc pl-6 space-y-1">
                        <li>DBpedia, Wikidata 같은 대용량 데이터 덤프</li>
                        <li>스트리밍 처리가 필요한 경우</li>
                        <li>파싱 속도가 중요한 경우</li>
                        <li>단순하고 안정적인 처리가 필요한 경우</li>
                    </ul>
                </div>

                <div class="border-2 border-blue-300 rounded-lg p-4 bg-blue-50">
                    <h3 class="font-bold text-lg mb-2 text-blue-700">Turtle을 사용하세요</h3>
                    <ul class="list-disc pl-6 space-y-1">
                        <li>사람이 직접 작성하고 읽어야 하는 경우</li>
                        <li>온톨로지나 스키마 정의</li>
                        <li>중간 크기의 RDF 데이터</li>
                        <li>대부분의 일반적인 경우</li>
                    </ul>
                </div>

                <div class="border-2 border-purple-300 rounded-lg p-4 bg-purple-50">
                    <h3 class="font-bold text-lg mb-2 text-purple-700">N3를 사용하세요</h3>
                    <ul class="list-disc pl-6 space-y-1">
                        <li>추론 규칙을 표현해야 하는 경우</li>
                        <li>복잡한 논리 규칙이 필요한 경우</li>
                        <li>연구나 실험적인 프로젝트</li>
                        <li>Tim Berners-Lee 팬이라면!</li>
                    </ul>
                </div>
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
                        <strong>N-Triples는 가장 단순한 RDF 형식</strong>
                        <br><small class="text-gray-600">한 줄에 하나의 트리플, 대용량 데이터 처리 최적화</small>
                    </li>
                    <li>
                        <strong>N-Quads는 N-Triples + 그래프 이름</strong>
                        <br><small class="text-gray-600">데이터 출처와 컨텍스트 구분 가능</small>
                    </li>
                    <li>
                        <strong>N3는 Turtle + 추론 기능</strong>
                        <br><small class="text-gray-600">변수, 규칙, 논리 표현 가능</small>
                    </li>
                    <li>
                        <strong>포함 관계: N-Triples ⊂ Turtle ⊂ N3</strong>
                        <br><small class="text-gray-600">상위 형식은 하위 형식 포함</small>
                    </li>
                    <li>
                        <strong>용도에 맞는 형식 선택이 중요</strong>
                        <br><small class="text-gray-600">성능 vs 편의성 vs 표현력의 트레이드오프</small>
                    </li>
                </ul>
            </div>

            <div class="mt-6 bg-green-50 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">다음 단계</h3>
                <p>
                    N-Triples/N3를 배웠다면, 다음으로 <strong>Apache Jena</strong>나 <strong>rdflib</strong>로
                    실제 대용량 RDF 데이터를 처리해보세요!
                </p>
                <p class="mt-2">
                    N3 추론에 관심이 있다면 <strong>cwm</strong>이나 <strong>EYE</strong> 추론 엔진을 사용해보세요.
                </p>
            </div>
        </div>
    </section>
</div>
"""

def update_ntriples_n3_content():
    """N-Triples/N3 콘텐츠 업데이트"""
    try:
        content = Content.objects.get(slug='ntriples-n3-simplicity-and-power')

        content.content_html = ntriples_n3_content_html
        content.save()

        print("✓ N-Triples/N3 교육자료가 업데이트되었습니다!")
        print(f"  - 제목: {content.title}")
        print(f"  - URL: /contents/ntriples-n3-simplicity-and-power")

    except Content.DoesNotExist:
        print("✗ N-Triples/N3 콘텐츠를 찾을 수 없습니다.")
    except Exception as e:
        print(f"✗ 오류 발생: {e}")

if __name__ == '__main__':
    update_ntriples_n3_content()
