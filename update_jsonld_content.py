#!/usr/bin/env python
"""JSON-LD 교육자료 업데이트 스크립트"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content

# JSON-LD 교육 콘텐츠
jsonld_content_html = """
<div class="space-y-8">
    <section>
        <h2 class="text-2xl font-bold mb-4">JSON-LD란 무엇인가요? 🌐</h2>
        <div class="prose prose-lg">
            <p>
                <strong>JSON-LD (JSON for Linking Data)</strong>는 JSON 형식으로 Linked Data를 표현하는
                웹 개발자 친화적인 RDF 직렬화 형식입니다.
            </p>
            <p>
                일반 JSON처럼 보이지만, <code style="color: #1f2937;">@context</code>, <code style="color: #1f2937;">@id</code>,
                <code style="color: #1f2937;">@type</code> 등의 키워드로 시맨틱 의미를 추가합니다.
            </p>

            <div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-4">
                <p class="font-semibold">💡 왜 JSON-LD를 배워야 할까요?</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>웹 개발자에게 가장 친숙한 JSON 형식 사용</li>
                    <li>기존 JSON API에 시맨틱 의미를 쉽게 추가 가능</li>
                    <li>Google, Microsoft 등이 구조화 데이터로 활용</li>
                    <li>SEO 향상에 도움 (Rich Results)</li>
                    <li>Schema.org와 완벽하게 호환</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">JSON-LD의 기본 구조 📝</h2>
        <div class="prose prose-lg">
            <h3 class="text-xl font-semibold mb-3">일반 JSON과 JSON-LD 비교</h3>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-4">
                <div>
                    <p class="text-sm font-semibold mb-2">일반 JSON</p>
                    <div style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.375rem;">
                        <pre class="text-sm"><code style="color: #1f2937;">{
  "name": "김철수",
  "age": 25,
  "email": "kim@example.org"
}</code></pre>
                    </div>
                    <p class="text-xs text-gray-600 mt-2">단순 데이터, 의미 없음</p>
                </div>

                <div>
                    <p class="text-sm font-semibold text-green-600 mb-2">✅ JSON-LD</p>
                    <div style="background-color: #f0fdf4; padding: 0.75rem; border-radius: 0.375rem;">
                        <pre class="text-sm"><code style="color: #1f2937;">{
  "@context": "http://schema.org",
  "@type": "Person",
  "name": "김철수",
  "age": 25,
  "email": "kim@example.org"
}</code></pre>
                    </div>
                    <p class="text-xs text-gray-600 mt-2">시맨틱 의미 추가됨</p>
                </div>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">핵심 키워드 🔑</h2>
        <div class="prose prose-lg">
            <div class="space-y-4">
                <div class="border rounded-lg p-4">
                    <h3 class="font-bold text-lg mb-2">1. @context - 문맥 정의</h3>
                    <p class="mb-2">용어의 의미를 정의하는 부분입니다.</p>
                    <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
                        <pre style="margin: 0;"><code style="color: #f9fafb; font-family: monospace;">{
  "@context": {
    "name": "http://schema.org/name",
    "email": "http://schema.org/email",
    "Person": "http://schema.org/Person"
  },
  "@type": "Person",
  "name": "김철수",
  "email": "kim@example.org"
}</code></pre>
                    </div>
                </div>

                <div class="border rounded-lg p-4">
                    <h3 class="font-bold text-lg mb-2">2. @id - 자원의 식별자</h3>
                    <p class="mb-2">자원을 고유하게 식별하는 URI입니다.</p>
                    <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
                        <pre style="margin: 0;"><code style="color: #f9fafb; font-family: monospace;">{
  "@context": "http://schema.org",
  "@id": "http://example.org/person/kim",
  "@type": "Person",
  "name": "김철수"
}</code></pre>
                    </div>
                </div>

                <div class="border rounded-lg p-4">
                    <h3 class="font-bold text-lg mb-2">3. @type - 자원의 타입</h3>
                    <p class="mb-2">자원이 어떤 종류인지 나타냅니다.</p>
                    <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
                        <pre style="margin: 0;"><code style="color: #f9fafb; font-family: monospace;">{
  "@context": "http://schema.org",
  "@type": "Book",
  "name": "어린왕자",
  "author": {
    "@type": "Person",
    "name": "생텍쥐페리"
  }
}</code></pre>
                    </div>
                </div>

                <div class="border rounded-lg p-4">
                    <h3 class="font-bold text-lg mb-2">4. @graph - 여러 자원 묶기</h3>
                    <p class="mb-2">여러 개의 독립적인 자원을 하나의 문서에 담습니다.</p>
                    <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
                        <pre style="margin: 0;"><code style="color: #f9fafb; font-family: monospace;">{
  "@context": "http://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "name": "김철수"
    },
    {
      "@type": "Person",
      "name": "이영희"
    }
  ]
}</code></pre>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">Schema.org와 함께 사용하기 🏗️</h2>
        <div class="prose prose-lg">
            <p>Google, Microsoft, Yahoo 등이 공동으로 만든 <strong>Schema.org</strong> 어휘를 사용하면
            검색 엔진이 내용을 더 잘 이해합니다.</p>

            <h3 class="text-xl font-semibold mb-3 mt-6">웹사이트에 구조화 데이터 추가하기</h3>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">&lt;script type="application/ld+json"&gt;
{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "어린왕자",
  "author": {
    "@type": "Person",
    "name": "생텍쥐페리"
  },
  "publisher": {
    "@type": "Organization",
    "name": "민음사"
  },
  "datePublished": "2015",
  "isbn": "978-8937460449",
  "bookFormat": "Paperback",
  "numberOfPages": 120,
  "inLanguage": "ko",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "1247"
  }
}
&lt;/script&gt;</code></pre>
            </div>

            <div class="bg-green-50 border-l-4 border-green-500 p-4 my-4">
                <p class="font-semibold">🎯 이렇게 하면 Google 검색 결과에서:</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>별점과 리뷰 수가 표시됩니다</li>
                    <li>저자, 출판사 정보가 표시됩니다</li>
                    <li>더 풍부한 검색 결과 (Rich Results) 제공</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">실전 예제: 도서관 장서 정보 📚</h2>
        <div class="prose prose-lg">
            <p>도서관 웹사이트에서 사용할 수 있는 JSON-LD 예제입니다.</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">{
  "@context": "https://schema.org",
  "@type": "Library",
  "name": "중앙도서관",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "세종대로 110",
    "addressLocality": "서울",
    "postalCode": "03172"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "장서 목록",
    "itemListElement": [
      {
        "@type": "Book",
        "@id": "http://library.example.org/book/001",
        "name": "어린왕자",
        "author": {
          "@type": "Person",
          "name": "생텍쥐페리"
        },
        "publisher": {
          "@type": "Organization",
          "name": "민음사"
        },
        "datePublished": "2015",
        "isbn": "978-8937460449",
        "bookEdition": "개정판",
        "numberOfPages": 120,
        "inLanguage": "ko",
        "genre": "아동문학",
        "offers": {
          "@type": "Offer",
          "availability": "https://schema.org/InStock",
          "price": "0",
          "priceCurrency": "KRW"
        }
      },
      {
        "@type": "Book",
        "@id": "http://library.example.org/book/002",
        "name": "데미안",
        "author": {
          "@type": "Person",
          "name": "헤르만 헤세"
        },
        "publisher": {
          "@type": "Organization",
          "name": "민음사"
        },
        "datePublished": "2018",
        "isbn": "978-8932917221",
        "inLanguage": "ko",
        "genre": "독일문학",
        "offers": {
          "@type": "Offer",
          "availability": "https://schema.org/OutOfStock"
        }
      }
    ]
  }
}</code></pre>
            </div>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">💡 이 예제의 특징</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>도서관 정보와 장서 목록을 계층적으로 표현</li>
                    <li>대출 가능 여부를 Schema.org의 <code style="color: #1f2937;">availability</code>로 표현</li>
                    <li>무료 대출이므로 가격을 0으로 설정</li>
                    <li>검색 엔진이 도서관 정보를 이해하고 인덱싱</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">고급 기능: @language와 다국어 지원 🌍</h2>
        <div class="prose prose-lg">
            <p>여러 언어로 된 콘텐츠를 표현할 수 있습니다.</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">{
  "@context": {
    "@vocab": "http://schema.org/",
    "@language": "ko"
  },
  "@type": "Book",
  "name": "어린왕자",
  "alternateName": {
    "@value": "The Little Prince",
    "@language": "en"
  },
  "description": "어린 왕자와 사막에서 만난 조종사의 이야기"
}</code></pre>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">JSON-LD vs 다른 RDF 형식 ⚖️</h2>
        <div class="prose prose-lg">
            <div class="bg-gradient-to-r from-purple-50 to-purple-100 border-2 border-purple-300 rounded-lg p-6 mb-6">
                <h3 class="font-bold text-xl mb-4">📊 형식 비교</h3>

                <table class="w-full border-collapse">
                    <thead>
                        <tr class="bg-purple-200">
                            <th class="border border-purple-300 p-2">형식</th>
                            <th class="border border-purple-300 p-2">장점</th>
                            <th class="border border-purple-300 p-2">단점</th>
                            <th class="border border-purple-300 p-2">주요 사용처</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="border border-purple-300 p-2 font-semibold">JSON-LD</td>
                            <td class="border border-purple-300 p-2">웹 개발자 친화적, API 통합 쉬움</td>
                            <td class="border border-purple-300 p-2">파일 크기 큼</td>
                            <td class="border border-purple-300 p-2">웹 API, SEO, 구조화 데이터</td>
                        </tr>
                        <tr class="bg-purple-50">
                            <td class="border border-purple-300 p-2 font-semibold">Turtle</td>
                            <td class="border border-purple-300 p-2">사람이 읽기 쉬움, 간결</td>
                            <td class="border border-purple-300 p-2">프로그래머에게 낯섦</td>
                            <td class="border border-purple-300 p-2">온톨로지 작성, 데이터 편집</td>
                        </tr>
                        <tr>
                            <td class="border border-purple-300 p-2 font-semibold">RDF/XML</td>
                            <td class="border border-purple-300 p-2">XML 도구 활용 가능</td>
                            <td class="border border-purple-300 p-2">장황하고 복잡함</td>
                            <td class="border border-purple-300 p-2">레거시 시스템</td>
                        </tr>
                        <tr class="bg-purple-50">
                            <td class="border border-purple-300 p-2 font-semibold">N-Triples</td>
                            <td class="border border-purple-300 p-2">파싱 단순, 스트리밍 처리</td>
                            <td class="border border-purple-300 p-2">중복 많음, 파일 큼</td>
                            <td class="border border-purple-300 p-2">대용량 데이터 처리</td>
                        </tr>
                    </tbody>
                </table>
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
                        <strong>JSON-LD는 JSON 형식의 Linked Data</strong>
                        <br><small class="text-gray-600">웹 개발자가 가장 쉽게 접근할 수 있는 RDF 형식</small>
                    </li>
                    <li>
                        <strong>@context로 용어의 의미를 정의</strong>
                        <br><small class="text-gray-600">일반 JSON에 시맨틱 의미 추가</small>
                    </li>
                    <li>
                        <strong>@id로 자원을 식별, @type으로 타입 지정</strong>
                        <br><small class="text-gray-600">Linked Data의 핵심 원칙 준수</small>
                    </li>
                    <li>
                        <strong>Schema.org와 함께 사용하면 SEO 효과</strong>
                        <br><small class="text-gray-600">Google Rich Results, 구조화 데이터</small>
                    </li>
                    <li>
                        <strong>웹 API에 쉽게 통합 가능</strong>
                        <br><small class="text-gray-600">JavaScript로 직접 파싱 가능</small>
                    </li>
                </ul>
            </div>

            <div class="mt-6 bg-green-50 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">다음 단계</h3>
                <p>
                    JSON-LD를 배웠다면, 다음으로 <strong>JSON-LD Playground</strong>에서 실습하고,
                    <strong>Google Structured Data Testing Tool</strong>로 검증해보세요!
                </p>
                <p class="mt-2">
                    또한 <strong>SPARQL</strong>로 JSON-LD 데이터를 쿼리하는 방법도 배워보세요.
                </p>
            </div>
        </div>
    </section>
</div>
"""

def update_jsonld_content():
    """JSON-LD 콘텐츠 업데이트"""
    try:
        content = Content.objects.get(slug='jsonld-rdf-for-web-developers')

        content.content_html = jsonld_content_html
        content.save()

        print("✓ JSON-LD 교육자료가 업데이트되었습니다!")
        print(f"  - 제목: {content.title}")
        print(f"  - URL: /contents/jsonld-rdf-for-web-developers")

    except Content.DoesNotExist:
        print("✗ JSON-LD 콘텐츠를 찾을 수 없습니다.")
    except Exception as e:
        print(f"✗ 오류 발생: {e}")

if __name__ == '__main__':
    update_jsonld_content()
