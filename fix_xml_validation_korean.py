#!/usr/bin/env python
"""XML 실습 검증 메시지 한글화 스크립트"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contents.models import Content

try:
    content = Content.objects.get(slug='xml-practice')
    
    # 기존 내용을 읽어서 검증 스크립트 부분만 교체
    html = content.content_html
    
    # 기존 검증 함수들을 개선된 버전으로 교체
    # 먼저 getKoreanErrorMessage 함수를 추가
    korean_error_function = """            <script>
                function getKoreanErrorMessage(xmlText, errorText) {
                    // 일반적인 XML 오류 패턀 검사
                    
                    // 1. 태그가 닫히지 않은 경우
                    if (errorText.includes('mismatch') || errorText.includes('not closed')) {
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

                (function() {"""
    
    # 기존 스크립트를 새 버전으로 교체 (practice1)
    old_script1_start = '            <script>\n                (function() {'
    if old_script1_start in html:
        html = html.replace(old_script1_start, korean_error_function, 1)
    
    # parseError[0].textContent를 getKoreanErrorMessage로 교체
    html = html.replace(
        "parseError[0].textContent",
        "getKoreanErrorMessage(xmlText, parseError[0].textContent)"
    )
    
    # catch error의 error.message도 한글로
    html = html.replace(
        "'<span style=\"color: #991b1b;\">' + error.message + '</span>'",
        "'<span style=\"color: #991b1b;\">예상치 못한 오류가 발생했습니다. XML 문법을 확인해주세요.</span>'"
    )
    
    content.content_html = html
    content.save()
    
    print("✅ XML 실습 검증 메시지가 한글로 업데이트되었습니다!")
    print(f"   제목: {content.title}")
    print(f"   URL: /contents/xml-practice")
    
except Content.DoesNotExist:
    print("❌ XML 실습 콘텐츠를 찾을 수 없습니다.")
except Exception as e:
    print(f"❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
