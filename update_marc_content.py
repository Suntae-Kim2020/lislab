#!/usr/bin/env python
"""
MARC21 콘텐츠 업데이트 스크립트
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content

# MARC21 콘텐츠 가져오기
content = Content.objects.get(slug='marc21-complete-guide')

# 상세 콘텐츠로 업데이트
content.content_html = """
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

  <div class="structure-box">
    <h4>구조 다이어그램</h4>
    <ol>
      <li><strong>Leader (리더)</strong>: 24바이트 고정길이 - 레코드 전체 정보</li>
      <li><strong>Directory (디렉토리)</strong>: 가변길이 - 각 필드의 위치 정보</li>
      <li><strong>Variable Fields (가변 필드)</strong>:
        <ul>
          <li>제어 필드 (00X): 제어번호, 수정일시 등</li>
          <li>데이터 필드 (01X-9XX): 실제 서지데이터</li>
        </ul>
      </li>
    </ol>
  </div>

  <h3>① Leader (리더)</h3>
  <p>레코드 전체에 대한 정보를 담은 <strong>24바이트 고정길이</strong> 필드입니다.</p>
  <div class="example-box">
    <p><strong>예시</strong>: 00725cam a2200205 a 4500</p>
    <ul>
      <li>위치 00-04: 00725 → 레코드 길이 (725바이트)</li>
      <li>위치 05: c → 레코드 상태 (c=수정됨)</li>
      <li>위치 06: a → 자료 유형 (a=언어자료)</li>
      <li>위치 07: m → 서지 레벨 (m=단행본)</li>
    </ul>
  </div>

  <h3>② Directory (디렉토리)</h3>
  <p>각 필드의 <strong>태그, 길이, 시작 위치</strong>를 기록하는 색인입니다.</p>
  <div class="example-box">
    <p><strong>예시</strong>:</p>
    <ul>
      <li>245004000110 → 245 필드, 40바이트, 110번째 위치에서 시작</li>
      <li>100001700151 → 100 필드, 17바이트, 151번째 위치에서 시작</li>
    </ul>
  </div>

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
        <td>1 $a 조남주</td>
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
        <td>$a 개정판</td>
      </tr>
      <tr>
        <td><strong>260</strong></td>
        <td>발행사항</td>
        <td>출판 정보 (구)</td>
        <td>$a 서울 : $b 민음사, $c 2016</td>
      </tr>
      <tr>
        <td><strong>264</strong></td>
        <td>제작/발행사항</td>
        <td>출판 정보 (신)</td>
        <td>1 $a 서울 : $b 민음사, $c 2016</td>
      </tr>
      <tr>
        <td><strong>300</strong></td>
        <td>형태사항</td>
        <td>면수, 크기 등</td>
        <td>$a 192 p. ; $c 19 cm</td>
      </tr>
      <tr>
        <td><strong>650</strong></td>
        <td>주제명</td>
        <td>주제 접근점</td>
        <td>0 $a 한국소설</td>
      </tr>
    </tbody>
  </table>

  <h3>🔍 지시기호(Indicators)와 서브필드(Subfields)</h3>

  <div class="example-box">
    <h4>245 필드 상세 분석</h4>
    <p><strong>245 10 $a 82년생 김지영 / $c 조남주 지음.</strong></p>
    <ul>
      <li><strong>245</strong>: 필드 태그 (표제)</li>
      <li><strong>10</strong>: 지시기호 (1=저록 작성, 0=표제에 관사 없음)</li>
      <li><strong>$a</strong>: 서브필드 코드 (본표제)</li>
      <li><strong>$c</strong>: 서브필드 코드 (책임표시)</li>
    </ul>
    <p><strong>지시기호</strong>: 필드의 처리 방법을 지정 (2자리, 0-9 또는 #)</p>
    <p><strong>서브필드</strong>: 필드 내 세부 데이터 구분 ($ + 영문자/숫자)</p>
  </div>
</div>

<div class="content-section">
  <h2>4. 실전 예제: "82년생 김지영"</h2>

  <div class="example-book">
    <h3>📕 예제 도서</h3>
    <ul>
      <li>저자: 조남주</li>
      <li>제목: 82년생 김지영</li>
      <li>출판사: 민음사</li>
      <li>출판연도: 2016</li>
      <li>ISBN: 978-89-546-5050-4</li>
      <li>면수: 192쪽, 19cm</li>
    </ul>
  </div>

  <h4>주요 필드 예시</h4>
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
        <td>$a 82년생 김지영 / $c 조남주 지음</td>
        <td>표제와 책임표시</td>
      </tr>
      <tr>
        <td><strong>260</strong></td>
        <td>$a 서울 : $b 민음사, $c 2016</td>
        <td>출판지, 출판사, 출판연도</td>
      </tr>
      <tr>
        <td><strong>300</strong></td>
        <td>$a 192 p. ; $c 19 cm</td>
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
      <table class="data-table">
        <tr>
          <td><strong>020</strong></td>
          <td>$a 9788983920281</td>
        </tr>
        <tr>
          <td><strong>041</strong></td>
          <td>1 $a kor $h eng (번역서)</td>
        </tr>
        <tr>
          <td><strong>082</strong></td>
          <td>04 $a 823.914</td>
        </tr>
        <tr>
          <td><strong>100</strong></td>
          <td>1 $a Rowling, J. K.</td>
        </tr>
        <tr>
          <td><strong>245</strong></td>
          <td>10 $a 해리 포터와 마법사의 돌 / $c J. K. 롤링 지음 ; 김혜원 옮김</td>
        </tr>
        <tr>
          <td><strong>260</strong></td>
          <td>$a 서울 : $b 문학수첩, $c 1999</td>
        </tr>
        <tr>
          <td><strong>300</strong></td>
          <td>$a 416 p. ; $c 22 cm</td>
        </tr>
        <tr>
          <td><strong>650</strong></td>
          <td>0 $a 영국소설</td>
        </tr>
        <tr>
          <td><strong>650</strong></td>
          <td>0 $a 판타지소설</td>
        </tr>
        <tr>
          <td><strong>700</strong></td>
          <td>1 $a 김혜원, $e 역 (역자 정보)</td>
        </tr>
      </table>

      <p><strong>주요 포인트:</strong></p>
      <ul>
        <li>041 필드: 번역서이므로 원어(영어)와 번역어(한국어) 명시</li>
        <li>100 필드: 원저자명을 로마자 표기</li>
        <li>700 필드: 역자 정보 추가</li>
        <li>740 필드: 원표제 추가 가능</li>
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

.highlight-box, .example-box, .practice-box, .summary-box, .structure-box {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 1rem;
  margin: 1rem 0;
  border-radius: 4px;
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

<div class="content-section" style="margin-top: 3rem;">
  <h2>🎓 MARC 데이터 입력 실습</h2>

  <p>실제로 MARC 데이터를 입력하고 검증해보세요. MARC21과 KORMARC 형식을 모두 지원합니다.</p>

  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
    <h3 style="color: white; margin-top: 0;">📋 실습 방법</h3>
    <ol style="line-height: 2;">
      <li><strong>형식 선택</strong>: MARC21 또는 KORMARC 중 선택</li>
      <li><strong>태그 선택</strong>: 입력할 MARC 필드 선택</li>
      <li><strong>설명 확인</strong>: 지시기호와 서브필드의 의미 확인</li>
      <li><strong>데이터 입력</strong>: 지시기호와 서브필드 데이터 입력</li>
      <li><strong>검증</strong>: 입력한 데이터의 올바름 확인</li>
    </ol>
  </div>

  <!-- 형식 선택 -->
  <div style="background-color: #f0f9ff; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #3b82f6;">
    <h3 style="color: #1e40af; margin-top: 0;">1단계: MARC 형식 선택</h3>
    <div style="display: flex; gap: 15px; margin-top: 15px;">
      <button onclick="selectFormat('MARC21')" id="btnMARC21" style="flex: 1; padding: 15px; background-color: #3b82f6; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold;">
        MARC21
      </button>
      <button onclick="selectFormat('KORMARC')" id="btnKORMARC" style="flex: 1; padding: 15px; background-color: #6b7280; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold;">
        KORMARC
      </button>
    </div>
    <div id="formatInfo" style="margin-top: 15px; padding: 15px; background-color: white; border-radius: 6px; display: none;">
      <p id="formatDescription" style="margin: 0;"></p>
    </div>
  </div>

  <!-- 태그 선택 -->
  <div id="tagSelection" style="background-color: #f0fdf4; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #10b981; display: none;">
    <h3 style="color: #065f46; margin-top: 0;">2단계: MARC 필드(태그) 선택</h3>
    <select id="tagSelect" onchange="selectTag()" style="width: 100%; padding: 12px; border: 2px solid #10b981; border-radius: 6px; font-size: 15px;">
      <option value="">-- 필드를 선택하세요 --</option>
      <option value="020">020 - ISBN (국제표준도서번호)</option>
      <option value="100">100 - 개인저자명</option>
      <option value="245">245 - 표제와 책임표시</option>
      <option value="250">250 - 판사항</option>
      <option value="260">260 - 발행사항 (구)</option>
      <option value="264">264 - 제작/발행사항 (신)</option>
      <option value="300">300 - 형태사항</option>
      <option value="490">490 - 총서사항</option>
      <option value="650">650 - 주제명</option>
      <option value="700">700 - 부출저자명</option>
    </select>
  </div>

  <!-- 필드 설명 -->
  <div id="fieldInfo" style="background-color: #fef3c7; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #f59e0b; display: none;">
    <h3 style="color: #92400e; margin-top: 0;">📖 필드 상세 정보</h3>
    <div id="fieldDescription"></div>
  </div>

  <!-- 데이터 입력 -->
  <div id="dataInput" style="background-color: #ede9fe; padding: 20px; border-radius: 10px; margin: 20px 0; border: 2px solid #8b5cf6; display: none;">
    <h3 style="color: #5b21b6; margin-top: 0;">3단계: 데이터 입력</h3>

    <div style="margin-bottom: 20px;">
      <label style="display: block; margin-bottom: 8px; font-weight: bold; color: #6b21a8;">
        필드 태그: <span id="displayTag" style="color: #8b5cf6; font-size: 18px;"></span>
      </label>
    </div>

    <!-- 입력 방식 선택 탭 -->
    <div style="margin-bottom: 20px;">
      <div style="display: flex; gap: 10px; border-bottom: 2px solid #c4b5fd;">
        <button onclick="switchInputMode('oneline')" id="btnOneLine"
                style="padding: 10px 20px; background-color: #8b5cf6; color: white; border: none; border-radius: 6px 6px 0 0; cursor: pointer; font-weight: bold;">
          한 줄 입력
        </button>
        <button onclick="switchInputMode('detailed')" id="btnDetailed"
                style="padding: 10px 20px; background-color: #c4b5fd; color: #5b21b6; border: none; border-radius: 6px 6px 0 0; cursor: pointer; font-weight: bold;">
          상세 입력
        </button>
      </div>
    </div>

    <!-- 한 줄 입력 모드 -->
    <div id="oneLineInput" style="margin-bottom: 20px;">
      <label style="display: block; margin-bottom: 8px; font-weight: bold; color: #6b21a8;">
        MARC 형식으로 입력 (한 줄당 하나의 태그)
      </label>
      <textarea id="marcOneLine" rows="5"
             style="width: 100%; padding: 12px; border: 2px solid #8b5cf6; border-radius: 6px; font-family: monospace; font-size: 14px; resize: vertical;"
             placeholder="예:
100 1# $a 조남주
245 10 $a 82년생 김지영 / $c 조남주 지음
260 ## $a 서울 : $b 민음사, $c 2016"></textarea>
      <p style="font-size: 13px; color: #6b7280; margin-top: 5px;">
        💡 형식: 한 줄당 하나의 태그를 입력합니다. [지시기호1][지시기호2] $[코드] [값] $[코드] [값] ...
      </p>
      <p style="font-size: 13px; color: #6b7280; margin-top: 5px;">
        예시: <code style="background-color: #f3f4f6; padding: 2px 6px; border-radius: 3px;">100 1# $a 홍길동</code><br/>
        <code style="background-color: #f3f4f6; padding: 2px 6px; border-radius: 3px; margin-top: 3px; display: inline-block;">245 10 $a 도서관학 개론 / $c 홍길동 지음</code>
      </p>
    </div>

    <!-- 상세 입력 모드 -->
    <div id="detailedInput" style="display: none;">
      <div style="margin-bottom: 20px;">
        <label style="display: block; margin-bottom: 8px; font-weight: bold; color: #6b21a8;">
          지시기호 (Indicators)
        </label>
        <div style="display: flex; gap: 10px;">
          <div style="flex: 1;">
            <label style="display: block; margin-bottom: 5px; font-size: 14px;">제1지시기호</label>
            <input type="text" id="indicator1" maxlength="1"
                   style="width: 100%; padding: 10px; border: 2px solid #8b5cf6; border-radius: 6px; font-size: 16px; text-align: center; font-family: monospace;"
                   placeholder="#"/>
          </div>
          <div style="flex: 1;">
            <label style="display: block; margin-bottom: 5px; font-size: 14px;">제2지시기호</label>
            <input type="text" id="indicator2" maxlength="1"
                   style="width: 100%; padding: 10px; border: 2px solid #8b5cf6; border-radius: 6px; font-size: 16px; text-align: center; font-family: monospace;"
                   placeholder="#"/>
          </div>
        </div>
        <p style="font-size: 13px; color: #6b7280; margin-top: 5px;">
          💡 값이 없으면 # (blank) 사용
        </p>
      </div>

      <div id="subfieldContainer" style="margin-bottom: 20px;">
        <label style="display: block; margin-bottom: 8px; font-weight: bold; color: #6b21a8;">
          서브필드 (Subfields)
        </label>
        <div id="subfieldInputs"></div>
        <button onclick="addSubfield()" style="margin-top: 10px; padding: 8px 16px; background-color: #a855f7; color: white; border: none; border-radius: 6px; cursor: pointer;">
          + 서브필드 추가
        </button>
      </div>
    </div>

    <div style="margin-top: 20px;">
      <button onclick="validateInput()" style="width: 100%; padding: 15px; background-color: #8b5cf6; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold;">
        ✓ 입력 내용 검증하기
      </button>
    </div>
  </div>

  <!-- 검증 결과 -->
  <div id="validationResult" style="display: none; margin: 20px 0;"></div>

  <!-- MARC 출력 -->
  <div id="marcOutput" style="background-color: #1e293b; color: #e2e8f0; padding: 20px; border-radius: 10px; margin: 20px 0; display: none;">
    <h3 style="color: #22c55e; margin-top: 0;">✅ MARC 형식 출력</h3>
    <div style="background-color: #0f172a; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 14px; line-height: 1.8;">
      <div id="marcDisplay"></div>
    </div>
  </div>


<script>
// MARC 실습 초기화 체크
if (!window.marcPracticeInitialized) {
  window.marcPracticeInitialized = true;

  // MARC 실습 데이터
  if (!window.marcPractice) {
    window.marcPractice = {
      currentFormat: null,
      currentTag: null,
      subfieldCount: 0
    };
  }

  if (!window.marcData) {
    window.marcData = {
    MARC21: {
    '020': {
      name: 'ISBN (국제표준도서번호)',
      indicators: {
        ind1: { '#': '정의되지 않음' },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: 'ISBN', required: true, example: '978-89-546-5050-4' },
        'c': { name: '가격', required: false, example: '₩15,000' },
        'g': { name: '부가기호', required: false, example: '03810' }
      },
      example: '## $a 978-89-546-5050-4 $c ₩15,000 $g 03810',
      description: 'ISBN은 국제표준도서번호로, 각 도서를 고유하게 식별합니다.',
      isbd: {
        area: 'Area 8 (자원 식별 및 이용 가능성)',
        punctuation: 'ISBN : 가격',
        pattern: '$a : $c',
        note: '가격 표시는 기관 정책에 따라 생략 가능합니다.'
      }
    },
    '100': {
      name: '개인저자명',
      indicators: {
        ind1: {
          '0': '성만 표기',
          '1': '성, 이름 순서',
          '3': '가족명'
        },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: '개인명', required: true, example: '홍길동' },
        'b': { name: '숫자', required: false, example: 'I' },
        'd': { name: '생몰년', required: false, example: '1950-2020' },
        'e': { name: '관계명칭', required: false, example: '저' }
      },
      example: '1# $a 홍길동, $d 1950-2020',
      description: '주저자(개인)를 기술합니다. 제1지시기호는 이름 형식을 나타냅니다.',
      isbd: {
        area: 'Area 1 (표제와 책임표시 사항)',
        punctuation: '245 $c에서 책임표시로 표현됨',
        pattern: '100은 검색용 표목이며, 245 $c와 연계',
        note: '100 필드 자체는 ISBD 표시에 나타나지 않으며, 245 $c에 텍스트로 기술됩니다.'
      },
      relations: {
        required: '245 필드는 필수입니다.',
        affects: '100이 있으면 → 245 제1지시기호 = 1',
        examples: [
          '100 1# $a 홍길동',
          '245 10 $a 도서관학 개론 / $c 홍길동 지음'
        ],
        note: '✅ 100(주저자)이 있으면 245 제1지시기호를 1로 설정합니다.\\n✅ 100이 없으면 245 제1지시기호를 0으로 설정합니다.'
      }
    },
    '245': {
      name: '표제와 책임표시',
      indicators: {
        ind1: {
          '0': '저록 미작성',
          '1': '저록 작성'
        },
        ind2: {
          '0': '관사 없음',
          '1': '1자 무시',
          '2': '2자 무시',
          '3': '3자 무시',
          '4': '4자 무시'
        }
      },
      subfields: {
        'a': { name: '본표제', required: true, example: '82년생 김지영' },
        'b': { name: '부표제', required: false, example: '이야기' },
        'c': { name: '책임표시', required: false, example: '조남주 지음' },
        'n': { name: '부편명', required: false, example: '제1권' },
        'p': { name: '부편표제', required: false, example: '시작' }
      },
      example: '10 $a 82년생 김지영 / $c 조남주 지음',
      description: '도서의 본표제와 책임표시를 기술합니다. 제1지시기호는 저록 작성 여부, 제2지시기호는 정렬 시 무시할 관사의 글자 수를 나타냅니다.',
      isbd: {
        area: 'Area 1 (표제와 책임표시 사항)',
        punctuation: '본표제 : 부표제 / 책임표시 ; 부편명. 부편표제',
        pattern: '$a : $b / $c ; $n. $p',
        note: '콜론(:)은 $a와 $b 사이, 슬래시(/)는 $c 앞, 세미콜론(;)은 $n 앞, 마침표(.)는 $p 앞에 위치합니다. 기관에 따라 공백 사용 규칙이 다를 수 있습니다.'
      },
      relations: {
        required: '245는 필수 필드입니다. 모든 레코드에 반드시 있어야 합니다.',
        affects: '제1지시기호는 1XX 필드 존재 여부에 따라 결정됩니다.',
        examples: [
          '# 100이 있는 경우:',
          '100 1# $a 조남주',
          '245 10 $a 82년생 김지영 / $c 조남주 지음',
          '',
          '# 100이 없는 경우:',
          '245 00 $a 한국목록규칙'
        ],
        note: '✅ 245 제1지시기호 = 1 ⇔ 1XX(보통 100) 있음\\n✅ 245 제1지시기호 = 0 ⇔ 1XX(주표목) 없음\\n\\n[중요] 100이 있으면 245 10 / 100이 없으면 245 00 가 기본 매칭입니다.\\n(제2지시기호 0 = 무시할 문자 없음. 한국어 도서는 대부분 0 사용)\\n많은 시스템에서 이 규칙을 위반하면 오류/경고가 발생합니다.'
      }
    },
    '250': {
      name: '판사항',
      indicators: {
        ind1: { '#': '정의되지 않음' },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: '판차', required: true, example: '제2판' },
        'b': { name: '판차 책임표시', required: false, example: '개정판 / 홍길동 개정' }
      },
      example: '## $a 개정판',
      description: '자료의 판 정보를 기술합니다.',
      isbd: {
        area: 'Area 2 (판사항)',
        punctuation: '판차 / 판차 책임표시',
        pattern: '$a / $b',
        note: '판차가 없으면 생략합니다. 초판은 일반적으로 기술하지 않습니다.'
      }
    },
    '260': {
      name: '발행사항 (구)',
      indicators: {
        ind1: { '#': '정의되지 않음', '2': '중간 발행자', '3': '현재 발행자' },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: '발행지', required: true, example: '서울' },
        'b': { name: '발행처', required: true, example: '민음사' },
        'c': { name: '발행연도', required: true, example: '2016' },
        'e': { name: '제작지', required: false, example: '파주' },
        'f': { name: '제작처', required: false, example: '해냄출판사' },
        'g': { name: '제작연도', required: false, example: '2016' }
      },
      example: '## $a 서울 : $b 민음사, $c 2016',
      description: '발행지, 발행처, 발행연도 정보를 기술합니다. (구형식, 264 사용 권장)',
      isbd: {
        area: 'Area 4 (발행, 제작, 배포 사항)',
        punctuation: '발행지 : 발행처, 발행연도',
        pattern: '$a : $b, $c',
        note: '콜론(:)은 발행지와 발행처 사이, 쉼표(,)는 발행처와 연도 사이에 위치합니다. 264 필드 사용을 권장합니다.'
      }
    },
    '264': {
      name: '제작/발행사항 (신)',
      indicators: {
        ind1: { '#': '정의되지 않음', '2': '중간 발행자', '3': '현재 발행자' },
        ind2: { '0': '제작', '1': '발행', '2': '배포', '3': '제작발행', '4': '저작권' }
      },
      subfields: {
        'a': { name: '발행지', required: true, example: '서울' },
        'b': { name: '발행처', required: true, example: '민음사' },
        'c': { name: '발행연도', required: true, example: '2016' }
      },
      example: '#1 $a 서울 : $b 민음사, $c 2016',
      description: '발행지, 발행처, 발행연도 정보를 기술합니다. 제2지시기호로 발행/제작 구분합니다.',
      isbd: {
        area: 'Area 4 (발행, 제작, 배포 사항)',
        punctuation: '발행지 : 발행처, 발행연도',
        pattern: '$a : $b, $c',
        note: '260과 동일한 구두점 규칙입니다. RDA 규칙에서는 264 사용이 표준입니다.'
      }
    },
    '300': {
      name: '형태사항',
      indicators: {
        ind1: { '#': '정의되지 않음' },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: '페이지/수량', required: true, example: '192 p.' },
        'b': { name: '삽화사항', required: false, example: '삽화' },
        'c': { name: '크기', required: false, example: '19 cm' },
        'e': { name: '부록', required: false, example: '부록 포함' }
      },
      example: '## $a 192 p. ; $c 19 cm',
      description: '자료의 물리적 형태(페이지 수, 크기 등)를 기술합니다.',
      isbd: {
        area: 'Area 5 (형태사항)',
        punctuation: '수량 : 기타 형태사항 ; 크기 + 부록',
        pattern: '$a : $b ; $c + $e',
        note: '콜론(:)은 수량과 삽화사항 사이, 세미콜론(;)은 크기 앞, 플러스(+)는 부록 앞에 위치합니다.'
      }
    },
    '490': {
      name: '총서사항',
      indicators: {
        ind1: {
          '0': '총서 저록 미작성',
          '1': '총서 저록 작성 (8XX 필드에 총서 표목 존재)'
        },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: '총서명', required: true, example: '현대문학 세계문학 단편선' },
        'v': { name: '총서번호', required: false, example: '23' },
        'x': { name: 'ISSN', required: false, example: '1234-5678' }
      },
      example: '1# $a 현대문학 세계문학 단편선 ; $v 23',
      description: '총서(시리즈) 정보를 기술합니다.',
      isbd: {
        area: 'Area 6 (총서사항)',
        punctuation: '(총서명 ; 총서번호)',
        pattern: '($a ; $v)',
        note: '총서 전체를 괄호로 묶고, 세미콜론(;)으로 총서명과 번호를 구분합니다. 총서가 없으면 생략합니다.'
      }
    },
    '650': {
      name: '주제명',
      indicators: {
        ind1: {
          '#': '레벨 미지정',
          '0': '권위형 없음',
          '1': '1차 주제',
          '2': '2차 주제'
        },
        ind2: {
          '0': 'LCSH (Library of Congress Subject Headings)',
          '1': 'LC 아동용 주제명',
          '4': '출처 미지정',
          '7': '기타'
        }
      },
      subfields: {
        'a': { name: '주제어', required: true, example: '한국소설' },
        'x': { name: '일반세목', required: false, example: '역사' },
        'y': { name: '시대세목', required: false, example: '21세기' },
        'z': { name: '지리세목', required: false, example: '서울' }
      },
      example: '#0 $a 한국소설',
      description: '자료의 주제를 나타내는 통제어휘를 기술합니다.',
      isbd: {
        area: 'Area 7+ (주기사항 및 검색점)',
        punctuation: 'ISBD 표시에 직접 나타나지 않음',
        pattern: '검색용 필드',
        note: '650은 접근점(검색점)으로 ISBD 구두점 규칙을 따르지 않습니다. 기관의 주제명 정책에 따라 입력합니다.'
      }
    },
    '700': {
      name: '부출저자명 (개인)',
      indicators: {
        ind1: {
          '0': '성만 표기',
          '1': '성, 이름 순서',
          '3': '가족명'
        },
        ind2: {
          '#': '유형 미지정',
          '2': '분석저록'
        }
      },
      subfields: {
        'a': { name: '개인명', required: true, example: '김혜원' },
        'd': { name: '생몰년', required: false, example: '1970-' },
        'e': { name: '관계명칭', required: false, example: '역' },
        't': { name: '저작 표제', required: false, example: 'Harry Potter' }
      },
      example: '1# $a 김혜원, $e 역',
      description: '부저자, 역자, 삽화가 등 주저자 외의 책임자를 기술합니다.',
      isbd: {
        area: 'Area 1 (표제와 책임표시 사항)',
        punctuation: '245 $c에 포함되어 표현됨',
        pattern: '100과 유사하게 검색용 표목',
        note: '700 필드는 ISBD 표시에 직접 나타나지 않으며, 245 $c에 텍스트로 기술됩니다. 역자, 삽화가 등의 관계명칭은 기관 정책에 따라 다를 수 있습니다.'
      }
    }
  },
  KORMARC: {
    '020': {
      name: 'ISBN (국제표준도서번호)',
      indicators: {
        ind1: { '#': '정의되지 않음' },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: 'ISBN', required: true, example: '978-89-546-5050-4' },
        'c': { name: '가격', required: false, example: '₩15,000' },
        'g': { name: '부가기호', required: false, example: '03810' }
      },
      example: '## $a 978-89-546-5050-4 $c ₩15,000 $g 03810',
      description: 'ISBN은 국제표준도서번호로, 각 도서를 고유하게 식별합니다. (KORMARC은 MARC21과 동일)'
    },
    '100': {
      name: '개인저자명',
      indicators: {
        ind1: {
          '0': '성만 표기',
          '1': '성, 이름 순서 (외국인명)',
          '4': '한국인명 (성 + 이름)'
        },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: '개인명', required: true, example: '홍길동' },
        'd': { name: '생몰년', required: false, example: '1950-2020' },
        'g': { name: '기타사항', required: false, example: '저' }
      },
      example: '4# $a 홍길동, $d 1950-2020',
      description: '주저자(개인)를 기술합니다. KORMARC에서는 한국인명을 위해 제1지시기호 4를 사용합니다.'
    },
    '245': {
      name: '표제와 책임표시',
      indicators: {
        ind1: {
          '0': '저록 미작성',
          '1': '저록 작성'
        },
        ind2: {
          '0': '관사 없음',
          '1': '1자 무시',
          '2': '2자 무시'
        }
      },
      subfields: {
        'a': { name: '본표제', required: true, example: '82년생 김지영' },
        'b': { name: '부표제', required: false, example: '이야기' },
        'c': { name: '책임표시', required: false, example: '조남주 지음' },
        'd': { name: '병렬표제', required: false, example: 'Kim Ji-young, Born 1982' }
      },
      example: '10 $a 82년생 김지영 / $c 조남주 지음',
      description: '도서의 본표제와 책임표시를 기술합니다. MARC21과 거의 동일합니다.'
    },
    '250': {
      name: '판사항',
      indicators: {
        ind1: { '#': '정의되지 않음' },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: '판차', required: true, example: '제2판' },
        'b': { name: '판차 책임표시', required: false, example: '개정판 / 홍길동 개정' }
      },
      example: '## $a 개정판',
      description: '자료의 판 정보를 기술합니다.'
    },
    '260': {
      name: '발행사항',
      indicators: {
        ind1: { '#': '정의되지 않음' },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: '발행지', required: true, example: '서울' },
        'b': { name: '발행처', required: true, example: '민음사' },
        'c': { name: '발행연도', required: true, example: '2016' }
      },
      example: '## $a 서울 : $b 민음사, $c 2016',
      description: '발행지, 발행처, 발행연도 정보를 기술합니다. KORMARC에서는 260 필드를 주로 사용합니다.'
    },
    '300': {
      name: '형태사항',
      indicators: {
        ind1: { '#': '정의되지 않음' },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: '페이지/수량', required: true, example: '192 p.' },
        'b': { name: '삽화사항', required: false, example: '삽화' },
        'c': { name: '크기', required: false, example: '19 cm' }
      },
      example: '## $a 192 p. ; $c 19 cm',
      description: '자료의 물리적 형태(페이지 수, 크기 등)를 기술합니다.'
    },
    '440': {
      name: '총서사항',
      indicators: {
        ind1: { '#': '정의되지 않음' },
        ind2: {
          '0': '관사 없음',
          '1': '1자 무시',
          '2': '2자 무시'
        }
      },
      subfields: {
        'a': { name: '총서명', required: true, example: '현대문학 세계문학 단편선' },
        'v': { name: '총서번호', required: false, example: '23' }
      },
      example: '#0 $a 현대문학 세계문학 단편선 ; $v 23',
      description: 'KORMARC에서는 440 필드를 총서사항으로 사용합니다. (MARC21은 490 사용)'
    },
    '650': {
      name: '주제명',
      indicators: {
        ind1: { '#': '정의되지 않음' },
        ind2: {
          '0': 'LCSH',
          '1': 'LC 아동용',
          '3': '국립중앙도서관 주제명표목표',
          '4': '출처 미지정'
        }
      },
      subfields: {
        'a': { name: '주제어', required: true, example: '한국소설' },
        'x': { name: '일반세목', required: false, example: '역사' }
      },
      example: '#3 $a 한국소설',
      description: '자료의 주제를 나타냅니다. KORMARC에서는 제2지시기호 3(국립중앙도서관 주제명)을 주로 사용합니다.'
    },
    '700': {
      name: '부출저자명 (개인)',
      indicators: {
        ind1: {
          '0': '성만 표기',
          '1': '성, 이름 순서 (외국인명)',
          '4': '한국인명'
        },
        ind2: { '#': '정의되지 않음' }
      },
      subfields: {
        'a': { name: '개인명', required: true, example: '김혜원' },
        'd': { name: '생몰년', required: false, example: '1970-' },
        'g': { name: '기타사항', required: false, example: '역' }
      },
      example: '4# $a 김혜원, $g 역',
      description: '부저자, 역자 등을 기술합니다. KORMARC에서는 한국인명에 제1지시기호 4를 사용합니다.'
    }
  }
  };
  }
  const marcData = window.marcData;

  function selectFormat(format) {
    window.marcPractice.currentFormat = format;

  // 버튼 스타일 변경
  const btn21 = document.getElementById('btnMARC21');
  const btnKOR = document.getElementById('btnKORMARC');

  if (format === 'MARC21') {
    btn21.style.backgroundColor = '#3b82f6';
    btnKOR.style.backgroundColor = '#6b7280';
  } else {
    btn21.style.backgroundColor = '#6b7280';
    btnKOR.style.backgroundColor = '#3b82f6';
  }

  // 형식 정보 표시
  const formatInfo = document.getElementById('formatInfo');
  const formatDesc = document.getElementById('formatDescription');

  if (format === 'MARC21') {
    formatDesc.innerHTML = '<strong>MARC21</strong>을 선택하셨습니다. 미국 의회도서관(Library of Congress)에서 제정한 국제 표준 형식입니다.';
  } else {
    formatDesc.innerHTML = '<strong>KORMARC</strong>을 선택하셨습니다. 한국문헌자동화목록형식으로, MARC21을 기반으로 한국 실정에 맞게 조정한 형식입니다.';
  }

  formatInfo.style.display = 'block';

  // 태그 선택 섹션 표시
  document.getElementById('tagSelection').style.display = 'block';

  // 기존 선택 초기화
  document.getElementById('tagSelect').value = '';
  document.getElementById('fieldInfo').style.display = 'none';
  document.getElementById('dataInput').style.display = 'none';
  document.getElementById('validationResult').style.display = 'none';
  document.getElementById('marcOutput').style.display = 'none';
  }

  function selectTag() {
  const tag = document.getElementById('tagSelect').value;
  if (!tag) {
    document.getElementById('fieldInfo').style.display = 'none';
    document.getElementById('dataInput').style.display = 'none';
    return;
  }

  window.marcPractice.currentTag = tag;
  const format = window.marcPractice.currentFormat;
  const fieldData = marcData[format][tag];

  // 필드 설명 표시
  const fieldInfo = document.getElementById('fieldInfo');
  const fieldDesc = document.getElementById('fieldDescription');

  let html = `
    <h4 style="color: #92400e; margin-top: 0;">${tag} - ${fieldData.name}</h4>
    <p style="background-color: white; padding: 12px; border-radius: 6px; margin: 10px 0;">
      ${fieldData.description}
    </p>

    <h5 style="color: #92400e; margin-top: 15px;">📌 지시기호 (Indicators)</h5>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 10px 0;">
      <div style="background-color: white; padding: 12px; border-radius: 6px;">
        <strong>제1지시기호:</strong>
        <ul style="margin: 5px 0; padding-left: 20px;">
  `;

  for (const [code, desc] of Object.entries(fieldData.indicators.ind1)) {
    html += `<li><code>${code}</code> = ${desc}</li>`;
  }

  html += `
        </ul>
      </div>
      <div style="background-color: white; padding: 12px; border-radius: 6px;">
        <strong>제2지시기호:</strong>
        <ul style="margin: 5px 0; padding-left: 20px;">
  `;

  for (const [code, desc] of Object.entries(fieldData.indicators.ind2)) {
    html += `<li><code>${code}</code> = ${desc}</li>`;
  }

  html += `
        </ul>
      </div>
    </div>

    <h5 style="color: #92400e; margin-top: 15px;">🔖 서브필드 (Subfields)</h5>
    <table style="width: 100%; background-color: white; border-collapse: collapse; border-radius: 6px; overflow: hidden;">
      <thead>
        <tr style="background-color: #f59e0b; color: white;">
          <th style="padding: 10px; text-align: left;">코드</th>
          <th style="padding: 10px; text-align: left;">이름</th>
          <th style="padding: 10px; text-align: left;">필수</th>
          <th style="padding: 10px; text-align: left;">예시</th>
        </tr>
      </thead>
      <tbody>
  `;

  for (const [code, info] of Object.entries(fieldData.subfields)) {
    html += `
      <tr style="border-bottom: 1px solid #fef3c7;">
        <td style="padding: 10px;"><strong>$${code}</strong></td>
        <td style="padding: 10px;">${info.name}</td>
        <td style="padding: 10px;">${info.required ? '✓ 필수' : '선택'}</td>
        <td style="padding: 10px; font-family: monospace; color: #7c2d12;">${info.example}</td>
      </tr>
    `;
  }

  html += `
      </tbody>
    </table>
  `;

  // ISBD 정보 추가
  if (fieldData.isbd) {
    html += `
      <div style="background-color: #dbeafe; padding: 15px; border-radius: 6px; margin-top: 15px; border-left: 4px solid #3b82f6;">
        <h5 style="color: #1e40af; margin-top: 0; display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 20px;">📘</span> ISBD 구두점 규칙
        </h5>
        <div style="background-color: white; padding: 12px; border-radius: 4px; margin: 10px 0;">
          <div style="margin-bottom: 8px;">
            <strong style="color: #1e40af;">구역:</strong>
            <span style="color: #374151;">${fieldData.isbd.area}</span>
          </div>
          <div style="margin-bottom: 8px;">
            <strong style="color: #1e40af;">구두점:</strong>
            <span style="color: #374151;">${fieldData.isbd.punctuation}</span>
          </div>
          <div style="margin-bottom: 8px;">
            <strong style="color: #1e40af;">패턴:</strong>
            <code style="background-color: #f3f4f6; padding: 2px 6px; border-radius: 3px; color: #7c2d12;">${fieldData.isbd.pattern}</code>
          </div>
          ${fieldData.isbd.note ? `
          <div style="background-color: #fef3c7; padding: 10px; border-radius: 4px; margin-top: 10px; border-left: 3px solid #f59e0b;">
            <strong style="color: #92400e;">💡 참고:</strong><br/>
            <span style="color: #78350f; font-size: 14px;">${fieldData.isbd.note}</span>
          </div>
          ` : ''}
        </div>
      </div>
    `;
  }

  html += `
    <div style="background-color: #fed7aa; padding: 12px; border-radius: 6px; margin-top: 15px;">
      <strong>💡 예제:</strong>
      <div style="font-family: monospace; font-size: 15px; margin-top: 8px; color: #7c2d12;">
        ${tag} ${fieldData.example}
      </div>
    </div>
  `;

  // 태그 간 관계 정보 추가
  if (fieldData.relations) {
    html += `
      <div style="background-color: #fef2f2; padding: 15px; border-radius: 6px; margin-top: 15px; border-left: 4px solid #dc2626;">
        <h5 style="color: #991b1b; margin-top: 0; display: flex; align-items: center; gap: 8px;">
          <span style="font-size: 20px;">🔗</span> 관련 태그 및 요구사항
        </h5>
        <div style="background-color: white; padding: 12px; border-radius: 4px; margin: 10px 0;">
          ${fieldData.relations.required ? `
          <div style="margin-bottom: 10px; padding: 8px; background-color: #fee2e2; border-radius: 4px;">
            <strong style="color: #991b1b;">📌 필수 요구사항:</strong><br/>
            <span style="color: #7f1d1d;">${fieldData.relations.required}</span>
          </div>
          ` : ''}
          ${fieldData.relations.affects ? `
          <div style="margin-bottom: 10px;">
            <strong style="color: #991b1b;">⚡ 영향:</strong><br/>
            <span style="color: #7f1d1d;">${fieldData.relations.affects}</span>
          </div>
          ` : ''}
          ${fieldData.relations.note ? `
          <div style="margin-bottom: 10px; padding: 10px; background-color: #fef3c7; border-radius: 4px; border-left: 3px solid #f59e0b;">
            <span style="color: #78350f; font-size: 14px; white-space: pre-line;">${fieldData.relations.note}</span>
          </div>
          ` : ''}
          ${fieldData.relations.examples && fieldData.relations.examples.length > 0 ? `
          <div style="margin-top: 12px;">
            <strong style="color: #991b1b;">📝 관계 예제:</strong>
            <div style="background-color: #f9fafb; padding: 10px; border-radius: 4px; margin-top: 8px; font-family: monospace; font-size: 14px; color: #1f2937;">
              ${fieldData.relations.examples.map(ex => ex ? ex : '<br/>').join('<br/>')}
            </div>
          </div>
          ` : ''}
        </div>
      </div>
    `;
  }

  fieldDesc.innerHTML = html;
  fieldInfo.style.display = 'block';

  // 데이터 입력 섹션 초기화 및 표시
  document.getElementById('displayTag').textContent = tag;
  document.getElementById('indicator1').value = '';
  document.getElementById('indicator2').value = '';
  document.getElementById('marcOneLine').value = '';

  // 서브필드 입력 필드 초기화
  window.marcPractice.subfieldCount = 0;
  const subfieldInputs = document.getElementById('subfieldInputs');
  subfieldInputs.innerHTML = '';

  // 첫 번째 서브필드 자동 추가
  addSubfield();

  // 입력 모드 초기화 (한 줄 입력이 기본)
  switchInputMode('oneline');

  document.getElementById('dataInput').style.display = 'block';
  document.getElementById('validationResult').style.display = 'none';
  document.getElementById('marcOutput').style.display = 'none';
  }

  function switchInputMode(mode) {
  const oneLineInput = document.getElementById('oneLineInput');
  const detailedInput = document.getElementById('detailedInput');
  const btnOneLine = document.getElementById('btnOneLine');
  const btnDetailed = document.getElementById('btnDetailed');

  if (mode === 'oneline') {
    oneLineInput.style.display = 'block';
    detailedInput.style.display = 'none';
    btnOneLine.style.backgroundColor = '#8b5cf6';
    btnOneLine.style.color = 'white';
    btnDetailed.style.backgroundColor = '#c4b5fd';
    btnDetailed.style.color = '#5b21b6';
  } else {
    oneLineInput.style.display = 'none';
    detailedInput.style.display = 'block';
    btnOneLine.style.backgroundColor = '#c4b5fd';
    btnOneLine.style.color = '#5b21b6';
    btnDetailed.style.backgroundColor = '#8b5cf6';
    btnDetailed.style.color = 'white';
  }
  }

  function parseOneLine(input) {
  // MARC 한 줄 입력 파싱
  // 형식: [ind1][ind2] $a value $c value ...
  const trimmed = input.trim();

  // 지시기호 추출 (처음 2자)
  let ind1 = '#';
  let ind2 = '#';
  let datapart = trimmed;

  // 첫 $의 위치 찾기
  const firstDollar = trimmed.indexOf('$');
  if (firstDollar > 0) {
    const indicators = trimmed.substring(0, firstDollar).trim();
    if (indicators.length >= 1) {
      ind1 = indicators[0];
    }
    if (indicators.length >= 2) {
      ind2 = indicators[1];
    }
    datapart = trimmed.substring(firstDollar);
  }

  // 서브필드 파싱
  const subfields = [];
  const parts = datapart.split('$').filter(p => p.trim());

  for (const part of parts) {
    const trimmedPart = part.trim();
    if (trimmedPart.length > 0) {
      const code = trimmedPart[0];
      const value = trimmedPart.substring(1).trim();
      if (value) {
        subfields.push({ code, value });
      }
    }
  }

  return { ind1, ind2, subfields };
  }

  function addSubfield() {
  const count = ++window.marcPractice.subfieldCount;
  const container = document.getElementById('subfieldInputs');

  const div = document.createElement('div');
  div.id = `subfield-${count}`;
  div.style.cssText = 'display: flex; gap: 10px; margin-bottom: 10px; align-items: center;';

  div.innerHTML = `
    <div style="flex: 0 0 100px;">
      <input type="text" id="subfieldCode-${count}" maxlength="1"
             style="width: 100%; padding: 10px; border: 2px solid #8b5cf6; border-radius: 6px; text-align: center; font-family: monospace; font-size: 16px;"
             placeholder="$a"/>
    </div>
    <div style="flex: 1;">
      <input type="text" id="subfieldValue-${count}"
             style="width: 100%; padding: 10px; border: 2px solid #8b5cf6; border-radius: 6px; font-family: monospace; font-size: 14px;"
             placeholder="값을 입력하세요"/>
    </div>
    <button onclick="removeSubfield(${count})"
            style="padding: 10px 15px; background-color: #ef4444; color: white; border: none; border-radius: 6px; cursor: pointer;">
      삭제
    </button>
  `;

  container.appendChild(div);
  }

  function removeSubfield(id) {
  const element = document.getElementById(`subfield-${id}`);
  if (element) {
    element.remove();
  }
  }

  function validateMultipleLines(lines, format) {
  const allResults = [];
  const allErrors = [];
  const allWarnings = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;

    // 태그 추출 (첫 3자리)
    const tagMatch = line.match(/^(\d{3})\s/);
    if (!tagMatch) {
      allErrors.push(`줄 ${lineNum}: 태그를 찾을 수 없습니다. (형식: "XXX ## $a ...")`);
      continue;
    }

    const tag = tagMatch[1];
    const fieldData = marcData[format][tag];

    if (!fieldData) {
      allWarnings.push(`줄 ${lineNum}: 태그 ${tag}는 현재 지원하지 않는 태그입니다.`);
      continue;
    }

    // 태그 제거 후 나머지 파싱
    const restOfLine = line.substring(3).trim();
    const parsed = parseOneLine(restOfLine);

    // 검증
    const errors = [];
    const warnings = [];

    // 지시기호 검증
    if (!fieldData.indicators.ind1[parsed.ind1]) {
      errors.push(`줄 ${lineNum} (${tag}): 제1지시기호 "${parsed.ind1}"은(는) 유효하지 않습니다.`);
    }

    if (!fieldData.indicators.ind2[parsed.ind2]) {
      errors.push(`줄 ${lineNum} (${tag}): 제2지시기호 "${parsed.ind2}"은(는) 유효하지 않습니다.`);
    }

    // 서브필드 검증
    if (parsed.subfields.length === 0) {
      errors.push(`줄 ${lineNum} (${tag}): 최소 하나 이상의 서브필드를 입력해야 합니다.`);
    }

    const providedCodes = new Set();
    for (const sf of parsed.subfields) {
      if (providedCodes.has(sf.code)) {
        warnings.push(`줄 ${lineNum} (${tag}): 서브필드 $${sf.code}이(가) 중복되었습니다.`);
      }
      providedCodes.add(sf.code);

      if (!fieldData.subfields[sf.code]) {
        warnings.push(`줄 ${lineNum} (${tag}): 서브필드 $${sf.code}은(는) 정의되지 않은 서브필드입니다.`);
      }
    }

    // 필수 서브필드 확인
    for (const [code, info] of Object.entries(fieldData.subfields)) {
      if (info.required && !providedCodes.has(code)) {
        errors.push(`줄 ${lineNum} (${tag}): 필수 서브필드 $${code} (${info.name})이(가) 누락되었습니다.`);
      }
    }

    allErrors.push(...errors);
    allWarnings.push(...warnings);

    if (errors.length === 0) {
      allResults.push({ tag, ind1: parsed.ind1, ind2: parsed.ind2, subfields: parsed.subfields, fieldData });
    }
  }

  // 결과 표시
  displayMultipleValidationResults(allErrors, allWarnings, allResults);
  }

  function displayMultipleValidationResults(errors, warnings, results) {
  const resultDiv = document.getElementById('validationResult');
  let resultHTML = '';

  if (errors.length > 0) {
    resultHTML += `
      <div style="background-color: #fef2f2; padding: 20px; border-radius: 8px; border-left: 4px solid #ef4444;">
        <h3 style="color: #991b1b; margin-top: 0;">❌ 오류 발견</h3>
        <ul style="margin: 10px 0; color: #7f1d1d;">
    `;
    errors.forEach(err => {
      resultHTML += `<li>${err}</li>`;
    });
    resultHTML += `</ul></div>`;
  }

  if (warnings.length > 0) {
    resultHTML += `
      <div style="background-color: #fffbeb; padding: 20px; border-radius: 8px; border-left: 4px solid #f59e0b; margin-top: 15px;">
        <h3 style="color: #92400e; margin-top: 0;">⚠️ 경고</h3>
        <ul style="margin: 10px 0; color: #78350f;">
    `;
    warnings.forEach(warn => {
      resultHTML += `<li>${warn}</li>`;
    });
    resultHTML += `</ul></div>`;
  }

  if (errors.length === 0 && results.length > 0) {
    resultHTML += `
      <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981;">
        <h3 style="color: #065f46; margin-top: 0;">✅ 검증 성공!</h3>
        <p style="margin: 0; color: #064e3b;">
          ${results.length}개의 MARC 필드가 올바르게 작성되었습니다.
        </p>
      </div>
    `;

    // MARC 형식으로 출력
    displayMultipleMARC(results);
  }

  resultDiv.innerHTML = resultHTML;
  resultDiv.style.display = 'block';
  }

  function displayMultipleMARC(results) {
  const marcOutput = document.getElementById('marcOutput');
  const marcDisplay = document.getElementById('marcDisplay');

  let marcText = '';
  results.forEach((result, index) => {
    marcText += `<div style="margin-bottom: 10px;">`;
    marcText += `<strong style="color: #22c55e;">${result.tag}</strong> `;
    marcText += `<span style="color: #3b82f6;">${result.ind1}${result.ind2}</span> `;

    result.subfields.forEach(sf => {
      marcText += `<span style="color: #8b5cf6;">$${sf.code}</span> ${sf.value} `;
    });
    marcText += `</div>`;
  });

  marcDisplay.innerHTML = marcText;
  marcOutput.style.display = 'block';
  document.getElementById('validationResult').style.display = 'none';
  }

  function validateInput() {
  const format = window.marcPractice.currentFormat;

  // 입력 모드 확인
  const oneLineInput = document.getElementById('oneLineInput');
  const isOneLine = oneLineInput.style.display !== 'none';

  if (isOneLine) {
    // 한 줄 입력 모드 - 여러 줄 처리
    const oneLineValue = document.getElementById('marcOneLine').value;
    if (!oneLineValue.trim()) {
      showValidationError('MARC 데이터를 입력해주세요.', '예:\\n100 1# $a 홍길동\\n245 10 $a 도서관학 개론 / $c 홍길동 지음');
      return;
    }

    // 여러 줄 처리
    const lines = oneLineValue.split('\\n').map(line => line.trim()).filter(line => line);
    validateMultipleLines(lines, format);
    return;
  } else {
    // 상세 입력 모드 - 기존 단일 태그 처리
    const tag = window.marcPractice.currentTag;
    const fieldData = marcData[format][tag];
    let ind1, ind2, subfields;
    // 상세 입력 모드
    ind1 = document.getElementById('indicator1').value || '#';
    ind2 = document.getElementById('indicator2').value || '#';

    // 서브필드 수집
    subfields = [];
    for (let i = 1; i <= window.marcPractice.subfieldCount; i++) {
      const codeInput = document.getElementById(`subfieldCode-${i}`);
      const valueInput = document.getElementById(`subfieldValue-${i}`);

      if (codeInput && valueInput && codeInput.value && valueInput.value) {
        subfields.push({
          code: codeInput.value.replace('$', ''),
          value: valueInput.value.trim()
        });
      }
    }
  }

  // 검증
  const errors = [];
  const warnings = [];

  // 지시기호 검증
  if (!fieldData.indicators.ind1[ind1]) {
    errors.push(`제1지시기호 "${ind1}"은(는) 유효하지 않습니다. 사용 가능한 값: ${Object.keys(fieldData.indicators.ind1).join(', ')}`);
  }

  if (!fieldData.indicators.ind2[ind2]) {
    errors.push(`제2지시기호 "${ind2}"은(는) 유효하지 않습니다. 사용 가능한 값: ${Object.keys(fieldData.indicators.ind2).join(', ')}`);
  }

  // 서브필드 검증
  if (subfields.length === 0) {
    errors.push('최소 하나 이상의 서브필드를 입력해야 합니다.');
  }

  const providedCodes = new Set();
  for (const sf of subfields) {
    // 중복 체크
    if (providedCodes.has(sf.code)) {
      warnings.push(`서브필드 $${sf.code}이(가) 중복되었습니다.`);
    }
    providedCodes.add(sf.code);

    // 정의된 서브필드인지 확인
    if (!fieldData.subfields[sf.code]) {
      warnings.push(`서브필드 $${sf.code}은(는) 이 필드에서 정의되지 않은 서브필드입니다.`);
    }
  }

  // 필수 서브필드 확인
  for (const [code, info] of Object.entries(fieldData.subfields)) {
    if (info.required && !providedCodes.has(code)) {
      errors.push(`필수 서브필드 $${code} (${info.name})이(가) 누락되었습니다.`);
    }
  }

  // 결과 표시
  const resultDiv = document.getElementById('validationResult');
  let resultHTML = '';

  if (errors.length > 0) {
    resultHTML += `
      <div style="background-color: #fef2f2; padding: 20px; border-radius: 8px; border-left: 4px solid #ef4444;">
        <h3 style="color: #991b1b; margin-top: 0;">❌ 오류 발견</h3>
        <ul style="margin: 10px 0; color: #7f1d1d;">
    `;
    errors.forEach(err => {
      resultHTML += `<li>${err}</li>`;
    });
    resultHTML += `</ul></div>`;
  }

  if (warnings.length > 0) {
    resultHTML += `
      <div style="background-color: #fffbeb; padding: 20px; border-radius: 8px; border-left: 4px solid #f59e0b; margin-top: 15px;">
        <h3 style="color: #92400e; margin-top: 0;">⚠️ 경고</h3>
        <ul style="margin: 10px 0; color: #78350f;">
    `;
    warnings.forEach(warn => {
      resultHTML += `<li>${warn}</li>`;
    });
    resultHTML += `</ul></div>`;
  }

  if (errors.length === 0) {
    resultHTML += `
      <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981;">
        <h3 style="color: #065f46; margin-top: 0;">✅ 검증 성공!</h3>
        <p style="margin: 0; color: #064e3b;">
          입력하신 MARC 데이터가 형식에 맞게 올바르게 작성되었습니다.
        </p>
      </div>
    `;

    // MARC 형식으로 출력
    displayMARC(tag, ind1, ind2, subfields, fieldData);
  }

  resultDiv.innerHTML = resultHTML;
  resultDiv.style.display = 'block';
  }

  function displayMARC(tag, ind1, ind2, subfields, fieldData) {
  const marcOutput = document.getElementById('marcOutput');
  const marcDisplay = document.getElementById('marcDisplay');

  // MARC 형식 생성
  let marcText = `<strong style="color: #22c55e;">${tag}</strong> `;
  marcText += `<span style="color: #fbbf24;">${ind1}${ind2}</span> `;

  subfields.forEach((sf, idx) => {
    if (idx > 0) marcText += ' ';
    marcText += `<span style="color: #60a5fa;">$${sf.code}</span> ${sf.value}`;
  });

  // 설명 추가
  let explanation = '<div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #334155;">';
  explanation += '<div style="color: #94a3b8; font-size: 13px; margin-bottom: 10px;">📝 필드 구성 요소:</div>';
  explanation += `<div style="color: #cbd5e1; font-size: 13px; line-height: 1.8;">`;
  explanation += `• <strong style="color: #22c55e;">태그 ${tag}</strong>: ${fieldData.name}<br>`;
  explanation += `• <strong style="color: #fbbf24;">지시기호 ${ind1}${ind2}</strong>: `;
  explanation += `제1지시기호=${fieldData.indicators.ind1[ind1] || '?'}, `;
  explanation += `제2지시기호=${fieldData.indicators.ind2[ind2] || '?'}<br>`;

  subfields.forEach(sf => {
    const sfInfo = fieldData.subfields[sf.code];
    if (sfInfo) {
      explanation += `• <strong style="color: #60a5fa;">$${sf.code}</strong> (${sfInfo.name}): ${sf.value}<br>`;
    }
  });

  explanation += '</div></div>';

  marcDisplay.innerHTML = marcText + explanation;
  marcOutput.style.display = 'block';
  }

  function showValidationError(message, details = '') {
  const resultDiv = document.getElementById('validationResult');
  let html = `
    <div style="background-color: #fef2f2; padding: 20px; border-radius: 8px; border-left: 4px solid #ef4444;">
      <h3 style="color: #991b1b; margin-top: 0;">❌ 오류</h3>
      <p style="margin: 10px 0; color: #7f1d1d;"><strong>${message}</strong></p>
  `;
  if (details) {
    html += `<p style="margin: 10px 0; color: #991b1b; font-size: 14px;">${details}</p>`;
  }
  html += `</div>`;

  resultDiv.innerHTML = html;
  resultDiv.style.display = 'block';
  document.getElementById('marcOutput').style.display = 'none';
  }

} // End of window.marcPracticeInitialized check
</script>
</div>
"""

content.save()
print("✅ MARC21 콘텐츠가 업데이트되었습니다!")
print(f"확인: http://localhost:3000/contents/{content.slug}")
