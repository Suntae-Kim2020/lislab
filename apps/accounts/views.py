from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from .models import User, MailingPreference
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    MailingPreferenceSerializer
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
