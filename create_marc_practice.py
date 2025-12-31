import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.contents.models import Content, Category

User = get_user_model()

# Get category and author
category = Category.objects.get(slug='practice')
admin_user = User.objects.filter(role='ADMIN').first()
if not admin_user:
    admin_user = User.objects.filter(is_superuser=True).first()

# Create or update the content
content, created = Content.objects.update_or_create(
    slug='marc-practice',
    defaults={
        'title': 'MARC 실습',
        'summary': 'MARC21 태그를 직접 입력하고 ISBD 규칙에 따라 검증해보는 실습',
        'category': category,
        'author': admin_user,
        'difficulty': 'ADVANCED',
        'estimated_time': 60,
        'status': 'PUBLISHED',
        'content_html': '''
<div class="content-section">
  <h2>MARC 실습</h2>
  <p>MARC21 레코드를 작성하고 ISBD 규칙에 따라 검증하는 실습입니다.</p>

  <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <h3>📝 실습 방법</h3>
    <ol>
      <li>아래 입력창에 MARC 태그를 한 줄씩 입력하세요</li>
      <li>각 줄은 <strong>태그 지시기호 $서브필드</strong> 형식으로 작성합니다</li>
      <li>"검증하기" 버튼을 클릭하면 ISBD 규칙에 따라 검증됩니다</li>
    </ol>

    <h4>입력 형식 예시:</h4>
    <pre style="background-color: white; padding: 15px; border-radius: 6px; border: 1px solid #ddd;">100 1# $a 조남주
245 10 $a 82년생 김지영 / $c 조남주 지음
260 ## $a 서울 : $b 민음사, $c 2016
300 ## $a 215 p. ; $c 21 cm</pre>
  </div>
</div>

<div style="margin: 30px 0;">
  <h3>MARC 레코드 입력</h3>
  <textarea id="marcInput" rows="15"
    style="width: 100%; padding: 15px; font-family: 'Courier New', monospace; font-size: 14px; border: 2px solid #8b5cf6; border-radius: 8px; resize: vertical;"
    placeholder="예:
100 1# $a 조남주
245 10 $a 82년생 김지영 / $c 조남주 지음
260 ## $a 서울 : $b 민음사, $c 2016
300 ## $a 215 p. ; $c 21 cm"></textarea>

  <div style="margin-top: 15px; display: flex; gap: 10px;">
    <button id="validateBtn" onclick="validateMARC()"
      style="padding: 12px 30px; background-color: #8b5cf6; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; font-weight: bold;">
      검증하기
    </button>
    <button onclick="clearInput()"
      style="padding: 12px 30px; background-color: #6b7280; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer;">
      초기화
    </button>
    <button onclick="loadExample()"
      style="padding: 12px 30px; background-color: #10b981; color: white; border: none; border-radius: 6px; font-size: 16px; cursor: pointer;">
      예시 불러오기
    </button>
  </div>
</div>

<div id="validationResult" style="margin-top: 30px;"></div>

<div class="content-section" style="margin-top: 40px;">
  <h3>💡 ISBD 검증 항목</h3>
  <ul>
    <li><strong>필수 서브필드 확인</strong>: 각 태그에 필수 서브필드가 포함되어 있는지 검증</li>
    <li><strong>지시기호 유효성</strong>: 지시기호가 유효한 값인지 확인</li>
    <li><strong>ISBD 구두점</strong>: Area별 올바른 구두점이 사용되었는지 검증</li>
    <li><strong>태그 관계</strong>: 100-245 관계 등 태그 간 의존성 확인</li>
  </ul>
</div>

<script>
if (!window.marcPracticeInitialized) {
  window.marcPracticeInitialized = true;

  // MARC 데이터 정의
  window.marcData = {
    MARC21: {
      '020': {
        name: 'ISBN',
        indicators: { ind1: { '#': '정의되지 않음' }, ind2: { '#': '정의되지 않음' } },
        subfields: { 'a': { name: 'ISBN', required: true }, 'c': { name: '가격', required: false } },
        isbd: { area: 'Area 8', punctuation: 'ISBN : 가격', note: 'ISBN은 구두점 없이 기술' }
      },
      '100': {
        name: '개인저자명',
        indicators: { ind1: { '0': '성만', '1': '성, 이름', '3': '가족명' }, ind2: { '#': '정의되지 않음' } },
        subfields: { 'a': { name: '개인명', required: true }, 'd': { name: '생몰년', required: false } },
        isbd: { area: 'Area 1', punctuation: '245 $c에서 표현', note: '100은 검색용 표목' }
      },
      '245': {
        name: '표제와 책임표시',
        indicators: {
          ind1: { '0': '저록 미작성', '1': '저록 작성' },
          ind2: { '0': '관사 없음', '1': '1자 무시', '2': '2자 무시', '3': '3자 무시', '4': '4자 무시' }
        },
        subfields: {
          'a': { name: '본표제', required: true },
          'b': { name: '부표제', required: false },
          'c': { name: '책임표시', required: false }
        },
        isbd: {
          area: 'Area 1',
          punctuation: '본표제 : 부표제 / 책임표시',
          pattern: '$a : $b / $c',
          note: '콜론(:)은 $a와 $b 사이, 슬래시(/)는 $c 앞에 위치'
        }
      },
      '250': {
        name: '판사항',
        indicators: { ind1: { '#': '정의되지 않음' }, ind2: { '#': '정의되지 않음' } },
        subfields: { 'a': { name: '판차', required: true }, 'b': { name: '판차 책임표시', required: false } },
        isbd: { area: 'Area 2', punctuation: '판차 / 판차 책임표시', note: '판 정보는 Area 2에 해당' }
      },
      '260': {
        name: '발행사항',
        indicators: { ind1: { '#': '정의되지 않음' }, ind2: { '#': '정의되지 않음' } },
        subfields: {
          'a': { name: '발행지', required: false },
          'b': { name: '발행처', required: false },
          'c': { name: '발행년', required: false }
        },
        isbd: {
          area: 'Area 4',
          punctuation: '발행지 : 발행처, 발행년',
          pattern: '$a : $b, $c',
          note: '콜론(:)은 발행지 다음, 쉼표(,)는 발행년 앞'
        }
      },
      '264': {
        name: '제작/발행/배포/제조사항',
        indicators: {
          ind1: { '#': '정의되지 않음', '2': '중간 발행자', '3': '현재 발행자' },
          ind2: { '0': '제작', '1': '발행', '2': '배포', '3': '제조', '4': '저작권 연도' }
        },
        subfields: {
          'a': { name: '장소', required: false },
          'b': { name: '기관명', required: false },
          'c': { name: '날짜', required: false }
        },
        isbd: { area: 'Area 4', punctuation: '장소 : 기관명, 날짜', note: 'RDA 규칙에서 주로 사용' }
      },
      '300': {
        name: '형태사항',
        indicators: { ind1: { '#': '정의되지 않음' }, ind2: { '#': '정의되지 않음' } },
        subfields: {
          'a': { name: '수량', required: false },
          'b': { name: '기타 형태사항', required: false },
          'c': { name: '크기', required: false }
        },
        isbd: {
          area: 'Area 5',
          punctuation: '수량 : 기타사항 ; 크기',
          pattern: '$a : $b ; $c',
          note: '콜론(:)은 기타사항 앞, 세미콜론(;)은 크기 앞'
        }
      },
      '490': {
        name: '총서사항',
        indicators: {
          ind1: { '0': '추적하지 않음', '1': '추적함' },
          ind2: { '#': '정의되지 않음' }
        },
        subfields: {
          'a': { name: '총서명', required: true },
          'v': { name: '권차', required: false }
        },
        isbd: { area: 'Area 6', punctuation: '총서명 ; 권차', note: '총서는 Area 6에 해당' }
      },
      '650': {
        name: '주제명',
        indicators: {
          ind1: { '#': '정의되지 않음', '0': 'LCSH', '1': 'LC 아동주제표목', '2': 'MeSH' },
          ind2: { '0': '주제어', '1': '지리적', '2': '고유명' }
        },
        subfields: {
          'a': { name: '주제어', required: true },
          'x': { name: '일반세목', required: false }
        },
        isbd: { area: 'n/a', punctuation: '주제어 -- 세목', note: '주제명은 ISBD 표시에 포함되지 않음' }
      },
      '700': {
        name: '부출저자',
        indicators: {
          ind1: { '0': '성만', '1': '성, 이름', '3': '가족명' },
          ind2: { '#': '정의되지 않음', '2': '분석저록' }
        },
        subfields: {
          'a': { name: '개인명', required: true },
          'e': { name: '역할', required: false }
        },
        isbd: { area: 'Area 1', punctuation: '245 $c에서 표현', note: '700은 검색용 부출 표목' }
      }
    }
  };

  function parseMARC(line) {
    const trimmed = line.trim();
    if (!trimmed) return null;

    // 태그 추출
    const tagMatch = trimmed.match(/^(\\d{3})\\s+/);
    if (!tagMatch) return null;

    const tag = tagMatch[1];
    const rest = trimmed.substring(4);

    // 지시기호와 서브필드 분리
    const dollarIndex = rest.indexOf('$');
    let ind1 = '#', ind2 = '#';
    let subfieldPart = rest;

    if (dollarIndex > 0) {
      const indicators = rest.substring(0, dollarIndex).trim();
      if (indicators.length >= 1) ind1 = indicators[0];
      if (indicators.length >= 2) ind2 = indicators[1];
      subfieldPart = rest.substring(dollarIndex);
    } else if (dollarIndex === -1) {
      // No subfields, just indicators
      const indicators = rest.trim();
      if (indicators.length >= 1) ind1 = indicators[0];
      if (indicators.length >= 2) ind2 = indicators[1];
      subfieldPart = '';
    }

    // 서브필드 파싱
    const subfields = [];
    const parts = subfieldPart.split('$').filter(p => p.trim());
    for (const part of parts) {
      const trimmedPart = part.trim();
      if (trimmedPart.length > 0) {
        const code = trimmedPart[0];
        const value = trimmedPart.substring(1).trim();
        subfields.push({ code, value });
      }
    }

    return { tag, ind1, ind2, subfields };
  }

  function validateISBDPunctuation(tag, subfields, lineNum, line, warnings) {
    // 태그별 ISBD 구두점 검증
    switch(tag) {
      case '245': // 표제와 책임표시
        // $a와 $b 사이에 공백:공백 필요
        const has245b = subfields.some(sf => sf.code === 'b');
        if (has245b && !line.includes(' : ')) {
          warnings.push(`줄 ${lineNum} (245): 본표제($a)와 부표제($b) 사이에 ' : ' 구두점이 필요합니다.`);
        }
        // $c 앞에 공백/공백 필요
        const has245c = subfields.some(sf => sf.code === 'c');
        if (has245c && !line.includes(' / ')) {
          warnings.push(`줄 ${lineNum} (245): 책임표시($c) 앞에 ' / ' 구두점이 필요합니다.`);
        }
        break;

      case '260': // 발행사항
      case '264': // 제작/발행사항
        // $a와 $b 사이에 공백:공백 필요
        const hasPub_b = subfields.some(sf => sf.code === 'b');
        if (hasPub_b && !line.includes(' : ')) {
          warnings.push(`줄 ${lineNum} (${tag}): 발행지($a)와 발행처($b) 사이에 ' : ' 구두점이 필요합니다.`);
        }
        // $b와 $c 사이에 ,공백 필요
        const hasPub_c = subfields.some(sf => sf.code === 'c');
        if (hasPub_c && hasPub_b && !line.includes(', ')) {
          warnings.push(`줄 ${lineNum} (${tag}): 발행처($b)와 발행년($c) 사이에 ', ' 구두점이 필요합니다.`);
        }
        break;

      case '300': // 형태사항
        // $a와 $b 사이에 공백:공백 필요
        const has300b = subfields.some(sf => sf.code === 'b');
        if (has300b && !line.includes(' : ')) {
          warnings.push(`줄 ${lineNum} (300): 수량($a)과 기타사항($b) 사이에 ' : ' 구두점이 필요합니다.`);
        }
        // $a나 $b와 $c 사이에 공백;공백 필요
        const has300c = subfields.some(sf => sf.code === 'c');
        if (has300c && !line.includes(' ; ')) {
          warnings.push(`줄 ${lineNum} (300): 크기($c) 앞에 ' ; ' 구두점이 필요합니다.`);
        }
        break;

      case '490': // 총서사항
        // $a와 $v 사이에 공백;공백 필요
        const has490v = subfields.some(sf => sf.code === 'v');
        if (has490v && !line.includes(' ; ')) {
          warnings.push(`줄 ${lineNum} (490): 총서명($a)과 권차($v) 사이에 ' ; ' 구두점이 필요합니다.`);
        }
        break;
    }
  }

  function validateMARC() {
    const input = document.getElementById('marcInput').value;
    const lines = input.split('\\n').filter(line => line.trim());

    if (lines.length === 0) {
      showResult('입력된 MARC 데이터가 없습니다.', 'error');
      return;
    }

    const records = [];
    const errors = [];
    const warnings = [];

    lines.forEach((line, index) => {
      const lineNum = index + 1;
      const parsed = parseMARC(line);

      if (!parsed) {
        errors.push(`줄 ${lineNum}: MARC 형식이 올바르지 않습니다.`);
        return;
      }

      const { tag, ind1, ind2, subfields } = parsed;
      const fieldData = window.marcData.MARC21[tag];

      if (!fieldData) {
        warnings.push(`줄 ${lineNum}: 태그 ${tag}는 지원하지 않는 태그입니다.`);
        return;
      }

      records.push({ lineNum, tag, ind1, ind2, subfields, fieldData });

      // 지시기호 검증
      if (!fieldData.indicators.ind1[ind1]) {
        errors.push(`줄 ${lineNum} (${tag}): 제1지시기호 "${ind1}"은(는) 유효하지 않습니다.`);
      }
      if (!fieldData.indicators.ind2[ind2]) {
        errors.push(`줄 ${lineNum} (${tag}): 제2지시기호 "${ind2}"은(는) 유효하지 않습니다.`);
      }

      // 서브필드 검증
      if (subfields.length === 0) {
        errors.push(`줄 ${lineNum} (${tag}): 서브필드가 없습니다.`);
      }

      const providedCodes = new Set();
      subfields.forEach(sf => {
        if (!fieldData.subfields[sf.code]) {
          warnings.push(`줄 ${lineNum} (${tag}): 서브필드 $${sf.code}은(는) 정의되지 않은 서브필드입니다.`);
        }
        providedCodes.add(sf.code);
      });

      // 필수 서브필드 확인
      Object.keys(fieldData.subfields).forEach(code => {
        if (fieldData.subfields[code].required && !providedCodes.has(code)) {
          errors.push(`줄 ${lineNum} (${tag}): 필수 서브필드 $${code}이(가) 누락되었습니다.`);
        }
      });

      // ISBD 구두점 검증
      validateISBDPunctuation(tag, subfields, lineNum, line, warnings);
    });

    // 태그 관계 검증 (100-245)
    const has100 = records.some(r => r.tag === '100');
    const field245 = records.find(r => r.tag === '245');

    if (field245) {
      if (has100 && field245.ind1 !== '1') {
        warnings.push(`100 필드가 있으므로 245 제1지시기호는 '1'이어야 합니다. (현재: '${field245.ind1}')`);
      }
      if (!has100 && field245.ind1 !== '0') {
        warnings.push(`100 필드가 없으므로 245 제1지시기호는 '0'이어야 합니다. (현재: '${field245.ind1}')`);
      }
    }

    displayValidationResult(records, errors, warnings);
  }

  function displayValidationResult(records, errors, warnings) {
    let html = '';

    if (errors.length > 0) {
      html += `
        <div style="background-color: #fef2f2; padding: 20px; border-radius: 8px; border-left: 4px solid #ef4444; margin-bottom: 20px;">
          <h3 style="color: #991b1b; margin-top: 0;">❌ 오류 발견</h3>
          <ul style="margin: 10px 0; color: #7f1d1d;">
            ${errors.map(err => `<li>${err}</li>`).join('')}
          </ul>
        </div>
      `;
    }

    if (warnings.length > 0) {
      html += `
        <div style="background-color: #fffbeb; padding: 20px; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 20px;">
          <h3 style="color: #92400e; margin-top: 0;">⚠️ 경고</h3>
          <ul style="margin: 10px 0; color: #78350f;">
            ${warnings.map(warn => `<li>${warn}</li>`).join('')}
          </ul>
        </div>
      `;
    }

    if (errors.length === 0 && warnings.length === 0 && records.length > 0) {
      html += `
        <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; border-left: 4px solid #10b981;">
          <h3 style="color: #065f46; margin-top: 0;">✅ 검증 성공!</h3>
          <p style="margin: 0; color: #064e3b;">모든 MARC 태그가 올바르게 입력되었습니다.</p>
        </div>
      `;
    }

    // ISBD 표시 생성
    if (records.length > 0) {
      html += `
        <div style="background-color: #f0f9ff; padding: 20px; border-radius: 8px; border-left: 4px solid #3b82f6; margin-top: 20px;">
          <h3 style="color: #1e40af; margin-top: 0;">📖 ISBD 표시</h3>
          ${generateISBDDisplay(records)}
        </div>
      `;
    }

    document.getElementById('validationResult').innerHTML = html;
  }

  function generateISBDDisplay(records) {
    let html = '<div style="font-family: serif; font-size: 16px; line-height: 1.8;">';

    // Area 1: Title and Statement of Responsibility
    const field245 = records.find(r => r.tag === '245');
    if (field245) {
      const title = field245.subfields.find(sf => sf.code === 'a')?.value || '';
      const subtitle = field245.subfields.find(sf => sf.code === 'b')?.value || '';
      const responsibility = field245.subfields.find(sf => sf.code === 'c')?.value || '';

      html += `<div><strong>Area 1:</strong> ${title}`;
      if (subtitle) html += ` : ${subtitle}`;
      if (responsibility) html += ` / ${responsibility}`;
      html += '</div>';
    }

    // Area 2: Edition
    const field250 = records.find(r => r.tag === '250');
    if (field250) {
      const edition = field250.subfields.find(sf => sf.code === 'a')?.value || '';
      if (edition) {
        html += `<div><strong>Area 2:</strong> ${edition}</div>`;
      }
    }

    // Area 4: Publication
    const field260 = records.find(r => r.tag === '260');
    const field264 = records.find(r => r.tag === '264');
    const pubField = field260 || field264;
    if (pubField) {
      const place = pubField.subfields.find(sf => sf.code === 'a')?.value || '';
      const publisher = pubField.subfields.find(sf => sf.code === 'b')?.value || '';
      const date = pubField.subfields.find(sf => sf.code === 'c')?.value || '';

      html += `<div><strong>Area 4:</strong> `;
      if (place) html += place;
      if (publisher) html += ` : ${publisher}`;
      if (date) html += `, ${date}`;
      html += '</div>';
    }

    // Area 5: Physical Description
    const field300 = records.find(r => r.tag === '300');
    if (field300) {
      const extent = field300.subfields.find(sf => sf.code === 'a')?.value || '';
      const other = field300.subfields.find(sf => sf.code === 'b')?.value || '';
      const dimensions = field300.subfields.find(sf => sf.code === 'c')?.value || '';

      html += `<div><strong>Area 5:</strong> ${extent}`;
      if (other) html += ` : ${other}`;
      if (dimensions) html += ` ; ${dimensions}`;
      html += '</div>';
    }

    // Area 6: Series
    const field490 = records.find(r => r.tag === '490');
    if (field490) {
      const series = field490.subfields.find(sf => sf.code === 'a')?.value || '';
      const volume = field490.subfields.find(sf => sf.code === 'v')?.value || '';

      html += `<div><strong>Area 6:</strong> (${series}`;
      if (volume) html += ` ; ${volume}`;
      html += ')</div>';
    }

    // Area 8: ISBN
    const field020 = records.find(r => r.tag === '020');
    if (field020) {
      const isbn = field020.subfields.find(sf => sf.code === 'a')?.value || '';
      const price = field020.subfields.find(sf => sf.code === 'c')?.value || '';

      html += `<div><strong>Area 8:</strong> ISBN ${isbn}`;
      if (price) html += ` : ${price}`;
      html += '</div>';
    }

    html += '</div>';
    return html;
  }

  function showResult(message, type) {
    const colors = {
      error: { bg: '#fef2f2', border: '#ef4444', text: '#991b1b' },
      success: { bg: '#f0fdf4', border: '#10b981', text: '#065f46' },
      warning: { bg: '#fffbeb', border: '#f59e0b', text: '#92400e' }
    };
    const color = colors[type] || colors.error;

    document.getElementById('validationResult').innerHTML = `
      <div style="background-color: ${color.bg}; padding: 20px; border-radius: 8px; border-left: 4px solid ${color.border};">
        <p style="color: ${color.text}; margin: 0;">${message}</p>
      </div>
    `;
  }

  function clearInput() {
    document.getElementById('marcInput').value = '';
    document.getElementById('validationResult').innerHTML = '';
  }

  function loadExample() {
    document.getElementById('marcInput').value = `100 1# $a 조남주
245 10 $a 82년생 김지영 / $c 조남주 지음
250 ## $a 개정판
260 ## $a 서울 : $b 민음사, $c 2016
300 ## $a 215 p. ; $c 21 cm
650 #0 $a 한국소설`;
  }

  // Attach functions to window object for onclick handlers
  window.validateMARC = validateMARC;
  window.clearInput = clearInput;
  window.loadExample = loadExample;
}
</script>
''',
    }
)

if created:
    print(f'✅ MARC 실습 콘텐츠가 생성되었습니다!')
else:
    print(f'✅ MARC 실습 콘텐츠가 업데이트되었습니다!')

print(f'확인: http://localhost:3000/contents/marc-practice')
