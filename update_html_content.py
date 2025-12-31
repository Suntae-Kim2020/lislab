#!/usr/bin/env python
"""HTML 교육자료 업데이트 스크립트"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content

# HTML 교육자료 내용
html_content = """
<div class="space-y-8">
    <section>
        <h2 class="text-2xl font-bold mb-4">HTML이란 무엇인가요? 🌐</h2>
        <div class="prose prose-lg">
            <p>
                <strong>HTML (HyperText Markup Language)</strong>은 웹 페이지를 만드는 가장 기본적인 언어입니다.
                웹 브라우저가 이해할 수 있는 마크업 언어로, 웹 페이지의 구조와 내용을 정의합니다.
            </p>
            <p>
                HTML은 프로그래밍 언어가 아니라 <strong>마크업 언어</strong>입니다.
                즉, 컴퓨터에게 "이것을 계산해라"가 아니라 "이 부분은 제목이고, 저 부분은 문단이야"라고
                의미를 표시하는 언어입니다.
            </p>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">HTML 요소(Element)란? 📦</h2>
        <div class="prose prose-lg">
            <p>
                <strong>요소(Element)</strong>는 HTML 문서를 구성하는 기본 단위입니다.
                여는 태그, 내용, 닫는 태그로 이루어져 있습니다.
            </p>

            <div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre><code style="color: #1f2937;">&lt;p&gt;안녕하세요!&lt;/p&gt;</code></pre>
            </div>

            <p>위 예제를 분해해보면:</p>
            <ul class="list-disc pl-6 space-y-2">
                <li><code>&lt;p&gt;</code> - <strong>여는 태그(Opening Tag)</strong>: 문단의 시작을 알립니다</li>
                <li><code>안녕하세요!</code> - <strong>내용(Content)</strong>: 실제로 보여질 텍스트입니다</li>
                <li><code>&lt;/p&gt;</code> - <strong>닫는 태그(Closing Tag)</strong>: 문단의 끝을 알립니다</li>
            </ul>

            <div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-4">
                <p class="font-semibold">💡 기억하세요!</p>
                <p>여는 태그 + 내용 + 닫는 태그 = 하나의 완전한 요소</p>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">주요 HTML 요소들 📝</h2>
        <div class="space-y-4">
            <div class="border rounded-lg p-4">
                <h3 class="font-bold text-lg mb-2">제목 요소</h3>
                <div style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem;">
                    <pre><code>&lt;h1&gt;가장 큰 제목&lt;/h1&gt;
&lt;h2&gt;두 번째로 큰 제목&lt;/h2&gt;
&lt;h3&gt;세 번째 제목&lt;/h3&gt;
...
&lt;h6&gt;가장 작은 제목&lt;/h6&gt;</code></pre>
                </div>
                <p class="mt-2 text-sm text-gray-600">h1이 가장 중요한 제목이고, h6로 갈수록 덜 중요한 제목입니다.</p>
            </div>

            <div class="border rounded-lg p-4">
                <h3 class="font-bold text-lg mb-2">문단 요소</h3>
                <div style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem;">
                    <pre><code>&lt;p&gt;이것은 하나의 문단입니다.&lt;/p&gt;</code></pre>
                </div>
                <p class="mt-2 text-sm text-gray-600">텍스트를 문단으로 묶을 때 사용합니다.</p>
            </div>

            <div class="border rounded-lg p-4">
                <h3 class="font-bold text-lg mb-2">링크 요소</h3>
                <div style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem;">
                    <pre><code>&lt;a href="https://example.com"&gt;클릭하세요&lt;/a&gt;</code></pre>
                </div>
                <p class="mt-2 text-sm text-gray-600">다른 페이지로 이동하는 링크를 만듭니다.</p>
            </div>

            <div class="border rounded-lg p-4">
                <h3 class="font-bold text-lg mb-2">이미지 요소</h3>
                <div style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem;">
                    <pre><code>&lt;img src="cat.jpg" alt="귀여운 고양이"&gt;</code></pre>
                </div>
                <p class="mt-2 text-sm text-gray-600">이미지를 표시합니다. 닫는 태그가 없는 특별한 요소입니다!</p>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">속성(Attribute)이란? 🏷️</h2>
        <div class="prose prose-lg">
            <p>
                <strong>속성(Attribute)</strong>은 HTML 요소에 추가 정보를 제공합니다.
                여는 태그 안에 <code>이름="값"</code> 형태로 작성합니다.
            </p>

            <div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre><code style="color: #1f2937;">&lt;a href="https://www.google.com" target="_blank"&gt;구글로 가기&lt;/a&gt;</code></pre>
            </div>

            <p>위 예제에서 속성을 살펴보면:</p>
            <ul class="list-disc pl-6 space-y-2">
                <li>
                    <code>href="https://www.google.com"</code>
                    <ul class="list-circle pl-6 mt-1">
                        <li><strong>속성 이름:</strong> href (링크 주소를 의미)</li>
                        <li><strong>속성 값:</strong> "https://www.google.com"</li>
                        <li><strong>역할:</strong> 어디로 이동할지 지정</li>
                    </ul>
                </li>
                <li>
                    <code>target="_blank"</code>
                    <ul class="list-circle pl-6 mt-1">
                        <li><strong>속성 이름:</strong> target</li>
                        <li><strong>속성 값:</strong> "_blank"</li>
                        <li><strong>역할:</strong> 새 탭에서 열기</li>
                    </ul>
                </li>
            </ul>

            <div class="bg-green-50 border-l-4 border-green-500 p-4 my-4">
                <p class="font-semibold">✅ 속성 작성 규칙</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>속성 이름과 값 사이에는 <code>=</code>를 씁니다</li>
                    <li>속성 값은 쌍따옴표(<code>"</code>) 안에 씁니다</li>
                    <li>여러 속성은 공백으로 구분합니다</li>
                    <li>대소문자를 구분하지 않지만, 소문자를 권장합니다</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">자주 사용하는 속성들 🔑</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="border rounded-lg p-4">
                <h3 class="font-bold mb-2">id</h3>
                <p class="text-sm text-gray-600 mb-2">요소에 고유한 이름을 부여합니다</p>
                <div style="background-color: #f3f4f6; padding: 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;">
                    <code>&lt;div id="header"&gt;...&lt;/div&gt;</code>
                </div>
            </div>

            <div class="border rounded-lg p-4">
                <h3 class="font-bold mb-2">class</h3>
                <p class="text-sm text-gray-600 mb-2">요소를 그룹으로 분류합니다</p>
                <div style="background-color: #f3f4f6; padding: 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;">
                    <code>&lt;p class="important"&gt;...&lt;/p&gt;</code>
                </div>
            </div>

            <div class="border rounded-lg p-4">
                <h3 class="font-bold mb-2">style</h3>
                <p class="text-sm text-gray-600 mb-2">요소의 스타일을 직접 지정합니다</p>
                <div style="background-color: #f3f4f6; padding: 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;">
                    <code>&lt;p style="color: red;"&gt;...&lt;/p&gt;</code>
                </div>
            </div>

            <div class="border rounded-lg p-4">
                <h3 class="font-bold mb-2">title</h3>
                <p class="text-sm text-gray-600 mb-2">마우스를 올렸을 때 툴팁을 표시합니다</p>
                <div style="background-color: #f3f4f6; padding: 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;">
                    <code>&lt;abbr title="웹 표준"&gt;W3C&lt;/abbr&gt;</code>
                </div>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">기본 HTML 문서 구조 📄</h2>
        <div class="prose prose-lg">
            <p>모든 HTML 문서는 다음과 같은 기본 구조를 가집니다:</p>

            <div style="background-color: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre><code style="color: #1f2937;">&lt;!DOCTYPE html&gt;
&lt;html lang="ko"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;페이지 제목&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;안녕하세요!&lt;/h1&gt;
    &lt;p&gt;이것은 HTML 문서입니다.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
            </div>

            <p>각 부분의 역할:</p>
            <ul class="list-disc pl-6 space-y-2">
                <li><code style="color: #1f2937;">&lt;!DOCTYPE html&gt;</code> - 이 문서가 HTML5 문서임을 선언</li>
                <li><code style="color: #1f2937;">&lt;html&gt;</code> - HTML 문서의 시작과 끝</li>
                <li><code style="color: #1f2937;">&lt;head&gt;</code> - 문서의 메타 정보 (제목, 인코딩 등)</li>
                <li><code style="color: #1f2937;">&lt;body&gt;</code> - 실제로 화면에 보이는 내용</li>
            </ul>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">실습 예제 💻</h2>
        <div class="prose prose-lg">
            <p>간단한 자기소개 페이지를 만들어봅시다:</p>

            <div style="background-color: #111827; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                <pre style="margin: 0; overflow-x: auto;"><code style="color: #f9fafb; font-family: monospace;">&lt;!DOCTYPE html&gt;
&lt;html lang="ko"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;나의 자기소개&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;김철수의 자기소개&lt;/h1&gt;

    &lt;h2&gt;기본 정보&lt;/h2&gt;
    &lt;p&gt;안녕하세요! 저는 &lt;strong&gt;김철수&lt;/strong&gt;입니다.&lt;/p&gt;
    &lt;p&gt;저는 &lt;em&gt;도서관 정보학&lt;/em&gt;을 공부하고 있습니다.&lt;/p&gt;

    &lt;h2&gt;취미&lt;/h2&gt;
    &lt;ul&gt;
        &lt;li&gt;독서&lt;/li&gt;
        &lt;li&gt;영화 감상&lt;/li&gt;
        &lt;li&gt;코딩&lt;/li&gt;
    &lt;/ul&gt;

    &lt;h2&gt;연락처&lt;/h2&gt;
    &lt;p&gt;
        이메일: &lt;a href="mailto:chulsoo@example.com"&gt;chulsoo@example.com&lt;/a&gt;
    &lt;/p&gt;

    &lt;img src="profile.jpg" alt="김철수 프로필 사진" width="200"&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
            </div>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">🎯 실습 과제</p>
                <p class="mt-2">위 예제를 참고해서 여러분만의 자기소개 페이지를 만들어보세요!</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>제목(h1, h2)을 사용해서 섹션을 구분하세요</li>
                    <li>강조(strong, em)를 사용해서 중요한 내용을 표시하세요</li>
                    <li>목록(ul, li)을 사용해서 여러 항목을 나열하세요</li>
                    <li>링크(a)를 사용해서 이메일이나 웹사이트를 추가하세요</li>
                </ul>
            </div>
        </div>
    </section>

    <section class="mt-8">
        <h2 class="text-2xl font-bold mb-4">직접 해보기! HTML 실습 🎨</h2>
        <div class="prose prose-lg mb-4">
            <p>
                아래 에디터에서 HTML 코드를 직접 작성해보세요!
                코드를 입력한 후 <strong class="text-blue-600">▶ 실행</strong> 버튼을 클릭하면 오른쪽에서 결과를 확인할 수 있습니다.
            </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
                <div class="flex items-center justify-between mb-2">
                    <h3 class="font-bold">HTML 코드 입력</h3>
                    <div style="display: flex; gap: 0.5rem;">
                        <button
                            onclick="runCode()"
                            style="font-size: 0.875rem; padding: 0.25rem 1rem; background-color: #2563eb; color: white; border: none; border-radius: 0.25rem; cursor: pointer; font-weight: 600;"
                            onmouseover="this.style.backgroundColor='#1d4ed8'"
                            onmouseout="this.style.backgroundColor='#2563eb'"
                        >
                            ▶ 실행
                        </button>
                        <button
                            onclick="resetCode()"
                            style="font-size: 0.875rem; padding: 0.25rem 0.75rem; background-color: #e5e7eb; color: #374151; border: none; border-radius: 0.25rem; cursor: pointer;"
                            onmouseover="this.style.backgroundColor='#d1d5db'"
                            onmouseout="this.style.backgroundColor='#e5e7eb'"
                        >
                            초기화
                        </button>
                    </div>
                </div>
                <textarea
                    id="htmlEditor"
                    class="w-full h-96 p-4 font-mono text-sm border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                    spellcheck="false"
                >&lt;!DOCTYPE html&gt;
&lt;html lang="ko"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;나의 첫 HTML&lt;/title&gt;
    &lt;style&gt;
        body {
            font-family: sans-serif;
            padding: 20px;
            background-color: #f9f9f9;
        }
        h1 {
            color: #2563eb;
        }
    &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;안녕하세요! 👋&lt;/h1&gt;
    &lt;p&gt;이것은 제가 만든 첫 HTML 페이지입니다.&lt;/p&gt;

    &lt;h2&gt;좋아하는 것들&lt;/h2&gt;
    &lt;ul&gt;
        &lt;li&gt;HTML 배우기&lt;/li&gt;
        &lt;li&gt;웹 페이지 만들기&lt;/li&gt;
        &lt;li&gt;코딩하기&lt;/li&gt;
    &lt;/ul&gt;

    &lt;p&gt;
        더 알아보기:
        &lt;a href="https://developer.mozilla.org/ko/docs/Web/HTML" target="_blank"&gt;
            MDN HTML 가이드
        &lt;/a&gt;
    &lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</textarea>
            </div>

            <div>
                <h3 class="font-bold mb-2">실행 결과</h3>
                <iframe
                    id="preview"
                    class="w-full h-96 border-2 border-gray-300 rounded-lg bg-white"
                    sandbox="allow-scripts allow-same-origin"
                ></iframe>
            </div>
        </div>

        <div class="bg-purple-50 border-l-4 border-purple-500 p-4 mb-4">
            <p class="font-semibold">💪 도전 과제</p>
            <p class="mt-2">다음을 시도해보세요:</p>
            <ul class="list-disc pl-6 mt-2 space-y-1">
                <li>제목의 색상을 빨간색(<code style="color: #1f2937;">color: red;</code>)로 바꿔보세요</li>
                <li>새로운 문단(<code style="color: #1f2937;">&lt;p&gt;</code>)을 추가해보세요</li>
                <li>이미지를 추가해보세요: <code style="color: #1f2937;">&lt;img src="https://picsum.photos/200" alt="랜덤 이미지"&gt;</code></li>
                <li>표(<code style="color: #1f2937;">&lt;table&gt;</code>)를 만들어보세요</li>
                <li>버튼(<code style="color: #1f2937;">&lt;button&gt;</code>)을 추가해보세요</li>
            </ul>
        </div>

        <details style="background-color: #f9fafb; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem;">
            <summary class="cursor-pointer font-semibold">📖 예제 코드 모음 (클릭하여 펼치기)</summary>
            <div class="mt-4 space-y-4">
                <div>
                    <h4 class="font-semibold mb-2">1️⃣ 간단한 표 만들기</h4>
                    <button
                        onclick="loadExample(1)"
                        style="font-size: 0.875rem; padding: 0.25rem 0.75rem; background-color: #3b82f6; color: white; border: none; border-radius: 0.25rem; cursor: pointer; margin-bottom: 0.5rem;"
                        onmouseover="this.style.backgroundColor='#2563eb'"
                        onmouseout="this.style.backgroundColor='#3b82f6'"
                    >
                        에디터에 불러오기
                    </button>
                    <pre style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem; font-size: 0.875rem; overflow-x: auto; margin: 0;"><code style="color: #1f2937;">&lt;table border="1"&gt;
  &lt;tr&gt;
    &lt;th&gt;이름&lt;/th&gt;
    &lt;th&gt;나이&lt;/th&gt;
  &lt;/tr&gt;
  &lt;tr&gt;
    &lt;td&gt;홍길동&lt;/td&gt;
    &lt;td&gt;25&lt;/td&gt;
  &lt;/tr&gt;
&lt;/table&gt;</code></pre>
                </div>

                <div>
                    <h4 class="font-semibold mb-2">2️⃣ 폼 만들기</h4>
                    <button
                        onclick="loadExample(2)"
                        style="font-size: 0.875rem; padding: 0.25rem 0.75rem; background-color: #3b82f6; color: white; border: none; border-radius: 0.25rem; cursor: pointer; margin-bottom: 0.5rem;"
                        onmouseover="this.style.backgroundColor='#2563eb'"
                        onmouseout="this.style.backgroundColor='#3b82f6'"
                    >
                        에디터에 불러오기
                    </button>
                    <pre style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem; font-size: 0.875rem; overflow-x: auto; margin: 0;"><code style="color: #1f2937;">&lt;form&gt;
  &lt;label&gt;이름: &lt;input type="text" placeholder="이름 입력"&gt;&lt;/label&gt;
  &lt;br&gt;&lt;br&gt;
  &lt;label&gt;이메일: &lt;input type="email" placeholder="email@example.com"&gt;&lt;/label&gt;
  &lt;br&gt;&lt;br&gt;
  &lt;button type="submit"&gt;전송&lt;/button&gt;
&lt;/form&gt;</code></pre>
                </div>

                <div>
                    <h4 class="font-semibold mb-2">3️⃣ 카드 디자인</h4>
                    <button
                        onclick="loadExample(3)"
                        style="font-size: 0.875rem; padding: 0.25rem 0.75rem; background-color: #3b82f6; color: white; border: none; border-radius: 0.25rem; cursor: pointer; margin-bottom: 0.5rem;"
                        onmouseover="this.style.backgroundColor='#2563eb'"
                        onmouseout="this.style.backgroundColor='#3b82f6'"
                    >
                        에디터에 불러오기
                    </button>
                    <pre style="background-color: #f3f4f6; padding: 0.75rem; border-radius: 0.25rem; font-size: 0.875rem; overflow-x: auto; margin: 0;"><code style="color: #1f2937;">&lt;div style="border: 2px solid #ddd; border-radius: 8px; padding: 20px; max-width: 300px;"&gt;
  &lt;h2 style="margin-top: 0; color: #333;"&gt;상품 카드&lt;/h2&gt;
  &lt;img src="https://picsum.photos/280/160" alt="상품 이미지" style="width: 100%; border-radius: 4px;"&gt;
  &lt;p&gt;이것은 상품 설명입니다.&lt;/p&gt;
  &lt;button style="background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer;"&gt;
    구매하기
  &lt;/button&gt;
&lt;/div&gt;</code></pre>
                </div>
            </div>
        </details>

        <script>
            // Wait for elements to be ready
            (function() {
                const editor = document.getElementById('htmlEditor');
                const preview = document.getElementById('preview');

                if (!editor || !preview) {
                    console.error('Editor or preview element not found');
                    return;
                }

                const initialCode = editor.value;

                // 예제 코드
                const examples = {
                    1: `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>표 예제</title>
</head>
<body>
    <h1>학생 명단</h1>
    <table border="1" style="border-collapse: collapse;">
        <tr>
            <th style="padding: 8px;">이름</th>
            <th style="padding: 8px;">나이</th>
            <th style="padding: 8px;">학과</th>
        </tr>
        <tr>
            <td style="padding: 8px;">홍길동</td>
            <td style="padding: 8px;">25</td>
            <td style="padding: 8px;">문헌정보학</td>
        </tr>
        <tr>
            <td style="padding: 8px;">김영희</td>
            <td style="padding: 8px;">23</td>
            <td style="padding: 8px;">컴퓨터공학</td>
        </tr>
    </table>
</body>
</html>`,
                    2: `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>폼 예제</title>
</head>
<body>
    <h1>회원가입</h1>
    <form>
        <div style="margin-bottom: 15px;">
            <label>이름:
                <input type="text" placeholder="이름 입력" style="padding: 5px;">
            </label>
        </div>
        <div style="margin-bottom: 15px;">
            <label>이메일:
                <input type="email" placeholder="email@example.com" style="padding: 5px;">
            </label>
        </div>
        <div style="margin-bottom: 15px;">
            <label>비밀번호:
                <input type="password" placeholder="비밀번호" style="padding: 5px;">
            </label>
        </div>
        <button type="submit" style="background: #10b981; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer;">
            가입하기
        </button>
    </form>
</body>
</html>`,
                    3: `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>카드 디자인</title>
</head>
<body style="background: #f3f4f6; padding: 40px; font-family: sans-serif;">
    <div style="border: 2px solid #ddd; border-radius: 8px; padding: 20px; max-width: 300px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h2 style="margin-top: 0; color: #333;">멋진 상품</h2>
        <img src="https://picsum.photos/280/160" alt="상품 이미지" style="width: 100%; border-radius: 4px; margin-bottom: 15px;">
        <p style="color: #666; line-height: 1.6;">
            이것은 아주 멋진 상품입니다.
            HTML과 CSS를 사용해서 이런 카드 디자인을 만들 수 있습니다!
        </p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
            <span style="font-size: 24px; font-weight: bold; color: #2563eb;">₩29,900</span>
            <button style="background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: bold;">
                구매하기
            </button>
        </div>
    </div>
</body>
</html>`
                };

                function updatePreview() {
                    try {
                        const code = editor.value;
                        const previewDoc = preview.contentDocument || preview.contentWindow.document;
                        previewDoc.open();
                        previewDoc.write(code);
                        previewDoc.close();
                    } catch (error) {
                        console.error('Preview update failed:', error);
                    }
                }

                window.runCode = function() {
                    updatePreview();
                };

                window.resetCode = function() {
                    editor.value = initialCode;
                    updatePreview();
                };

                window.loadExample = function(num) {
                    editor.value = examples[num];
                    updatePreview();
                    // 에디터로 스크롤
                    editor.scrollIntoView({ behavior: 'smooth', block: 'center' });
                };

                // 초기 로드
                updatePreview();
            })();
        </script>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">정리하며 📚</h2>
        <div class="prose prose-lg">
            <div class="bg-blue-50 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">핵심 개념 정리</h3>
                <ul class="space-y-2">
                    <li>
                        <strong>HTML</strong>은 웹 페이지의 구조를 만드는 마크업 언어입니다
                    </li>
                    <li>
                        <strong>요소(Element)</strong>는 여는 태그 + 내용 + 닫는 태그로 구성됩니다
                        <br><code style="color: #1f2937;">&lt;p&gt;내용&lt;/p&gt;</code>
                    </li>
                    <li>
                        <strong>속성(Attribute)</strong>은 요소에 추가 정보를 제공합니다
                        <br><code style="color: #1f2937;">&lt;a href="주소" target="_blank"&gt;</code>
                    </li>
                    <li>
                        모든 HTML 문서는 <code style="color: #1f2937;">&lt;!DOCTYPE html&gt;</code>로 시작하고
                        <br><code style="color: #1f2937;">&lt;html&gt;</code>, <code style="color: #1f2937;">&lt;head&gt;</code>, <code style="color: #1f2937;">&lt;body&gt;</code> 구조를 가집니다
                    </li>
                </ul>
            </div>

            <div class="mt-6 bg-green-50 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">다음 단계</h3>
                <p>
                    HTML의 기초를 배웠다면, 이제 CSS를 배워서 웹 페이지를 예쁘게 꾸미고,
                    JavaScript를 배워서 동적인 기능을 추가해보세요!
                </p>
            </div>
        </div>
    </section>
</div>
"""

def update_html_content():
    """HTML 교육자료 업데이트"""
    try:
        content = Content.objects.get(slug='html')
        content.content_html = html_content
        content.summary = "HTML 태그를 직접 작성하고 결과를 확인하면서 웹 페이지의 기본 구조를 학습합니다. 요소(Element)와 속성(Attribute)의 개념을 친절하게 설명하고, 실습 예제를 통해 HTML의 기초를 확실하게 이해합니다."
        content.learning_objectives = "HTML의 기본 개념 이해, 요소와 속성의 차이점 파악, 기본 HTML 문서 구조 학습, 자기소개 페이지 만들기 실습"
        content.prerequisites = "없음"
        content.estimated_time = 45
        content.save()

        print(f"✓ HTML 교육자료가 업데이트되었습니다!")
        print(f"  - 제목: {content.title}")
        print(f"  - URL: /contents/{content.slug}")
        print(f"  - 예상 시간: {content.estimated_time}분")

    except Content.DoesNotExist:
        print("✗ HTML 콘텐츠를 찾을 수 없습니다.")
    except Exception as e:
        print(f"✗ 오류 발생: {e}")

if __name__ == '__main__':
    update_html_content()
