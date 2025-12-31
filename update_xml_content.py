#!/usr/bin/env python
"""XML 교육자료 업데이트 스크립트"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content

# XML 교육 콘텐츠
xml_content_html = """
<div class="space-y-8">
    <section>
        <h2 class="text-2xl font-bold mb-4">XML이란 무엇인가요? 📋</h2>
        <div class="prose prose-lg">
            <p>
                <strong>XML (eXtensible Markup Language)</strong>은 데이터를 저장하고 전달하기 위한 마크업 언어입니다.
                HTML이 "어떻게 보일지"를 정의한다면, XML은 "무엇인지"를 정의합니다.
            </p>
            <p>
                쉽게 말해서, XML은 <strong>데이터를 담는 상자에 라벨을 붙이는 방법</strong>입니다.
                예를 들어 도서관에서 책을 분류할 때 "제목", "저자", "출판사" 같은 라벨을 붙이는 것과 같습니다.
            </p>

            <div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-4">
                <p class="font-semibold">💡 왜 XML을 배워야 할까요?</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>도서관 시스템에서 책 정보를 주고받을 때 사용됩니다 (MARC XML 등)</li>
                    <li>웹사이트끼리 데이터를 교환할 때 사용됩니다</li>
                    <li>설정 파일이나 문서를 구조화해서 저장할 때 사용됩니다</li>
                    <li>다양한 시스템 간에 데이터를 표준화된 방법으로 공유할 수 있습니다</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">HTML과 XML의 차이점 🤔</h2>

        <div class="bg-purple-50 border-2 border-purple-300 rounded-lg p-6 mb-6">
            <h3 class="font-bold text-xl mb-4">📊 목적의 차이</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <h4 class="font-semibold text-lg mb-2 text-blue-600">HTML의 목적</h4>
                    <p class="mb-2">웹 브라우저에서 <strong>"어떻게 보여줄지"</strong>를 정의합니다.</p>
                    <div class="bg-white p-3 rounded text-sm">
                        <p class="font-mono text-gray-800">&lt;h1&gt;제목&lt;/h1&gt;</p>
                        <p class="text-xs text-gray-600 mt-1">→ "이것을 크게 표시하세요"</p>
                    </div>
                </div>
                <div>
                    <h4 class="font-semibold text-lg mb-2 text-green-600">XML의 목적</h4>
                    <p class="mb-2">데이터가 <strong>"무엇인지"</strong>를 정의합니다.</p>
                    <div class="bg-white p-3 rounded text-sm">
                        <p class="font-mono text-gray-800">&lt;도서제목&gt;어린왕자&lt;/도서제목&gt;</p>
                        <p class="text-xs text-gray-600 mt-1">→ "이것은 도서 제목입니다"</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div class="border-2 border-blue-200 rounded-lg p-4 bg-blue-50">
                <h3 class="font-bold text-lg mb-3">HTML</h3>
                <ul class="space-y-2 text-sm">
                    <li>✓ <strong>목적:</strong> 데이터를 "표시"하기 위함</li>
                    <li>✓ <strong>태그:</strong> 미리 정해진 태그만 사용 (h1, p, div 등)</li>
                    <li>✓ <strong>초점:</strong> 어떻게 보이는가</li>
                    <li>✓ <strong>문법:</strong> 비교적 유연함 (태그 안 닫아도 동작)</li>
                    <li>✓ <strong>예시:</strong> 웹 페이지, 블로그</li>
                </ul>
            </div>

            <div class="border-2 border-green-200 rounded-lg p-4 bg-green-50">
                <h3 class="font-bold text-lg mb-3">XML</h3>
                <ul class="space-y-2 text-sm">
                    <li>✓ <strong>목적:</strong> 데이터를 "저장/전달"하기 위함</li>
                    <li>✓ <strong>태그:</strong> 원하는 태그를 직접 만들 수 있음</li>
                    <li>✓ <strong>초점:</strong> 무엇인가 (데이터의 의미)</li>
                    <li>✓ <strong>문법:</strong> 엄격함 (모든 태그 반드시 닫아야 함)</li>
                    <li>✓ <strong>예시:</strong> 설정 파일, 데이터 교환, API</li>
                </ul>
            </div>
        </div>

        <div class="bg-gradient-to-r from-amber-50 to-amber-100 border-2 border-amber-300 rounded-lg p-6">
            <h3 class="font-bold text-xl mb-4">🎯 실제 사용 예시로 비교하기</h3>

            <div class="space-y-4">
                <div>
                    <p class="font-semibold mb-2">같은 정보를 표현하는 방법:</p>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <p class="text-sm font-semibold text-blue-600 mb-2">HTML - 보여주기용</p>
                            <div class="bg-white p-3 rounded">
                                <pre class="text-sm"><code style="color: #1f2937;">&lt;div class="book"&gt;
  &lt;h2&gt;어린왕자&lt;/h2&gt;
  &lt;p&gt;저자: 생텍쥐페리&lt;/p&gt;
  &lt;p&gt;가격: 10,000원&lt;/p&gt;
&lt;/div&gt;</code></pre>
                            </div>
                            <p class="text-xs text-gray-600 mt-2">→ 브라우저에서 예쁘게 표시됨</p>
                        </div>

                        <div>
                            <p class="text-sm font-semibold text-green-600 mb-2">XML - 데이터 저장용</p>
                            <div class="bg-white p-3 rounded">
                                <pre class="text-sm"><code style="color: #1f2937;">&lt;도서&gt;
  &lt;제목&gt;어린왕자&lt;/제목&gt;
  &lt;저자&gt;생텍쥐페리&lt;/저자&gt;
  &lt;가격&gt;10000&lt;/가격&gt;
&lt;/도서&gt;</code></pre>
                            </div>
                            <p class="text-xs text-gray-600 mt-2">→ 프로그램이 읽고 처리함</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">XML의 장점과 단점 ⚖️</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="border-2 border-green-300 rounded-lg p-5 bg-green-50">
                <h3 class="font-bold text-xl mb-4 text-green-700">✅ 장점</h3>
                <ul class="space-y-3">
                    <li>
                        <strong class="text-green-600">1. 사람이 읽기 쉽다</strong>
                        <p class="text-sm text-gray-700 ml-4">태그 이름만 봐도 무슨 데이터인지 알 수 있습니다</p>
                    </li>
                    <li>
                        <strong class="text-green-600">2. 플랫폼 독립적</strong>
                        <p class="text-sm text-gray-700 ml-4">Windows, Mac, Linux 어디서나 사용 가능합니다</p>
                    </li>
                    <li>
                        <strong class="text-green-600">3. 확장성이 좋다</strong>
                        <p class="text-sm text-gray-700 ml-4">필요한 태그를 자유롭게 추가할 수 있습니다</p>
                    </li>
                    <li>
                        <strong class="text-green-600">4. 계층 구조 표현</strong>
                        <p class="text-sm text-gray-700 ml-4">복잡한 데이터 관계를 명확하게 표현 가능합니다</p>
                    </li>
                    <li>
                        <strong class="text-green-600">5. 표준화</strong>
                        <p class="text-sm text-gray-700 ml-4">W3C 표준으로 많은 도구와 라이브러리 지원</p>
                    </li>
                    <li>
                        <strong class="text-green-600">6. 자기 설명적</strong>
                        <p class="text-sm text-gray-700 ml-4">별도 설명서 없이도 데이터 구조를 이해할 수 있습니다</p>
                    </li>
                </ul>
            </div>

            <div class="border-2 border-red-300 rounded-lg p-5 bg-red-50">
                <h3 class="font-bold text-xl mb-4 text-red-700">❌ 단점</h3>
                <ul class="space-y-3">
                    <li>
                        <strong class="text-red-600">1. 용량이 크다</strong>
                        <p class="text-sm text-gray-700 ml-4">태그 때문에 같은 데이터라도 파일 크기가 큽니다</p>
                    </li>
                    <li>
                        <strong class="text-red-600">2. 처리 속도가 느리다</strong>
                        <p class="text-sm text-gray-700 ml-4">파싱(분석)하는 데 시간과 자원이 필요합니다</p>
                    </li>
                    <li>
                        <strong class="text-red-600">3. 문법이 엄격하다</strong>
                        <p class="text-sm text-gray-700 ml-4">작은 실수 하나로도 전체 문서가 오류 발생</p>
                    </li>
                    <li>
                        <strong class="text-red-600">4. 중복이 많다</strong>
                        <p class="text-sm text-gray-700 ml-4">여는 태그와 닫는 태그가 중복됩니다</p>
                    </li>
                    <li>
                        <strong class="text-red-600">5. 배열 표현이 불편</strong>
                        <p class="text-sm text-gray-700 ml-4">같은 항목을 반복할 때 태그를 계속 써야 합니다</p>
                    </li>
                </ul>
            </div>
        </div>

        <div class="bg-blue-50 border-l-4 border-blue-500 p-4 mt-6">
            <p class="font-semibold">💡 그래서 언제 XML을 쓰나요?</p>
            <ul class="list-disc pl-6 mt-2 space-y-1 text-sm">
                <li><strong>데이터 교환:</strong> 서로 다른 시스템 간 데이터를 주고받을 때</li>
                <li><strong>설정 파일:</strong> 프로그램 설정을 저장할 때 (가독성 중요)</li>
                <li><strong>문서 저장:</strong> 복잡한 구조의 문서를 저장할 때 (DOCX, XLSX 등)</li>
                <li><strong>API 통신:</strong> 웹 서비스 간 통신 (요즘은 JSON도 많이 씀)</li>
                <li><strong>표준 준수:</strong> 업계 표준을 따라야 할 때 (도서관 MARC, RSS 등)</li>
            </ul>
            <p class="mt-3 text-sm">
                <strong>참고:</strong> 요즘은 JSON이 더 많이 쓰이지만,
                도서관·출판·정부 시스템에서는 아직 XML을 많이 사용합니다!
            </p>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">XML의 기본 문법 📝</h2>
        <div class="prose prose-lg">
            <p>XML도 HTML처럼 태그를 사용하지만, 태그 이름을 직접 정할 수 있습니다!</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;도서&gt;
    &lt;제목&gt;어린왕자&lt;/제목&gt;
    &lt;저자&gt;생텍쥐페리&lt;/저자&gt;
    &lt;출판사&gt;민음사&lt;/출판사&gt;
    &lt;가격&gt;10000&lt;/가격&gt;
&lt;/도서&gt;</code></pre>
            </div>

            <p>위 예제를 분해해보면:</p>
            <ul class="list-disc pl-6 space-y-2">
                <li>
                    <code style="color: #1f2937;">&lt;?xml version="1.0" encoding="UTF-8"?&gt;</code> -
                    <strong>XML 선언</strong>: "이 문서는 XML 문서입니다"라고 알리는 첫 줄
                </li>
                <li>
                    <code style="color: #1f2937;">&lt;도서&gt;...&lt;/도서&gt;</code> -
                    <strong>루트 요소</strong>: 모든 내용을 감싸는 최상위 요소 (반드시 하나만!)
                </li>
                <li>
                    <code style="color: #1f2937;">&lt;제목&gt;, &lt;저자&gt;</code> 등 -
                    <strong>자식 요소</strong>: 실제 데이터를 담는 요소들
                </li>
            </ul>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">XML 문법 규칙 📏</h2>
        <div class="space-y-4">
            <div class="border rounded-lg p-4">
                <h3 class="font-bold text-lg mb-2">1. 모든 태그는 닫혀야 합니다</h3>
                <div class="grid grid-cols-2 gap-4 mt-2">
                    <div>
                        <p class="text-sm font-semibold text-green-600 mb-1">✓ 올바른 예</p>
                        <div class="bg-green-50 p-2 rounded text-sm">
                            <code style="color: #1f2937;">&lt;이름&gt;홍길동&lt;/이름&gt;</code>
                        </div>
                    </div>
                    <div>
                        <p class="text-sm font-semibold text-red-600 mb-1">✗ 잘못된 예</p>
                        <div class="bg-red-50 p-2 rounded text-sm">
                            <code style="color: #1f2937;">&lt;이름&gt;홍길동</code>
                        </div>
                    </div>
                </div>
            </div>

            <div class="border rounded-lg p-4">
                <h3 class="font-bold text-lg mb-2">2. 태그는 대소문자를 구분합니다</h3>
                <div class="bg-yellow-50 p-3 rounded">
                    <p class="text-sm mb-2"><code style="color: #1f2937;">&lt;도서&gt;</code>와 <code style="color: #1f2937;">&lt;Doso&gt;</code>는 <strong>완전히 다른</strong> 태그입니다!</p>
                    <p class="text-sm">보통은 소문자나 한글을 사용합니다.</p>
                </div>
            </div>

            <div class="border rounded-lg p-4">
                <h3 class="font-bold text-lg mb-2">3. 태그는 제대로 중첩되어야 합니다</h3>
                <div class="grid grid-cols-2 gap-4 mt-2">
                    <div>
                        <p class="text-sm font-semibold text-green-600 mb-1">✓ 올바른 예</p>
                        <div class="bg-green-50 p-2 rounded text-sm">
                            <code style="color: #1f2937;">&lt;책&gt;&lt;제목&gt;어린왕자&lt;/제목&gt;&lt;/책&gt;</code>
                        </div>
                    </div>
                    <div>
                        <p class="text-sm font-semibold text-red-600 mb-1">✗ 잘못된 예</p>
                        <div class="bg-red-50 p-2 rounded text-sm">
                            <code style="color: #1f2937;">&lt;책&gt;&lt;제목&gt;어린왕자&lt;/책&gt;&lt;/제목&gt;</code>
                        </div>
                    </div>
                </div>
            </div>

            <div class="border rounded-lg p-4">
                <h3 class="font-bold text-lg mb-2">4. 반드시 하나의 루트 요소가 있어야 합니다</h3>
                <div class="grid grid-cols-2 gap-4 mt-2">
                    <div>
                        <p class="text-sm font-semibold text-green-600 mb-1">✓ 올바른 예</p>
                        <div class="bg-green-50 p-2 rounded text-sm">
                            <pre style="margin: 0; overflow-x: auto;"><code style="color: #1f2937; font-family: monospace;">&lt;도서관&gt;
  &lt;책&gt;어린왕자&lt;/책&gt;
  &lt;책&gt;해리포터&lt;/책&gt;
&lt;/도서관&gt;</code></pre>
                        </div>
                    </div>
                    <div>
                        <p class="text-sm font-semibold text-red-600 mb-1">✗ 잘못된 예</p>
                        <div class="bg-red-50 p-2 rounded text-sm">
                            <pre style="margin: 0; overflow-x: auto;"><code style="color: #1f2937; font-family: monospace;">&lt;책&gt;어린왕자&lt;/책&gt;
&lt;책&gt;해리포터&lt;/책&gt;</code></pre>
                            <p class="text-xs mt-1">루트 요소가 2개!</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="border rounded-lg p-4">
                <h3 class="font-bold text-lg mb-2">5. 속성 값은 반드시 따옴표로 감싸야 합니다</h3>
                <div class="grid grid-cols-2 gap-4 mt-2">
                    <div>
                        <p class="text-sm font-semibold text-green-600 mb-1">✓ 올바른 예</p>
                        <div class="bg-green-50 p-2 rounded text-sm">
                            <code style="color: #1f2937;">&lt;책 isbn="978-1234567890"&gt;</code>
                        </div>
                    </div>
                    <div>
                        <p class="text-sm font-semibold text-red-600 mb-1">✗ 잘못된 예</p>
                        <div class="bg-red-50 p-2 rounded text-sm">
                            <code style="color: #1f2937;">&lt;책 isbn=978-1234567890&gt;</code>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">Well-formed vs Valid XML 🎯</h2>
        <div class="prose prose-lg">
            <p class="text-lg font-semibold mb-4">
                이것이 가장 중요한 개념입니다! 두 가지를 확실히 구분해야 합니다.
            </p>

            <div class="bg-gradient-to-r from-blue-50 to-blue-100 border-2 border-blue-300 rounded-lg p-6 mb-6">
                <h3 class="font-bold text-xl mb-3">📐 Well-formed XML (형식이 올바른 XML)</h3>
                <p class="mb-3">
                    <strong>"문법 규칙을 지킨 XML"</strong>이라는 뜻입니다.
                </p>
                <p class="mb-3">위에서 배운 5가지 규칙만 지키면 Well-formed XML입니다:</p>
                <ul class="list-disc pl-6 space-y-1">
                    <li>모든 태그가 닫혀있다</li>
                    <li>태그가 제대로 중첩되어 있다</li>
                    <li>루트 요소가 하나다</li>
                    <li>속성 값이 따옴표로 감싸져 있다</li>
                </ul>

                <div class="bg-white p-4 rounded mt-4">
                    <p class="text-sm font-semibold mb-2">예시: Well-formed XML</p>
                    <pre style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem; font-size: 0.875rem; margin: 0;"><code style="color: #1f2937;">&lt;?xml version="1.0"?&gt;
&lt;사람&gt;
    &lt;이름&gt;김철수&lt;/이름&gt;
    &lt;나이&gt;25&lt;/나이&gt;
    &lt;취미&gt;독서&lt;/취미&gt;
&lt;/사람&gt;</code></pre>
                    <p class="text-sm text-green-600 mt-2">
                        ✓ 문법 규칙을 모두 지켰으므로 Well-formed입니다!<br>
                        ✓ 태그 이름은 아무거나 만들어도 OK!
                    </p>
                </div>
            </div>

            <div class="bg-gradient-to-r from-green-50 to-green-100 border-2 border-green-300 rounded-lg p-6">
                <h3 class="font-bold text-xl mb-3">✅ Valid XML (유효한 XML)</h3>
                <p class="mb-3">
                    <strong>"문법 규칙도 지키고, 정해진 구조 규칙도 지킨 XML"</strong>입니다.
                </p>
                <p class="mb-3">
                    Well-formed + <strong>DTD나 Schema라는 "설계도"에 맞게 작성</strong>된 XML을 말합니다.
                </p>

                <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                    <p class="font-semibold">🏗️ 비유로 이해하기</p>
                    <p class="mt-2">
                        <strong>Well-formed XML</strong>은 "문법에 맞는 한국어 문장"입니다.<br>
                        <em>"나는 어제 하늘을 먹었다"</em> - 문법은 맞지만 의미가 이상하죠?
                    </p>
                    <p class="mt-2">
                        <strong>Valid XML</strong>은 "문법도 맞고 의미도 맞는 문장"입니다.<br>
                        <em>"나는 어제 밥을 먹었다"</em> - 문법도 맞고 의미도 정상입니다!
                    </p>
                </div>

                <div class="bg-white p-4 rounded mt-4">
                    <p class="text-sm font-semibold mb-2">예시: Valid XML을 만들기 위한 DTD (설계도)</p>
                    <pre style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem; font-size: 0.875rem; margin: 0;"><code style="color: #1f2937;">&lt;!-- DTD: 도서 정보는 반드시 제목, 저자, 출판사를 포함해야 함 --&gt;
&lt;!DOCTYPE 도서 [
    &lt;!ELEMENT 도서 (제목, 저자, 출판사)&gt;
    &lt;!ELEMENT 제목 (#PCDATA)&gt;
    &lt;!ELEMENT 저자 (#PCDATA)&gt;
    &lt;!ELEMENT 출판사 (#PCDATA)&gt;
]&gt;</code></pre>

                    <p class="text-sm font-semibold mb-2 mt-4">이 DTD에 맞는 Valid XML:</p>
                    <pre style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem; font-size: 0.875rem; margin: 0;"><code style="color: #1f2937;">&lt;?xml version="1.0"?&gt;
&lt;!DOCTYPE 도서 SYSTEM "book.dtd"&gt;
&lt;도서&gt;
    &lt;제목&gt;어린왕자&lt;/제목&gt;
    &lt;저자&gt;생텍쥐페리&lt;/저자&gt;
    &lt;출판사&gt;민음사&lt;/출판사&gt;
&lt;/도서&gt;</code></pre>
                    <p class="text-sm text-green-600 mt-2">
                        ✓ Well-formed (문법 규칙 준수) + DTD 규칙 준수 = Valid!
                    </p>

                    <p class="text-sm font-semibold mb-2 mt-4 text-red-600">❌ Invalid XML 예시:</p>
                    <pre class="bg-red-50 p-3 rounded text-sm"><code style="color: #1f2937;">&lt;?xml version="1.0"?&gt;
&lt;도서&gt;
    &lt;제목&gt;어린왕자&lt;/제목&gt;
    &lt;저자&gt;생텍쥐페리&lt;/저자&gt;
    &lt;!-- 출판사가 없음! --&gt;
&lt;/도서&gt;</code></pre>
                    <p class="text-sm text-red-600 mt-2">
                        ✓ Well-formed이지만,<br>
                        ✗ DTD 규칙을 어겨서 Invalid!
                    </p>
                </div>
            </div>

            <div class="bg-purple-50 border-2 border-purple-300 rounded-lg p-6 mt-6">
                <h3 class="font-bold text-lg mb-3">📊 정리 표</h3>
                <table class="w-full border-collapse">
                    <thead>
                        <tr class="bg-purple-200">
                            <th class="border border-purple-300 p-2">구분</th>
                            <th class="border border-purple-300 p-2">Well-formed XML</th>
                            <th class="border border-purple-300 p-2">Valid XML</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="border border-purple-300 p-2 font-semibold">정의</td>
                            <td class="border border-purple-300 p-2">XML 문법 규칙을 지킨 문서</td>
                            <td class="border border-purple-300 p-2">문법 + 구조 규칙(DTD/Schema)을 지킨 문서</td>
                        </tr>
                        <tr class="bg-purple-50">
                            <td class="border border-purple-300 p-2 font-semibold">필수 조건</td>
                            <td class="border border-purple-300 p-2">5가지 문법 규칙</td>
                            <td class="border border-purple-300 p-2">Well-formed + DTD/Schema 준수</td>
                        </tr>
                        <tr>
                            <td class="border border-purple-300 p-2 font-semibold">태그 자유도</td>
                            <td class="border border-purple-300 p-2">태그 이름 자유롭게 생성 가능</td>
                            <td class="border border-purple-300 p-2">DTD/Schema에 정의된 태그만 사용</td>
                        </tr>
                        <tr class="bg-purple-50">
                            <td class="border border-purple-300 p-2 font-semibold">사용 예</td>
                            <td class="border border-purple-300 p-2">간단한 설정 파일, 개인 프로젝트</td>
                            <td class="border border-purple-300 p-2">표준 문서, 데이터 교환, 도서관 시스템</td>
                        </tr>
                        <tr>
                            <td class="border border-purple-300 p-2 font-semibold">예시</td>
                            <td class="border border-purple-300 p-2">문법만 맞으면 OK</td>
                            <td class="border border-purple-300 p-2">MARC XML, RSS Feed 등</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">속성 (Attribute) 사용하기 🏷️</h2>
        <div class="prose prose-lg">
            <p>XML에서도 HTML처럼 속성을 사용할 수 있습니다.</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">&lt;?xml version="1.0"?&gt;
&lt;도서 isbn="978-1234567890" 언어="한국어"&gt;
    &lt;제목&gt;어린왕자&lt;/제목&gt;
    &lt;저자 국적="프랑스"&gt;생텍쥐페리&lt;/저자&gt;
    &lt;출판연도&gt;2020&lt;/출판연도&gt;
&lt;/도서&gt;</code></pre>
            </div>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">🤔 요소 vs 속성, 언제 뭘 쓸까요?</p>
                <p class="mt-2"><strong>요소로 표현:</strong> 데이터의 주요 내용 (제목, 저자, 내용 등)</p>
                <p class="mt-1"><strong>속성으로 표현:</strong> 데이터에 대한 부가 정보 (ID, 언어, 버전 등)</p>

                <div class="mt-3 grid grid-cols-2 gap-4">
                    <div>
                        <p class="text-sm font-semibold">요소 사용 예:</p>
                        <pre class="bg-white p-2 rounded text-xs mt-1"><code style="color: #1f2937;">&lt;도서&gt;
  &lt;제목&gt;어린왕자&lt;/제목&gt;
  &lt;저자&gt;생텍쥐페리&lt;/저자&gt;
&lt;/도서&gt;</code></pre>
                    </div>
                    <div>
                        <p class="text-sm font-semibold">속성 사용 예:</p>
                        <pre class="bg-white p-2 rounded text-xs mt-1"><code style="color: #1f2937;">&lt;도서 id="001" 언어="ko"&gt;
  &lt;제목&gt;어린왕자&lt;/제목&gt;
&lt;/도서&gt;</code></pre>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">실전 예제: 도서관 장서 목록 📚</h2>
        <div class="prose prose-lg">
            <p>도서관에서 실제로 사용할 수 있는 XML 문서를 만들어봅시다!</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;도서관&gt;
    &lt;장서&gt;
        &lt;도서 isbn="978-8937460449" 대출가능="true"&gt;
            &lt;제목&gt;어린왕자&lt;/제목&gt;
            &lt;저자&gt;
                &lt;이름&gt;생텍쥐페리&lt;/이름&gt;
                &lt;국적&gt;프랑스&lt;/국적&gt;
            &lt;/저자&gt;
            &lt;출판정보&gt;
                &lt;출판사&gt;민음사&lt;/출판사&gt;
                &lt;출판연도&gt;2015&lt;/출판연도&gt;
            &lt;/출판정보&gt;
            &lt;분류&gt;
                &lt;주제&gt;아동문학&lt;/주제&gt;
                &lt;청구기호&gt;863-생63ㅇ&lt;/청구기호&gt;
            &lt;/분류&gt;
            &lt;소장정보&gt;
                &lt;위치&gt;제1자료실&lt;/위치&gt;
                &lt;수량&gt;3&lt;/수량&gt;
            &lt;/소장정보&gt;
        &lt;/도서&gt;

        &lt;도서 isbn="978-8932917221" 대출가능="false"&gt;
            &lt;제목&gt;데미안&lt;/제목&gt;
            &lt;저자&gt;
                &lt;이름&gt;헤르만 헤세&lt;/이름&gt;
                &lt;국적&gt;독일&lt;/국적&gt;
            &lt;/저자&gt;
            &lt;출판정보&gt;
                &lt;출판사&gt;민음사&lt;/출판사&gt;
                &lt;출판연도&gt;2018&lt;/출판연도&gt;
            &lt;/출판정보&gt;
            &lt;분류&gt;
                &lt;주제&gt;독일문학&lt;/주제&gt;
                &lt;청구기호&gt;853-헤53ㄷ&lt;/청구기호&gt;
            &lt;/분류&gt;
            &lt;소장정보&gt;
                &lt;위치&gt;제2자료실&lt;/위치&gt;
                &lt;수량&gt;2&lt;/수량&gt;
            &lt;/소장정보&gt;
        &lt;/도서&gt;
    &lt;/장서&gt;
&lt;/도서관&gt;</code></pre>
            </div>

            <div class="bg-green-50 border-l-4 border-green-500 p-4 my-4">
                <p class="font-semibold">💡 이 XML 문서의 구조</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li><strong>계층 구조:</strong> 도서관 → 장서 → 도서 → 세부 정보</li>
                    <li><strong>반복 가능:</strong> 여러 권의 도서 정보를 담을 수 있음</li>
                    <li><strong>확장 가능:</strong> 필요하면 새로운 요소 추가 가능 (예: 리뷰, 평점)</li>
                    <li><strong>검색 용이:</strong> 프로그램으로 특정 데이터를 쉽게 찾을 수 있음</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">XML 주석 달기 💬</h2>
        <div class="prose prose-lg">
            <p>HTML처럼 XML에서도 주석을 달 수 있습니다!</p>

            <div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #1f2937; font-family: monospace;">&lt;?xml version="1.0"?&gt;
&lt;!-- 이것은 주석입니다. 화면에 표시되지 않습니다. --&gt;
&lt;도서&gt;
    &lt;!--
        여러 줄 주석도 가능합니다
        도서 정보를 입력하는 부분
    --&gt;
    &lt;제목&gt;어린왕자&lt;/제목&gt;
    &lt;저자&gt;생텍쥐페리&lt;/저자&gt; &lt;!-- 프랑스 작가 --&gt;
&lt;/도서&gt;</code></pre>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">특수 문자 처리하기 🔤</h2>
        <div class="prose prose-lg">
            <p>XML에서 &lt;, &gt;, &amp; 같은 특수 문자는 태그와 혼동될 수 있어서 특별한 방법으로 써야 합니다.</p>

            <div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <table class="w-full border-collapse">
                    <thead>
                        <tr class="bg-gray-200">
                            <th class="border border-gray-400 p-2">사용하고 싶은 문자</th>
                            <th class="border border-gray-400 p-2">XML에서 쓰는 방법</th>
                            <th class="border border-gray-400 p-2">이름</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="border border-gray-400 p-2 text-center">&lt;</td>
                            <td class="border border-gray-400 p-2 text-center"><code style="color: #1f2937;">&amp;lt;</code></td>
                            <td class="border border-gray-400 p-2">less than</td>
                        </tr>
                        <tr class="bg-gray-50">
                            <td class="border border-gray-400 p-2 text-center">&gt;</td>
                            <td class="border border-gray-400 p-2 text-center"><code style="color: #1f2937;">&amp;gt;</code></td>
                            <td class="border border-gray-400 p-2">greater than</td>
                        </tr>
                        <tr>
                            <td class="border border-gray-400 p-2 text-center">&amp;</td>
                            <td class="border border-gray-400 p-2 text-center"><code style="color: #1f2937;">&amp;amp;</code></td>
                            <td class="border border-gray-400 p-2">ampersand</td>
                        </tr>
                        <tr class="bg-gray-50">
                            <td class="border border-gray-400 p-2 text-center">"</td>
                            <td class="border border-gray-400 p-2 text-center"><code style="color: #1f2937;">&amp;quot;</code></td>
                            <td class="border border-gray-400 p-2">quotation</td>
                        </tr>
                        <tr>
                            <td class="border border-gray-400 p-2 text-center">'</td>
                            <td class="border border-gray-400 p-2 text-center"><code style="color: #1f2937;">&amp;apos;</code></td>
                            <td class="border border-gray-400 p-2">apostrophe</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="bg-yellow-50 p-4 rounded-lg my-4">
                <p class="font-semibold mb-2">예시:</p>
                <pre class="bg-white p-3 rounded"><code style="color: #1f2937;">&lt;수학식&gt;5 &amp;lt; 10 &amp;amp;&amp;amp; 10 &amp;gt; 3&lt;/수학식&gt;
&lt;!-- 화면에는: 5 &lt; 10 &amp;&amp; 10 &gt; 3 으로 표시됨 --&gt;</code></pre>
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
                        <strong>XML은 데이터 저장/전달용 언어</strong>입니다
                        <br><small class="text-gray-600">HTML은 표시용, XML은 의미 전달용</small>
                    </li>
                    <li>
                        <strong>Well-formed XML:</strong> 문법 규칙만 지킨 XML
                        <br><small class="text-gray-600">태그 닫기, 중첩, 루트 요소, 속성 따옴표, 대소문자</small>
                    </li>
                    <li>
                        <strong>Valid XML:</strong> 문법 + DTD/Schema 규칙까지 지킨 XML
                        <br><small class="text-gray-600">Well-formed이면서 정해진 구조도 따름</small>
                    </li>
                    <li>
                        <strong>태그 이름을 자유롭게 만들 수 있습니다</strong>
                        <br><small class="text-gray-600">의미에 맞게 이름을 정하세요 (도서, 저자, 제목 등)</small>
                    </li>
                    <li>
                        <strong>도서관, 출판, 데이터 교환 등에 활용</strong>됩니다
                        <br><small class="text-gray-600">MARC XML, RSS, 설정 파일 등</small>
                    </li>
                </ul>
            </div>

            <div class="mt-6 bg-green-50 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">다음 단계</h3>
                <p>
                    XML의 기초를 배웠다면, 다음으로 <strong>XPath</strong>로 XML 데이터를 검색하고,
                    <strong>XSLT</strong>로 XML을 HTML로 변환하는 방법을 배워보세요!
                </p>
                <p class="mt-2">
                    또한 실무에서는 <strong>XML Schema (XSD)</strong>를 사용해서 더 정교한 Valid XML을 만듭니다.
                </p>
            </div>
        </div>
    </section>
</div>
"""

def update_xml_content():
    """XML 콘텐츠 업데이트"""
    try:
        content = Content.objects.get(slug='xml')

        content.title = "XML 기초 학습"
        content.summary = "XML의 기본 개념과 문법을 배우고, Well-formed XML과 Valid XML의 차이를 이해합니다. 도서관 시스템에서 사용되는 XML 문서 구조를 실습합니다."
        content.content_html = xml_content_html
        content.difficulty = 'BEGINNER'
        content.estimated_time = 50
        content.prerequisites = "HTML 기초 이해"
        content.learning_objectives = "XML의 개념 이해, Well-formed와 Valid XML의 차이점 파악, 도서관 데이터를 XML로 구조화하기, XML 문법 규칙 이해"

        content.save()

        print("✓ XML 교육자료가 업데이트되었습니다!")
        print(f"  - 제목: {content.title}")
        print(f"  - URL: /contents/xml")
        print(f"  - 예상 시간: {content.estimated_time}분")

    except Content.DoesNotExist:
        print("✗ XML 콘텐츠를 찾을 수 없습니다. slug='xml'인 콘텐츠를 먼저 생성해주세요.")
    except Exception as e:
        print(f"✗ 오류 발생: {e}")

if __name__ == '__main__':
    update_xml_content()
