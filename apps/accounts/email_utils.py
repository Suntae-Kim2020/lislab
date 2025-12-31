"""
이메일 발송 유틸리티
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from collections import defaultdict


def send_weekly_digest(user, week_start, week_end, contents_by_category):
    """
    주간 다이제스트 이메일 발송

    Args:
        user: User 객체
        week_start: 주 시작 날짜 (datetime)
        week_end: 주 종료 날짜 (datetime)
        contents_by_category: 카테고리별 콘텐츠 딕셔너리 {category_name: [content1, content2, ...]}
    """
    # 전체 콘텐츠 수 계산
    total_contents = sum(len(contents) for contents in contents_by_category.values())
    total_categories = len(contents_by_category)

    # 예상 소요 시간 계산 (분)
    estimated_time = 0
    for contents in contents_by_category.values():
        for content in contents:
            estimated_time += content.estimated_time or 0

    # 사이트 URL 설정
    site_url = getattr(settings, 'SITE_URL', 'http://localhost:3000')

    # 컨텍스트 준비
    context = {
        'user': user,
        'week_start': week_start,
        'week_end': week_end,
        'contents_by_category': contents_by_category,
        'total_contents': total_contents,
        'total_categories': total_categories,
        'estimated_time': estimated_time,
        'site_url': site_url,
    }

    # HTML 및 텍스트 버전 렌더링
    html_content = render_to_string('emails/weekly_digest.html', context)
    text_content = render_to_string('emails/weekly_digest.txt', context)

    # 이메일 제목
    subject = f'[LIS Lab] 주간 다이제스트 ({week_start.strftime("%m/%d")} - {week_end.strftime("%m/%d")})'

    # 이메일 생성
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    # HTML 버전 첨부
    email.attach_alternative(html_content, "text/html")

    # 이메일 발송
    email.send()


def get_weekly_contents_for_user(user, week_start, week_end):
    """
    특정 사용자의 메일링 설정에 따라 주간 콘텐츠를 가져옴

    Args:
        user: User 객체
        week_start: 주 시작 날짜 (datetime)
        week_end: 주 종료 날짜 (datetime)

    Returns:
        dict: 카테고리별 콘텐츠 딕셔너리 {category_name: [content1, content2, ...]}
    """
    from apps.contents.models import Content
    from .models import MailingPreference

    try:
        preference = user.mailing_preference
    except MailingPreference.DoesNotExist:
        return {}

    # 메일링이 비활성화되어 있으면 빈 딕셔너리 반환
    if not preference.enabled:
        return {}

    # 주간 빈도가 아니면 빈 딕셔너리 반환
    if preference.frequency != 'WEEKLY':
        return {}

    # 기간 내 발행된 콘텐츠 필터링
    contents_query = Content.objects.filter(
        status='PUBLISHED',
        published_at__gte=week_start,
        published_at__lt=week_end
    ).select_related('category')

    # 카테고리 필터링
    if not preference.all_categories:
        selected_category_ids = list(preference.selected_categories.values_list('id', flat=True))
        if not selected_category_ids:
            return {}
        contents_query = contents_query.filter(category_id__in=selected_category_ids)

    # 카테고리별로 그룹화
    contents_by_category = defaultdict(list)
    for content in contents_query.order_by('category__name', '-published_at'):
        category_name = content.category.name if content.category else '기타'
        contents_by_category[category_name].append(content)

    return dict(contents_by_category)


def send_immediate_content_notification(user, content):
    """
    즉시 알림 이메일 발송 (새 콘텐츠 발행 시)

    Args:
        user: User 객체
        content: Content 객체
    """
    from .models import MailingPreference

    try:
        preference = user.mailing_preference
    except MailingPreference.DoesNotExist:
        return

    # 메일링이 비활성화되어 있으면 반환
    if not preference.enabled:
        return

    # 즉시 알림이 아니면 반환
    if preference.frequency != 'IMMEDIATE':
        return

    # 카테고리 체크
    if not preference.all_categories:
        selected_category_ids = list(preference.selected_categories.values_list('id', flat=True))
        if content.category_id not in selected_category_ids:
            return

    # 사이트 URL 설정
    site_url = getattr(settings, 'SITE_URL', 'http://localhost:3000')

    # 컨텍스트 준비
    context = {
        'user': user,
        'content': content,
        'site_url': site_url,
    }

    # 이메일 제목
    subject = f'[LIS Lab] 새 콘텐츠: {content.title}'

    # 간단한 텍스트 버전 (템플릿 생성 필요시 추가 가능)
    text_content = f"""
안녕하세요, {user.username}님!

LIS Lab에 새로운 콘텐츠가 발행되었습니다.

제목: {content.title}
카테고리: {content.category.name if content.category else '기타'}
난이도: {content.get_difficulty_display()}
예상 시간: {content.estimated_time}분

{content.summary}

지금 학습하기: {site_url}/contents/{content.slug}

----
© 2025 LIS Lab. All rights reserved.
메일링 설정: {site_url}/my/mailing-settings
"""

    # 이메일 발송
    from django.core.mail import send_mail
    try:
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        print(f"[Email] Successfully sent to {user.email}")
    except Exception as e:
        print(f"[Email] Failed to send to {user.email}: {str(e)}")
        raise
