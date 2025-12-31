#!/usr/bin/env python
"""
MARC 실습 기능 추가 스크립트
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

# 기존 content_html 끝에 실습 섹션 추가
practice_section = """

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

</div>

<script>
// MARC 실습 데이터
if (!window.marcPractice) {
  window.marcPractice = {
    currentFormat: null,
    currentTag: null,
    subfieldCount: 0
  };
}

const marcData = {
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
      description: 'ISBN은 국제표준도서번호로, 각 도서를 고유하게 식별합니다.'
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
      description: '주저자(개인)를 기술합니다. 제1지시기호는 이름 형식을 나타냅니다.'
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
      description: '도서의 본표제와 책임표시를 기술합니다. 제1지시기호는 저록 작성 여부, 제2지시기호는 정렬 시 무시할 관사의 글자 수를 나타냅니다.'
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
      description: '발행지, 발행처, 발행연도 정보를 기술합니다. (구형식, 264 사용 권장)'
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
      description: '발행지, 발행처, 발행연도 정보를 기술합니다. 제2지시기호로 발행/제작 구분합니다.'
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
      description: '자료의 물리적 형태(페이지 수, 크기 등)를 기술합니다.'
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
      description: '총서(시리즈) 정보를 기술합니다.'
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
      description: '자료의 주제를 나타내는 통제어휘를 기술합니다.'
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
      description: '부저자, 역자, 삽화가 등 주저자 외의 책임자를 기술합니다.'
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

    <div style="background-color: #fed7aa; padding: 12px; border-radius: 6px; margin-top: 15px;">
      <strong>💡 예제:</strong>
      <div style="font-family: monospace; font-size: 15px; margin-top: 8px; color: #7c2d12;">
        ${tag} ${fieldData.example}
      </div>
    </div>
  `;

  fieldDesc.innerHTML = html;
  fieldInfo.style.display = 'block';

  // 데이터 입력 섹션 초기화 및 표시
  document.getElementById('displayTag').textContent = tag;
  document.getElementById('indicator1').value = '';
  document.getElementById('indicator2').value = '';

  // 서브필드 입력 필드 초기화
  window.marcPractice.subfieldCount = 0;
  const subfieldInputs = document.getElementById('subfieldInputs');
  subfieldInputs.innerHTML = '';

  // 첫 번째 서브필드 자동 추가
  addSubfield();

  document.getElementById('dataInput').style.display = 'block';
  document.getElementById('validationResult').style.display = 'none';
  document.getElementById('marcOutput').style.display = 'none';
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

function validateInput() {
  const format = window.marcPractice.currentFormat;
  const tag = window.marcPractice.currentTag;
  const fieldData = marcData[format][tag];

  const ind1 = document.getElementById('indicator1').value || '#';
  const ind2 = document.getElementById('indicator2').value || '#';

  // 서브필드 수집
  const subfields = [];
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
</script>

<style>
button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  transition: all 0.2s;
}

input:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.3);
}

select:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.3);
}

details summary {
  cursor: pointer;
  user-select: none;
}

@media (max-width: 768px) {
  div[style*="grid-template-columns: 1fr 1fr"] {
    grid-template-columns: 1fr !important;
  }
}
</style>
"""

# 기존 콘텐츠의 마지막 </style> 바로 뒤에 실습 섹션 추가
if content.content_html:
    # 마지막 </style> 태그를 찾아서 그 뒤에 삽입
    last_style_end = content.content_html.rfind('</style>')
    if last_style_end != -1:
        # </style> 바로 뒤에 삽입
        insert_pos = last_style_end + len('</style>')
        content.content_html = content.content_html[:insert_pos] + '\n' + practice_section + content.content_html[insert_pos:]
    else:
        # </style>이 없으면 끝에 추가
        content.content_html += practice_section

content.save()

print("✅ MARC 실습 기능이 추가되었습니다!")
print(f"확인: http://localhost:3000/contents/{content.slug}")
