#!/usr/bin/env python
"""XML 실습 검증 기능 개선 스크립트"""
import os
import sys
import django

# Django 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content

# 개선된 검증 스크립트를 포함한 HTML
validation_script = """
<script>
function getKoreanErrorMessage(xmlText, errorText) {
    // 일반적인 XML 오류 패턴 검사

    // 1. 태그가 닫히지 않은 경우
    if (errorText.includes('mismatch') || errorText.includes('not closed')) {
        const openTags = [];
        const closeTags = [];

        // 열린 태그 찾기
        const openMatches = xmlText.matchAll(/<([^\/\s>?!][^>\s]*)[^>]*>/g);
        for (const match of openMatches) {
            if (!match[0].includes('<?') && !match[0].includes('/>')) {
                openTags.push(match[1]);
            }
        }

        // 닫힌 태그 찾기
        const closeMatches = xmlText.matchAll(/<\/([^>]+)>/g);
        for (const match of closeMatches) {
            closeTags.push(match[1]);
        }

        // 매칭되지 않는 태그 찾기
        const unclosedTags = openTags.filter(tag => !closeTags.includes(tag));

        if (unclosedTags.length > 0) {
            return `태그가 올바르게 닫히지 않았습니다. "&lt;${unclosedTags[0]}&gt;" 태그의 닫는 태그를 확인하세요.`;
        }

        return '여는 태그와 닫는 태그가 일치하지 않습니다. 모든 태그가 올바르게 닫혀있는지 확인하세요.';
    }

    // 2. 루트 요소가 여러 개인 경우
    if (errorText.includes('Extra content') || errorText.includes('multiple')) {
        return '루트 요소가 여러 개입니다. XML 문서는 반드시 하나의 루트 요소만 가져야 합니다.';
    }

    // 3. 속성 값에 따옴표가 없는 경우
    if (errorText.includes('AttValue') || errorText.includes('quote')) {
        return '속성 값이 따옴표로 감싸져 있지 않습니다. 모든 속성 값은 큰따옴표("")로 감싸야 합니다.';
    }

    // 4. 태그 이름이 잘못된 경우
    if (errorText.includes('Name') || errorText.includes('invalid')) {
        return '태그 이름이 잘못되었습니다. 태그 이름은 문자로 시작해야 하며 공백을 포함할 수 없습니다.';
    }

    // 5. XML 선언 오류
    if (errorText.includes('declaration') || errorText.includes('version')) {
        return 'XML 선언이 잘못되었습니다. 올바른 형식: &lt;?xml version="1.0" encoding="UTF-8"?&gt;';
    }

    // 6. 태그가 중첩이 잘못된 경우
    if (errorText.includes('nested') || errorText.includes('overlap')) {
        return '태그가 올바르게 중첩되지 않았습니다. 예: &lt;a&gt;&lt;b&gt;...&lt;/b&gt;&lt;/a&gt; (올바름) vs &lt;a&gt;&lt;b&gt;...&lt;/a&gt;&lt;/b&gt; (잘못됨)';
    }

    // 일반 오류 메시지
    return 'XML 문법 오류가 있습니다. 다음을 확인하세요:<br>' +
           '• 모든 태그가 올바르게 닫혀있나요?<br>' +
           '• 속성 값이 따옴표로 감싸져 있나요?<br>' +
           '• 루트 요소가 하나만 있나요?<br>' +
           '• 태그가 올바르게 중첩되어 있나요?';
}

(function() {
    const defaultXML1 = \`<?xml version="1.0" encoding="UTF-8"?>
<도서>
    <제목>어린왕자</제목>
    <저자>생텍쥐페리</저자>
    <출판사>민음사</출판사>
    <출판연도>2015</출판연도>
</도서>\`;

    window.validateXML1 = function() {
        const xmlText = document.getElementById('practice1-xml-editor').value;
        const resultDiv = document.getElementById('practice1-result');

        try {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
            const parseError = xmlDoc.getElementsByTagName('parsererror');

            if (parseError.length > 0) {
                const errorText = parseError[0].textContent;
                const koreanMessage = getKoreanErrorMessage(xmlText, errorText);

                resultDiv.style.display = 'block';
                resultDiv.style.backgroundColor = '#fef2f2';
                resultDiv.style.borderLeft = '4px solid #ef4444';
                resultDiv.innerHTML = '<strong style="color: #dc2626;">❌ XML 오류 발견!</strong><br>' +
                                     '<span style="color: #991b1b;">' + koreanMessage + '</span>';
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
                                 '<span style="color: #991b1b;">예상치 못한 오류가 발생했습니다. XML 문법을 확인해주세요.</span>';
        }
    };

    window.resetXML1 = function() {
        document.getElementById('practice1-xml-editor').value = defaultXML1;
        document.getElementById('practice1-result').style.display = 'none';
    };
})();

(function() {
    const defaultXML2 = \`<?xml version="1.0" encoding="UTF-8"?>
<도서 isbn="978-8937460449" 대출가능="true">
    <제목>어린왕자</제목>
    <저자 국적="프랑스">생텍쥐페리</저자>
    <출판사>민음사</출판사>
    <출판연도>2015</출판연도>
    <분류>
        <주제>아동문학</주제>
        <청구기호>863-생63ㅇ</청구기호>
    </분류>
</도서>\`;

    window.validateXML2 = function() {
        const xmlText = document.getElementById('practice2-xml-editor').value;
        const resultDiv = document.getElementById('practice2-result');

        try {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
            const parseError = xmlDoc.getElementsByTagName('parsererror');

            if (parseError.length > 0) {
                const errorText = parseError[0].textContent;
                const koreanMessage = getKoreanErrorMessage(xmlText, errorText);

                resultDiv.style.display = 'block';
                resultDiv.style.backgroundColor = '#fef2f2';
                resultDiv.style.borderLeft = '4px solid #ef4444';
                resultDiv.innerHTML = '<strong style="color: #dc2626;">❌ XML 오류 발견!</strong><br>' +
                                     '<span style="color: #991b1b;">' + koreanMessage + '</span>';
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
                                 '<span style="color: #991b1b;">예상치 못한 오류가 발생했습니다. XML 문법을 확인해주세요.</span>';
        }
    };

    window.resetXML2 = function() {
        document.getElementById('practice2-xml-editor').value = defaultXML2;
        document.getElementById('practice2-result').style.display = 'none';
    };
})();

(function() {
    const defaultXML3 = \`<?xml version="1.0" encoding="UTF-8"?>
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
</도서관>\`;

    window.validateXML3 = function() {
        const xmlText = document.getElementById('practice3-xml-editor').value;
        const resultDiv = document.getElementById('practice3-result');

        try {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, 'text/xml');
            const parseError = xmlDoc.getElementsByTagName('parsererror');

            if (parseError.length > 0) {
                const errorText = parseError[0].textContent;
                const koreanMessage = getKoreanErrorMessage(xmlText, errorText);

                resultDiv.style.display = 'block';
                resultDiv.style.backgroundColor = '#fef2f2';
                resultDiv.style.borderLeft = '4px solid #ef4444';
                resultDiv.innerHTML = '<strong style="color: #dc2626;">❌ XML 오류 발견!</strong><br>' +
                                     '<span style="color: #991b1b;">' + koreanMessage + '</span>';
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
                                 '<span style="color: #991b1b;">예상치 못한 오류가 발생했습니다. XML 문법을 확인해주세요.</span>';
        }
    };

    window.resetXML3 = function() {
        document.getElementById('practice3-xml-editor').value = defaultXML3;
        document.getElementById('practice3-result').style.display = 'none';
    };
})();
</script>
"""

print("검증 스크립트가 준비되었습니다. XML 실습 콘텐츠를 업데이트합니다...")
print("\n새로운 기능:")
print("- 한글로 된 명확한 오류 메시지")
print("- 태그 미스매치 감지 및 안내")
print("- 일반적인 XML 오류 패턴 인식")
print("\n스크립트를 실행하려면 create_xml_practice.py를 다시 실행하세요.")
