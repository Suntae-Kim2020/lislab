#!/usr/bin/env python
"""XML 실습 페이지 생성 스크립트"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content, Category, Tag
from apps.accounts.models import User

# XML 실습 콘텐츠
xml_practice_content = """
<div class="space-y-8">
    <section>
        <h2 class="text-2xl font-bold mb-4">XML 실습 🎯</h2>
        <div class="prose prose-lg">
            <p>
                이 실습에서는 XML 문서를 직접 작성하고 구조를 확인할 수 있습니다.
                XML의 문법 규칙을 지키면서 다양한 데이터를 표현하는 방법을 익혀봅시다.
            </p>

            <div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-4">
                <p class="font-semibold">💡 실습 방법</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>왼쪽 편집기에서 XML 코드를 작성하세요</li>
                    <li>"✓ 검증" 버튼을 클릭하면 문법 오류를 확인할 수 있습니다</li>
                    <li>"초기화" 버튼으로 예제 코드로 돌아갈 수 있습니다</li>
                    <li>Well-formed XML 작성이 목표입니다</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">실습 1: 도서 정보 XML 작성 📚</h2>
        <div class="prose prose-lg">
            <p class="mb-4">
                <strong>목표:</strong> XML의 기본 구조를 이해하고 도서 정보를 XML로 표현해봅시다.
            </p>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">📋 요구사항</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>XML 선언 추가 (&lt;?xml version="1.0" encoding="UTF-8"?&gt;)</li>
                    <li>루트 요소로 &lt;도서&gt; 사용</li>
                    <li>제목, 저자, 출판사, 출판연도 요소 포함</li>
                    <li>모든 태그가 올바르게 닫혀야 함</li>
                </ul>
            </div>

            <div style="background-color: #f9fafb; border-radius: 0.5rem; padding: 1.5rem; margin-top: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.75rem;">📝 XML 편집기</h3>
                <textarea
                    id="practice1-xml-editor"
                    style="width: 100%; height: 350px; font-family: 'Courier New', monospace; font-size: 0.875rem; padding: 1rem; border: 2px solid #d1d5db; border-radius: 0.5rem; resize: vertical; background-color: white;"
                    spellcheck="false"><?xml version="1.0" encoding="UTF-8"?>
<도서>
    <제목>어린왕자</제목>
    <저자>생텍쥐페리</저자>
    <출판사>민음사</출판사>
    <출판연도>2015</출판연도>
</도서></textarea>

                <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                    <button
                        onclick="validateXML1()"
                        style="font-size: 0.875rem; padding: 0.5rem 1.25rem; background-color: #10b981; color: white; border: none; border-radius: 0.375rem; cursor: pointer; font-weight: 600;"
                        onmouseover="this.style.backgroundColor='#059669'"
                        onmouseout="this.style.backgroundColor='#10b981'"
                    >
                        ✓ 검증
                    </button>
                    <button
                        onclick="resetXML1()"
                        style="font-size: 0.875rem; padding: 0.5rem 1rem; background-color: #e5e7eb; color: #374151; border: none; border-radius: 0.375rem; cursor: pointer;"
                        onmouseover="this.style.backgroundColor='#d1d5db'"
                        onmouseout="this.style.backgroundColor='#e5e7eb'"
                    >
                        초기화
                    </button>
                </div>

                <div id="practice1-result" style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; display: none;"></div>
            </div>

            <script>
                (function() {
                    const defaultXML1 = `<?xml version="1.0" encoding="UTF-8"?>
<도서>
    <제목>어린왕자</제목>
    <저자>생텍쥐페리</저자>
    <출판사>민음사</출판사>
    <출판연도>2015</출판연도>
</도서>`;

                    window.validateXML1 = function() {
                        const xmlText = document.getElementById('practice1-xml-editor').value;
                        const resultDiv = document.getElementById('practice1-result');

                        try {
                            const parser = new DOMParser();
                            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');

                            const parseError = xmlDoc.getElementsByTagName('parsererror');

                            if (parseError.length > 0) {
                                resultDiv.style.display = 'block';
                                resultDiv.style.backgroundColor = '#fef2f2';
                                resultDiv.style.borderLeft = '4px solid #ef4444';
                                resultDiv.innerHTML = '<strong style="color: #dc2626;">❌ XML 오류 발견!</strong><br>' +
                                                     '<span style="color: #991b1b;">' + parseError[0].textContent + '</span>';
                            } else {
                                resultDiv.style.display = 'block';
                                resultDiv.style.backgroundColor = '#f0fdf4';
                                resultDiv.style.borderLeft = '4px solid #10b981';
                                resultDiv.innerHTML = '<strong style="color: #059669;">✓ Well-formed XML입니다!</strong><br>' +
                                                     '<span style="color: #065f46;">모든 문법 규칙을 올바르게 지켰습니다.</span>';
                            }
                        } catch (error) {
                            resultDiv.style.display = 'block';
                            resultDiv.style.backgroundColor = '#fef2f2';
                            resultDiv.style.borderLeft = '4px solid #ef4444';
                            resultDiv.innerHTML = '<strong style="color: #dc2626;">❌ 검증 오류!</strong><br>' +
                                                 '<span style="color: #991b1b;">' + error.message + '</span>';
                        }
                    };

                    window.resetXML1 = function() {
                        document.getElementById('practice1-xml-editor').value = defaultXML1;
                        document.getElementById('practice1-result').style.display = 'none';
                    };
                })();
            </script>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">실습 2: 속성 활용하기 🏷️</h2>
        <div class="prose prose-lg">
            <p class="mb-4">
                <strong>목표:</strong> XML 속성을 사용하여 추가 정보를 표현해봅시다.
            </p>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">📋 요구사항</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>&lt;도서&gt; 요소에 isbn 속성 추가</li>
                    <li>&lt;도서&gt; 요소에 대출가능 속성 추가 (true/false)</li>
                    <li>&lt;저자&gt; 요소에 국적 속성 추가</li>
                    <li>속성 값은 반드시 따옴표로 감싸기</li>
                </ul>
            </div>

            <div style="background-color: #f9fafb; border-radius: 0.5rem; padding: 1.5rem; margin-top: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.75rem;">📝 XML 편집기</h3>
                <textarea
                    id="practice2-xml-editor"
                    style="width: 100%; height: 350px; font-family: 'Courier New', monospace; font-size: 0.875rem; padding: 1rem; border: 2px solid #d1d5db; border-radius: 0.5rem; resize: vertical; background-color: white;"
                    spellcheck="false"><?xml version="1.0" encoding="UTF-8"?>
<도서 isbn="978-8937460449" 대출가능="true">
    <제목>어린왕자</제목>
    <저자 국적="프랑스">생텍쥐페리</저자>
    <출판사>민음사</출판사>
    <출판연도>2015</출판연도>
    <분류>
        <주제>아동문학</주제>
        <청구기호>863-생63ㅇ</청구기호>
    </분류>
</도서></textarea>

                <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                    <button
                        onclick="validateXML2()"
                        style="font-size: 0.875rem; padding: 0.5rem 1.25rem; background-color: #10b981; color: white; border: none; border-radius: 0.375rem; cursor: pointer; font-weight: 600;"
                        onmouseover="this.style.backgroundColor='#059669'"
                        onmouseout="this.style.backgroundColor='#10b981'"
                    >
                        ✓ 검증
                    </button>
                    <button
                        onclick="resetXML2()"
                        style="font-size: 0.875rem; padding: 0.5rem 1rem; background-color: #e5e7eb; color: #374151; border: none; border-radius: 0.375rem; cursor: pointer;"
                        onmouseover="this.style.backgroundColor='#d1d5db'"
                        onmouseout="this.style.backgroundColor='#e5e7eb'"
                    >
                        초기화
                    </button>
                </div>

                <div id="practice2-result" style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; display: none;"></div>
            </div>

            <script>
                (function() {
                    const defaultXML2 = `<?xml version="1.0" encoding="UTF-8"?>
<도서 isbn="978-8937460449" 대출가능="true">
    <제목>어린왕자</제목>
    <저자 국적="프랑스">생텍쥐페리</저자>
    <출판사>민음사</출판사>
    <출판연도>2015</출판연도>
    <분류>
        <주제>아동문학</주제>
        <청구기호>863-생63ㅇ</청구기호>
    </분류>
</도서>`;

                    window.validateXML2 = function() {
                        const xmlText = document.getElementById('practice2-xml-editor').value;
                        const resultDiv = document.getElementById('practice2-result');

                        try {
                            const parser = new DOMParser();
                            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
                            const parseError = xmlDoc.getElementsByTagName('parsererror');

                            if (parseError.length > 0) {
                                resultDiv.style.display = 'block';
                                resultDiv.style.backgroundColor = '#fef2f2';
                                resultDiv.style.borderLeft = '4px solid #ef4444';
                                resultDiv.innerHTML = '<strong style="color: #dc2626;">❌ XML 오류 발견!</strong><br>' +
                                                     '<span style="color: #991b1b;">' + parseError[0].textContent + '</span>';
                            } else {
                                resultDiv.style.display = 'block';
                                resultDiv.style.backgroundColor = '#f0fdf4';
                                resultDiv.style.borderLeft = '4px solid #10b981';
                                resultDiv.innerHTML = '<strong style="color: #059669;">✓ Well-formed XML입니다!</strong><br>' +
                                                     '<span style="color: #065f46;">속성을 올바르게 사용했습니다.</span>';
                            }
                        } catch (error) {
                            resultDiv.style.display = 'block';
                            resultDiv.style.backgroundColor = '#fef2f2';
                            resultDiv.style.borderLeft = '4px solid #ef4444';
                            resultDiv.innerHTML = '<strong style="color: #dc2626;">❌ 검증 오류!</strong><br>' +
                                                 '<span style="color: #991b1b;">' + error.message + '</span>';
                        }
                    };

                    window.resetXML2 = function() {
                        document.getElementById('practice2-xml-editor').value = defaultXML2;
                        document.getElementById('practice2-result').style.display = 'none';
                    };
                })();
            </script>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">실습 3: 여러 항목 표현하기 📋</h2>
        <div class="prose prose-lg">
            <p class="mb-4">
                <strong>목표:</strong> 도서관의 여러 책을 하나의 XML 문서로 표현해봅시다.
            </p>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">📋 요구사항</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>루트 요소를 &lt;도서관&gt;으로 변경</li>
                    <li>&lt;도서관&gt; 안에 &lt;장서&gt; 요소 추가</li>
                    <li>&lt;장서&gt; 안에 최소 3권의 &lt;도서&gt; 추가</li>
                    <li>각 도서는 제목, 저자, 출판사 정보 포함</li>
                </ul>
            </div>

            <div style="background-color: #f9fafb; border-radius: 0.5rem; padding: 1.5rem; margin-top: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.75rem;">📝 XML 편집기</h3>
                <textarea
                    id="practice3-xml-editor"
                    style="width: 100%; height: 400px; font-family: 'Courier New', monospace; font-size: 0.875rem; padding: 1rem; border: 2px solid #d1d5db; border-radius: 0.5rem; resize: vertical; background-color: white;"
                    spellcheck="false"><?xml version="1.0" encoding="UTF-8"?>
<도서관>
    <장서>
        <도서 isbn="978-8937460449">
            <제목>어린왕자</제목>
            <저자>생텍쥐페리</저자>
            <출판사>민음사</출판사>
        </도서>

        <도서 isbn="978-8932917221">
            <제목>데미안</제목>
            <저자>헤르만 헤세</저자>
            <출판사>민음사</출판사>
        </도서>

        <도서 isbn="978-8949120683">
            <제목>1984</제목>
            <저자>조지 오웰</저자>
            <출판사>민음사</출판사>
        </도서>
    </장서>
</도서관></textarea>

                <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                    <button
                        onclick="validateXML3()"
                        style="font-size: 0.875rem; padding: 0.5rem 1.25rem; background-color: #10b981; color: white; border: none; border-radius: 0.375rem; cursor: pointer; font-weight: 600;"
                        onmouseover="this.style.backgroundColor='#059669'"
                        onmouseout="this.style.backgroundColor='#10b981'"
                    >
                        ✓ 검증
                    </button>
                    <button
                        onclick="resetXML3()"
                        style="font-size: 0.875rem; padding: 0.5rem 1rem; background-color: #e5e7eb; color: #374151; border: none; border-radius: 0.375rem; cursor: pointer;"
                        onmouseover="this.style.backgroundColor='#d1d5db'"
                        onmouseout="this.style.backgroundColor='#e5e7eb'"
                    >
                        초기화
                    </button>
                </div>

                <div id="practice3-result" style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; display: none;"></div>
            </div>

            <script>
                (function() {
                    const defaultXML3 = `<?xml version="1.0" encoding="UTF-8"?>
<도서관>
    <장서>
        <도서 isbn="978-8937460449">
            <제목>어린왕자</제목>
            <저자>생텍쥐페리</저자>
            <출판사>민음사</출판사>
        </도서>

        <도서 isbn="978-8932917221">
            <제목>데미안</제목>
            <저자>헤르만 헤세</저자>
            <출판사>민음사</출판사>
        </도서>

        <도서 isbn="978-8949120683">
            <제목>1984</제목>
            <저자>조지 오웰</저자>
            <출판사>민음사</출판사>
        </도서>
    </장서>
</도서관>`;

                    window.validateXML3 = function() {
                        const xmlText = document.getElementById('practice3-xml-editor').value;
                        const resultDiv = document.getElementById('practice3-result');

                        try {
                            const parser = new DOMParser();
                            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
                            const parseError = xmlDoc.getElementsByTagName('parsererror');

                            if (parseError.length > 0) {
                                resultDiv.style.display = 'block';
                                resultDiv.style.backgroundColor = '#fef2f2';
                                resultDiv.style.borderLeft = '4px solid #ef4444';
                                resultDiv.innerHTML = '<strong style="color: #dc2626;">❌ XML 오류 발견!</strong><br>' +
                                                     '<span style="color: #991b1b;">' + parseError[0].textContent + '</span>';
                            } else {
                                resultDiv.style.display = 'block';
                                resultDiv.style.backgroundColor = '#f0fdf4';
                                resultDiv.style.borderLeft = '4px solid #10b981';
                                resultDiv.innerHTML = '<strong style="color: #059669;">✓ Well-formed XML입니다!</strong><br>' +
                                                     '<span style="color: #065f46;">계층 구조를 올바르게 표현했습니다.</span>';
                            }
                        } catch (error) {
                            resultDiv.style.display = 'block';
                            resultDiv.style.backgroundColor = '#fef2f2';
                            resultDiv.style.borderLeft = '4px solid #ef4444';
                            resultDiv.innerHTML = '<strong style="color: #dc2626;">❌ 검증 오류!</strong><br>' +
                                                 '<span style="color: #991b1b;">' + error.message + '</span>';
                        }
                    };

                    window.resetXML3 = function() {
                        document.getElementById('practice3-xml-editor').value = defaultXML3;
                        document.getElementById('practice3-result').style.display = 'none';
                    };
                })();
            </script>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">도전 과제 🏆</h2>
        <div class="prose prose-lg">
            <div class="bg-purple-50 border-2 border-purple-300 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">종합 실습: 도서관 시스템 XML 설계</h3>
                <p class="mb-3">지금까지 배운 내용을 모두 활용하여 도서관 시스템 XML을 설계해보세요!</p>

                <p class="font-semibold mb-2">포함할 요소:</p>
                <ul class="list-disc pl-6 space-y-1">
                    <li>도서 정보 (제목, 저자, ISBN, 출판사, 출판연도)</li>
                    <li>소장 정보 (위치, 수량, 대출 가능 여부)</li>
                    <li>저자 정보 (이름, 국적)</li>
                    <li>분류 정보 (주제, 청구기호)</li>
                    <li>적절한 속성 활용</li>
                    <li>올바른 계층 구조</li>
                </ul>

                <p class="mt-4 text-sm text-gray-600">
                    힌트: 실습 1, 2, 3을 참고하여 종합적인 XML 문서를 작성해보세요!
                </p>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">자주하는 실수 ⚠️</h2>
        <div class="prose prose-lg">
            <div class="space-y-4">
                <div class="border-2 border-red-300 rounded-lg p-4 bg-red-50">
                    <h3 class="font-bold text-lg mb-2 text-red-700">1. 태그를 닫지 않음</h3>
                    <div style="background-color: white; padding: 0.75rem; border-radius: 0.375rem; margin-top: 0.5rem;">
                        <code style="color: #dc2626;">&lt;제목&gt;어린왕자</code> ❌<br>
                        <code style="color: #059669;">&lt;제목&gt;어린왕자&lt;/제목&gt;</code> ✓
                    </div>
                </div>

                <div class="border-2 border-red-300 rounded-lg p-4 bg-red-50">
                    <h3 class="font-bold text-lg mb-2 text-red-700">2. 태그가 교차됨</h3>
                    <div style="background-color: white; padding: 0.75rem; border-radius: 0.375rem; margin-top: 0.5rem;">
                        <code style="color: #dc2626;">&lt;책&gt;&lt;제목&gt;어린왕자&lt;/책&gt;&lt;/제목&gt;</code> ❌<br>
                        <code style="color: #059669;">&lt;책&gt;&lt;제목&gt;어린왕자&lt;/제목&gt;&lt;/책&gt;</code> ✓
                    </div>
                </div>

                <div class="border-2 border-red-300 rounded-lg p-4 bg-red-50">
                    <h3 class="font-bold text-lg mb-2 text-red-700">3. 속성 값에 따옴표 누락</h3>
                    <div style="background-color: white; padding: 0.75rem; border-radius: 0.375rem; margin-top: 0.5rem;">
                        <code style="color: #dc2626;">&lt;도서 isbn=123&gt;</code> ❌<br>
                        <code style="color: #059669;">&lt;도서 isbn="123"&gt;</code> ✓
                    </div>
                </div>

                <div class="border-2 border-red-300 rounded-lg p-4 bg-red-50">
                    <h3 class="font-bold text-lg mb-2 text-red-700">4. 루트 요소가 여러 개</h3>
                    <div style="background-color: white; padding: 0.75rem; border-radius: 0.375rem; margin-top: 0.5rem;">
                        <code style="color: #dc2626;">&lt;책&gt;...&lt;/책&gt;&lt;책&gt;...&lt;/책&gt;</code> ❌<br>
                        <code style="color: #059669;">&lt;도서관&gt;&lt;책&gt;...&lt;/책&gt;&lt;책&gt;...&lt;/책&gt;&lt;/도서관&gt;</code> ✓
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">정리 📚</h2>
        <div class="prose prose-lg">
            <div class="bg-green-50 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">실습을 마치며</h3>
                <p>
                    축하합니다! XML의 기본 문법을 익히고 Well-formed XML 문서를 작성하는 방법을 배웠습니다.
                    더 많은 연습을 통해 XML에 익숙해지세요.
                </p>
                <p class="mt-3">
                    <strong>다음 단계:</strong> DTD나 XML Schema를 배워서 Valid XML을 작성해보세요!
                </p>
            </div>
        </div>
    </section>
</div>
"""

def create_xml_practice():
    """XML 실습 콘텐츠 생성"""
    try:
        # 카테고리 가져오기
        category = Category.objects.get(slug='practice')

        # 관리자 사용자 가져오기
        admin_user = User.objects.filter(role='ADMIN').first()
        if not admin_user:
            print("❌ 관리자 사용자를 찾을 수 없습니다.")
            return

        # 콘텐츠 생성 또는 업데이트
        content, created = Content.objects.update_or_create(
            slug='xml-practice',
            defaults={
                'title': 'XML 실습',
                'summary': 'XML 문서를 직접 작성하고 문법을 검증하며 학습합니다. 도서 정보 표현, 속성 활용, 계층 구조 설계 등 다양한 실습 문제를 통해 Well-formed XML 작성법을 익힙니다.',
                'content_html': xml_practice_content,
                'category': category,
                'author': admin_user,
                'difficulty': 'BEGINNER',
                'estimated_time': 50,
                'status': 'PUBLISHED',
                'prerequisites': 'XML 기초 학습 완료',
                'learning_objectives': 'XML 기본 문법 실습, 속성 사용법, 계층 구조 설계, Well-formed XML 작성, 문법 오류 디버깅'
            }
        )

        # 태그 추가
        tag_names = ['XML', 'Practice', '실습', 'Well-formed', 'Data Structure', '데이터구조']
        tags = []
        for tag_name in tag_names:
            tag = Tag.objects.filter(name=tag_name).first()
            if not tag:
                try:
                    tag = Tag.objects.create(name=tag_name)
                except Exception as e:
                    print(f"  ⚠️  태그 '{tag_name}' 생성 실패: {e}")
                    continue
            if tag:
                tags.append(tag)

        if tags:
            content.tags.set(tags)

        if created:
            print("✅ XML 실습 콘텐츠 생성 완료!")
        else:
            print("✅ XML 실습 콘텐츠 업데이트 완료!")

        print(f"   제목: {content.title}")
        print(f"   카테고리: {content.category.name}")
        print(f"   URL: /contents/xml-practice")
        print(f"   난이도: {content.get_difficulty_display()}")
        print(f"   예상 시간: {content.estimated_time}분")

    except Category.DoesNotExist:
        print("❌ '실습' 카테고리를 찾을 수 없습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_xml_practice()
