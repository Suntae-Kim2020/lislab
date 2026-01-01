"""
카카오 메시지 발송 유틸리티
"""
import requests
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

KAKAO_MESSAGE_SEND_URL = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'


def send_kakao_message_notification(user, content):
    """
    카카오톡 메시지로 새 콘텐츠 알림 발송

    Args:
        user: User 객체 (kakao_message_token이 있어야 함)
        content: Content 객체

    Returns:
        bool: 발송 성공 여부
    """
    # 카카오 메시지 토큰이 없으면 발송 불가
    if not user.kakao_message_token:
        logger.warning(f"[KAKAO MESSAGE] 토큰 없음: {user.username}")
        return False

    # 메일링 설정 확인
    try:
        preference = user.mailing_preference
    except Exception:
        logger.warning(f"[KAKAO MESSAGE] 메일링 설정 없음: {user.username}")
        return False

    # 카카오 알림이 비활성화되어 있으면 발송 안 함
    if not preference.kakao_notification_enabled:
        return False

    # 사이트 URL 설정
    site_url = getattr(settings, 'SITE_URL', 'http://localhost:3000')
    content_url = f"{site_url}/contents/{content.slug}"

    # 카카오 메시지 템플릿 구성 (피드 템플릿 - 카드 전체 클릭 가능)
    # 매우 짧게 유지 (카카오톡 표시 제한)
    short_summary = content.summary[:50] + "..." if len(content.summary) > 50 else content.summary

    template_object = {
        "object_type": "feed",
        "content": {
            "title": f"🔔 {content.title}",
            "description": f"👉 탭해서 학습하기\n\n{short_summary}\n📂 {content.category.name if content.category else '기타'} | ⭐ {content.get_difficulty_display()}",
            "image_url": "https://mud-kage.kakao.com/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg",
            "image_width": 800,
            "image_height": 800,
            "link": {
                "web_url": content_url,
                "mobile_web_url": content_url
            }
        }
    }

    # API 요청 헤더
    headers = {
        'Authorization': f'Bearer {user.kakao_message_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # API 요청 데이터
    data = {
        'template_object': json.dumps(template_object, ensure_ascii=False)
    }

    try:
        # 카카오 메시지 API 호출
        response = requests.post(
            KAKAO_MESSAGE_SEND_URL,
            headers=headers,
            data=data
        )

        if response.status_code == 200:
            logger.info(f"[KAKAO MESSAGE] 발송 성공: {user.username} <- {content.title}")
            return True
        else:
            logger.error(f"[KAKAO MESSAGE] 발송 실패 ({user.username}): {response.status_code} - {response.text}")

            # 토큰이 만료되었거나 잘못된 경우
            if response.status_code == 401:
                logger.warning(f"[KAKAO MESSAGE] 토큰 만료/무효: {user.username}")
                # 토큰 삭제 (사용자가 재연동해야 함)
                user.kakao_message_token = None
                user.save()

            return False

    except Exception as e:
        logger.error(f"[KAKAO MESSAGE] 예외 발생 ({user.username}): {str(e)}")
        return False
