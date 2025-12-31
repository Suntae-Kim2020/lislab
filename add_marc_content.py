#!/usr/bin/env python
"""
MARC21 학습 콘텐츠 추가 스크립트
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

def create_marc_content():
    # Admin 사용자 가져오기
    admin = User.objects.filter(is_superuser=True).first()
    if not admin:
        print("❌ Admin 사용자를 찾을 수 없습니다.")
        return
    print("✓ Admin 사용자 확인")

    # 상위 카테고리 생성 또는 가져오기: 메타데이터
    metadata_category, created = Category.objects.get_or_create(
        slug='metadata',
        defaults={
            'name': '메타데이터',
            'description': '도서관 메타데이터 표준과 포맷',
            'parent': None
        }
    )
    if created:
        print("✓ 상위 카테고리 생성: 메타데이터")
    else:
        print("✓ 상위 카테고리 확인: 메타데이터")

    # 하위 카테고리 생성 또는 가져오기: MARC21
    marc_category, created = Category.objects.get_or_create(
        slug='marc21',
        defaults={
            'name': 'MARC21',
            'description': 'MARC21 메타데이터 포맷',
            'parent': metadata_category
        }
    )
    if created:
        print("✓ 하위 카테고리 생성: MARC21")
    else:
        print("✓ 하위 카테고리 확인: MARC21")

    # 태그 생성 또는 가져오기
    tag_data = [
        {'name': '메타데이터 포맷', 'slug': 'metadata-format'},
        {'name': '인코딩포맷', 'slug': 'encoding-format'},
        {'name': '교환포맷', 'slug': 'exchange-format'}
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
        title="MARC21 완벽 가이드: 도서관 메타데이터의 표준",
        slug="marc21-complete-guide",
        summary="도서관 서지데이터의 국제 표준 MARC21의 구조와 활용법을 실전 예제와 함께 배웁니다.",
        content_html="""
<div class="content-section">
  <h2>🎯 학습 목표</h2>
  <ul>
    <li>MARC21이 무엇인지, 왜 중요한지 이해하기</li>
    <li>MARC21 레코드의 구조 파악하기</li>
    <li>주요 필드와 서브필드 활용법 익히기</li>
    <li>실전 예제로 MARC21 레코드 읽고 작성하기</li>
  </ul>
</div>

<div class="content-section">
  <h2>1. MARC21이란?</h2>

  <h3>📚 MARC의 탄생</h3>
  <p><strong>MARC (MAchine-Readable Cataloging)</strong>은 1960년대 미국 의회도서관(Library of Congress)에서 개발한 <strong>기계가 읽을 수 있는 목록 형식</strong>입니다.</p>

  <div class="highlight-box">
    <h4>왜 MARC가 필요했을까?</h4>
    <p>과거 도서관은 카드 목록을 수작업으로 만들었습니다. 컴퓨터 시대가 도래하면서 서지정보를 컴퓨터로 처리하고 도서관끼리 데이터를 교환할 필요가 생겼습니다.</p>
    <ul>
      <li><strong>문제</strong>: 각 도서관마다 다른 형식으로 데이터 저장</li>
      <li><strong>해결</strong>: 표준화된 형식 = MARC</li>
    </ul>
  </div>

  <h3>🌍 MARC21의 특징</h3>
  <ul>
    <li><strong>국제 표준</strong>: 전 세계 도서관이 사용하는 메타데이터 교환 포맷</li>
    <li><strong>ISO 2709 기반</strong>: 국제 표준 규격을 따름</li>
    <li><strong>다양한 자료 유형</strong>: 도서, 연속간행물, 지도, 악보, 시청각자료 등</li>
    <li><strong>MARC21 포맷</strong>: 1999년 USMARC와 CAN/MARC 통합</li>
  </ul>
</div>

<div class="content-section">
  <h2>2. MARC21 레코드 구조</h2>

  <p>MARC21 레코드는 <strong>3개의 주요 부분</strong>으로 구성됩니다:</p>

  <div class="structure-diagram">
    <pre>
┌──────────────┐
│   Leader     │ ← 24바이트 고정길이 (레코드 전체 정보)
├──────────────┤
│  Directory   │ ← 가변길이 (각 필드의 위치 정보)
├──────────────┤
│ Variable     │
│  Control     │ ← 00X 필드 (제어 필드)
│   Fields     │
├──────────────┤
│ Variable     │
│   Data       │ ← 01X-9XX 필드 (데이터 필드)
│   Fields     │
└──────────────┘
    </pre>
  </div>

  <h3>① Leader (리더)</h3>
  <p>레코드 전체에 대한 정보를 담은 <strong>24바이트 고정길이</strong> 필드입니다.</p>
  <pre class="code-block">
예시: 00725cam a2200205 a 4500

00-04: 00725  → 레코드 길이 (725바이트)
05:    c      → 레코드 상태 (c=수정됨)
06:    a      → 자료 유형 (a=언어자료)
07:    m      → 서지 레벨 (m=단행본)
  </pre>

  <h3>② Directory (디렉토리)</h3>
  <p>각 필드의 <strong>태그, 길이, 시작 위치</strong>를 기록하는 색인입니다.</p>
  <pre class="code-block">
245004000110  → 245 필드, 40바이트, 110번째 위치에서 시작
100001700151  → 100 필드, 17바이트, 151번째 위치에서 시작
  </pre>

  <h3>③ Variable Fields (가변 필드)</h3>
  <p>실제 서지 데이터를 담고 있는 부분입니다.</p>

  <h4>📌 제어 필드 (00X)</h4>
  <ul>
    <li><strong>001</strong>: 제어번호</li>
    <li><strong>005</strong>: 최종 수정 일시</li>
    <li><strong>008</strong>: 고정길이 데이터 요소 (출판연도, 국가 등)</li>
  </ul>

  <h4>📌 데이터 필드 (01X-9XX)</h4>
  <p>데이터 필드는 <strong>지시기호(Indicators)</strong>와 <strong>서브필드(Subfields)</strong>로 구성됩니다.</p>
</div>

<div class="content-section">
  <h2>3. 주요 MARC21 필드</h2>

  <h3>📖 자주 사용하는 필드들</h3>

  <table class="data-table">
    <thead>
      <tr>
        <th>필드</th>
        <th>이름</th>
        <th>설명</th>
        <th>예시</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>020</strong></td>
        <td>ISBN</td>
        <td>국제표준도서번호</td>
        <td>$a 978-89-546-5050-4</td>
      </tr>
      <tr>
        <td><strong>100</strong></td>
        <td>개인저자</td>
        <td>주저자명</td>
        <td>1# $a 조남주</td>
      </tr>
      <tr>
        <td><strong>245</strong></td>
        <td>표제</td>
        <td>본표제와 책임표시</td>
        <td>10 $a 82년생 김지영 / $c 조남주 지음</td>
      </tr>
      <tr>
        <td><strong>250</strong></td>
        <td>판사항</td>
        <td>판 정보</td>
        <td>## $a 개정판</td>
      </tr>
      <tr>
        <td><strong>260</strong></td>
        <td>발행사항</td>
        <td>출판 정보 (구)</td>
        <td>## $a 서울 : $b 민음사, $c 2016</td>
      </tr>
      <tr>
        <td><strong>264</strong></td>
        <td>제작/발행사항</td>
        <td>출판 정보 (신)</td>
        <td>#1 $a 서울 : $b 민음사, $c 2016</td>
      </tr>
      <tr>
        <td><strong>300</strong></td>
        <td>형태사항</td>
        <td>면수, 크기 등</td>
        <td>## $a 192 p. ; $c 19 cm</td>
      </tr>
      <tr>
        <td><strong>650</strong></td>
        <td>주제명</td>
        <td>주제 접근점</td>
        <td>#0 $a 한국소설</td>
      </tr>
    </tbody>
  </table>

  <h3>🔍 지시기호(Indicators)와 서브필드(Subfields)</h3>

  <div class="example-box">
    <h4>245 필드 상세 분석</h4>
    <pre class="code-block">
245 10 $a 82년생 김지영 / $c 조남주 지음.
│   │  │                │
│   │  │                └─ $c: 책임표시
│   │  └──────────────────── $a: 본표제
│   └─────────────────────── 두 번째 지시기호 (0=표제에 관사 없음)
└─────────────────────────── 첫 번째 지시기호 (1=저록 작성)
    </pre>

    <p><strong>지시기호</strong>: 필드의 처리 방법을 지정 (2자리, 0-9 또는 #)</p>
    <p><strong>서브필드</strong>: 필드 내 세부 데이터 구분 ($ + 영문자/숫자)</p>
  </div>
</div>

<div class="content-section">
  <h2>4. 실전 예제: 완전한 MARC21 레코드</h2>

  <div class="example-book">
    <h3>📕 예제 도서: "82년생 김지영"</h3>
    <ul>
      <li>저자: 조남주</li>
      <li>출판사: 민음사</li>
      <li>출판연도: 2016</li>
      <li>ISBN: 978-89-546-5050-4</li>
      <li>면수: 192쪽, 19cm</li>
    </ul>
  </div>

  <h4>완성된 MARC21 레코드</h4>
  <pre class="code-block">
=LDR  00725cam a2200205 a 4500
=001  KMO201600123
=005  20161015120000.0
=008  161015s2016\\\\ulk\\\\\\\\\\\000\1\kor\d

=020  \\$a 9788954650504 $g 03810
=040  \\$a 211009 $c 211009 $d 211009
=041  0\$a kor
=082  04$a 813.7 $2 23
=090  \\$a 813.7 $b 조211ㅍ

=100  1\$a 조남주
=245  10$a 82년생 김지영 / $c 조남주 지음.
=260  \\$a 서울 : $b 민음사, $c 2016.
=300  \\$a 192 p. ; $c 19 cm.

=650  \0$a 한국소설
=650  \0$a 장편소설
=655  \7$a 소설 $2 lcgft

=900  1\$a 조남주, $e 저
=945  \\$a KDC5
  </pre>

  <h4>🔎 필드별 해설</h4>
  <table class="data-table">
    <thead>
      <tr>
        <th>필드</th>
        <th>내용</th>
        <th>설명</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>LDR</strong></td>
        <td>00725cam a2200205 a 4500</td>
        <td>레코드 길이 725바이트, 언어자료, 단행본</td>
      </tr>
      <tr>
        <td><strong>001</strong></td>
        <td>KMO201600123</td>
        <td>제어번호</td>
      </tr>
      <tr>
        <td><strong>005</strong></td>
        <td>20161015120000.0</td>
        <td>최종 수정: 2016년 10월 15일 12시</td>
      </tr>
      <tr>
        <td><strong>008</strong></td>
        <td>161015s2016\\\\ulk...</td>
        <td>입력일, 출판연도, 국가코드(한국) 등</td>
      </tr>
      <tr>
        <td><strong>020</strong></td>
        <td>$a 9788954650504 $g 03810</td>
        <td>ISBN과 부가기호</td>
      </tr>
      <tr>
        <td><strong>082</strong></td>
        <td>$a 813.7</td>
        <td>듀이십진분류번호(DDC)</td>
      </tr>
      <tr>
        <td><strong>090</strong></td>
        <td>$a 813.7 $b 조211ㅍ</td>
        <td>청구기호</td>
      </tr>
      <tr>
        <td><strong>100</strong></td>
        <td>$a 조남주</td>
        <td>개인저자</td>
      </tr>
      <tr>
        <td><strong>245</strong></td>
        <td>$a 82년생 김지영 / $c 조남주 지음.</td>
        <td>표제와 책임표시</td>
      </tr>
      <tr>
        <td><strong>260</strong></td>
        <td>$a 서울 : $b 민음사, $c 2016.</td>
        <td>출판지, 출판사, 출판연도</td>
      </tr>
      <tr>
        <td><strong>300</strong></td>
        <td>$a 192 p. ; $c 19 cm.</td>
        <td>면수와 크기</td>
      </tr>
      <tr>
        <td><strong>650</strong></td>
        <td>$a 한국소설, 장편소설</td>
        <td>주제명</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="content-section">
  <h2>5. MARC21의 장단점</h2>

  <h3>✅ 장점</h3>
  <ul>
    <li><strong>범용성</strong>: 전 세계 도서관이 사용하는 표준</li>
    <li><strong>호환성</strong>: 시스템 간 데이터 교환 용이</li>
    <li><strong>완성도</strong>: 다양한 자료 유형과 상세한 서지정보 표현 가능</li>
    <li><strong>검증된 시스템</strong>: 60년 이상의 역사와 노하우</li>
  </ul>

  <h3>❌ 단점</h3>
  <ul>
    <li><strong>복잡성</strong>: 배우기 어렵고 유지보수 비용 높음</li>
    <li><strong>구시대 포맷</strong>: 1960년대 설계로 현대 웹 환경에 부적합</li>
    <li><strong>가독성 낮음</strong>: 사람이 읽기 어려운 인코딩 방식</li>
    <li><strong>확장성 제한</strong>: 새로운 요구사항 대응 어려움</li>
  </ul>
</div>

<div class="content-section">
  <h2>6. MARC21의 미래</h2>

  <h3>🌐 BIBFRAME으로의 전환</h3>
  <p>미국 의회도서관은 MARC21을 대체할 <strong>BIBFRAME (Bibliographic Framework)</strong>을 개발하고 있습니다.</p>

  <div class="comparison-table">
    <h4>MARC21 vs BIBFRAME</h4>
    <table class="data-table">
      <thead>
        <tr>
          <th>특성</th>
          <th>MARC21</th>
          <th>BIBFRAME</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>기술방식</strong></td>
          <td>고정/가변 필드</td>
          <td>RDF 그래프</td>
        </tr>
        <tr>
          <td><strong>데이터 모델</strong></td>
          <td>평면 레코드</td>
          <td>연결된 개체</td>
        </tr>
        <tr>
          <td><strong>웹 친화성</strong></td>
          <td>낮음</td>
          <td>높음 (Linked Data)</td>
        </tr>
        <tr>
          <td><strong>확장성</strong></td>
          <td>제한적</td>
          <td>유연함</td>
        </tr>
        <tr>
          <td><strong>현재 상태</strong></td>
          <td>주력 사용</td>
          <td>전환 준비 중</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="highlight-box">
    <h4>💡 그래도 MARC21을 배워야 하는 이유</h4>
    <ul>
      <li>전 세계 대부분의 도서관이 여전히 MARC21 사용</li>
      <li>수십억 건의 기존 MARC 레코드 존재</li>
      <li>BIBFRAME으로의 전환은 점진적으로 진행 (향후 10년+)</li>
      <li>MARC21 이해가 BIBFRAME 이해의 기초</li>
    </ul>
  </div>
</div>

<div class="content-section">
  <h2>7. 실습: MARC21 레코드 작성하기</h2>

  <div class="practice-box">
    <h3>📝 연습 문제</h3>
    <p>다음 도서 정보를 MARC21 레코드로 작성해보세요:</p>

    <div class="book-info">
      <ul>
        <li><strong>표제</strong>: 해리 포터와 마법사의 돌</li>
        <li><strong>저자</strong>: J. K. 롤링</li>
        <li><strong>역자</strong>: 김혜원</li>
        <li><strong>출판사</strong>: 문학수첩</li>
        <li><strong>출판연도</strong>: 1999</li>
        <li><strong>ISBN</strong>: 978-89-8392-028-1</li>
        <li><strong>면수</strong>: 416쪽</li>
        <li><strong>크기</strong>: 22 cm</li>
        <li><strong>주제</strong>: 영국소설, 판타지소설</li>
      </ul>
    </div>

    <details>
      <summary><strong>💡 정답 확인하기</strong></summary>
      <pre class="code-block">
=LDR  00823cam a2200265 a 4500
=001  KMO199900456
=008  990615s1999\\\\ulk\\\\\\\\\\\000\1\kor\d

=020  \\$a 9788983920281
=041  1\$a kor $h eng
=082  04$a 823.914 $2 23
=090  \\$a 823.914 $b 롤239ㅎ

=100  1\$a Rowling, J. K.
=245  10$a 해리 포터와 마법사의 돌 / $c J. K. 롤링 지음 ; 김혜원 옮김.
=260  \\$a 서울 : $b 문학수첩, $c 1999.
=300  \\$a 416 p. ; $c 22 cm.

=650  \0$a 영국소설
=650  \0$a 판타지소설
=700  1\$a 김혜원, $e 역

=740  0\$a Harry Potter and the philosopher's stone
      </pre>

      <p><strong>주요 포인트:</strong></p>
      <ul>
        <li>041 필드: 번역서이므로 원어(영어)와 번역어(한국어) 명시</li>
        <li>100 필드: 원저자명을 로마자 표기</li>
        <li>700 필드: 역자 정보 추가</li>
        <li>740 필드: 원표제 추가</li>
      </ul>
    </details>
  </div>
</div>

<div class="content-section">
  <h2>8. 요약 및 학습 점검</h2>

  <div class="summary-box">
    <h3>📌 핵심 요약</h3>
    <ol>
      <li><strong>MARC21</strong>은 도서관 서지데이터의 국제 표준 교환 포맷</li>
      <li>레코드 구조: <strong>Leader + Directory + Variable Fields</strong></li>
      <li>필드 구성: <strong>태그 + 지시기호 + 서브필드</strong></li>
      <li>주요 필드: 100(저자), 245(표제), 260/264(출판), 300(형태)</li>
      <li>현재는 MARC21이 주력이지만 <strong>BIBFRAME으로 전환 중</strong></li>
    </ol>
  </div>

  <div class="quiz-section">
    <h3>🎯 학습 점검 퀴즈</h3>

    <div class="quiz-item">
      <p><strong>Q1.</strong> MARC21 레코드의 세 가지 주요 구성 요소는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ Leader(리더), Directory(디렉토리), Variable Fields(가변 필드)</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q2.</strong> 245 필드는 무엇을 나타내는가?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ 표제(Title Statement) - 도서의 제목과 책임표시</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q3.</strong> "$a"와 "$c"는 무엇을 의미하는가?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ 서브필드 코드 ($a: 주저자명/본표제, $c: 책임표시 등 필드마다 다름)</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q4.</strong> MARC21의 후속 포맷으로 개발 중인 것은?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ BIBFRAME (Bibliographic Framework)</p>
      </details>
    </div>

    <div class="quiz-item">
      <p><strong>Q5.</strong> 제어 필드(00X)와 데이터 필드(01X-9XX)의 차이는?</p>
      <details>
        <summary>정답 보기</summary>
        <p>✓ 제어 필드는 지시기호와 서브필드가 없고, 데이터 필드는 지시기호(2자리)와 서브필드($)를 가짐</p>
      </details>
    </div>
  </div>
</div>

<div class="content-section">
  <h2>📚 추가 학습 자료</h2>
  <ul>
    <li><strong>MARC 21 Format for Bibliographic Data</strong> - Library of Congress 공식 문서</li>
    <li><strong>국가서지 LOD</strong> - 국립중앙도서관 MARC 데이터</li>
    <li><strong>OCLC Bibliographic Formats and Standards</strong> - 실무 가이드</li>
    <li><strong>KORMARC</strong> - 한국문헌자동화목록형식 (한국형 MARC)</li>
  </ul>
</div>

<style>
.content-section {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.highlight-box, .example-box, .practice-box, .summary-box {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
}

.structure-diagram, .code-block {
  background: #263238;
  color: #aed581;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', monospace;
  font-size: 0.9rem;
  line-height: 1.5;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  background: white;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 0.75rem;
  text-align: left;
}

.data-table th {
  background: #1976d2;
  color: white;
  font-weight: bold;
}

.data-table tr:nth-child(even) {
  background: #f5f5f5;
}

.example-book {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
}

.book-info {
  background: #fff;
  padding: 1rem;
  border-radius: 4px;
  margin: 0.5rem 0;
}

.comparison-table {
  margin: 1rem 0;
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
  margin: 0.5rem 0;
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

ul, ol {
  line-height: 1.8;
}

strong {
  color: #0d47a1;
}
</style>
        """,
        category=marc_category,
        author=admin,
        difficulty='INTERMEDIATE',
        estimated_time=305,
        prerequisites="",
        learning_objectives="MARC21의 구조와 목적 이해하기, 주요 필드와 서브필드 활용법 익히기, 실전 MARC21 레코드 읽고 작성하기, MARC21과 현대 메타데이터 포맷의 관계 파악하기",
        status=Content.Status.PUBLISHED
    )

    # 태그 연결
    content.tags.set(tags)

    print("\n✅ 학습 콘텐츠가 생성되었습니다!")
    print(f"\n📊 콘텐츠 정보:")
    print(f"  - 제목: {content.title}")
    print(f"  - 슬러그: {content.slug}")
    print(f"  - 카테고리: {marc_category.name} (상위: {metadata_category.name})")
    print(f"  - 난이도: 중급")
    print(f"  - 소요시간: {content.estimated_time}분")
    print(f"  - 태그: {', '.join([tag.name for tag in tags])}")
    print(f"  - 공개 상태: 공개")
    print(f"\n💡 확인:")
    print(f"  - 콘텐츠 목록: http://localhost:3000/contents?category=metadata")
    print(f"  - 상세 페이지: http://localhost:3000/contents/{content.slug}")

if __name__ == '__main__':
    create_marc_content()
