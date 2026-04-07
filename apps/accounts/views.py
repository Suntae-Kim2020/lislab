import secrets
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.utils import timezone
from django.views import View
from rest_framework_simplejwt.tokens import AccessToken
from .models import User, MailingPreference, TeamMember, PasswordResetToken
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    MailingPreferenceSerializer,
    TeamMemberSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    사용자 관리 ViewSet

    - list: 사용자 목록 조회 (관리자만)
    - retrieve: 사용자 상세 조회
    - create: 회원가입
    - update: 사용자 정보 수정
    - destroy: 회원 탈퇴
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        """사용자 목록 조회 (관리자만)"""
        if not request.user.is_admin:
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """사용자 상세 조회 (본인 또는 관리자만)"""
        instance = self.get_object()
        if not (request.user == instance or request.user.is_admin):
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """사용자 정보 수정 (본인 또는 관리자만)"""
        instance = self.get_object()
        if not (request.user == instance or request.user.is_admin):
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """회원 탈퇴 (본인 또는 관리자만)"""
        instance = self.get_object()
        if not (request.user == instance or request.user.is_admin):
            return Response(
                {"detail": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Soft delete (is_active = False)
        instance.is_active = False
        instance.save()

        return Response(
            {"detail": "회원 탈퇴가 완료되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """현재 로그인한 사용자 정보"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """비밀번호 변경"""
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # 기존 비밀번호 확인
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": "기존 비밀번호가 올바르지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 새 비밀번호 설정
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        # 세션 유지
        update_session_auth_hash(request, user)

        return Response(
            {"detail": "비밀번호가 변경되었습니다."},
            status=status.HTTP_200_OK
        )


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    팀 멤버 ViewSet (읽기 전용, 인증 불필요)
    """

    serializer_class = TeamMemberSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True)


class MailingPreferenceViewSet(viewsets.ModelViewSet):
    """
    메일링 설정 ViewSet

    - retrieve: 현재 사용자의 메일링 설정 조회
    - update: 메일링 설정 수정
    - partial_update: 메일링 설정 부분 수정
    """

    serializer_class = MailingPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """현재 사용자의 메일링 설정만 조회"""
        return MailingPreference.objects.filter(user=self.request.user)

    def get_object(self):
        """현재 사용자의 메일링 설정 가져오기 (없으면 생성)"""
        preference, created = MailingPreference.objects.get_or_create(
            user=self.request.user
        )
        return preference

    def list(self, request, *args, **kwargs):
        """현재 사용자의 메일링 설정 반환"""
        preference = self.get_object()
        serializer = self.get_serializer(preference)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """메일링 설정 업데이트"""
        preference = self.get_object()
        serializer = self.get_serializer(preference, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """비밀번호 재설정 요청 - 이메일로 재설정 링크 발송

    보안: 이메일이 존재하지 않더라도 동일한 응답을 반환하여 사용자 열거 방지.
    """
    email = (request.data.get('email') or '').strip().lower()
    if not email:
        return Response(
            {"email": "이메일을 입력해주세요."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.filter(email__iexact=email, is_active=True).first()
    if user:
        # 기존 미사용 토큰 무효화
        PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)

        token_str = secrets.token_urlsafe(48)
        PasswordResetToken.objects.create(
            user=user,
            token=token_str,
            expires_at=timezone.now() + timedelta(hours=1),
        )

        site_url = getattr(settings, 'SITE_URL', 'http://localhost:3000').rstrip('/')
        reset_url = f"{site_url}/reset-password/{token_str}"

        subject = '[LIS Lab] 비밀번호 재설정 안내'
        message = (
            f"안녕하세요, {user.first_name or user.username}님.\n\n"
            f"LIS Lab 비밀번호 재설정을 요청하셨습니다.\n"
            f"아래 링크를 클릭하여 새 비밀번호를 설정해주세요. (1시간 동안 유효)\n\n"
            f"{reset_url}\n\n"
            f"본인이 요청하지 않으셨다면 이 메일을 무시하셔도 됩니다.\n"
            f"계정 보안을 위해 비밀번호를 정기적으로 변경해주세요.\n\n"
            f"— LIS Lab"
        )
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as exc:
            # 이메일 발송 실패 시 토큰 정리하고 500 반환
            PasswordResetToken.objects.filter(user=user, token=token_str).delete()
            return Response(
                {"detail": "이메일 발송에 실패했습니다. 잠시 후 다시 시도해주세요."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return Response(
        {"detail": "입력하신 이메일이 등록되어 있다면 재설정 링크를 발송했습니다."},
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """비밀번호 재설정 확인 - 토큰 검증 후 새 비밀번호로 변경"""
    token_str = (request.data.get('token') or '').strip()
    new_password = request.data.get('new_password') or ''
    new_password_confirm = request.data.get('new_password_confirm') or ''

    if not token_str or not new_password or not new_password_confirm:
        return Response(
            {"detail": "필수 값이 누락되었습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if new_password != new_password_confirm:
        return Response(
            {"new_password": "비밀번호가 일치하지 않습니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token = PasswordResetToken.objects.filter(token=token_str).first()
    if not token or token.is_used or token.expires_at < timezone.now():
        return Response(
            {"detail": "유효하지 않거나 만료된 토큰입니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        validate_password(new_password, user=token.user)
    except ValidationError as exc:
        return Response(
            {"new_password": list(exc.messages)},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = token.user
    user.set_password(new_password)
    user.save()

    token.is_used = True
    token.save()

    return Response(
        {"detail": "비밀번호가 재설정되었습니다. 새 비밀번호로 로그인해주세요."},
        status=status.HTTP_200_OK,
    )


class AdminLoginView(View):
    """JWT 토큰으로 Django admin 세션을 생성하고 리다이렉트"""

    def get(self, request):
        token_str = request.GET.get('token', '')
        if not token_str:
            return HttpResponseBadRequest('토큰이 필요합니다.')

        try:
            access_token = AccessToken(token_str)
            user_id = access_token['user_id']
            user = User.objects.get(pk=user_id)
        except Exception:
            return HttpResponseBadRequest('유효하지 않은 토큰입니다.')

        if not user.is_staff:
            return HttpResponseForbidden('관리자 권한이 없습니다.')

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('/admin/')
