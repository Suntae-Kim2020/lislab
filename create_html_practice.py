#!/usr/bin/env python
"""HTML 실습 페이지 생성 스크립트"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content, Category, Tag
from apps.accounts.models import User

# HTML 실습 콘텐츠
html_practice_content = """
<div class="space-y-8">
    <section>
        <h2 class="text-2xl font-bold mb-4">HTML 실습 🎯</h2>
        <div class="prose prose-lg">
            <p>
                이 실습에서는 HTML을 직접 작성하고 실시간으로 결과를 확인할 수 있습니다.
                왼쪽 편집기에 HTML 코드를 입력하고 "▶ 실행" 버튼을 클릭하면 오른쪽에 결과가 표시됩니다.
            </p>

            <div class="bg-blue-50 border-l-4 border-blue-500 p-4 my-4">
                <p class="font-semibold">💡 실습 방법</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>왼쪽 편집기에서 HTML 코드를 자유롭게 작성하세요</li>
                    <li>"▶ 실행" 버튼을 클릭하면 결과를 확인할 수 있습니다</li>
                    <li>"초기화" 버튼을 클릭하면 예제 코드로 돌아갑니다</li>
                    <li>각 실습 문제를 순서대로 풀어보세요</li>
                </ul>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">실습 1: 기본 구조 만들기 📝</h2>
        <div class="prose prose-lg">
            <p class="mb-4">
                <strong>목표:</strong> HTML 문서의 기본 구조를 이해하고 간단한 자기소개 페이지를 만들어봅시다.
            </p>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">📋 요구사항</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>제목(h1)으로 자신의 이름 표시</li>
                    <li>부제목(h2)으로 "자기소개" 표시</li>
                    <li>단락(p)으로 자기소개 내용 작성</li>
                    <li>좋아하는 것들을 순서 없는 목록(ul, li)으로 표시</li>
                </ul>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem; margin-bottom: 1.5rem;">
                <div>
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.75rem;">📝 코드 입력</h3>
                    <div style="background-color: #f3f4f6; border-radius: 0.5rem; padding: 1rem;">
                        <textarea
                            id="practice1-editor"
                            style="width: 100%; height: 300px; font-family: 'Courier New', monospace; font-size: 0.875rem; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; resize: vertical;"
                            placeholder="여기에 HTML 코드를 작성하세요..."><!DOCTYPE html>
<html>
<head>
    <title>자기소개</title>
</head>
<body>
    <h1>홍길동</h1>
    <h2>자기소개</h2>
    <p>안녕하세요! 저는 도서관에서 일하는 사서입니다.</p>

    <h3>좋아하는 것들</h3>
    <ul>
        <li>책 읽기</li>
        <li>음악 듣기</li>
        <li>산책하기</li>
    </ul>
</body>
</html></textarea>
                        <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem;">
                            <button
                                onclick="runPractice1()"
                                style="font-size: 0.875rem; padding: 0.25rem 1rem; background-color: #2563eb; color: white; border: none; border-radius: 0.25rem; cursor: pointer; font-weight: 600;"
                                onmouseover="this.style.backgroundColor='#1d4ed8'"
                                onmouseout="this.style.backgroundColor='#2563eb'"
                            >
                                ▶ 실행
                            </button>
                            <button
                                onclick="resetPractice1()"
                                style="font-size: 0.875rem; padding: 0.25rem 0.75rem; background-color: #e5e7eb; color: #374151; border: none; border-radius: 0.25rem; cursor: pointer;"
                                onmouseover="this.style.backgroundColor='#d1d5db'"
                                onmouseout="this.style.backgroundColor='#e5e7eb'"
                            >
                                초기화
                            </button>
                        </div>
                    </div>
                </div>

                <div>
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.75rem;">👀 실행 결과</h3>
                    <div style="background-color: white; border: 2px solid #e5e7eb; border-radius: 0.5rem; padding: 1rem; min-height: 300px;">
                        <iframe
                            id="practice1-preview"
                            style="width: 100%; height: 350px; border: none;"
                            sandbox="allow-scripts allow-same-origin"
                        ></iframe>
                    </div>
                </div>
            </div>

            <script>
                (function() {
                    const defaultCode1 = `<!DOCTYPE html>
<html>
<head>
    <title>자기소개</title>
</head>
<body>
    <h1>홍길동</h1>
    <h2>자기소개</h2>
    <p>안녕하세요! 저는 도서관에서 일하는 사서입니다.</p>

    <h3>좋아하는 것들</h3>
    <ul>
        <li>책 읽기</li>
        <li>음악 듣기</li>
        <li>산책하기</li>
    </ul>
</body>
</html>`;

                    window.runPractice1 = function() {
                        try {
                            const code = document.getElementById('practice1-editor').value;
                            const preview = document.getElementById('practice1-preview');
                            const previewDoc = preview.contentDocument || preview.contentWindow.document;
                            previewDoc.open();
                            previewDoc.write(code);
                            previewDoc.close();
                        } catch (error) {
                            console.error('Error running code:', error);
                            alert('코드 실행 중 오류가 발생했습니다: ' + error.message);
                        }
                    };

                    window.resetPractice1 = function() {
                        document.getElementById('practice1-editor').value = defaultCode1;
                        runPractice1();
                    };

                    // 페이지 로드 시 초기 실행
                    if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', runPractice1);
                    } else {
                        setTimeout(runPractice1, 100);
                    }
                })();
            </script>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">실습 2: 링크와 이미지 📷</h2>
        <div class="prose prose-lg">
            <p class="mb-4">
                <strong>목표:</strong> 하이퍼링크와 이미지를 추가하여 페이지를 풍부하게 만들어봅시다.
            </p>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">📋 요구사항</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>좋아하는 웹사이트로 이동하는 링크 3개 추가 (a 태그)</li>
                    <li>각 링크는 새 탭에서 열리도록 설정 (target="_blank")</li>
                    <li>이미지 1개 추가 (img 태그 - 임의의 URL 사용 가능)</li>
                </ul>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem; margin-bottom: 1.5rem;">
                <div>
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.75rem;">📝 코드 입력</h3>
                    <div style="background-color: #f3f4f6; border-radius: 0.5rem; padding: 1rem;">
                        <textarea
                            id="practice2-editor"
                            style="width: 100%; height: 300px; font-family: 'Courier New', monospace; font-size: 0.875rem; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; resize: vertical;"><!DOCTYPE html>
<html>
<head>
    <title>링크와 이미지 실습</title>
</head>
<body>
    <h1>내가 좋아하는 사이트들</h1>

    <h2>자주 방문하는 사이트</h2>
    <ul>
        <li><a href="https://www.google.com" target="_blank">구글</a></li>
        <li><a href="https://www.wikipedia.org" target="_blank">위키백과</a></li>
        <li><a href="https://www.github.com" target="_blank">GitHub</a></li>
    </ul>

    <h2>좋아하는 이미지</h2>
    <img src="https://via.placeholder.com/300x200" alt="예제 이미지">
</body>
</html></textarea>
                        <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem;">
                            <button
                                onclick="runPractice2()"
                                style="font-size: 0.875rem; padding: 0.25rem 1rem; background-color: #2563eb; color: white; border: none; border-radius: 0.25rem; cursor: pointer; font-weight: 600;"
                                onmouseover="this.style.backgroundColor='#1d4ed8'"
                                onmouseout="this.style.backgroundColor='#2563eb'"
                            >
                                ▶ 실행
                            </button>
                            <button
                                onclick="resetPractice2()"
                                style="font-size: 0.875rem; padding: 0.25rem 0.75rem; background-color: #e5e7eb; color: #374151; border: none; border-radius: 0.25rem; cursor: pointer;"
                                onmouseover="this.style.backgroundColor='#d1d5db'"
                                onmouseout="this.style.backgroundColor='#e5e7eb'"
                            >
                                초기화
                            </button>
                        </div>
                    </div>
                </div>

                <div>
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.75rem;">👀 실행 결과</h3>
                    <div style="background-color: white; border: 2px solid #e5e7eb; border-radius: 0.5rem; padding: 1rem; min-height: 300px;">
                        <iframe
                            id="practice2-preview"
                            style="width: 100%; height: 350px; border: none;"
                            sandbox="allow-scripts allow-same-origin allow-popups"
                        ></iframe>
                    </div>
                </div>
            </div>

            <script>
                (function() {
                    const defaultCode2 = `<!DOCTYPE html>
<html>
<head>
    <title>링크와 이미지 실습</title>
</head>
<body>
    <h1>내가 좋아하는 사이트들</h1>

    <h2>자주 방문하는 사이트</h2>
    <ul>
        <li><a href="https://www.google.com" target="_blank">구글</a></li>
        <li><a href="https://www.wikipedia.org" target="_blank">위키백과</a></li>
        <li><a href="https://www.github.com" target="_blank">GitHub</a></li>
    </ul>

    <h2>좋아하는 이미지</h2>
    <img src="https://via.placeholder.com/300x200" alt="예제 이미지">
</body>
</html>`;

                    window.runPractice2 = function() {
                        try {
                            const code = document.getElementById('practice2-editor').value;
                            const preview = document.getElementById('practice2-preview');
                            const previewDoc = preview.contentDocument || preview.contentWindow.document;
                            previewDoc.open();
                            previewDoc.write(code);
                            previewDoc.close();
                        } catch (error) {
                            console.error('Error running code:', error);
                            alert('코드 실행 중 오류가 발생했습니다: ' + error.message);
                        }
                    };

                    window.resetPractice2 = function() {
                        document.getElementById('practice2-editor').value = defaultCode2;
                        runPractice2();
                    };

                    if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', runPractice2);
                    } else {
                        setTimeout(runPractice2, 100);
                    }
                })();
            </script>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">실습 3: 표 만들기 📊</h2>
        <div class="prose prose-lg">
            <p class="mb-4">
                <strong>목표:</strong> HTML 표를 사용하여 정보를 구조화해봅시다.
            </p>

            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 my-4">
                <p class="font-semibold">📋 요구사항</p>
                <ul class="list-disc pl-6 mt-2 space-y-1">
                    <li>책 목록을 표로 만들기 (table, tr, th, td 사용)</li>
                    <li>헤더: 제목, 저자, 출판년도</li>
                    <li>최소 3권의 책 데이터 추가</li>
                    <li>표에 테두리 스타일 추가</li>
                </ul>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem; margin-bottom: 1.5rem;">
                <div>
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.75rem;">📝 코드 입력</h3>
                    <div style="background-color: #f3f4f6; border-radius: 0.5rem; padding: 1rem;">
                        <textarea
                            id="practice3-editor"
                            style="width: 100%; height: 300px; font-family: 'Courier New', monospace; font-size: 0.875rem; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 0.375rem; resize: vertical;"><!DOCTYPE html>
<html>
<head>
    <title>도서 목록</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
    </style>
</head>
<body>
    <h1>나의 책장</h1>

    <table>
        <tr>
            <th>제목</th>
            <th>저자</th>
            <th>출판년도</th>
        </tr>
        <tr>
            <td>어린왕자</td>
            <td>생텍쥐페리</td>
            <td>2015</td>
        </tr>
        <tr>
            <td>데미안</td>
            <td>헤르만 헤세</td>
            <td>2018</td>
        </tr>
        <tr>
            <td>1984</td>
            <td>조지 오웰</td>
            <td>2020</td>
        </tr>
    </table>
</body>
</html></textarea>
                        <div style="display: flex; gap: 0.5rem; margin-top: 0.75rem;">
                            <button
                                onclick="runPractice3()"
                                style="font-size: 0.875rem; padding: 0.25rem 1rem; background-color: #2563eb; color: white; border: none; border-radius: 0.25rem; cursor: pointer; font-weight: 600;"
                                onmouseover="this.style.backgroundColor='#1d4ed8'"
                                onmouseout="this.style.backgroundColor='#2563eb'"
                            >
                                ▶ 실행
                            </button>
                            <button
                                onclick="resetPractice3()"
                                style="font-size: 0.875rem; padding: 0.25rem 0.75rem; background-color: #e5e7eb; color: #374151; border: none; border-radius: 0.25rem; cursor: pointer;"
                                onmouseover="this.style.backgroundColor='#d1d5db'"
                                onmouseout="this.style.backgroundColor='#e5e7eb'"
                            >
                                초기화
                            </button>
                        </div>
                    </div>
                </div>

                <div>
                    <h3 style="font-size: 1.125rem; font-weight: 600; margin-bottom: 0.75rem;">👀 실행 결과</h3>
                    <div style="background-color: white; border: 2px solid #e5e7eb; border-radius: 0.5rem; padding: 1rem; min-height: 300px;">
                        <iframe
                            id="practice3-preview"
                            style="width: 100%; height: 350px; border: none;"
                            sandbox="allow-scripts allow-same-origin"
                        ></iframe>
                    </div>
                </div>
            </div>

            <script>
                (function() {
                    const defaultCode3 = `<!DOCTYPE html>
<html>
<head>
    <title>도서 목록</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
    </style>
</head>
<body>
    <h1>나의 책장</h1>

    <table>
        <tr>
            <th>제목</th>
            <th>저자</th>
            <th>출판년도</th>
        </tr>
        <tr>
            <td>어린왕자</td>
            <td>생텍쥐페리</td>
            <td>2015</td>
        </tr>
        <tr>
            <td>데미안</td>
            <td>헤르만 헤세</td>
            <td>2018</td>
        </tr>
        <tr>
            <td>1984</td>
            <td>조지 오웰</td>
            <td>2020</td>
        </tr>
    </table>
</body>
</html>`;

                    window.runPractice3 = function() {
                        try {
                            const code = document.getElementById('practice3-editor').value;
                            const preview = document.getElementById('practice3-preview');
                            const previewDoc = preview.contentDocument || preview.contentWindow.document;
                            previewDoc.open();
                            previewDoc.write(code);
                            previewDoc.close();
                        } catch (error) {
                            console.error('Error running code:', error);
                            alert('코드 실행 중 오류가 발생했습니다: ' + error.message);
                        }
                    };

                    window.resetPractice3 = function() {
                        document.getElementById('practice3-editor').value = defaultCode3;
                        runPractice3();
                    };

                    if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', runPractice3);
                    } else {
                        setTimeout(runPractice3, 100);
                    }
                })();
            </script>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">도전 과제 🏆</h2>
        <div class="prose prose-lg">
            <div class="bg-purple-50 border-2 border-purple-300 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">종합 실습: 도서관 웹페이지 만들기</h3>
                <p class="mb-3">지금까지 배운 내용을 모두 활용하여 간단한 도서관 소개 페이지를 만들어보세요!</p>

                <p class="font-semibold mb-2">포함할 요소:</p>
                <ul class="list-disc pl-6 space-y-1">
                    <li>도서관 이름과 소개 (h1, p 태그)</li>
                    <li>층별 안내 (h2, ul/ol 태그)</li>
                    <li>인기 도서 목록 표 (table 태그)</li>
                    <li>도서관 홈페이지 링크 (a 태그)</li>
                    <li>도서관 사진 (img 태그)</li>
                    <li>CSS로 꾸미기 (style 태그)</li>
                </ul>

                <p class="mt-4 text-sm text-gray-600">
                    힌트: 위의 실습 1, 2, 3을 참고하여 자유롭게 작성해보세요!
                </p>
            </div>
        </div>
    </section>

    <section>
        <h2 class="text-2xl font-bold mb-4">정리 📚</h2>
        <div class="prose prose-lg">
            <div class="bg-green-50 rounded-lg p-6">
                <h3 class="font-bold text-lg mb-3">실습을 마치며</h3>
                <p>
                    축하합니다! HTML의 기본 요소들을 직접 작성하고 실행해보았습니다.
                    더 많은 연습을 통해 HTML에 익숙해지세요.
                </p>
                <p class="mt-3">
                    <strong>다음 단계:</strong> CSS를 배워서 페이지를 더 아름답게 꾸며보세요!
                </p>
            </div>
        </div>
    </section>
</div>
"""

def create_html_practice():
    """HTML 실습 콘텐츠 생성"""
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
            slug='html-practice',
            defaults={
                'title': 'HTML 실습',
                'summary': 'HTML의 기본 요소들을 직접 작성하고 실시간으로 실행 결과를 확인하며 학습합니다. 자기소개 페이지, 링크와 이미지, 표 만들기 등 다양한 실습 문제를 풀어보세요.',
                'content_html': html_practice_content,
                'category': category,
                'author': admin_user,
                'difficulty': 'BEGINNER',
                'estimated_time': 60,
                'status': 'PUBLISHED',
                'prerequisites': 'HTML 기초 학습 완료',
                'learning_objectives': 'HTML 기본 태그 실습, 하이퍼링크와 이미지 사용, 표 작성, 실전 웹페이지 제작'
            }
        )

        # 태그 추가
        tag_names = ['HTML', 'Practice', '실습', 'Web', '웹개발', 'Hands-on']
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
            print("✅ HTML 실습 콘텐츠 생성 완료!")
        else:
            print("✅ HTML 실습 콘텐츠 업데이트 완료!")

        print(f"   제목: {content.title}")
        print(f"   카테고리: {content.category.name}")
        print(f"   URL: /contents/html-practice")
        print(f"   난이도: {content.get_difficulty_display()}")
        print(f"   예상 시간: {content.estimated_time}분")

    except Category.DoesNotExist:
        print("❌ '실습' 카테고리를 찾을 수 없습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    create_html_practice()
