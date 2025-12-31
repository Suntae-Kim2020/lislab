"""관리자 통계 뷰"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import User
from apps.contents.models import Content, Favorite
from apps.boards.models import Post, PostReply


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_statistics(request):
    """관리자 통계 데이터"""

    # 관리자 권한 확인
    if not request.user.is_admin:
        return Response(
            {"detail": "관리자 권한이 필요합니다."},
            status=status.HTTP_403_FORBIDDEN
        )

    # 현재 날짜
    now = timezone.now()
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # 1. 콘텐츠 통계
    # 가장 많이 즐겨찾기된 콘텐츠 (상위 10개)
    top_favorited_contents = Content.objects.annotate(
        favorite_count=Count('favorited_by')
    ).filter(
        favorite_count__gt=0
    ).order_by('-favorite_count')[:10].values(
        'id', 'title', 'slug', 'favorite_count'
    )

    # 가장 많이 읽힌 콘텐츠 (상위 10개)
    top_viewed_contents = Content.objects.filter(
        view_count__gt=0
    ).order_by('-view_count')[:10].values(
        'id', 'title', 'slug', 'view_count'
    )

    # 2. 회원 통계
    # 전체 회원 수
    total_users = User.objects.filter(is_active=True).count()

    # 이번 달 신규 회원 수
    new_users_this_month = User.objects.filter(
        created_at__gte=this_month_start
    ).count()

    # 이번 달 신규 회원 목록 (최근 10명)
    recent_new_users = User.objects.filter(
        created_at__gte=this_month_start
    ).order_by('-created_at')[:10].values(
        'id', 'username', 'email', 'user_type', 'organization', 'created_at'
    )

    # 월별 회원 등록 건수 (최근 12개월)
    monthly_registrations = []
    for i in range(11, -1, -1):
        month_start = (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i*30)).replace(day=1)
        if i > 0:
            month_end = (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=(i-1)*30)).replace(day=1)
        else:
            month_end = now

        count = User.objects.filter(
            created_at__gte=month_start,
            created_at__lt=month_end
        ).count()

        monthly_registrations.append({
            'month': month_start.strftime('%Y-%m'),
            'count': count
        })

    # 직업별 회원 수
    users_by_type = User.objects.filter(
        is_active=True
    ).values('user_type').annotate(
        count=Count('id')
    ).order_by('-count')

    user_type_labels = dict(User.UserType.choices)
    users_by_type_formatted = [
        {
            'type': item['user_type'],
            'label': user_type_labels.get(item['user_type'], item['user_type']),
            'count': item['count']
        }
        for item in users_by_type
    ]

    # 기관별 회원 수 (상위 10개, 기관 정보가 있는 경우만)
    users_by_organization = User.objects.filter(
        is_active=True,
        organization__isnull=False
    ).exclude(
        organization=''
    ).values('organization').annotate(
        count=Count('id')
    ).order_by('-count')[:10]

    # 3. 가장 많이 로그인한 회원 (last_login 기준, 최근 로그인한 사용자)
    # Note: Django는 로그인 횟수를 기본적으로 추적하지 않으므로,
    # last_login이 최근인 사용자를 반환
    most_active_users = User.objects.filter(
        is_active=True,
        last_login__isnull=False
    ).order_by('-last_login')[:10].values(
        'id', 'username', 'email', 'user_type', 'last_login'
    )

    # 4. 가장 왕성한 활동을 한 회원
    # 활동 점수 = 게시글 작성 수 + 답글 작성 수 + 즐겨찾기 수
    active_users_data = []
    users = User.objects.filter(is_active=True)

    for user in users:
        post_count = Post.objects.filter(author=user, is_deleted=False).count()
        reply_count = PostReply.objects.filter(author=user).count()
        favorite_count = Favorite.objects.filter(user=user).count()

        activity_score = post_count + reply_count + favorite_count

        if activity_score > 0:
            # 이름 구성
            full_name = f"{user.last_name}{user.first_name}".strip() if user.first_name or user.last_name else '-'

            active_users_data.append({
                'id': user.id,
                'username': user.username,
                'full_name': full_name,
                'email': user.email,
                'user_type': user.user_type,
                'organization': user.organization or '-',
                'post_count': post_count,
                'reply_count': reply_count,
                'favorite_count': favorite_count,
                'activity_score': activity_score,
            })

    # 활동 점수로 정렬
    most_active_contributors = sorted(
        active_users_data,
        key=lambda x: x['activity_score'],
        reverse=True
    )[:10]

    return Response({
        'content_statistics': {
            'top_favorited': list(top_favorited_contents),
            'top_viewed': list(top_viewed_contents),
        },
        'user_statistics': {
            'total_users': total_users,
            'new_users_this_month': new_users_this_month,
            'recent_new_users': list(recent_new_users),
            'monthly_registrations': monthly_registrations,
            'users_by_type': users_by_type_formatted,
            'users_by_organization': list(users_by_organization),
            'most_active_users': list(most_active_users),
            'most_active_contributors': most_active_contributors,
        }
    })
