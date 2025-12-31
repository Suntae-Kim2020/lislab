#!/usr/bin/env python
"""
JSON 학습 콘텐츠 추가 스크립트
"""
import os
import sys
import django

# Django 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.contents.models import Content, Category, Tag

User = get_user_model()

def create_json_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 가져오기: 웹문서
    web_docs_category = Category.objects.get(slug='web-docs')
    print("✓ 상위 카테고리 확인: 웹문서")

    # 하위 카테고리 생성 또는 가져오기: JSON
    json_category, created = Category.objects.get_or_create(
        slug='json',
        defaults={
            'name': 'JSON',
            'description': 'JSON (JavaScript Object Notation)',
            'parent': web_docs_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: JSON")
    else:
        print("✓ 하위 카테고리 확인: JSON")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': 'JSON', 'slug': 'json'},
        {'name': 'JavaScript', 'slug': 'javascript'},
        {'name': '데이터 형식', 'slug': 'data-format'},
        {'name': 'API', 'slug': 'api'},
        {'name': 'REST API', 'slug': 'rest-api'},
        {'name': '웹 개발', 'slug': 'web-development'},
        {'name': 'XML', 'slug': 'xml'},
        {'name': '데이터 교환', 'slug': 'data-exchange'}
    ]
    tags = []
    for tag_info in tag_data:
        tag, created = Tag.objects.get_or_create(
            name=tag_info['name'],
            defaults={'slug': tag_info['slug']}
        )
        tags.append(tag)
        print(f"  ✓ 태그 확인: {tag_info['name']}")

    # 학습 콘텐츠 생성
    content = Content.objects.create(
        title="JSON: 웹의 언어로 데이터 주고받기",
        slug="json-data-format",
        summary="JSON은 웹에서 가장 많이 쓰이는 데이터 형식! 사람도 읽기 쉽고 컴퓨터도 처리하기 쉬운 JSON의 모든 것을 배워봅시다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>JSON이 무엇인지, 왜 필요한지 이해하기</li>
    <li>JSON의 기본 문법과 데이터 타입 배우기</li>
    <li>실제로 JSON 데이터 작성하고 읽기</li>
    <li>JSON과 XML의 차이점 명확히 알기</li>
    <li>JSON이 실제로 어떻게 사용되는지 파악하기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. JSON을 한 문장으로</h2>

  <div class="hero-definition">
    <h3>📦 JSON이란?</h3>
    <p class="big-statement">
      <strong>JSON (JavaScript Object Notation)</strong>은<br>
      사람도 읽기 쉽고 컴퓨터도 처리하기 쉬운<br>
      <strong>텍스트 기반 데이터 형식</strong>입니다.
    </p>
  </div>

  <div class="json-intro">
    <h4>💡 JSON의 탄생 이야기</h4>
    <div class="timeline-story">
      <div class="story-item">
        <div class="year">2000년대 초반</div>
        <div class="situation">
          <p class="problem">❌ <strong>문제:</strong> XML은 너무 복잡하고 무거워요!</p>
          <pre class="example-bad">
&lt;person&gt;
  &lt;name&gt;김철수&lt;/name&gt;
  &lt;age&gt;25&lt;/age&gt;
&lt;/person&gt;
          </pre>
        </div>
      </div>

      <div class="arrow-down">⬇️</div>

      <div class="story-item">
        <div class="year">2001년</div>
        <div class="situation">
          <p class="solution">✅ <strong>해결:</strong> Douglas Crockford가 JSON 발명!</p>
          <pre class="example-good">
{
  "name": "김철수",
  "age": 25
}
          </pre>
          <p class="benefit">👉 훨씬 간단하고 읽기 쉬워졌어요!</p>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>2. JSON 기본 문법</h2>

  <div class="syntax-intro">
    <p>JSON은 <strong>단 두 가지 구조</strong>만 있으면 됩니다!</p>
  </div>

  <div class="syntax-grid">
    <div class="syntax-card object-card">
      <div class="card-number">1</div>
      <h4>객체 (Object)</h4>
      <p class="card-desc">이름-값 쌍의 모음</p>

      <div class="syntax-example">
        <pre class="code-block">
{
  "이름": "값",
  "나이": 25,
  "도시": "서울"
}
        </pre>
      </div>

      <div class="syntax-rules">
        <h5>규칙:</h5>
        <ul>
          <li><code>{ }</code> 중괄호로 감싸기</li>
          <li><code>"이름": 값</code> 형태</li>
          <li>쉼표 <code>,</code>로 구분</li>
          <li>이름은 <strong>반드시 쌍따옴표</strong></li>
        </ul>
      </div>

      <div class="real-example">
        <h5>🌟 실제 예시: 사람 정보</h5>
        <pre class="code-block">
{
  "name": "이영희",
  "age": 28,
  "email": "younghee@example.com",
  "isStudent": false
}
        </pre>
      </div>
    </div>

    <div class="syntax-card array-card">
      <div class="card-number">2</div>
      <h4>배열 (Array)</h4>
      <p class="card-desc">값들의 순서있는 목록</p>

      <div class="syntax-example">
        <pre class="code-block">
[
  "사과",
  "바나나",
  "오렌지"
]
        </pre>
      </div>

      <div class="syntax-rules">
        <h5>규칙:</h5>
        <ul>
          <li><code>[ ]</code> 대괄호로 감싸기</li>
          <li>값들을 쉼표로 구분</li>
          <li>순서가 있음 (0부터 시작)</li>
          <li>같은 타입 아니어도 OK</li>
        </ul>
      </div>

      <div class="real-example">
        <h5>🌟 실제 예시: 과일 목록</h5>
        <pre class="code-block">
[
  "사과",
  "바나나",
  123,
  true,
  { "name": "오렌지" }
]
        </pre>
      </div>
    </div>
  </div>

  <div class="combine-example">
    <h4>🔗 객체와 배열을 합치면?</h4>
    <p>복잡한 데이터도 표현할 수 있어요!</p>

    <pre class="code-block">
{
  "학교": "서울대학교",
  "학생들": [
    {
      "이름": "김철수",
      "나이": 20,
      "전공": "컴퓨터공학"
    },
    {
      "이름": "이영희",
      "나이": 22,
      "전공": "문헌정보학"
    }
  ],
  "설립년도": 1946,
  "활성화": true
}
    </pre>
  </div>
</div>

<div class="content-section">
  <h2>3. JSON 데이터 타입</h2>

  <div class="types-intro">
    <p>JSON은 <strong>6가지 데이터 타입</strong>을 지원합니다:</p>
  </div>

  <div class="types-grid">
    <div class="type-card">
      <div class="type-icon">📝</div>
      <h4>문자열 (String)</h4>
      <p class="type-desc">쌍따옴표로 감싼 텍스트</p>
      <pre class="code-mini">
"안녕하세요"
"Hello, World!"
"123"  // 이것도 문자열!
      </pre>
      <div class="type-note">
        ⚠️ <strong>반드시 쌍따옴표</strong> 사용<br>
        작은따옴표 <code>'안녕'</code> ❌
      </div>
    </div>

    <div class="type-card">
      <div class="type-icon">🔢</div>
      <h4>숫자 (Number)</h4>
      <p class="type-desc">정수, 소수, 음수 모두 가능</p>
      <pre class="code-mini">
42
3.14
-10
1.5e10  // 과학적 표기법
      </pre>
      <div class="type-note">
        💡 정수/소수 구분 없음<br>
        모두 같은 숫자 타입
      </div>
    </div>

    <div class="type-card">
      <div class="type-icon">✅</div>
      <h4>불린 (Boolean)</h4>
      <p class="type-desc">참 또는 거짓</p>
      <pre class="code-mini">
true
false
      </pre>
      <div class="type-note">
        ⚠️ 소문자로만 작성<br>
        <code>True</code> ❌
      </div>
    </div>

    <div class="type-card">
      <div class="type-icon">⭕</div>
      <h4>null</h4>
      <p class="type-desc">값이 없음을 나타냄</p>
      <pre class="code-mini">
{
  "email": null,
  "phone": null
}
      </pre>
      <div class="type-note">
        💡 빈 문자열 <code>""</code>과 다름<br>
        진짜 "없음"을 의미
      </div>
    </div>

    <div class="type-card">
      <div class="type-icon">📦</div>
      <h4>객체 (Object)</h4>
      <p class="type-desc">{ } 중괄호</p>
      <pre class="code-mini">
{
  "name": "JSON",
  "year": 2001
}
      </pre>
    </div>

    <div class="type-card">
      <div class="type-icon">📋</div>
      <h4>배열 (Array)</h4>
      <p class="type-desc">[ ] 대괄호</p>
      <pre class="code-mini">
[1, 2, 3, 4, 5]
["a", "b", "c"]
      </pre>
    </div>
  </div>

  <div class="type-practice">
    <h4>✍️ 실습: 도서 정보 JSON</h4>
    <pre class="code-block">
{
  "title": "해리포터와 마법사의 돌",
  "author": "J.K. 롤링",
  "year": 1997,
  "pages": 309,
  "available": true,
  "genres": ["판타지", "모험", "청소년"],
  "rating": 4.7,
  "publisher": {
    "name": "문학수첩",
    "country": "대한민국"
  },
  "ebook": null
}
    </pre>

    <div class="practice-check">
      <h5>🔍 타입 확인:</h5>
      <ul>
        <li><code>"title"</code>: <strong>문자열</strong></li>
        <li><code>"year"</code>: <strong>숫자</strong></li>
        <li><code>"available"</code>: <strong>불린</strong></li>
        <li><code>"genres"</code>: <strong>배열</strong></li>
        <li><code>"publisher"</code>: <strong>객체</strong></li>
        <li><code>"ebook"</code>: <strong>null</strong></li>
      </ul>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>4. JSON 만들기 실습</h2>

  <div class="practice-intro">
    <p>직접 JSON을 작성해봅시다!</p>
  </div>

  <div class="practice-steps">
    <div class="practice-step">
      <h4>📝 Step 1: 간단한 프로필</h4>
      <div class="step-content">
        <p><strong>목표:</strong> 자신의 프로필을 JSON으로 만들기</p>

        <div class="before-after">
          <div class="before">
            <h5>요구사항:</h5>
            <ul>
              <li>이름</li>
              <li>나이</li>
              <li>직업</li>
              <li>취미 (3개)</li>
            </ul>
          </div>

          <div class="after">
            <h5>정답 예시:</h5>
            <pre class="code-block">
{
  "name": "김도서",
  "age": 25,
  "job": "사서",
  "hobbies": [
    "독서",
    "영화감상",
    "코딩"
  ]
}
            </pre>
          </div>
        </div>
      </div>
    </div>

    <div class="practice-step">
      <h4>📚 Step 2: 도서관 장서 목록</h4>
      <div class="step-content">
        <p><strong>목표:</strong> 여러 권의 책을 배열로 표현하기</p>

        <pre class="code-block">
{
  "library": "중앙도서관",
  "books": [
    {
      "isbn": "978-89-01234-56-7",
      "title": "JSON 마스터",
      "author": "홍길동",
      "available": true,
      "borrowCount": 15
    },
    {
      "isbn": "978-89-12345-67-8",
      "title": "웹 API 개발",
      "author": "김영희",
      "available": false,
      "borrowCount": 23
    }
  ],
  "totalBooks": 2,
  "lastUpdate": "2024-01-15"
}
        </pre>
      </div>
    </div>

    <div class="practice-step">
      <h4>🌐 Step 3: API 응답 데이터</h4>
      <div class="step-content">
        <p><strong>목표:</strong> 실제 API 응답처럼 만들기</p>

        <pre class="code-block">
{
  "status": "success",
  "code": 200,
  "message": "검색 완료",
  "data": {
    "query": "JSON",
    "totalResults": 127,
    "results": [
      {
        "id": 1,
        "title": "JSON 완벽 가이드",
        "score": 0.95
      },
      {
        "id": 2,
        "title": "웹 개발과 JSON",
        "score": 0.87
      }
    ]
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
        </pre>

        <div class="api-structure">
          <h5>📋 일반적인 API 응답 구조:</h5>
          <ul>
            <li><code>status</code>: 성공/실패 상태</li>
            <li><code>code</code>: HTTP 상태 코드</li>
            <li><code>message</code>: 설명 메시지</li>
            <li><code>data</code>: 실제 데이터</li>
            <li><code>timestamp</code>: 응답 시간</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>5. JSON vs XML: 무엇이 다를까?</h2>

  <div class="comparison-intro">
    <p>같은 데이터를 JSON과 XML로 표현해보면 차이가 명확해집니다!</p>
  </div>

  <div class="side-by-side">
    <div class="comparison-example">
      <div class="format-box json-box">
        <h4>📦 JSON</h4>
        <pre class="code-block">
{
  "person": {
    "name": "김철수",
    "age": 25,
    "city": "서울",
    "hobbies": ["독서", "영화", "코딩"]
  }
}
        </pre>
        <div class="stats">
          <strong>크기:</strong> 약 100 바이트
        </div>
      </div>

      <div class="vs-divider">VS</div>

      <div class="format-box xml-box">
        <h4>📄 XML</h4>
        <pre class="code-block">
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;person&gt;
  &lt;name&gt;김철수&lt;/name&gt;
  &lt;age&gt;25&lt;/age&gt;
  &lt;city&gt;서울&lt;/city&gt;
  &lt;hobbies&gt;
    &lt;hobby&gt;독서&lt;/hobby&gt;
    &lt;hobby&gt;영화&lt;/hobby&gt;
    &lt;hobby&gt;코딩&lt;/hobby&gt;
  &lt;/hobbies&gt;
&lt;/person&gt;
        </pre>
        <div class="stats">
          <strong>크기:</strong> 약 200 바이트
        </div>
      </div>
    </div>
  </div>

  <table class="detailed-comparison">
    <thead>
      <tr>
        <th>비교 항목</th>
        <th>JSON</th>
        <th>XML</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>가독성</strong></td>
        <td>⭐⭐⭐⭐⭐ 매우 좋음</td>
        <td>⭐⭐⭐ 보통</td>
      </tr>
      <tr>
        <td><strong>파일 크기</strong></td>
        <td>⭐⭐⭐⭐⭐ 작음</td>
        <td>⭐⭐ 큼 (태그 반복)</td>
      </tr>
      <tr>
        <td><strong>배우기 쉬운 정도</strong></td>
        <td>⭐⭐⭐⭐⭐ 매우 쉬움</td>
        <td>⭐⭐⭐ 보통</td>
      </tr>
      <tr>
        <td><strong>JavaScript 연동</strong></td>
        <td>✅ 완벽 (네이티브 지원)</td>
        <td>⚠️ 파싱 필요</td>
      </tr>
      <tr>
        <td><strong>데이터 타입</strong></td>
        <td>✅ 명확 (숫자, 불린 등)</td>
        <td>❌ 모두 문자열</td>
      </tr>
      <tr>
        <td><strong>주석</strong></td>
        <td>❌ 지원 안 함</td>
        <td>✅ 지원 <code>&lt;!-- --&gt;</code></td>
      </tr>
      <tr>
        <td><strong>속성</strong></td>
        <td>❌ 없음</td>
        <td>✅ 있음 <code>&lt;tag attr="value"&gt;</code></td>
      </tr>
      <tr>
        <td><strong>네임스페이스</strong></td>
        <td>❌ 없음</td>
        <td>✅ 있음</td>
      </tr>
      <tr>
        <td><strong>스키마 검증</strong></td>
        <td>⚠️ JSON Schema 사용</td>
        <td>✅ XSD로 강력</td>
      </tr>
      <tr>
        <td><strong>용도</strong></td>
        <td>웹 API, 설정 파일, 데이터 교환</td>
        <td>문서, 복잡한 데이터, 레거시</td>
      </tr>
      <tr>
        <td><strong>속도</strong></td>
        <td>⭐⭐⭐⭐⭐ 빠름</td>
        <td>⭐⭐⭐ 보통</td>
      </tr>
    </tbody>
  </table>

  <div class="when-to-use">
    <h4>🎯 언제 무엇을 쓸까?</h4>
    <div class="use-cases">
      <div class="use-case json-use">
        <h5>JSON을 쓰세요</h5>
        <ul>
          <li>✅ REST API 개발할 때</li>
          <li>✅ 웹 애플리케이션 데이터 교환</li>
          <li>✅ 설정 파일 (간단한 경우)</li>
          <li>✅ NoSQL 데이터베이스 (MongoDB 등)</li>
          <li>✅ JavaScript와 작업할 때</li>
          <li>✅ 모바일 앱 API</li>
        </ul>
      </div>

      <div class="use-case xml-use">
        <h5>XML을 쓰세요</h5>
        <ul>
          <li>✅ 복잡한 문서 구조</li>
          <li>✅ 속성이 많이 필요할 때</li>
          <li>✅ 강력한 스키마 검증 필요</li>
          <li>✅ 레거시 시스템 연동</li>
          <li>✅ SOAP 웹서비스</li>
          <li>✅ 도서관 메타데이터 (MARC, MODS, METS)</li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>6. JSON 실제 활용 사례</h2>

  <div class="use-cases-intro">
    <p>JSON은 현대 웹에서 <strong>어디에나</strong> 있습니다!</p>
  </div>

  <div class="real-world-examples">
    <div class="example-card">
      <div class="example-icon">🌐</div>
      <h4>1. REST API</h4>
      <p class="example-desc">가장 일반적인 사용</p>

      <div class="example-code">
        <h5>요청 (Request):</h5>
        <pre class="code-mini">
POST /api/books
Content-Type: application/json

{
  "title": "JSON 마스터",
  "author": "홍길동",
  "isbn": "978-89-01234-56-7"
}
        </pre>

        <h5>응답 (Response):</h5>
        <pre class="code-mini">
{
  "status": "success",
  "data": {
    "id": 1234,
    "title": "JSON 마스터",
    "created": "2024-01-15"
  }
}
        </pre>
      </div>
    </div>

    <div class="example-card">
      <div class="example-icon">⚙️</div>
      <h4>2. 설정 파일</h4>
      <p class="example-desc">package.json, tsconfig.json 등</p>

      <div class="example-code">
        <h5>package.json 예시:</h5>
        <pre class="code-mini">
{
  "name": "my-library-app",
  "version": "1.0.0",
  "description": "도서관 관리 시스템",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.0",
    "mongoose": "^7.0.0"
  }
}
        </pre>
      </div>
    </div>

    <div class="example-card">
      <div class="example-icon">💾</div>
      <h4>3. NoSQL 데이터베이스</h4>
      <p class="example-desc">MongoDB의 기본 형식</p>

      <div class="example-code">
        <h5>MongoDB 문서:</h5>
        <pre class="code-mini">
{
  "_id": "507f1f77bcf86cd799439011",
  "title": "해리포터",
  "author": "J.K. 롤링",
  "borrowers": [
    {
      "userId": 1001,
      "name": "김철수",
      "borrowDate": "2024-01-10",
      "returnDate": null
    }
  ],
  "tags": ["판타지", "베스트셀러"]
}
        </pre>
      </div>
    </div>

    <div class="example-card">
      <div class="example-icon">🔐</div>
      <h4>4. JWT (인증 토큰)</h4>
      <p class="example-desc">사용자 인증 정보</p>

      <div class="example-code">
        <h5>JWT Payload (디코딩 후):</h5>
        <pre class="code-mini">
{
  "sub": "1234567890",
  "name": "김철수",
  "role": "librarian",
  "iat": 1516239022,
  "exp": 1516242622
}
        </pre>
      </div>
    </div>

    <div class="example-card">
      <div class="example-icon">📱</div>
      <h4>5. 모바일 앱 통신</h4>
      <p class="example-desc">앱 ↔ 서버 데이터 교환</p>

      <div class="example-code">
        <h5>도서 검색 결과:</h5>
        <pre class="code-mini">
{
  "query": "python",
  "results": [
    {
      "id": 1,
      "title": "파이썬 프로그래밍",
      "thumbnail": "https://...",
      "available": true
    }
  ],
  "totalCount": 127,
  "page": 1
}
        </pre>
      </div>
    </div>

    <div class="example-card">
      <div class="example-icon">🎨</div>
      <h4>6. 프론트엔드 상태 관리</h4>
      <p class="example-desc">Redux, Vuex 등</p>

      <div class="example-code">
        <h5>애플리케이션 상태:</h5>
        <pre class="code-mini">
{
  "user": {
    "id": 1,
    "name": "김철수",
    "isLoggedIn": true
  },
  "cart": {
    "items": [
      { "bookId": 101, "title": "JSON 가이드" }
    ],
    "total": 1
  },
  "ui": {
    "theme": "dark",
    "language": "ko"
  }
}
        </pre>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>7. JSON 작업하기: 코드 예제</h2>

  <div class="code-examples">
    <div class="lang-example">
      <h4>🟨 JavaScript</h4>

      <div class="code-section">
        <h5>문자열 → JSON (파싱)</h5>
        <pre class="code-block">
// JSON 문자열
const jsonString = '{"name":"김철수","age":25}';

// 파싱: 문자열을 객체로 변환
const obj = JSON.parse(jsonString);

console.log(obj.name);  // "김철수"
console.log(obj.age);   // 25
        </pre>
      </div>

      <div class="code-section">
        <h5>JSON → 문자열 (직렬화)</h5>
        <pre class="code-block">
// JavaScript 객체
const person = {
  name: "이영희",
  age: 28,
  hobbies: ["독서", "영화"]
};

// 직렬화: 객체를 문자열로 변환
const jsonString = JSON.stringify(person);

console.log(jsonString);
// {"name":"이영희","age":28,"hobbies":["독서","영화"]}

// 보기 좋게 들여쓰기
const prettyJson = JSON.stringify(person, null, 2);
console.log(prettyJson);
/*
{
  "name": "이영희",
  "age": 28,
  "hobbies": [
    "독서",
    "영화"
  ]
}
*/
        </pre>
      </div>
    </div>

    <div class="lang-example">
      <h4>🐍 Python</h4>

      <div class="code-section">
        <h5>JSON 다루기</h5>
        <pre class="code-block">
import json

# 문자열 → Python 딕셔너리
json_string = '{"name": "김철수", "age": 25}'
data = json.loads(json_string)
print(data["name"])  # 김철수

# Python 딕셔너리 → JSON 문자열
person = {
    "name": "이영희",
    "age": 28,
    "hobbies": ["독서", "영화"]
}

json_string = json.dumps(person, ensure_ascii=False, indent=2)
print(json_string)

# 파일로 저장
with open('person.json', 'w', encoding='utf-8') as f:
    json.dump(person, f, ensure_ascii=False, indent=2)

# 파일에서 읽기
with open('person.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(data)
        </pre>
      </div>
    </div>

    <div class="lang-example">
      <h4>📱 Fetch API (웹)</h4>

      <div class="code-section">
        <h5>JSON API 호출하기</h5>
        <pre class="code-block">
// GET 요청
fetch('https://api.example.com/books')
  .then(response => response.json())  // JSON 파싱
  .then(data => {
    console.log(data);
    // 데이터 사용
  });

// POST 요청 (JSON 전송)
const newBook = {
  title: "JSON 마스터",
  author: "홍길동",
  year: 2024
};

fetch('https://api.example.com/books', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(newBook)  // 객체를 JSON으로
})
  .then(response => response.json())
  .then(data => console.log('생성됨:', data));
        </pre>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>8. JSON 작성 팁과 주의사항</h2>

  <div class="tips-grid">
    <div class="tip-card do-card">
      <h4>✅ 해야 할 것 (DO)</h4>
      <ul>
        <li>
          <strong>쌍따옴표 사용</strong>
          <pre class="code-mini">{"name": "김철수"}  ✅</pre>
        </li>
        <li>
          <strong>마지막 항목 뒤 쉼표 없음</strong>
          <pre class="code-mini">
{
  "a": 1,
  "b": 2
}  ✅
          </pre>
        </li>
        <li>
          <strong>들여쓰기로 가독성 높이기</strong>
          <pre class="code-mini">
{
  "person": {
    "name": "김철수"
  }
}  ✅
          </pre>
        </li>
        <li>
          <strong>의미있는 키 이름</strong>
          <pre class="code-mini">{"userName": "kim"}  ✅</pre>
        </li>
      </ul>
    </div>

    <div class="tip-card dont-card">
      <h4>❌ 하지 말아야 할 것 (DON'T)</h4>
      <ul>
        <li>
          <strong>작은따옴표 사용</strong>
          <pre class="code-mini">{'name': 'kim'}  ❌</pre>
        </li>
        <li>
          <strong>trailing comma</strong>
          <pre class="code-mini">
{
  "a": 1,
  "b": 2,
}  ❌
          </pre>
        </li>
        <li>
          <strong>주석 추가</strong>
          <pre class="code-mini">
{
  // 이것은 주석
  "name": "kim"
}  ❌
          </pre>
        </li>
        <li>
          <strong>함수나 날짜 객체</strong>
          <pre class="code-mini">
{
  "func": function() {},
  "date": new Date()
}  ❌
          </pre>
        </li>
        <li>
          <strong>undefined 사용</strong>
          <pre class="code-mini">{"value": undefined}  ❌</pre>
          <p class="note">null을 사용하세요 ✅</p>
        </li>
      </ul>
    </div>
  </div>

  <div class="common-errors">
    <h4>🔧 자주 하는 실수와 해결법</h4>

    <div class="error-item">
      <div class="error-title">❌ 쉼표 빠뜨림</div>
      <pre class="code-bad">
{
  "name": "김철수"
  "age": 25
}
      </pre>
      <div class="arrow-fix">⬇️ 수정</div>
      <pre class="code-good">
{
  "name": "김철수",
  "age": 25
}
      </pre>
    </div>

    <div class="error-item">
      <div class="error-title">❌ 키에 따옴표 없음</div>
      <pre class="code-bad">
{
  name: "김철수"
}
      </pre>
      <div class="arrow-fix">⬇️ 수정</div>
      <pre class="code-good">
{
  "name": "김철수"
}
      </pre>
    </div>

    <div class="error-item">
      <div class="error-title">❌ 마지막 쉼표</div>
      <pre class="code-bad">
{
  "name": "김철수",
  "age": 25,
}
      </pre>
      <div class="arrow-fix">⬇️ 수정</div>
      <pre class="code-good">
{
  "name": "김철수",
  "age": 25
}
      </pre>
    </div>
  </div>

  <div class="validation-tools">
    <h4>🛠️ JSON 검증 도구</h4>
    <div class="tools-list">
      <div class="tool-item">
        <strong>JSONLint</strong>
        <p>온라인 JSON 검증 도구</p>
        <p class="url">jsonlint.com</p>
      </div>
      <div class="tool-item">
        <strong>VSCode</strong>
        <p>자동 검증 및 포맷팅</p>
        <p class="shortcut">Alt+Shift+F (포맷팅)</p>
      </div>
      <div class="tool-item">
        <strong>Chrome DevTools</strong>
        <p>Network 탭에서 JSON 확인</p>
        <p class="shortcut">F12 → Network</p>
      </div>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>9. 요약: 한눈에 정리</h2>

  <div class="summary-grid">
    <div class="summary-main">
      <h3>📦 JSON이란?</h3>
      <p class="definition">
        사람과 컴퓨터 모두 읽기 쉬운 <strong>텍스트 기반 데이터 형식</strong>
      </p>

      <div class="key-points">
        <div class="point">
          <strong>구조:</strong> 객체 { } 와 배열 [ ]
        </div>
        <div class="point">
          <strong>타입:</strong> 문자열, 숫자, 불린, null, 객체, 배열
        </div>
        <div class="point">
          <strong>특징:</strong> 간결, 빠름, JavaScript 친화적
        </div>
        <div class="point">
          <strong>용도:</strong> API, 설정, 데이터베이스, 앱 통신
        </div>
      </div>
    </div>

    <div class="summary-comparison">
      <h4>JSON vs XML</h4>
      <table class="mini-table">
        <tr>
          <td><strong>JSON</strong></td>
          <td>간결, 빠름, 웹 API</td>
        </tr>
        <tr>
          <td><strong>XML</strong></td>
          <td>복잡, 문서, 레거시</td>
        </tr>
      </table>
    </div>
  </div>

  <div class="quick-reference">
    <h4>⚡ 빠른 참조</h4>
    <div class="ref-grid">
      <div class="ref-item">
        <strong>객체</strong>
        <pre class="code-tiny">{"key": "value"}</pre>
      </div>
      <div class="ref-item">
        <strong>배열</strong>
        <pre class="code-tiny">[1, 2, 3]</pre>
      </div>
      <div class="ref-item">
        <strong>중첩</strong>
        <pre class="code-tiny">{"a": [1, 2]}</pre>
      </div>
      <div class="ref-item">
        <strong>파싱</strong>
        <pre class="code-tiny">JSON.parse(str)</pre>
      </div>
      <div class="ref-item">
        <strong>직렬화</strong>
        <pre class="code-tiny">JSON.stringify(obj)</pre>
      </div>
      <div class="ref-item">
        <strong>주의</strong>
        <pre class="code-tiny">쌍따옴표, 마지막 쉼표 ✗</pre>
      </div>
    </div>
  </div>

  <div class="final-message">
    <h3>🎯 핵심 메시지</h3>
    <div class="message-box">
      <p class="big-text">
        <strong>JSON = 현대 웹의 표준 데이터 형식</strong>
      </p>
      <p>
        간단하고, 빠르고, 읽기 쉬운 JSON은<br>
        오늘날 거의 모든 웹 API와 앱에서 사용됩니다.
      </p>
      <p class="action">
        💡 지금 바로 JSON을 작성해보세요!
      </p>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>10. 학습 점검 퀴즈</h2>

  <div class="quiz-section">
    <div class="quiz-item">
      <p><strong>Q1.</strong> JSON에서 문자열을 표현할 때 무엇을 사용하나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>쌍따옴표 (double quotes)</strong>만 사용합니다. 작은따옴표는 안 됩니다!<br>
        예: <code>"안녕하세요"</code> ✅ | <code>'안녕하세요'</code> ❌</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> JSON의 6가지 데이터 타입은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>문자열, 숫자, 불린, null, 객체, 배열</strong></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> 다음 중 올바른 JSON은?</p>
      <pre class="code-mini">
A) {"name": "김철수", "age": 25,}
B) {'name': '김철수', 'age': 25}
C) {"name": "김철수", "age": 25}
      </pre>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>C번</strong>이 정답입니다!<br>
        A는 마지막 쉼표 때문에 ❌<br>
        B는 작은따옴표 때문에 ❌</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> JSON과 XML의 가장 큰 차이점은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ JSON은 <strong>훨씬 간결하고 가볍습니다</strong>. 같은 데이터를 표현해도 JSON이 XML보다 파일 크기가 작고, 읽기 쉽고, 파싱도 빠릅니다. 또한 JavaScript에서 네이티브로 지원됩니다.</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> JavaScript에서 문자열을 JSON 객체로 변환하는 함수는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <code>JSON.parse(문자열)</code><br>
        반대로 객체를 문자열로는 <code>JSON.stringify(객체)</code></p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q6.</strong> JSON에서 주석을 추가할 수 있나요?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ <strong>아니요</strong>, JSON은 주석을 지원하지 않습니다. 주석이 필요하면 별도 문서로 작성하거나, JSONC (JSON with Comments) 같은 확장 형식을 사용해야 합니다.</p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 더 알아보기</h2>
  <ul>
    <li><strong>JSON 공식 사이트</strong> - json.org</li>
    <li><strong>JSONLint</strong> - JSON 검증 도구</li>
    <li><strong>JSON Schema</strong> - JSON 구조 정의 및 검증</li>
    <li><strong>MDN JSON 가이드</strong> - Mozilla 개발자 문서</li>
    <li><strong>JSONPlaceholder</strong> - 테스트용 무료 JSON API</li>
  </ul>
</div>

<style>
.content-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.hero-definition {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2.5rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
}

.hero-definition h3,
.hero-definition p {
  color: white;
}

.big-statement {
  font-size: 1.4rem;
  line-height: 1.8;
  margin: 1rem 0;
}

.json-intro {
  margin: 2rem 0;
}

.timeline-story {
  background: white;
  padding: 2rem;
  border-radius: 8px;
}

.story-item {
  margin: 1.5rem 0;
}

.year {
  font-weight: bold;
  color: #1976d2;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.situation {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 4px;
}

.problem {
  color: #d32f2f;
  font-weight: bold;
  margin-bottom: 1rem;
}

.solution {
  color: #388e3c;
  font-weight: bold;
  margin-bottom: 1rem;
}

.example-bad,
.example-good {
  background: #263238;
  color: #ff6b6b;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  margin: 0.5rem 0;
}

.example-good {
  color: #69db7c;
}

.benefit {
  margin-top: 1rem;
  color: #388e3c;
  font-weight: bold;
}

.arrow-down {
  text-align: center;
  font-size: 2rem;
  color: #4caf50;
  margin: 1rem 0;
}

.syntax-intro {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  font-size: 1.1rem;
  margin: 2rem 0;
}

.syntax-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin: 2rem 0;
}

.syntax-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  position: relative;
  border: 3px solid #ddd;
}

.object-card {
  border-color: #2196f3;
}

.array-card {
  border-color: #4caf50;
}

.card-number {
  position: absolute;
  top: -15px;
  left: 15px;
  width: 40px;
  height: 40px;
  background: #1976d2;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
}

.syntax-card h4 {
  color: #1976d2;
  margin: 1rem 0 0.5rem 0;
}

.card-desc {
  color: #666;
  margin-bottom: 1rem;
}

.syntax-example {
  margin: 1.5rem 0;
}

.code-block {
  background: #263238;
  color: #aed581;
  padding: 1.5rem;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  line-height: 1.6;
  margin: 0;
}

.syntax-rules {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.syntax-rules h5 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.syntax-rules code {
  background: #263238;
  color: #aed581;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
}

.real-example {
  background: #fff3e0;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.real-example h5 {
  color: #e65100;
  margin-bottom: 0.75rem;
}

.combine-example {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
  color: white;
}

.combine-example h4,
.combine-example p {
  color: white;
}

.types-intro {
  background: #e8f5e9;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  font-size: 1.1rem;
  margin: 2rem 0;
}

.types-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin: 2rem 0;
}

.type-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #ddd;
  text-align: center;
}

.type-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.type-card h4 {
  color: #1976d2;
  margin: 0.5rem 0;
}

.type-desc {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.code-mini {
  background: #263238;
  color: #aed581;
  padding: 0.75rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
  text-align: left;
  margin: 0.5rem 0;
}

.type-note {
  background: #fff3e0;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 0.75rem;
  font-size: 0.85rem;
  text-align: left;
}

.type-practice {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.practice-check {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1.5rem;
}

.practice-check h5 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.practice-intro {
  background: #e8f5e9;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  font-size: 1.1rem;
  margin: 2rem 0;
}

.practice-steps {
  margin: 2rem 0;
}

.practice-step {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
  border-left: 4px solid #4caf50;
}

.practice-step h4 {
  color: #2e7d32;
  margin-bottom: 1rem;
}

.step-content {
  margin-top: 1rem;
}

.before-after {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 1.5rem 0;
}

.before,
.after {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 4px;
}

.before h5,
.after h5 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.api-structure {
  background: #fff3e0;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1.5rem;
}

.api-structure h5 {
  color: #e65100;
  margin-bottom: 1rem;
}

.comparison-intro {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  font-size: 1.1rem;
  margin: 2rem 0;
}

.side-by-side {
  margin: 2rem 0;
}

.comparison-example {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin: 2rem 0;
}

.format-box {
  flex: 1;
  padding: 1.5rem;
  border-radius: 8px;
}

.json-box {
  background: #e8f5e9;
  border: 3px solid #4caf50;
}

.xml-box {
  background: #fff3e0;
  border: 3px solid #ff9800;
}

.format-box h4 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.stats {
  background: white;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 1rem;
  text-align: center;
}

.vs-divider {
  font-size: 2rem;
  font-weight: bold;
  color: #666;
}

.detailed-comparison {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  background: white;
}

.detailed-comparison th,
.detailed-comparison td {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

.detailed-comparison th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.detailed-comparison tr:nth-child(even) {
  background: #f5f5f5;
}

.when-to-use {
  margin: 2rem 0;
}

.use-cases {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin-top: 1.5rem;
}

.use-case {
  padding: 1.5rem;
  border-radius: 8px;
}

.json-use {
  background: #e8f5e9;
  border: 3px solid #4caf50;
}

.xml-use {
  background: #fff3e0;
  border: 3px solid #ff9800;
}

.use-case h5 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.use-cases-intro {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  font-size: 1.1rem;
  margin: 2rem 0;
}

.real-world-examples {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin: 2rem 0;
}

.example-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #ddd;
}

.example-icon {
  font-size: 3rem;
  text-align: center;
  margin-bottom: 1rem;
}

.example-card h4 {
  color: #1976d2;
  margin-bottom: 0.5rem;
}

.example-desc {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.example-code {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.example-code h5 {
  color: #333;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.code-examples {
  margin: 2rem 0;
}

.lang-example {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
  border-left: 4px solid #4caf50;
}

.lang-example h4 {
  color: #2e7d32;
  margin-bottom: 1.5rem;
}

.code-section {
  margin: 1.5rem 0;
}

.code-section h5 {
  color: #1976d2;
  margin-bottom: 0.75rem;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  margin: 2rem 0;
}

.tip-card {
  padding: 2rem;
  border-radius: 8px;
}

.do-card {
  background: #e8f5e9;
  border: 3px solid #4caf50;
}

.dont-card {
  background: #ffebee;
  border: 3px solid #f44336;
}

.do-card h4 {
  color: #2e7d32;
  margin-bottom: 1.5rem;
}

.dont-card h4 {
  color: #c62828;
  margin-bottom: 1.5rem;
}

.tip-card ul {
  list-style: none;
  padding: 0;
}

.tip-card li {
  margin: 1.5rem 0;
}

.note {
  font-size: 0.85rem;
  color: #666;
  margin-top: 0.25rem;
}

.common-errors {
  background: #fff3e0;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.common-errors h4 {
  color: #e65100;
  margin-bottom: 1.5rem;
}

.error-item {
  background: white;
  padding: 1.5rem;
  border-radius: 4px;
  margin: 1.5rem 0;
}

.error-title {
  color: #d32f2f;
  font-weight: bold;
  margin-bottom: 0.75rem;
}

.code-bad {
  background: #ffebee;
  border-left: 4px solid #f44336;
  padding: 1rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  margin: 0.5rem 0;
}

.arrow-fix {
  text-align: center;
  font-size: 1.5rem;
  color: #4caf50;
  margin: 0.5rem 0;
  font-weight: bold;
}

.code-good {
  background: #e8f5e9;
  border-left: 4px solid #4caf50;
  padding: 1rem;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  margin: 0.5rem 0;
}

.validation-tools {
  background: #e3f2fd;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.validation-tools h4 {
  color: #1976d2;
  margin-bottom: 1.5rem;
}

.tools-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.tool-item {
  background: white;
  padding: 1.5rem;
  border-radius: 4px;
  text-align: center;
}

.tool-item strong {
  color: #1976d2;
  font-size: 1.1rem;
}

.url,
.shortcut {
  font-size: 0.85rem;
  color: #666;
  margin-top: 0.5rem;
  font-family: monospace;
}

.summary-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
}

.summary-main {
  background: white;
  padding: 2rem;
  border: 3px solid #4caf50;
  border-radius: 8px;
}

.definition {
  font-size: 1.1rem;
  color: #333;
  margin: 1rem 0;
}

.key-points {
  display: grid;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.point {
  background: #f5f5f5;
  padding: 0.75rem;
  border-radius: 4px;
}

.summary-comparison {
  background: #e3f2fd;
  padding: 1.5rem;
  border-radius: 8px;
}

.mini-table {
  width: 100%;
  margin-top: 1rem;
  font-size: 0.9rem;
}

.mini-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #ddd;
}

.quick-reference {
  background: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
}

.quick-reference h4 {
  color: #1976d2;
  margin-bottom: 1.5rem;
}

.ref-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.ref-item {
  background: white;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
}

.ref-item strong {
  color: #1976d2;
  font-size: 0.9rem;
}

.code-tiny {
  background: #263238;
  color: #aed581;
  padding: 0.5rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.75rem;
  margin-top: 0.5rem;
  display: block;
}

.final-message {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  margin: 2rem 0;
}

.final-message h3,
.final-message p {
  color: white;
}

.message-box {
  background: rgba(255,255,255,0.2);
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.big-text {
  font-size: 1.5rem;
  margin: 1rem 0;
}

.action {
  font-size: 1.1rem;
  margin-top: 1rem;
}

.quiz-section {
  background: #f1f8e9;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 1rem 0;
}

.quiz-item {
  background: white;
  padding: 1rem;
  margin: 0.75rem 0;
  border-radius: 4px;
  border-left: 3px solid #8bc34a;
}

.quiz-item details {
  margin-top: 0.5rem;
}

.quiz-item summary {
  cursor: pointer;
  color: #558b2f;
  font-weight: bold;
}

h2 {
  color: #1565c0;
  border-bottom: 2px solid #1565c0;
  padding-bottom: 0.5rem;
  margin-top: 2rem;
}

h3 {
  color: #1976d2;
  margin-top: 1.5rem;
}

h4 {
  color: #1e88e5;
  margin-top: 1rem;
}

ul {
  line-height: 1.8;
}

strong {
  color: #0d47a1;
}

code {
  background: #263238;
  color: #aed581;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

@media (max-width: 1024px) {
  .syntax-grid,
  .types-grid,
  .use-cases,
  .real-world-examples,
  .tips-grid,
  .tools-list,
  .ref-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .comparison-example,
  .before-after,
  .summary-grid,
  .syntax-grid,
  .types-grid,
  .use-cases,
  .real-world-examples,
  .tips-grid,
  .tools-list,
  .ref-grid {
    grid-template-columns: 1fr;
  }

  .vs-divider {
    transform: rotate(90deg);
  }
}
</style>
        """,
        category=json_category,
        author=admin,
        difficulty='BASIC',
        estimated_time=25,
        prerequisites="없음",
        learning_objectives="JSON의 기본 개념과 문법 이해하기, JSON 데이터를 직접 작성하고 읽을 수 있기, JSON과 XML의 차이점 명확히 알기, JSON이 실제로 어떻게 활용되는지 파악하기, JavaScript와 Python에서 JSON 다루는 방법 배우기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {json_category.name} (상위: {web_docs_category.name})")
    print(f"  - 난이도: 초급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=web-docs")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_json_content()
