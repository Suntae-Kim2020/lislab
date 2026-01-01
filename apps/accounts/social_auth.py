"""
소셜 로그인 (카카오) 처리
"""
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


KAKAO_TOKEN_URL = 'https://kauth.kakao.com/oauth/token'
KAKAO_USER_INFO_URL = 'https://kapi.kakao.com/v2/user/me'


def get_kakao_access_token(code, redirect_uri):
    """
    카카오 Authorization Code로 Access Token 발급
    """
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.KAKAO_REST_API_KEY,
        'redirect_uri': redirect_uri,
        'code': code,
    }

    response = requests.post(KAKAO_TOKEN_URL, data=data)

    if response.status_code != 200:
        return None

    return response.json().get('access_token')


def get_kakao_user_info(access_token):
    """
    카카오 Access Token으로 사용자 정보 조회
    """
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(KAKAO_USER_INFO_URL, headers=headers)

    if response.status_code != 200:
        return None

    return response.json()


@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_login(request):
    """
    카카오 로그인 콜백 처리

    Request Body:
    - code: 카카오에서 받은 authorization code
    - redirect_uri: 등록된 redirect URI

    Response:
    - access: JWT access token
    - refresh: JWT refresh token
    - user: 사용자 정보
    - is_new_user: 신규 사용자 여부 (추가 정보 입력 필요)
    """
    code = request.data.get('code')
    redirect_uri = request.data.get('redirect_uri')

    if not code or not redirect_uri:
        return Response(
            {'error': 'code와 redirect_uri가 필요합니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 1. 카카오 Access Token 발급
    kakao_access_token = get_kakao_access_token(code, redirect_uri)
    if not kakao_access_token:
        return Response(
            {'error': '카카오 토큰 발급에 실패했습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2. 카카오 사용자 정보 조회
    kakao_user_info = get_kakao_user_info(kakao_access_token)
    if not kakao_user_info:
        return Response(
            {'error': '카카오 사용자 정보 조회에 실패했습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    kakao_id = str(kakao_user_info.get('id'))
    kakao_account = kakao_user_info.get('kakao_account', {})
    profile = kakao_account.get('profile', {})

    email = kakao_account.get('email')
    nickname = profile.get('nickname', f'kakao_{kakao_id}')
    profile_image = profile.get('profile_image_url')

    # 3. 기존 사용자 확인 (소셜 ID로 검색)
    try:
        user = User.objects.get(
            social_provider=User.SocialProvider.KAKAO,
            social_id=kakao_id
        )
        is_new_user = False

    except User.DoesNotExist:
        # 4. 신규 사용자 생성 (기본 정보만)
        username = f'kakao_{kakao_id}'

        # 이메일 중복 체크
        if email and User.objects.filter(email=email).exists():
            # 같은 이메일의 다른 계정이 이미 존재
            return Response(
                {'error': '이미 해당 이메일로 가입된 계정이 있습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            username=username,
            email=email or '',
            first_name=nickname,
            social_provider=User.SocialProvider.KAKAO,
            social_id=kakao_id,
            is_email_verified=True if email else False,
        )

        # 프로필 이미지 URL 저장 (선택사항)
        if profile_image:
            user.bio = f'Profile Image: {profile_image}'
            user.save()

        is_new_user = True

    # 5. JWT 토큰 생성
    refresh = RefreshToken.for_user(user)

    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'user_type': user.user_type,
            'organization': user.organization,
            'social_provider': user.social_provider,
        },
        'is_new_user': is_new_user,
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([AllowAny])  # JWT 토큰을 받기 전이므로 AllowAny
def complete_social_signup(request):
    """
    소셜 로그인 후 추가 정보 입력

    Request Body:
    - user_id: 사용자 ID
    - user_type: 사용자 구분 (STUDENT, PROFESSOR, JOB_SEEKER, OTHER)
    - organization: 소속기관 (선택)
    - phone: 연락처 (선택)
    """
    user_id = request.data.get('user_id')

    if not user_id:
        return Response(
            {'error': 'user_id가 필요합니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(id=user_id, social_provider__in=[
            User.SocialProvider.KAKAO,
            User.SocialProvider.GOOGLE,
            User.SocialProvider.NAVER
        ])
    except User.DoesNotExist:
        return Response(
            {'error': '사용자를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # 추가 정보 업데이트
    user_type = request.data.get('user_type')
    if user_type and user_type in dict(User.UserType.choices):
        user.user_type = user_type

    organization = request.data.get('organization')
    if organization:
        user.organization = organization

    phone = request.data.get('phone')
    if phone:
        user.phone = phone

    user.save()

    return Response({
        'message': '추가 정보가 저장되었습니다.',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type,
            'organization': user.organization,
            'phone': user.phone,
        }
    }, status=status.HTTP_200_OK)
